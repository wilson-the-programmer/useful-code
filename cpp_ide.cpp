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
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMainWindow window;
    window.setWindowTitle("C++ IDE");
    window.resize(500, 600);

    window.menuBar()->setStyleSheet(
        "QMenuBar { font-size: 16px; }"
        "QMenu { font-size: 16px; }"
    );

    auto *editor = new QTextEdit;
    editor->setFont(QFont("Courier New", 11));

    editor->setPlainText(
        "#include <iostream>\n"
        "\n"
        "int main()\n"
        "{\n"
        "    std::cout << \"Hello from my IDE!\\n\";\n"
        "    return 0;\n"
        "}\n"
    );

    auto *output = new QTextEdit;
    output->setReadOnly(true);
    output->setFont(QFont("Courier New", 11));

    auto *languageLabel = new QLabel("Language:");

    auto *languageBox = new QComboBox;

    languageBox->addItem("C");
    languageBox->addItem("C++");
    languageBox->addItem("Bash");
    languageBox->addItem("Go");
    languageBox->addItem("Rust");
    languageBox->addItem("Python3");
    languageBox->addItem("JavaScript");

    languageBox->setCurrentText("C++");

    auto *runButton = new QPushButton("Run");
    auto *clearButton = new QPushButton("Clear");

    runButton->setMinimumHeight(50);
    clearButton->setMinimumHeight(50);

    runButton->setStyleSheet(
        "background-color: #FFFF00; color: #0000FF;"
    );

    clearButton->setStyleSheet(
        "background-color: #FFFF00; color: #0000FF;"
    );

    auto *splitter = new QSplitter(Qt::Vertical);

    splitter->addWidget(editor);
    splitter->addWidget(output);

    splitter->setSizes({400, 150});

    auto *languageLayout = new QHBoxLayout;

    languageLayout->addWidget(languageLabel);
    languageLayout->addWidget(languageBox);

    auto *buttonLayout = new QHBoxLayout;

    buttonLayout->addWidget(runButton);
    buttonLayout->addWidget(clearButton);

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
    auto *saveAsAction = new QAction("Save As", &window);
    auto *exitAction = new QAction("Exit", &window);

    fileMenu->addAction(openAction);
    fileMenu->addAction(saveAction);
    fileMenu->addAction(saveAsAction);
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

            QProcess compiler;

            compiler.start(
                "g++",
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
                "C++ IDE - " +
                QFileInfo(fileName).fileName()
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
                "Save File",
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
        saveAsAction,
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
