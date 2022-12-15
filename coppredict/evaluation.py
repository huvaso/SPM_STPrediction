# -*- coding: utf-8 -*-

import os
import psutil
import time


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_time():
    time_v = time.time()
    return time_v


def get_time_build(time_start, time_end, message):
    if time_start != -1 and time_end != -1:
        return "Time execution: " + message + str(time_end - time_start) + ' seconds' + '\n'


def get_memory_build(mem_start, mem_end, message):
    if mem_start != -1 and mem_end != -1:
        return "Memory Used: " + message + str((mem_end - mem_start)/1024) + ' Bytes' + '\n'
