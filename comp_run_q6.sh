#!/bin/bash

qt6_app="$1"

exeF="${qt6_app%.cpp}"

g++ "$qt6_app" -o "$exeF" $(pkg-config --cflags --libs Qt6Widgets) -lqtermwidget6

if [ $? -eq 0 ]; then
    ./"$exeF"
fi
