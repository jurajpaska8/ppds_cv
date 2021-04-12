from queue import Queue


class Task:
    t_id = 0
    t_priority = 0

    def __init__(self, target, priority):
        Task.t_id += 1
        self.t_priority = priority  # priority of task
        self.tid = Task.t_id  # Task ID
        self.target = target  # Target coroutine
        self.sendval = None  # Value to send

    def run(self):
        return self.target.send(self.sendval)


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target, priority):
        newtask = Task(target, priority)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def exit(self, task):
        print("Task %d Ukonceny" % task.tid)
        del self.taskmap[task.tid]

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)



