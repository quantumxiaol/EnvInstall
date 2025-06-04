#include <stdio.h>

__global__ void vectorAdd(int *a, int *b, int *c, int n) {
    int i = threadIdx.x;
    if (i < n)
        c[i] = a[i] + b[i];
}

int main() {
    int a[] = {1, 2, 3};
    int b[] = {4, 5, 6};
    int c[3];
    int n = 3;

    int *d_a, *d_b, *d_c;

    // 分配显存
    cudaMalloc(&d_a, n * sizeof(int));
    cudaMalloc(&d_b, n * sizeof(int));
    cudaMalloc(&d_c, n * sizeof(int));

    // 拷贝数据到显存
    cudaMemcpy(d_a, a, n * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, n * sizeof(int), cudaMemcpyHostToDevice);

    // 在 GPU 上执行 kernel
    vectorAdd<<<1, 3>>>(d_a, d_b, d_c, n);

    // 拷贝结果回主机内存
    cudaMemcpy(c, d_c, n * sizeof(int), cudaMemcpyDeviceToHost);

    // 打印结果
    for (int i = 0; i < n; i++) {
        printf("%d ", c[i]);
    }
    printf("\n");

    // 释放显存
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    return 0;
}