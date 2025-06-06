#include <stdio.h>
// 核函数必须使用 __global__ 修饰符声明。
__global__ void say_hello() {
    printf("Hello World from GPU!\n");
}

int main() {
    printf("Hello World from CPU!\n");

    // 启动内核，核函数调用语法
    say_hello<<<1, 1>>>();
    // 启动一个网格（grid），包含 1 个线程块（block）。
    // 每个线程块中包含 1 个线程（thread）。
    // 所以总共会启动 1 个线程 来执行 say_hello 这个核函数。

    // 等待GPU完成
    cudaDeviceSynchronize();

    return 0;
}

// kernel_name<<<grid_dim, block_dim, shared_mem_size, stream>>>(args...);
// 其中：
// kernel_name：你要调用的 CUDA 核函数名。
// <<<...>>>：这是 CUDA 特有的语法，用于配置核函数执行的线程结构和参数。
// grid_dim：网格中线程块的数量（dim3 类型），决定启动多少个线程块。
// block_dim：每个线程块中线程的数量（dim3 类型）。
// shared_mem_size（可选）：为该核函数分配的共享内存大小（以字节为单位），默认为 0。
// stream（可选）：指定异步流，默认为 0（即默认流）。

// CUDA 的 <<<...>>> 语法是扩展的 C++ 语法，只能被 CUDA 编译器识别（如 nvcc）。