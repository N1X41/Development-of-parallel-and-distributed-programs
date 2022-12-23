#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <math.h>

#define N 512

void matrixByVectorMultiply(double** matrix, double* vector, double* result) {
  int i, j;
  #pragma omp parallel for shared(matrix, vector, result) private(i, j)
  for (i = 0; i < N; i++) {
      result[i] = 0;
      for (j = 0; j < N; j++)
       result[i] += (matrix[i][j] * vector[j]);
  }
}

void multVectorByScalar(double* vector, double scalar) {
    int i;
    #pragma omp parallel for shared(vector) private(i)
    for (i = 0; i < N; i++)
     vector[i] *= scalar;
}

void diffVectors(double* self, double* vector) {
  int i;
  #pragma omp parrallel for shared(self, vector) private(i) 
  for (i = 0; i < N; i ++)
   self[i] -= vector[i];
}

double vectorNorm(double* vector) {
  int i;
  double s = 0;
  #pragma omp parrallel for shared(vector) private(i) reduction (+:s)
  for (i = 0; i < N; i++)
   s += (vector[i] * vector[i]);
  return sqrt(s);
}

int main(){  
  double epsilon = 0.00001;
  double tau = 0.1/N;
  
  double **A;
  A = (double**)malloc(sizeof(double*) * N);

  for (int i = 0; i < N; i++) {
    A[i] = (double*)malloc(sizeof(double)*N);
    for (int j = 0; j < N; j++) {
      if (i == j)
       A[i][j] = 2.0;
      else A[i][j] = 1.0;
    }
  }
  double* u;
  u = (double*)malloc(sizeof(double) * N);
  for (int i = 0; i < N; i ++)
   u[i] = sin((2 * M_PI * i)/N);
  double* x;
  x = (double*)malloc(sizeof(double) * N);
  for (int i = 0; i < N; i ++)
   x[i] =  0;
  double* b;
  double* y;
  b = (double*)malloc(sizeof(double) * N);
  y = (double*)malloc(sizeof(double) * N);
  matrixByVectorMultiply(A, u, b);
  double norm_b;
  norm_b = vectorNorm(b);
  while(1) {
    matrixByVectorMultiply(A, x, y);
    diffVectors(y, b);
    double norm_y;
    norm_y = vectorNorm(y);
    if ((norm_y / norm_b) < epsilon) {
      break;
    }
    multVectorByScalar(y, tau);
    diffVectors(x, y);
  }
  free(y);
  free(u);
  free(x);
  free(b);
  for (int i = 0; i < N; i++) {
    free(A[i]);
  }
  free(A);
  
  printf("Готово\n");
  return 0;
}  