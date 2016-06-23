# -*- coding: utf-8 -*-
import Queue
import thread
import threading
import time

import gevent
import gevent.queue
import gevent.socket
import gevent.ssl

from X.tools.log import log

# import psycogreen.gevent
# psycogreen.gevent.patch_psycopg()

sleep = gevent.sleep
socket = gevent.socket
ssl = gevent.ssl


class ThreadWorker(threading.Thread):
    def __init__(self, workQueue, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        self.queue = workQueue
        self.start()

    def run(self):
        while True:
            try:
                func, args, kwargs = self.queue.get()
                result = self.exec_func(func, *args, **kwargs)
            except Queue.Empty:
                continue

    def exec_func(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            log(
                title='WORKER_EXCEPTION',
                content=[func, args, kwargs],
                logger='sms',
                level='error'
            )
        return func(*args, **kwargs)


class ThreadWorkerManager:
    def __init__(self):
        pass

    size = 5
    workQueue = Queue.Queue()
    workers = [ThreadWorker(workQueue) for i in range(size)]

    @staticmethod
    def put(task):
        ThreadWorkerManager.workQueue.put(task)


class GeventWorker:
    def __init__(self, workQueue, **kwargs):
        self.queue = workQueue
        gevent.spawn(GeventWorker.run, self)

    def run(self):
        while True:
            try:
                func, args, kwargs = self.queue.get()
                result = self.exec_func(func, *args, **kwargs)
            except Queue.Empty:
                continue

    def exec_func(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            log(
                title='WORKER_EXCEPTION',
                content=[func, args, kwargs],
                logger='sms',
                level='error'
            )
        return func(*args, **kwargs)


class GeventWorkerManager:
    def __init__(self):
        pass

    size = 5
    workQueue = gevent.queue.Queue()
    workers = [GeventWorker(workQueue) for i in range(size)]

    @staticmethod
    def put(task):
        GeventWorkerManager.workQueue.put(task)


def gevent_task(function):
    def decorator(*args, **kwargs):
        gevent.spawn(function, *args, **kwargs)

    return decorator


def thread_task(function):
    def decorator(*args, **kwargs):
        thread.start_new_thread(function, args)

    return decorator


def thread_worker_task(function):
    def decorator(*args, **kwargs):
        ThreadWorkerManager.put([function, args, kwargs])

    return decorator


def gevent_worker_task(function):
    def decorator(*args, **kwargs):
        GeventWorkerManager.put([function, args, kwargs])

    return decorator


def delay_exec(function):
    def decorator(*args, **kwargs):
        sender = args[0]

        delay_name = '%s_delay' % function.func_name
        if not hasattr(sender, delay_name):
            setattr(sender, delay_name, 10)
        delay = getattr(sender, delay_name)

        sleep(delay)
        return function(*args, **kwargs)

    return decorator


def keep_interval(function):
    def decorator(*args, **kwargs):
        sender = args[0]

        interval_name = '%s_interval' % function.func_name
        last_time_name = '%s_last_time' % function.func_name
        sleep_mode_name = '%s_sleep_mode' % function.func_name

        if not hasattr(sender, interval_name):
            setattr(sender, interval_name, 10)
        interval = getattr(sender, interval_name)

        if not hasattr(sender, last_time_name):
            setattr(sender, last_time_name, time.time() - interval)
        last_time = getattr(sender, last_time_name)

        if hasattr(sender, sleep_mode_name):
            sleep_mode = getattr(sender, sleep_mode_name)
        else:
            sleep_mode = False

        now = time.time()
        if now < last_time + interval:
            if sleep_mode:
                sleep(last_time + interval - now)
            else:
                return None
        setattr(sender, last_time_name, last_time + interval)
        return function(*args, **kwargs)

    return decorator


def keep_interval_slow(function):  # slow
    def decorator(*args, **kwargs):
        sender = args[0]

        interval_name = '%s_interval' % function.func_name
        last_time_name = '%s_last_time' % function.func_name
        sleep_mode_name = '%s_sleep_mode' % function.func_name

        if not hasattr(sender, interval_name):
            setattr(sender, interval_name, 10)
        interval = getattr(sender, interval_name)

        if not hasattr(sender, last_time_name):
            setattr(sender, last_time_name, time.time() - interval)
        last_time = getattr(sender, last_time_name)

        if hasattr(sender, sleep_mode_name):
            sleep_mode = getattr(sender, sleep_mode_name)
        else:
            sleep_mode = False

        now = time.time()
        if now < last_time + interval:
            if sleep_mode:
                sleep(last_time + interval - now)
            else:
                return None
        # setattr(sender, last_time_name, last_time + interval)
        setattr(sender, last_time_name, time.time())

        return function(*args, **kwargs)

    return decorator
