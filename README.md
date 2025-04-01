# Queue System with Multi-Threading & Multi-Processing

This project implements a configurable queue system that processes API requests using **multi-threading** or **multi-processing**. It performs **matrix multiplications** using numpy.matmul() from Numpy to simulate API requests, allowing performance testing under different workloads.

## Features

- Supports both **multi-threading** and **multi-processing**.
- Configurable **queue size**, **number of workers**, **request rate**, and **total requests**.
- Processes large matrices (1000x1000) to simulate CPU-intensive tasks.
- Benchmarks and compares execution times between threading and processing.

