'''
Created on 2022-08-07

https://justpy.io/tutorial/ajax/

@author: wf
'''
import justpy as jp
import asyncio

wp = jp.WebPage(delete_flag=False)
wp.reload_interval = 2.5
count_div = jp.Div(a=wp, classes='text-center m-4 p-4 text-white bg-blue-500', style='font-size: 200px')

async def increment_counter(start):
    count_div.counter = start
    while True:
        count_div.counter += 1
        count_div.text = str(count_div.counter)
        await asyncio.sleep(1)

def start_counting():
    jp.run_task(increment_counter(500))

def reload_demo():
    return wp

from  jpdemo.examples.basedemo import Demo
Demo('ajax demo',reload_demo, startup=start_counting, websockets=False)