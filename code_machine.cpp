
/* This is a powerful IDE for multiple languages that I created using Chat GPT. */

//  for bash shell function
#include <qtermwidget6/qtermwidget.h>
#include <QInputDialog>
#include <QApplication>
#include <QMainWindow>
#include <QTextEdit>
#include <QPushButton> 
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSplitter>
#include <QProcess>
#include <QFile>
#include <QTemporaryDir>
#include <QFileDialog>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QFont>
#include <QComboBox>
#include <QFileInfo>
#include <QLabel>
#include <QSyntaxHighlighter>
#include <QTextCharFormat>
#include <QRegularExpression>
#include <QColor>

#include <QRegularExpression>
#include <vector>
#include <algorithm>

#include <QStackedWidget>



class CodeHighlighter : public QSyntaxHighlighter
{
public:
    CodeHighlighter(QTextDocument *parent = nullptr)
        : QSyntaxHighlighter(parent)
    {
        keywordFormat.setForeground(QColor("#FF0000"));
        stringFormat.setForeground(QColor("#004400"));
        numberFormat.setForeground(QColor("#0000B5"));
        commentFormat.setForeground(QColor("#00AA00"));
        preprocessorFormat.setForeground(QColor("#555500"));
        functionFormat.setForeground(QColor("#0055EE"));
        typeFormat.setForeground(QColor("#00CCCC"));
        variableFormat.setForeground(QColor("#CC6600"));
        equalsFormat.setForeground(QColor("#FF00FF"));

    }

    void setLanguage(const QString &language)
    {
        currentLanguage = language;
        rehighlight();
    }

protected:
    void highlightBlock(const QString &text) override
    {
        if (currentLanguage == "C" || currentLanguage == "C++" || currentLanguage == "Rust" || currentLanguage == "Go" || currentLanguage == "JavaScript")
            highlightCpp(text);
        else if (currentLanguage == "Python3")
            highlightPython(text);
    }

private:
    QTextCharFormat keywordFormat;
    QTextCharFormat stringFormat;
    QTextCharFormat numberFormat;
    QTextCharFormat commentFormat;
    QTextCharFormat preprocessorFormat;
    QTextCharFormat functionFormat;
    QTextCharFormat typeFormat;
    QTextCharFormat variableFormat;
    QTextCharFormat equalsFormat;

    QString currentLanguage = "Python3";

    void highlightCpp(const QString &text)
    {
        QStringList keywords = {
            "alignas", "alignof", "and", "asm", "auto",
            "bitand", "bitor", "bool", "break", "case",
            "catch", "char", "char8_t", "char16_t", "char32_t",
            "class", "compl", "concept", "const", "consteval",
            "constexpr", "constinit", "const_cast", "continue",
            "co_await", "co_return", "co_yield", "decltype",
            "default", "delete", "do", "double", "dynamic_cast",
            "else", "enum", "explicit", "export", "extern",
            "false", "float", "for", "friend", "goto",
            "if", "inline", "int", "long", "mutable",
            "namespace", "new", "noexcept", "not", "nullptr",
            "operator", "or", "private", "protected", "public",
            "register", "reinterpret_cast", "requires", "return",
            "short", "signed", "sizeof", "static", "static_assert",
            "static_cast", "struct", "switch", "template",
            "this", "thread_local", "throw", "true", "try",
            "typedef", "typeid", "typename", "union", "unsigned",
            "using", "virtual", "void", "volatile", "wchar_t",
            "while", "xor"
        };

        QString keywordPattern = "\\b(" + keywords.join("|") + ")\\b";

        QRegularExpression keywordRegex(keywordPattern);
        auto keywordIterator = keywordRegex.globalMatch(text);

        while (keywordIterator.hasNext())
        {
            auto match = keywordIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                keywordFormat
            );
        }

        QRegularExpression stringRegex(
            "\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'"
        );

        auto stringIterator = stringRegex.globalMatch(text);

        while (stringIterator.hasNext())
        {
            auto match = stringIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                stringFormat
            );
        }

        QRegularExpression numberRegex(
            "\\b\\d+(?:\\.\\d+)?\\b"
        );

        auto numberIterator = numberRegex.globalMatch(text);

        while (numberIterator.hasNext())
        {
            auto match = numberIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                numberFormat
            );
        }

        QRegularExpression commentRegex("//.*");

        auto commentIterator = commentRegex.globalMatch(text);

        while (commentIterator.hasNext())
        {
            auto match = commentIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                commentFormat
            );
        }

        QRegularExpression preprocessorRegex("^\\s*#.*");

        auto preprocessorIterator =
            preprocessorRegex.globalMatch(text);

        while (preprocessorIterator.hasNext())
        {
            auto match = preprocessorIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                preprocessorFormat
            );
        }

        QRegularExpression functionRegex(
            "\\b[A-Za-z_][A-Za-z0-9_]*(?=\\s*\\()"
        );

        auto functionIterator =
            functionRegex.globalMatch(text);

        while (functionIterator.hasNext())
        {
            auto match = functionIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                functionFormat
            );
        }

        QRegularExpression variableRegex("\\b[A-Za-z_][A-Za-z0-9_]*(?=\\s*=)");
        QRegularExpressionMatchIterator variableIterator = variableRegex.globalMatch(text);

        while (variableIterator.hasNext())
        {
            QRegularExpressionMatch match = variableIterator.next();
            setFormat(match.capturedStart(), match.capturedLength(), variableFormat);
        }

        QRegularExpression equalsRegex("=");
        QRegularExpressionMatchIterator equalsIterator = equalsRegex.globalMatch(text);

        while (equalsIterator.hasNext())
        {
            QRegularExpressionMatch match = equalsIterator.next();
            setFormat(match.capturedStart(), 1, equalsFormat);
        }
    
        
    }

    void highlightPython(const QString &text)
    {
        QStringList keywords = {
            "and", "as", "assert", "async", "await",
            "break", "case", "class", "continue",
            "def", "del", "elif", "else", "except",
            "False", "finally", "for", "from", "global",
            "if", "import", "in", "is", "lambda",
            "match", "None", "nonlocal", "not", "or",
            "pass", "raise", "return", "True", "try",
            "type", "while", "with", "yield"
        };

        QString keywordPattern = "\\b(" + keywords.join("|") + ")\\b";


        QRegularExpression variableRegex("\\b[A-Za-z_][A-Za-z0-9_]*(?=\\s*=)");
        QRegularExpressionMatchIterator variableIterator = variableRegex.globalMatch(text);

        while (variableIterator.hasNext())
        {
            QRegularExpressionMatch match = variableIterator.next();
            setFormat(match.capturedStart(), match.capturedLength(), variableFormat);
        }

        QRegularExpression equalsRegex("=");
        QRegularExpressionMatchIterator equalsIterator = equalsRegex.globalMatch(text);

        while (equalsIterator.hasNext())
        {
            QRegularExpressionMatch match = equalsIterator.next();
            setFormat(match.capturedStart(), 1, equalsFormat);
        }

        QRegularExpression keywordRegex(keywordPattern);
        auto keywordIterator = keywordRegex.globalMatch(text);

        while (keywordIterator.hasNext())
        {
            auto match = keywordIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                keywordFormat
            );
        }

        QRegularExpression stringRegex(
            "\"\"\".*\"\"\"|'''.*'''|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'"
        );

        auto stringIterator = stringRegex.globalMatch(text);

        while (stringIterator.hasNext())
        {
            auto match = stringIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                stringFormat
            );
        }

        QRegularExpression numberRegex(
            "\\b\\d+(?:\\.\\d+)?\\b"
        );

        auto numberIterator = numberRegex.globalMatch(text);

        while (numberIterator.hasNext())
        {
            auto match = numberIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                numberFormat
            );
        }

        QRegularExpression commentRegex("#.*");

        auto commentIterator = commentRegex.globalMatch(text);

        while (commentIterator.hasNext())
        {
            auto match = commentIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                commentFormat
            );
        }

        QRegularExpression functionRegex(
            "\\b[A-Za-z_][A-Za-z0-9_]*(?=\\s*\\()"
        );

        auto functionIterator =
            functionRegex.globalMatch(text);

        while (functionIterator.hasNext())
        {
            auto match = functionIterator.next();

            setFormat(
                match.capturedStart(),
                match.capturedLength(),
                functionFormat
            );
        }
    }
};


void goToLine(QTextEdit *editor)
{
    bool ok;

    int line = QInputDialog::getInt(
        nullptr,
        "Go To Line",
        "Line number:",
        1,
        1,
        editor->document()->blockCount(),
        1,
        &ok
    );

    if (!ok)
        return;

    QTextCursor cursor(editor->document()->findBlockByNumber(line - 1));

    editor->setTextCursor(cursor);
    editor->ensureCursorVisible();
    editor->setFocus();
}


void openBashShell()
{
    QTermWidget *terminal = new QTermWidget;

    terminal->setShellProgram("/bin/bash");
    terminal->setColorScheme("DarkPastels");
    terminal->setTerminalFont(QFont("Monospace", 15));

    terminal->resize(800, 600);
    terminal->move(40, 30);

    terminal->setAttribute(Qt::WA_DeleteOnClose);
    terminal->setWindowTitle("Bash Shell");

    terminal->show();
}


void findText(QTextEdit *editor)
{
    bool ok;

    QString text = QInputDialog::getText(
        nullptr,
        "Find",
        "Search for:",
        QLineEdit::Normal,
        "",
        &ok
    );

    if (!ok || text.isEmpty())
        return;

    if (editor->find(text))
    {
        editor->ensureCursorVisible();
        editor->setFocus();
    }
}

void listFunctions(QTextEdit *editor, QTextEdit *output)
{
    QStringList lines = editor->toPlainText().split('\n');

    struct FunctionInfo
    {
        QString name;
        int line;
    };

    std::vector<FunctionInfo> functions;

    QRegularExpression pythonPattern(
        "^\\s*def\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*\\("
    );

    QRegularExpression cppPattern(
        "^\\s*(?:[A-Za-z_][A-Za-z0-9_:<>*&\\s]+)\\s+([A-Za-z_][A-Za-z0-9_:]*)\\s*\\([^;]*\\)\\s*(?:\\{|$)"
    );

    for (int i = 0; i < lines.size(); ++i)
    {
        QString line = lines[i];

        QRegularExpressionMatch pythonMatch =
            pythonPattern.match(line);

        if (pythonMatch.hasMatch())
        {
            functions.push_back({
                pythonMatch.captured(1),
                i + 1
            });

            continue;
        }

        QRegularExpressionMatch cppMatch =
            cppPattern.match(line);

        if (cppMatch.hasMatch())
        {
            QString name = cppMatch.captured(1);

            if (name != "if" &&
                name != "for" &&
                name != "while" &&
                name != "switch" &&
                name != "catch")
            {
                functions.push_back({
                    name,
                    i + 1
                });
            }
        }
    }

    std::sort(
        functions.begin(),
        functions.end(),
        [](const FunctionInfo &a, const FunctionInfo &b)
        {
            return a.name.toLower() < b.name.toLower();
        }
    );

    QString result;
    result += "Function,   Line\n";
    result += "-------------------\n";

    for (const auto &function : functions)
    {
        result += function.name;
        result += "(), ";
        result += QString::number(function.line);
        result += "\n";
    }

    if (functions.empty())
        result += "No functions found.\n";

    output->setPlainText(result);
}

void codeMapper(QTextEdit *editor, QTextEdit *output)
{
    QStringList lines = editor->toPlainText().split('\n');

    struct Item
    {
        QString name;
        int line;
    };

    QVector<Item> functions;
    QVector<Item> classes;
    QVector<Item> includes;

    QRegularExpression pythonFunction(
        "^\\s*def\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*\\("
    );

    QRegularExpression cppFunction(
        "^\\s*(?:static\\s+|inline\\s+|virtual\\s+|const\\s+|constexpr\\s+|extern\\s+)*"
        "(?:[A-Za-z_][A-Za-z0-9_:<>]*\\s*[&*]?\\s+)"
        "([A-Za-z_][A-Za-z0-9_]*)\\s*\\([^;]*\\)\\s*(?:const\\s*)?(?:\\{|$)"
    );

    QRegularExpression classPattern(
        "^\\s*(?:class|struct)\\s+([A-Za-z_][A-Za-z0-9_]*)"
    );

    QRegularExpression includePattern(
        "^\\s*#include\\s*[<\"]([^>\"]+)[>\"]"
    );

    QStringList excluded =
    {
        "if",
        "for",
        "while",
        "switch",
        "catch"
    };

    for (int i = 0; i < lines.size(); ++i)
    {
        QString line = lines[i];
        int lineNumber = i + 1;

        QRegularExpressionMatch pyMatch =
            pythonFunction.match(line);

        if (pyMatch.hasMatch())
        {
            functions.append({
                pyMatch.captured(1),
                lineNumber
            });

            continue;
        }

        QRegularExpressionMatch cppMatch =
            cppFunction.match(line);

        if (cppMatch.hasMatch())
        {
            QString name = cppMatch.captured(1);

            if (!excluded.contains(name))
            {
                functions.append({
                    name,
                    lineNumber
                });
            }
        }

        QRegularExpressionMatch classMatch =
            classPattern.match(line);

        if (classMatch.hasMatch())
        {
            classes.append({
                classMatch.captured(1),
                lineNumber
            });
        }

        QRegularExpressionMatch includeMatch =
            includePattern.match(line);

        if (includeMatch.hasMatch())
        {
            includes.append({
                includeMatch.captured(1),
                lineNumber
            });
        }
    }

    auto sortItems = [](QVector<Item> &items)
    {
        std::sort(
            items.begin(),
            items.end(),
            [](const Item &a, const Item &b)
            {
                return a.name.toLower() < b.name.toLower();
            }
        );
    };

    sortItems(functions);
    sortItems(classes);
    sortItems(includes);

    QString result;

    result += "CODE MAP\n";
    result += "\n\n";

    result += "Functions\n";

    for (const Item &item : functions)
    {
        result += QString("  %1, %2\n")
            .arg(item.name + "()")
            .arg(item.line);
    }

    result += "\nClasses\n";

    for (const Item &item : classes)
    {
        result += QString("  %1, %2\n")
            .arg(item.name)
            .arg(item.line);
    }

    result += "\nIncludes\n";

    for (const Item &item : includes)
    {
        result += QString("  %1, %2\n")
            .arg(item.name)
            .arg(item.line);
    }

    output->setPlainText(result);
}


void showCursorPosition(QTextEdit *editor, QTextEdit *output)
{
    QTextCursor cursor = editor->textCursor();

    int line = cursor.blockNumber() + 1;
    int position = cursor.positionInBlock() + 1;

    output->setPlainText(
        QString("%1, %2")
        
            .arg(line)
            .arg(position)
    );
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMainWindow window;
    window.setWindowTitle("Code Machine");

    window.resize(900, 600);
    window.move(20, 20);
    window.setStyleSheet(
        "QMainWindow { background-color: grey; }"
    );
 
    window.menuBar()->setStyleSheet(
        "QMenuBar { background-color: black; color: white; font-family: 'Courier New'; font-size: 27px; }"
        "QMenu { background-color: white; color: black; font-family: 'Hack'; font-size: 22px; }"
    );
 


    auto *editor = new QTextEdit;
    editor->setFont(QFont("Hack", 14));

    auto *highlighter = new CodeHighlighter(editor->document());



    auto *output = new QTextEdit;
    //output->setReadOnly(true);
    output->setFont(QFont("Hack", 14));
    
    auto *terminal = new QTermWidget;
    terminal->setShellProgram("/bin/bash");
    terminal->setColorScheme("DarkPastels");
    terminal->setTerminalFont(QFont("Monospace", 9));

    auto *bottomStack = new QStackedWidget;

    bottomStack->addWidget(output);
    bottomStack->addWidget(terminal);

    auto *languageLabel = new QLabel("Language:");

    auto *languageBox = new QComboBox;
    languageBox->setStyleSheet("font-size: 20px;");

    languageBox->addItem("C");
    languageBox->addItem("C++");
    languageBox->addItem("Bash");
    languageBox->addItem("Go");
    languageBox->addItem("Rust");
    languageBox->addItem("Python3");
    languageBox->addItem("JavaScript");

    languageBox->setCurrentText("Rust");

    auto *runButton = new QPushButton("Run");
    auto *clearButton = new QPushButton("Clear");
    auto *bashButton = new QPushButton("Bash");

    runButton->setMinimumHeight(40);
    clearButton->setMinimumHeight(40);
    bashButton->setMinimumHeight(40); 

    runButton->setStyleSheet(
        "background-color: cyan; color: blue; font-size: 20px; font-family: 'Hack'"
    );
 
    clearButton->setStyleSheet(
        "background-color: red; color: white; font-size: 20px; font-family: 'Courier New';"
    );
    
    bashButton->setStyleSheet(
        "background-color: #222222; color: orange; font-size: 20px; font-family: 'Courier New';"
    );

 
    auto *splitter = new QSplitter(Qt::Vertical);

    splitter->addWidget(editor);
    splitter->addWidget(bottomStack);

    splitter->setSizes({200, 150});

    auto *languageLayout = new QHBoxLayout;

    languageLayout->addWidget(languageLabel);
    languageLayout->addWidget(languageBox);

    auto *buttonLayout = new QHBoxLayout;

    buttonLayout->addWidget(runButton);
    buttonLayout->addWidget(clearButton);
    buttonLayout->addWidget(bashButton);

    QObject::connect(bashButton,
    &QPushButton::clicked, [&]()
    {
        openBashShell();
    });

    auto *layout = new QVBoxLayout;

    layout->addLayout(languageLayout);
    layout->addWidget(splitter);
    layout->addLayout(buttonLayout);

    auto *central = new QWidget;
    central->setLayout(layout);

    window.setCentralWidget(central);

    auto *fileMenu = window.menuBar()->addMenu("File");

    auto *openAction = new QAction("Open", &window);
    auto *saveAction = new QAction("Save", &window);
    auto *exitAction = new QAction("Exit", &window);

    fileMenu->addAction(openAction);
    fileMenu->addAction(saveAction);
    fileMenu->addAction("Bash Shell Bottom", [&]()
    {
        bottomStack->setCurrentWidget(terminal);
        terminal->setFocus();
    });
    fileMenu->addAction("Code Map", [&]()
    {
        codeMapper(editor, output);
    });

    fileMenu->addAction("Go To Line", [&]()
    {
        goToLine(editor);
    });
    fileMenu->addAction("Find Text", [&]()
    {
        findText(editor);
    });
    fileMenu->addAction("Cursor Position", [&]()
    {
        showCursorPosition(editor, output);
    });
     
    fileMenu->addAction("Bash Shell", []()
    {
        openBashShell();
    });
    fileMenu->addAction("List Functions", [&]()
    {
        listFunctions(editor, output);
    });
    fileMenu->addSeparator();
    fileMenu->addAction(exitAction);

    auto *devMenu = window.menuBar()->addMenu("Dev");

    auto *runCAction = new QAction("Run C", &window);
    auto *runCppAction = new QAction("Run C++", &window);
    auto *runBashAction = new QAction("Run Bash", &window);
    auto *runGoAction = new QAction("Run Go", &window);
    auto *runRustAction = new QAction("Run Rust", &window);
    auto *runPythonAction = new QAction("Run Python3", &window);
    auto *runJavaScriptAction = new QAction("Run JavaScript", &window);

    devMenu->addAction(runCAction);
    devMenu->addAction(runCppAction);
    devMenu->addAction(runBashAction);
    devMenu->addAction(runGoAction);
    devMenu->addAction(runRustAction);
    devMenu->addAction(runPythonAction);
    devMenu->addAction(runJavaScriptAction);

    auto runCode = [&](const QString &language)
    {
        output->clear();

        QTemporaryDir tempDir;

        if (!tempDir.isValid())
        {
            output->setPlainText("Could not create temporary directory.");
            return;
        }

        QString sourceFile;
        QString executable;

        if (language == "C")
            sourceFile = tempDir.path() + "/program.c";
        else if (language == "C++")
            sourceFile = tempDir.path() + "/program.cpp";
        else if (language == "Bash")
            sourceFile = tempDir.path() + "/program.sh";
        else if (language == "Go")
            sourceFile = tempDir.path() + "/program.go";
        else if (language == "Rust")
            sourceFile = tempDir.path() + "/program.rs";
        else if (language == "Python3")
            sourceFile = tempDir.path() + "/program.py";
        else if (language == "JavaScript")
            sourceFile = tempDir.path() + "/program.js";

        QFile file(sourceFile);

        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            output->setPlainText("Could not create source file.");
            return;
        }

        file.write(editor->toPlainText().toUtf8());
        file.close();

if (language == "C")
{
    executable = tempDir.path() + "/program";

    QProcess compiler;

    compiler.start(
        "gcc",
        {sourceFile, "-o", executable}
    );

    compiler.waitForFinished();

    QString errors =
        QString::fromUtf8(compiler.readAllStandardError());

    if (compiler.exitCode() != 0)
    {
        output->setPlainText(errors);
        return;
    }

    QProcess program;

    program.start(executable);
    program.waitForFinished();

    output->setPlainText(
        QString::fromUtf8(program.readAllStandardOutput()) +
        QString::fromUtf8(program.readAllStandardError())
    );
}

else if (language == "C++")
{
    executable = tempDir.path() + "/program";

    QString code = editor->toPlainText();

    bool isQtProgram =
        code.contains("#include <QApplication>") ||
        code.contains("#include <QWidget>") ||
        code.contains("#include <QMainWindow>") ||
        code.contains("#include <QPushButton>") ||
        code.contains("#include <QLabel>") ||
        code.contains("#include <QTextEdit>");

    QProcess compiler;

    if (isQtProgram)
    {
        QStringList arguments;

        arguments << sourceFile;
        arguments << "-o";
        arguments << executable;

        QProcess pkgConfig;

        pkgConfig.start(
            "pkg-config",
            {"--cflags", "--libs", "Qt6Widgets"}
        );

        pkgConfig.waitForFinished();

        if (pkgConfig.exitCode() != 0)
        {
            output->setPlainText(
                QString::fromUtf8(pkgConfig.readAllStandardError())
            );
            return;
        }

        QString flags =
            QString::fromUtf8(pkgConfig.readAllStandardOutput()).trimmed();

        arguments += QProcess::splitCommand(flags);

        compiler.start("g++", arguments);
    }
    else
    {
        compiler.start(
            "g++",
            {sourceFile, "-o", executable}
        );
    }

    compiler.waitForFinished();

    QString errors =
        QString::fromUtf8(compiler.readAllStandardError());

    if (compiler.exitCode() != 0)
    {
        output->setPlainText(errors);
        return;
    }

    if (isQtProgram)
    {
        if (!QProcess::startDetached(executable))
        {
            output->setPlainText(
                "Could not start the Qt application."
            );
        }

        return;
    }

    QProcess program;

    program.start(executable);
    program.waitForFinished();

    output->setPlainText(
        QString::fromUtf8(program.readAllStandardOutput()) +
        QString::fromUtf8(program.readAllStandardError())
    );
}

        else if (language == "Bash")
        {
            QProcess program;

            program.start("bash", {sourceFile});
            program.waitForFinished();

            output->setPlainText(
                QString::fromUtf8(program.readAllStandardOutput()) +
                QString::fromUtf8(program.readAllStandardError())
            );
        }

        else if (language == "Go")
        {
            QProcess program;

            program.setWorkingDirectory(tempDir.path());

            program.start(
                "go",
                {"run", sourceFile}
            );

            program.waitForFinished();

            output->setPlainText(
                QString::fromUtf8(program.readAllStandardOutput()) +
                QString::fromUtf8(program.readAllStandardError())
            );
        }

        else if (language == "Rust")
        {
            executable = tempDir.path() + "/program";

            QProcess compiler;

            compiler.start(
                "rustc",
                {sourceFile, "-o", executable}
            );

            compiler.waitForFinished();

            QString errors =
                QString::fromUtf8(compiler.readAllStandardError());

            if (compiler.exitCode() != 0)
            {
                output->setPlainText(errors);
                return;
            }

            QProcess program;

            program.start(executable);
            program.waitForFinished();

            output->setPlainText(
                QString::fromUtf8(program.readAllStandardOutput()) +
                QString::fromUtf8(program.readAllStandardError())
            );
        }

        else if (language == "Python3")
        {
            QProcess program;

            program.start(
                "python3",
                {sourceFile}
            );

            program.waitForFinished();

            output->setPlainText(
                QString::fromUtf8(program.readAllStandardOutput()) +
                QString::fromUtf8(program.readAllStandardError())
            );
        }

        else if (language == "JavaScript")
        {
            QProcess program;

            program.start(
                "node",
                {sourceFile}
            );

            program.waitForFinished();

            output->setPlainText(
                QString::fromUtf8(program.readAllStandardOutput()) +
                QString::fromUtf8(program.readAllStandardError())
            );
        }
    };

    QObject::connect(
        languageBox,
        &QComboBox::currentTextChanged,
        [&](const QString &language)
        {
            highlighter->setLanguage(language);
        }
    );

    QObject::connect(
        runButton,
        &QPushButton::clicked,
        [&]()
        {
            runCode(languageBox->currentText());
        }
    );

    QObject::connect(
        clearButton,
        &QPushButton::clicked,
        [&]()
        {
            editor->clear();
        }
    );

    QObject::connect(
        runCAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("C");
            runCode("C");
        }
    );

    QObject::connect(
        runCppAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("C++");
            runCode("C++");
        }
    );

    QObject::connect(
        runBashAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("Bash");
            runCode("Bash");
        }
    );

    QObject::connect(
        runGoAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("Go");
            runCode("Go");
        }
    );

    QObject::connect(
        runRustAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("Rust");
            runCode("Rust");
        }
    );

    QObject::connect(
        runPythonAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("Python3");
            runCode("Python3");
        }
    );

    QObject::connect(
        runJavaScriptAction,
        &QAction::triggered,
        [&]()
        {
            languageBox->setCurrentText("JavaScript");
            runCode("JavaScript");
        }
    );

    QObject::connect(
        openAction,
        &QAction::triggered,
        [&]()
        {
            QString fileName = QFileDialog::getOpenFileName(
                &window,
                "Open File",
                "",
                "Source Files (*.c *.cpp *.cc *.cxx *.h *.hpp *.sh *.go *.rs *.py *.js);;All Files (*)"
            );

            if (fileName.isEmpty())
                return;

            QFile file(fileName);

            if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
            {
                QMessageBox::warning(
                    &window,
                    "Error",
                    "Could not open the file."
                );

                return;
            }

            editor->setPlainText(
                QString::fromUtf8(file.readAll())
            );

            file.close();

            window.setWindowTitle(
                "** Code Forge **"
            );
        }
    );

    QObject::connect(
        saveAction,
        &QAction::triggered,
        [&]()
        {

            QString fileName = QFileDialog::getSaveFileName(
                &window,
                "Save File As",
                "",
                "C++ Files (*.cpp);;C Files (*.c);;Bash Files (*.sh);;Go Files (*.go);;Rust Files (*.rs);;Python Files (*.py);;JavaScript Files (*.js);;All Files (*)"
            );

            if (fileName.isEmpty())
                return;

            QFile file(fileName);

            if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
            {
                QMessageBox::warning(
                    &window,
                    "Error",
                    "Could not save the file."
                );

                return;
            }

            file.write(editor->toPlainText().toUtf8());
            file.close();

            window.setWindowTitle(
                "C++ IDE - " +
                QFileInfo(fileName).fileName()
            );
        }
    );

    QObject::connect(
        exitAction,
        &QAction::triggered,
        [&]()
        {
            window.close();
        }
    );

    window.show();

    return app.exec();
}

       
