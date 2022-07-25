from datetime import datetime
from typing import List
import justpy as jp

class Table(jp.Div):
    '''
    a reactive justpy table
    '''

    t_classes = "table-auto"
    tr_even_classes = ''
    tr_odd_classes = ''
    th_classes = ''
    thead_classes=''

    def __init__(self, lod:List[dict],actionColumns:list=[],headerMap=None,primaryKey:str=None,allowInput:bool=True,debugContainer=None,**kwargs):
        '''
        constructor
        
        Args:
            lod(List[dict]): the table content
            actionColumns: a list of action columns
            headerMap(dict): a mapping for headers (if any)
            allowInput(bool): allow editing/input
            primaryKey(str): the column holding the primary key
        '''
        self.lod = lod
        self.primaryKey=primaryKey
        self.rowsByKey={}
        self.allowInput=allowInput
        super().__init__(**kwargs)
        self.table = jp.Table(a=self)
        self.table.set_class(self.t_classes)
        self.actionColumns = actionColumns
        #First row of values is header
        if self.lod and len(self.lod)>0:
            if headerMap is None:
                headerMap={}
                headerColumns = self.lod[0].keys()
                for headerColumn in headerColumns:
                    headerMap[headerColumn]=headerColumn
            thead = jp.Thead(a=self.table, classes=self.thead_classes)
            tr = jp.Tr(a=thead)
            for ac in self.actionColumns:
                jp.Th(text=ac.name,classes=self.th_classes,a=tr)
            for _column,header in headerMap.items():
                jp.Th(text=header, classes=self.th_classes, a=tr)    
            tbody = jp.Tbody(a=self.table)
            for _i, row in enumerate(self.lod):
                tableRow=TableRow(table=self,a=tbody, record=row, headerMap=headerMap, actionColumns=self.actionColumns)
                if self.primaryKey is not None:
                    key=row[primaryKey]
                    self.rowsByKey[key]=tableRow
        self.debugContainer=debugContainer
        
    def updateCell(self,key,column,value):
        '''
        update the given Cell
        '''
        if self.primaryKey is None:
            raise Exception("updateCell only possible when primaryKey is set")
        tableRow=self.rowsByKey[key]
        tableRow.updateCell(column,value)
        
    def getCellValue(self,key,column:str)->object:
        if self.primaryKey is None:
            raise Exception("getCellValue only possible when primaryKey is set")
        tableRow=self.rowsByKey[key]
        value=tableRow.getCellValue(column)
        return value
        

class TableRow(jp.Tr):
    '''
    a table row
    '''
    td_classes = ''

    def __init__(self, table,record:dict, headerMap:dict, actionColumns:list=None, **kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        self.table=table
        self.record = record
        self.headerMap=headerMap
        self.cellsMap = {}
        for actionCol in actionColumns:
            if isinstance(actionCol, ButtonColumn):
                actionCol.getTableData(a=self, row=self)
        for column in headerMap.keys():
            cell = TableData(a=self, inputValue=self.record.get(column), label=column, classes=self.td_classes, row=self,allowInput=self.table.allowInput)
            self.cellsMap[column]=cell
            
    def updateCell(self,column:str,value):
        '''
        update the given cell
        '''
        if column in self.cellsMap:
            cell=self.cellsMap[column]
            cell.setValue(value)
        
    def getCellValue(self,column:str)->object:
        value=None
        if column in self.cellsMap:
            cell=self.cellsMap[column]
            value=cell.getValue()
        return value

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

    def disableInput(self,disabled):
        """
        Disables or Enables input fields of the row
        """
        for cell in self.cellsMap.values():
            if cell.isInput:
                cell.input.disabled=disabled

class TableData(jp.Td):
    '''
    a table Cell
    '''
    def __init__(self, row:TableRow, inputValue, label:str, allowInput:bool=True,**kwargs):
        '''
        constructor
        '''
        super(TableData, self).__init__(**kwargs)
        self.row = row
        self.label = label
        self.isInput=allowInput
        self.inputValue=inputValue
        if allowInput:
            self.input = self.getInput()
        else:
            self.inner_html=inputValue
            
    def setValue(self,value):
        '''
        set my value
        
        Args:
            value(object): the value to set
        '''
        self.inputValue=value
        if self.isInput:
            self.input.value=value
        else:
            self.inner_html=value
            
    def getValue(self):
        return self.inputValue
        
    def getInput(self):
        if isinstance(self.inputValue, datetime):
            jpinput = jp.InputChangeOnly(a=self, type='date', value=self.inputValue.date().isoformat(), classes="form-input px-4 py-3 rounded-full")
        else:
            jpinput = jp.InputChangeOnly(a=self, value=self.inputValue, classes="form-input px-4 py-3 rounded-full")
        jpinput.on("change", self.on_input_change)
        jpinput.row = self.row
        jpinput.label = self.label
        return jpinput

    @staticmethod
    def on_input_change(self, msg):
        newValue = msg.value
        oldValue = self.row.updateRowRecord(self.a.label, newValue)
        #update record
        msg = f"{datetime.now().isoformat()} Changed {self.label} from '{oldValue}' to '{newValue}'"
        debugContainer=self.row.table.debugContainer
        if debugContainer is not None:
            debugContainer.addMessage(msg)

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
    button_classes = 'btn btn-primary'

    def __init__(self, label:str, **kwargs):
        super().__init__(**kwargs)
        self.btn = jp.Button(a=self, text=label, classes=self.button_classes)
        self.body = jp.Div(a=self)
        self.body.visibility_state = "invisible"
        self.btn.body=self.body
        self.body.a = self
        self.body.classes=''
        self.on("click", self.toggle_visible)

    @staticmethod
    def toggle_visible(self, _msg):
        if self.body.visibility_state == 'visible':
            self.body.set_class('invisible')
            self.body.visibility_state = 'invisible'
        else:
            self.body.set_class('visible')
            self.body.visibility_state = 'visible'


class ButtonColumn:
    '''
    a button column
    '''

    def __init__(self, name:str):
        self.name = name
        self.tdClass: type = TableDataButton

    def getTableData(self, a, row:TableRow) -> TableData:
        tabledata = self.tdClass(a=a, text=self.name, row=row, btnCol=self)
        return tabledata


    async def buttonFunctionOnClick(self, row:TableRow, debugContainer:DebugOutput, msg):
        return NotImplemented


class TableDataButton(jp.Td):

    btn_classes = "btn btn-primary"

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
