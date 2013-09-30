from threading import Thread
from Queue import Queue
from time import sleep

q = Queue()
NUM = 2
JOBS = 10

#single task
def do_something_using(arguments):
    print arguments

#working process  get work from queue
def working():
    while True:
        arguments = q.get()
        do_something_using(arguments)
        sleep(1)
        q.task_done()

for i in range(NUM):
    t = Thread(target=working)
    t.setDaemon(True)
    t.start()

for i in range(JOBS):
    q.put(i)

q.join()
