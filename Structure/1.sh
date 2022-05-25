#!/bin/bash
for layer1 in {1..3..1}
do
mkdir ${layer1}
cp main.py ${layer1}
cp Matrix_input.pkl ${layer1}
cp Matrix_output.pkl ${layer1}
cd ${layer1}
python3 main.py 8 29 29
cd ..
done

