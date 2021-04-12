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
        self.ready = []

    def new(self, target, priority):
        newtask = Task(target, priority)
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.append(task)

    def select_highest_priority_id(self):
        p = -1
        t_id = -1
        for t in self.ready:
            if t.t_priority > p:
                p = t.t_priority
                t_id = t.tid
        return t_id

    def select_with_id(self, t_id):
        for t in self.ready:
            if t.tid == t_id:
                return t

    def mainloop(self):
        while len(self.ready) > 0:
            selected_id = self.select_highest_priority_id()
            task = self.select_with_id(selected_id)
            self.ready.remove(task)
            try:
                task.run()
            except StopIteration:
                print(f'Odstranujem id = {task.tid}')
                continue
            self.schedule(task)


def coroutine1(printstring):
    print(printstring + ' cast 1')
    yield
    print(printstring + ' cast 2')
    yield
    print(printstring + ' cast 3')
    yield


def coroutine2(printstring):
    print(printstring + ' cast 1')
    yield
    print(printstring + ' cast 2')
    yield


def coroutine3(printstring):
    print(printstring + ' cast 1')
    yield
    print(printstring + ' cast 2')
    yield
    print(printstring + ' cast 3')
    yield
    print(printstring + ' cast 4')
    yield


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(coroutine1('t1'), 5)
    sched.new(coroutine2('t2'), 1)
    sched.new(coroutine3('t3'), 3)
    sched.mainloop()
