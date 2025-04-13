#!/bin/bash
g++ -o output *.cpp

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    ./output
    rm output
else
    echo "Compilation failed."
fi