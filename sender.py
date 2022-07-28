#!/usr/bin/env python
from sqlite3 import connect
import pika
import json
import psutil
import time
import sys
import os

def main():

    # standard rabbitmq client for python pika is used to open a blocking connnection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # connection = pika.SelectConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    print("Specify the interval of sending information (in seconds)")
    duration = int(input())


    while(True):
        #psutil lib is used to get cpu status
        cpu_count = psutil.cpu_count()

        #cpu usage is calculated over a period of time
    
        cpu_usage = psutil.cpu_percent(duration)

        cpu_freq = psutil.cpu_freq()

        cpu_stats = psutil.cpu_stats()

        memory = psutil.virtual_memory()

        disk_partitions = psutil.disk_partitions()

        cpu_data = {
                    "cpu_count": cpu_count,
                    "cpu_usage": cpu_usage,
                    "cpu_freq": cpu_freq.current,
                    "cpu_stats": {
                        "ctx_switches": cpu_stats.ctx_switches,
                        "interrupts": cpu_stats.interrupts,
                        "soft_interrupts": cpu_stats.soft_interrupts,
                        "syscalls": cpu_stats.syscalls
                    },
                    "memory": {
                        "total": memory.total,
                        "available": memory.available,
                        "free": memory.free,
                        "used": memory.used
                    },
                    "disk_partitions": disk_partitions
        }

        message = json.dumps(cpu_data)

        channel.basic_publish(
                                exchange='',
                                routing_key='cpu_info',
                                body=message
                            )

        print("Data Sent to Queue")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by User')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
