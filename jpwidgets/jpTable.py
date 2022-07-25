import asyncio
from datetime import datetime
from typing import List

import justpy as jp


class Table(jp.Div):
    '''
    a table
    '''

    t_classes = "table-auto"
    tr_even_classes = 'bg-gray-100 '
    tr_odd_classes = ''
    th_classes = 'w-1/2 border border-slate-300 dark:border-slate-600 font-semibold p-4 text-slate-900 dark:text-slate-200 text-left'
    thead_classes='bg-slate-50 dark:bg-slate-700'


    def __init__(self, lod:List[dict],actionColumns:list,**kwargs):
        '''
        constructor
        '''
        self.lod = lod
        super().__init__(**kwargs)
        self.table = jp.Table(a=self)
        self.table.set_class(self.t_classes)
        self.actionColumns = actionColumns
        #First row of values is header
        if self.lod:
            headers = self.lod[0].keys()
            headers = [*[ac.name for ac in self.actionColumns], *headers]
            thead = jp.Thead(a=self.table, classes=self.thead_classes)
            tr = jp.Tr(a=thead)
            for item in headers:
                jp.Th(text=item, classes=self.th_classes, a=tr)
            tbody = jp.Tbody(a=self.table)
            for i, row in enumerate(self.lod):
                TableRow(a=tbody, record=row, headers=headers, actionColumns=self.actionColumns)
        self.debugContainer = DebugOutput(a=self)


class TableRow(jp.Tr):
    '''
    a table row
    '''
    td_classes = 'px-4 py-2 text-center'

    def __init__(self, record:dict, headers:list, actionColumns:list=None, **kwargs):
        super().__init__(**kwargs)
        self.record = record
        self.headers=headers
        self.inputCells = []
        for actionCol in actionColumns:
            if isinstance(actionCol, ButtonColumn):
                actionCol.getTableData(a=self, row=self)
        for key in headers[len(actionColumns):]:
            cell = TableData(a=self, inputValue=self.record.get(key), label=key, classes=self.td_classes, row=self)
            self.inputCells.append(cell)

    def updateRowRecord(self, key:str, value):
        """
        Updates the row record with the given value and returns the old value.

        Args:
            key(str): record entry that should be updated
            value: value that should replace the existing value

        Returns:
            old value that was replaced by the given vaue
        """
        oldValue = self.record.get(key)
        self.record[key] = value
        return oldValue

    def disableInput(self):
        """
        Disables input fields of the row
        """
        for cell in self.inputCells:
            cell.input.disabled=True

    def enableInput(self):
        """
        enables input fields of the row
        """
        for cell in self.inputCells:
            cell.input.disabled=False


class TableData(jp.Td):
    '''
    '''
    def __init__(self, row:TableRow, inputValue, label:str, **kwargs):
        super(TableData, self).__init__(**kwargs)
        self.row = row
        self.inputValue = inputValue
        self.label = label
        if isinstance(self.inputValue, datetime):
            input = jp.InputChangeOnly(a=self, type='date', value=self.inputValue.date().isoformat(), classes="form-input px-4 py-3 rounded-full")
        else:
            input = jp.InputChangeOnly(a=self, value=self.inputValue, classes="form-input px-4 py-3 rounded-full")
        input.on("change", self.on_input_change)
        input.row = self.row
        input.label = self.label
        self.input = input

    @staticmethod
    def on_input_change(self, msg):
        newValue = msg.value
        oldValue = self.row.updateRowRecord(self.a.label, newValue)
        #update record
        msg = f"{datetime.now().isoformat()} Changed {self.label} from '{oldValue}' to '{newValue}'"
        self.a.a.a.a.a.debugContainer.addMessage(msg)


class DebugOutput(jp.Div):
    """
    shows debug messages
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.collapsible = Collapsible("Log", a=self)

    def react(self, data):
        if self.collapsible:
            self.collapsible.body.delete()
        ul = jp.Ul(a=self.collapsible.body, classes="list-none")
        for msg in reversed(self.messages):
            jp.Li(a=ul, text=msg)

    def addMessage(self, msg:str):
        self.messages.append(msg)


class Collapsible(jp.Div):
    """
    Collapsible div
    """
    button_classes = 'm-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'

    def __init__(self, label:str, **kwargs):
        super().__init__(**kwargs)
        self.btn = jp.Button(a=self, text=label, classes=self.button_classes)
        self.body = jp.Div(a=self)
        self.body.visibility_state = "invisible"
        self.btn.body=self.body
        self.body.a = self
        self.body.classes='flex flex-row'
        self.on("click", self.toggle_visible)

    @staticmethod
    def toggle_visible(self, msg):
        if self.body.visibility_state == 'visible':
            self.body.set_class('invisible')
            self.body.visibility_state = 'invisible'
        else:
            self.body.set_class('visible')
            self.body.visibility_state = 'visible'


class ButtonColumn:

    def __init__(self, name:str):
        self.name = name
        self.tdClass: type = TableDataButton

    def getTableData(self, a, row:TableRow) -> TableData:
        tabledata = self.tdClass(a=a, text=self.name, row=row, btnCol=self)
        return tabledata


    async def buttonFunctionOnClick(self, row:TableRow, debugContainer:DebugOutput, msg):
        return NotImplemented


class EchoButtonColumn(ButtonColumn):

    async def buttonFunctionOnClick(self, row:TableRow, debugContainer:DebugOutput, msg):
        print(msg)
        print(row.record)
        debugContainer.addMessage(str(row.record))


class EchoTwiceButtonColumn(ButtonColumn):

    async def buttonFunctionOnClick(self, row:TableRow, debugContainer:DebugOutput, msg):
        print(msg)
        print(row.record)
        debugContainer.addMessage(str(row.record))
        debugContainer.addMessage("Echoing in 5 seconds again")
        await msg.page.update()
        await asyncio.sleep(5)
        debugContainer.addMessage(str(row.record))
        await msg.page.update()


class EchoTwiceInputDisabledButtonColumn(ButtonColumn):

    async def buttonFunctionOnClick(self, row:TableRow, debugContainer:DebugOutput, msg):
        print(msg)
        print(row.record)
        debugContainer.addMessage(str(row.record))
        debugContainer.addMessage("Echoing in 5 seconds again")
        row.disableInput()
        await msg.page.update()
        await asyncio.sleep(5)
        debugContainer.addMessage(str(row.record))
        row.enableInput()
        await msg.page.update()



class TableDataButton(jp.Td):

    btn_classes = "px-4 py-2 font-semibold text-sm bg-cyan-500 text-white rounded-full shadow-sm"

    def __init__(self, text:str, row:TableRow, btnCol:ButtonColumn, **kwargs):
        super().__init__(**kwargs)
        self.btn = jp.Button(a=self, text=text, click=self.on_button_click, classes=self.btn_classes)
        self.btn.row = row
        self.btn.actionCol = btnCol

    @staticmethod
    async def on_button_click(self, msg):
        print(msg)
        debugContainer = self.row.a.a.a.debugContainer
        if getattr(self, "actionCol"):
            await self.actionCol.buttonFunctionOnClick(self.row, debugContainer, msg)








