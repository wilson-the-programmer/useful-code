use std::fs;
use std::io;
use std::path::PathBuf;                      use std::process::Command;
use std::time::Duration;                     
use crossterm::{
    event::{self, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{Block, Borders, Clear, List, ListItem, Paragraph, Wrap},
    Terminal,
};

#[derive(PartialEq)]
enum Popup {
    None,
    Delete,
    View,
}

struct App {
    cwd: PathBuf,
    files: Vec<PathBuf>,
    selected: usize,
    offset: usize,
    preview: String,
    scroll: usize,
    popup: Popup,
    view_scroll: usize,
}

impl App {
    fn new() -> Self {
        let cwd = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));

        let mut app = Self {
            cwd,
            files: vec![],
            selected: 0,
            offset: 0,
            preview: String::new(),
            scroll: 0,
            popup: Popup::None,
            view_scroll: 0,
        };

        app.reload();
        app
    }

    fn current_path(&self) -> Option<PathBuf> {
        self.files.get(self.selected).cloned()
    }

    fn reload(&mut self) {
        self.files = fs::read_dir(&self.cwd)
            .unwrap()
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| {
                p.file_name()
                    .and_then(|n| n.to_str())
                    .map(|s| !s.starts_with('.'))
                    .unwrap_or(false)
            })
            .collect();

        self.files.sort();
        self.selected = 0;
        self.offset = 0;
        self.scroll = 0;
        self.view_scroll = 0;
        self.update_preview();
    }

    fn update_preview(&mut self) {
        if let Some(path) = self.files.get(self.selected) {
            if path.is_file() {
                self.preview =
                    fs::read_to_string(path).unwrap_or_else(|_| "<binary>".to_string());
            } else {
                self.preview = "<directory>".to_string();
            }
        }
        self.scroll = 0;
        self.view_scroll = 0;
    }

    fn sync_scroll(&mut self) {
        let vh = 18;

        if self.selected < self.offset {
            self.offset = self.selected;
        }

        if self.selected >= self.offset + vh {
            self.offset = self.selected - vh + 1;
        }
    }

    fn up(&mut self) {
        if self.popup != Popup::None {
            return;
        }

        if self.selected > 0 {
            self.selected -= 1;
            self.sync_scroll();
            self.update_preview();
        }
    }

    fn down(&mut self) {
        if self.popup != Popup::None {
            return;
        }

        if self.selected + 1 < self.files.len() {
            self.selected += 1;
            self.sync_scroll();
            self.update_preview();
        }
    }

    fn open_selected(&mut self) {
        if self.popup != Popup::None {
            return;
        }

        if let Some(path) = self.files.get(self.selected).cloned() {
            if path.is_dir() {
                self.cwd = path;
                self.reload();
            } else {
                disable_raw_mode().ok();
                execute!(io::stdout(), LeaveAlternateScreen).ok();
                Command::new("nano").arg(&path).status().ok();
                std::process::exit(0);
            }
        }
    }

    fn trigger_delete(&mut self) {
        if self.current_path().is_some() {
            self.popup = Popup::Delete;
        }
    }

    fn confirm_delete(&mut self) {
        if let Some(path) = self.current_path() {
            let _ = fs::remove_file(path);
            self.popup = Popup::None;
            self.reload();
        }
    }

    fn cancel_popup(&mut self) {
        self.popup = Popup::None;
    }

    fn trigger_view(&mut self) {
        if self.current_path().is_some() {
            self.popup = Popup::View;
            self.view_scroll = 0;
        }
    }

    fn preview_up(&mut self) {
        if self.scroll > 0 {
            self.scroll -= 1;
        }
    }

    fn preview_down(&mut self) {
        let max = self.preview.lines().count().saturating_sub(1);
        if self.scroll < max {
            self.scroll += 1;
        }
    }

    fn view_up(&mut self) {
        if self.view_scroll > 0 {
            self.view_scroll -= 1;
        }
    }

    fn view_down(&mut self) {
        let max = self.preview.lines().count().saturating_sub(1);
        if self.view_scroll < max {
            self.view_scroll += 1;
        }
    }
}

fn highlight_line(line: &str) -> Line<'_> {
    let rust_keywords = [
        "as","break","const","continue","crate","else","enum","extern","false","fn","for","if","impl",
        "in","let","loop","match","mod","move","mut","pub","ref","return","self","Self","static",
        "struct","super","trait","true","type","unsafe","use","where","while","async","await","dyn",
    ];

    let python_keywords = [
        "False","None","True","and","as","assert","async","await","break","class","continue","def",
        "del","elif","else","except","finally","for","from","global","if","import","in","is","lambda",
        "nonlocal","not","or","pass","raise","return","try","while","with","yield",
    ];

    let arm_keywords = [
        "mov","add","sub","mul","sdiv","udiv","ldr","str","ldp","stp","b","bl","br","cbz","cbnz",
        "cmp","tst","and","orr","eor","lsl","lsr","asr","nop","ret","adr","adrp",
    ];

    let mut spans = Vec::new();
    let mut word = String::new();

    for c in line.chars() {
        if c.is_alphanumeric() || c == '_' {
            word.push(c);
        } else {
            if !word.is_empty() {
                if rust_keywords.contains(&word.as_str())
                    || python_keywords.contains(&word.as_str())
                    || arm_keywords.contains(&word.as_str())
                {
                    spans.push(Span::styled(
                        word.clone(),
                        Style::default().fg(Color::LightCyan).add_modifier(Modifier::BOLD),
                    ));
                } else {
                    spans.push(Span::raw(word.clone()));
                }
                word.clear();
            }
            spans.push(Span::raw(c.to_string()));
        }
    }

    if !word.is_empty() {
        if rust_keywords.contains(&word.as_str())
            || python_keywords.contains(&word.as_str())
            || arm_keywords.contains(&word.as_str())
        {
            spans.push(Span::styled(
                word,
                Style::default().fg(Color::LightCyan).add_modifier(Modifier::BOLD),
            ));
        } else {
            spans.push(Span::raw(word));
        }
    }

    Line::from(spans)
}

fn main() -> Result<(), io::Error> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;

    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let mut app = App::new();

    loop {
        terminal.draw(|f| {
            let size = f.size();

            let chunks = Layout::default()
                .direction(Direction::Horizontal)
                .constraints([
                    Constraint::Percentage(35),
                    Constraint::Percentage(65),
                ])
                .split(size);

            let items: Vec<ListItem> = app
                .files
                .iter()
                .enumerate()
                .skip(app.offset)
                .take(18)
                .map(|(i, p)| {
                    let name = p.file_name().unwrap_or_default().to_string_lossy();

                    let style = if i == app.selected {
                        Style::default()
                            .bg(Color::DarkGray)
                            .fg(Color::Yellow)
                            .add_modifier(Modifier::BOLD)
                    } else {
                        Style::default()
                    };

                    ListItem::new(name).style(style)
                })
                .collect();

            let list = List::new(items).block(Block::default().borders(Borders::ALL));

            let preview_lines: Vec<Line> = app
                .preview
                .lines()
                .skip(app.scroll)
                .take(40)
                .map(|l| highlight_line(l))
                .collect();

            let preview = Paragraph::new(Text::from(preview_lines))
                .block(Block::default().borders(Borders::ALL))
                .wrap(Wrap { trim: false });

            if app.popup == Popup::None {
                f.render_widget(list, chunks[0]);
                f.render_widget(Clear, chunks[1]);
                f.render_widget(preview, chunks[1]);
            }

            if let Popup::Delete = app.popup {
                let file_name = app
                    .current_path()
                    .and_then(|p| p.file_name().map(|n| n.to_string_lossy().to_string()))
                    .unwrap_or_else(|| "unknown".to_string());

                let text = format!("Delete: {}\n\n   1) Yes    2) Cancel", file_name);

                let popup = Paragraph::new(text)
                    .block(Block::default().borders(Borders::ALL))
                    .style(Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD));

                f.render_widget(Clear, size);
                f.render_widget(popup, size);
            }

            if let Popup::View = app.popup {
                let lines: Vec<Line> = app
                    .preview
                    .lines()
                    .skip(app.view_scroll)
                    .take(50)
                    .map(|l| highlight_line(l))
                    .collect();

                let popup = Paragraph::new(Text::from(lines))
                    .wrap(Wrap { trim: false });

                f.render_widget(Clear, size);
                f.render_widget(popup, size);
            }
        })?;

        if event::poll(Duration::from_millis(80))? {
            if let Event::Key(k) = event::read()? {
                match k.code {
                    KeyCode::Char('q') => {
                        if app.popup == Popup::None {
                            break;
                        } else {
                            app.popup = Popup::None;
                        }
                    }
                    KeyCode::Char('d') => app.trigger_delete(),
                    KeyCode::Char('v') => app.trigger_view(),
                    KeyCode::Char('1') => app.confirm_delete(),
                    KeyCode::Char('2') => app.cancel_popup(),
                    KeyCode::Up => app.up(),
                    KeyCode::Down => app.down(),
                    KeyCode::Enter => app.open_selected(),

                    KeyCode::PageUp => {
                        if app.popup == Popup::View {
                            app.view_up();
                        } else {
                            app.preview_up();
                        }
                    }

                    KeyCode::PageDown => {
                        if app.popup == Popup::View {
                            app.view_down();
                        } else {
                            app.preview_down();
                        }
                    }

                    _ => {}
                }
            }
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    Ok(())
}


