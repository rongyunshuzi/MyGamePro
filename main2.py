import threading
import requests
import time

# 计数器的初始值
counter = 0
counter_lock = threading.Lock()  # 用于线程安全地操作计数器


# 用于访问网站的函数
def task(thread_id, url):
    global counter
    with counter_lock:
        counter += 1  # 线程启动时，计数器 +1
    # print(f"线程 {thread_id} 开始请求 {url}")

    try:
        response = requests.get(url)  # 访问指定的网站
        # print(f"线程 {thread_id} 请求完成，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"线程 {thread_id} 请求失败: {e}")

    with counter_lock:
        counter -= 1  # 请求完成后，计数器 -1
    # print(f"线程 {thread_id} 完成工作，当前计数器: {counter}")


# 线程数
num_threads = 50
url = "http://localhost"  # 需要访问的网址

# 创建线程并启动
threads = []
start_time = time.time()
for i in range(num_threads):
    thread = threading.Thread(target=task, args=(i, url))
    threads.append(thread)
    thread.start()

end_time = time.time() - start_time
print(end_time)

# 等待所有线程完成
for thread in threads:
    thread.join()

print("所有线程完成工作")