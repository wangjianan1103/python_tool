#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time
import threading
from queue import Queue


class Worker(threading.Thread):
    def __init__(self, selfManager, name):
        threading.Thread.__init__(self)
        self.work_queue = selfManager.work_queue
        self.name = name
        self.start()

    def run(self):
        while True:
            try:
                if self.work_queue.empty():
                    # print("thread-%s: queue is empty, waiting for task." % self.name)
                    continue
                text = self.work_queue.get(block=True)
                # todo Anything
                print("%s thread-%s: doing task text: %s" % (
                str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), self.getName(), str(text)))

                time.sleep(10)
                self.work_queue.task_done()
            except Exception as e:
                print("thread-%s: task is error: %s" % (self.getName(), str(e)))
                break


class WorkManager:
    def __init__(self, thread_num):
        self.work_queue = Queue()  # 队列对象
        self.threads = []
        self._init_thread_pool(thread_num)

    def _init_thread_pool(self, thread_num):
        """初始化线程"""
        for name in range(thread_num):
            self.threads.append(Worker(self, str(name)))

    def add_job(self, job):
        """初始化工作队列"""
        self.work_queue.put(job)


if __name__ == '__main__':
    work_manager = WorkManager(5)
    for i in range(100):
        work_manager.add_job(i)
