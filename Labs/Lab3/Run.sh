#!/bin/bash
export OMP_NUM_THREADS=1
TIMEFORMAT="Время выполнения %lR"
time {
    ./lab3
}

export OMP_NUM_THREADS=2
TIMEFORMAT="Время выполнения %lR"
time {
    ./lab3
}

export OMP_NUM_THREADS=4
TIMEFORMAT="Время выполнения %lR"
time {
    ./lab3
}

export OMP_NUM_THREADS=8
TIMEFORMAT="Время выполнения %lR"
time {
    ./lab3
}
