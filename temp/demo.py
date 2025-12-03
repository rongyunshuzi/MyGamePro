import threading
import concurrent.futures
import time
from typing import List


class Spinner:
    def __init__(self, target_count: int = 1000, num_workers: int = 10):
        self.target_count = target_count
        self.num_workers = num_workers
        self.count = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.start_time = None
        self.end_time = None

    def spin(self, worker_id: int = None):
        """执行spin的线程函数"""
        while not self.stop_event.is_set():
            with self.lock:
                # 检查是否达到目标
                if self.count >= self.target_count:
                    self.stop_event.set()
                    break

                # 增加计数
                self.count += 1
                current_count = self.count

            # 模拟工作
            time.sleep(0.2)

            # 显示进度（避免频繁打印）
            if current_count % 100 == 0:
                print(f"进度: {current_count}/{self.target_count}")

        # 线程结束
        if worker_id is not None:
            print(f"工作线程 {worker_id} 已结束")

    def start(self):
        """启动所有线程"""
        self.start_time = time.time()
        print(f"开始执行，目标: {self.target_count} 次，使用 {self.num_workers} 个线程")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            # 提交所有任务
            futures = []
            for i in range(self.num_workers):
                future = executor.submit(self.spin, i)
                futures.append(future)

            try:
                # 监控并等待所有任务完成
                while not self.stop_event.is_set():
                    time.sleep(0.1)  # 监控间隔

                    # 双重检查（以防万一）
                    with self.lock:
                        if self.count >= self.target_count:
                            self.stop_event.set()
                            break

                # 等待所有任务完成
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result(timeout=1.0)
                    except concurrent.futures.TimeoutError:
                        print("任务超时")
                    except Exception as e:
                        print(f"任务异常: {e}")

            except KeyboardInterrupt:
                print("\n用户中断，正在停止...")
                self.stop_event.set()

                # 取消所有任务
                for future in futures:
                    future.cancel()

            finally:
                self.end_time = time.time()
                self.print_summary()

    def print_summary(self):
        """打印执行摘要"""
        print("\n" + "=" * 50)
        print("执行摘要:")
        print(f"目标次数: {self.target_count}")
        print(f"实际完成: {self.count}")

        if self.start_time and self.end_time:
            elapsed = self.end_time - self.start_time
            print(f"总耗时: {elapsed:.2f} 秒")

            if elapsed > 0:
                print(f"平均速度: {self.count / elapsed:.2f} 次/秒")

        print("=" * 50)


if __name__ == '__main__':
    # 创建Spinner实例并运行
    spinner = Spinner(target_count=1000, num_workers=10)
    spinner.start()