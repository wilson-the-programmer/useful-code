echo ""

read -p "C++ Qt6: " qt6_file

exeF="${qt6_file%.cpp}"

g++ "$qt6_file" -o "$exeF" $(pkg-config --cflags --libs Qt6Widgets) -lqtermwidget6

if [ $? -eq 0 ]; then
./"$exeF"
fi

