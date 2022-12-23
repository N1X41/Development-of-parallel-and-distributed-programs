import random
import time
import multiprocessing
import numpy
import ctypes

class matrix(object):
    def __init__(self):
        self.n = 0 # количество строк и столбцов
        self.lines = []

    def set_matrix(self, file):
        new_file = file.readlines()
        self.n = int(new_file[0])
        for i in range(0, self.n):
            line = []
            for j in range(0, self.n):
                line.append(float(new_file[j + i * self.n + 2]))
            self.lines.append(line)

    def print(self):
        for line in self.lines:
            print(line)

    def set_empty(self, n):
        self.n = n
        for i in range(0, self.n):
            line = []
            for j in range(0, self.n):
                line.append(0)
            self.lines.append(line)

def make_answer(shared_array, shape, x, y, start, end):
    var_answer = to_numpy_array(shared_array, shape)
    for i in range(start, end):
        for j in range(0, x.n):
            cage = 0
            for k in range(0, x.n):
                cage = cage + x.lines[i][k] * y.lines[k][j]
            var_answer[i][j] = cage

def make_answer_1():
    for i in range(0, answer.n):
        for j in range(0, answer.n):
            cage = 0
            for k in range(0, answer.n):
                cage = cage + x.lines[i][k] * y.lines[k][j]
            answer.lines[i][j] = cage

def to_shared_array(arr, ctype):
    shared_array = multiprocessing.Array(ctype, arr.size, lock=False)
    temp = numpy.frombuffer(shared_array, dtype=arr.dtype)
    temp[:] = arr.flatten(order='C')
    return shared_array

def to_numpy_array(shared_array, shape):
    arr = numpy.ctypeslib.as_array(shared_array)
    return arr.reshape(shape)

x = matrix()
y = matrix()
answer = matrix()
if __name__ == '__main__':
    file = open('matrix.txt', 'w')
    file.write("400\n")
    for i in range(0, 160000):
        file.write("\n" + str(random.uniform(-10.0, 10.0)))
    file.close()

    file = open('matrix 2.txt', 'w')
    file.write("400\n")
    for i in range(0, 160000):
        file.write("\n" + str(random.uniform(-10.0, 10.0)))
    file.close()

    file1 = open('matrix.txt', 'r')
    file2 = open('matrix 2.txt', 'r')

    x.set_matrix(file1)
    y.set_matrix(file2)

    file1.close()
    file2.close()

    answer.set_empty(x.n)

    # без многопоточности
    time_start = time.perf_counter()

    make_answer_1()

    time_end = time.perf_counter()
    print("Время без многопоточности : " + str(time_end - time_start))
    print("Ячейка 135 277 равна : " + str(round(answer.lines[134][276], 4)))
    print()

    # 2 потока
    time_start = time.perf_counter()

    mp_array = numpy.zeros((400, 400), dtype=numpy.float32)
    shared_array = to_shared_array(mp_array, ctypes.c_float)
    answer_mp = to_numpy_array(shared_array, mp_array.shape)

    th1 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 0, 200,))
    th2 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 200, 400,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    time_end = time.perf_counter()
    print("Время c 2 потоками : " + str(time_end - time_start))
    print("Ячейка 135 277 равна : " + str(round(answer_mp[134][276], 4)))
    print()

    # 4 потока
    time_start = time.perf_counter()

    mp_array = numpy.zeros((400, 400), dtype=numpy.float32)
    shared_array = to_shared_array(mp_array, ctypes.c_float)
    answer_mp = to_numpy_array(shared_array, mp_array.shape)

    th1 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 0, 100, ))
    th2 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 100, 200, ))
    th3 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 200, 300, ))
    th4 = multiprocessing.Process(target=make_answer, args=(shared_array, mp_array.shape, x, y, 300, 400, ))

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    time_end = time.perf_counter()
    print("Время c 4 потоками : " + str(time_end - time_start))
    print("Ячейка 135 277 равна : " + str(round(answer_mp[134][276], 4)))