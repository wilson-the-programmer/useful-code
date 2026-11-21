/*

Note:


you may need to do:

sudo apt install build-essential qt6-base-dev libqtermwidget6-2-dev pkg-config

*/










#include <QApplication>
#include <QTabWidget>
#include <qtermwidget6/qtermwidget.h>
#include <QFont>
#include <QStringList>

QStringList color_schemes = {
    "BlackOnLightYellow",
    "BlackOnRandomLight",
    "BlackOnWhite",
    "BreezeModified",
    "DarkPastels",
    "Falcon",
    "GreenOnBlack",
    "Linux",
    "Nord",
    "Solarized",
    "SolarizedLight",
    "Tango",
    "Ubuntu",
    "WhiteOnWhite"
};

QString my_scheme = "Falcon";

QTermWidget *createTerminal()
{
    QTermWidget *terminal = new QTermWidget();

    terminal->setShellProgram("/bin/bash");
    terminal->setColorScheme(my_scheme);
    terminal->setTerminalFont(QFont("Monospace", 12));

    return terminal;
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTabWidget tabs;

    tabs.addTab(createTerminal(), "Shell 1");
    tabs.addTab(createTerminal(), "Shell 2");
    tabs.addTab(createTerminal(), "Shell 3");

    tabs.setWindowTitle("My Qt Terminal");
    tabs.setTabPosition(QTabWidget::North);
    tabs.setMovable(true);
    tabs.setDocumentMode(true);

    tabs.resize(800, 650);
    tabs.move(100, 100);

    tabs.show();

    return app.exec();
}

