#!/bin/sh

x=10
y=3
z=3

while [ $x -lt 500 ]; do
    while [ $y -lt 10 ]; do
        z=$y
        python fsm.py $x $y $z >> levenshtein.results
        y=$(( $y + 1 ))
    done
    x=$(( $x*2 ))
    y=3
done
