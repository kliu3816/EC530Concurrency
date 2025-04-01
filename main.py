import numpy as np
import threading
import queue
import multiprocessing
import time

def process_matrix(matrices):
    A, B = matrices  # Get the two matrices
    result = np.matmul(A, B)  # Multiply them
    return result

##################Implement Multi-threading############
request_queue = queue.Queue(10)

def thread_worker(task_queue, thread_id):
    while True:
        matrices = task_queue.get()
        process_matrix(matrices)
        print(f"[Thread-{thread_id}] Processed matrix of size {matrices[0].shape}")
        task_queue.task_done()

#-----------------Implement Multi-processing------------#
request_queue = multiprocessing.Queue(maxsize=10)

def process_worker(task_queue):
    while True:
        matrices = task_queue.get()
        if matrices is None:  # Stop signal received
            break
        process_matrix(matrices)
        print(f"[Process {multiprocessing.current_process().name}] Processed matrix of size {matrices[0].shape}")



# Function to generate and add requests to the queue
def generate_requests(task_queue, num_requests, delay):
    for i in range(num_requests):
        A = np.random.rand(1000, 1000)  # Generate large matrices
        B = np.random.rand(1000, 1000)
        task_queue.put((A, B))  # Add to queue
        print(f"[Main] Added request {i+1}/{num_requests}")
        time.sleep(delay)  # Simulate different request speeds

def main():
    # Prompt user for threading or processing
    while True:
        user_choice = input("Choose processing mode: (1) Multi-threading, (2) Multi-processing: ").strip()
        if user_choice in ["1", "2"]:
            use_threads = user_choice == "1"
            break
        print("Invalid choice! Please enter 1 or 2.")

    # Prompt for configuration values
    queue_size = int(input("Enter queue size (default: 10): ") or 10)
    num_workers = int(input("Enter number of workers (threads/processes) (default: 4): ") or 4)
    num_requests = int(input("Enter number of requests to simulate (default: 20): ") or 20)
    delay = float(input("Enter delay between requests (seconds) (default: 0.05): ") or 0.05)

    print(f"\nStarting {'Multi-threading' if use_threads else 'Multi-processing'} Queue System...\n")

    if use_threads:
        task_queue = queue.Queue(maxsize=queue_size)  # Thread-safe queue
        workers = []
        
        for i in range(num_workers):
            t = threading.Thread(target=thread_worker, args=(task_queue, i+1), daemon=True)
            t.start()
            workers.append(t)

    else:
        task_queue = multiprocessing.Queue(maxsize=queue_size)  # Process-safe queue
        workers = []

        for _ in range(num_workers):
            p = multiprocessing.Process(target=process_worker, args=(task_queue,), daemon=True)
            p.start()
            workers.append(p)

    start_time = time.time()
    generate_requests(task_queue, num_requests, delay)
    
    if use_threads:
        task_queue.join()  # Wait for all tasks to finish in threads
    else:
    # Send "None" signals to tell processes to exit
        for _ in range(num_workers):
            task_queue.put(None)  # Each worker will get a None and break out of the loop
    
    # Wait for all worker processes to finish
        for p in workers:
            p.join()

    end_time = time.time()
    print(f"\nAll tasks completed in {end_time - start_time:.2f} seconds.")

# Run main function
if __name__ == "__main__":
    main()
