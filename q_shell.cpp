#include <QApplication>
#include <qtermwidget6/qtermwidget.h>
#include <QRandomGenerator>
#include <vector>

QString randScheme()
{
    std::vector<QString> schemes = {
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

    int index = QRandomGenerator::global()->bounded(static_cast<int>(schemes.size()));

    return schemes[index];
}



//QString my_scheme = randScheme();


QString my_scheme = "Linux";


//terminal->setColorScheme(my_scheme);





int main(int argc, char *argv[])
{

    QApplication app(argc, argv);

    QTermWidget terminal;

    terminal.setShellProgram("/bin/bash");
    terminal.setColorScheme(my_scheme);
    terminal.setTerminalFont(QFont("Monospace", 12));
    //terminal.sendText("Terminal Scheme: " + my_scheme + "\n");

    terminal.resize(800, 650);

    terminal.show();

    return app.exec();

}

