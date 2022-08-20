'''
Created on 2022-07-26
see https://github.com/partrita/justPy/blob/master/Number_input.py

@author: wf
'''
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-128 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2 w-128'

async def my_input(self, msg):
    self.div.text = self.value

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(type='number', size=30, a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input)
    return wp

from  jpdemo.examples.basedemo import Demo
Demo('number input',input_demo)
