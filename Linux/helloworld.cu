#include <stdio.h>

__global__ void say_hello() {
    printf("Hello World from GPU!\n");
}

int main() {
    printf("Hello World from CPU!\n");

    // 启动内核
    say_hello<<<1, 1>>>();

    // 等待GPU完成
    cudaDeviceSynchronize();

    return 0;
}