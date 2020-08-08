import queue
import threading
import time
queue = queue.Queue()


class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while (True):
            if (queue.qsize() < 30):
                for i in range(15):
                    count += 1
                    m = '生产商品' + str(count)
                    print(m)
                    print()
                    queue.put(m)
                time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global queue
        while (True):
            if (queue.qsize() > 25):
                for i in range(5):
                    n = self.name + '消费了' + queue.get()
                    print(n)
                    print()


def main():
    for i in range(50):
        queue.put('初始商品' + str(i))
    p = Producer()
    p.start()
    for i in range(5):
        c = Consumer()
        c.start()


if __name__ == '__main__':
    main()
