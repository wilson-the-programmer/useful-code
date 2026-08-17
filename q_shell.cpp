
#include <QApplication>
#include <qtermwidget6/qtermwidget.h>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTermWidget terminal;

    terminal.setShellProgram("/bin/bash");
    terminal.setColorScheme("DarkPastels");
    terminal.setTerminalFont(QFont("Monospace", 9));

    terminal.resize(200, 200);
    terminal.show();

    return app.exec();
}

