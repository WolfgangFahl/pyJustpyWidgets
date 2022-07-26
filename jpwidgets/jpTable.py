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

    def __init__(self, lod:List[dict],headerMap=None,primaryKey:str=None,allowInput:bool=True,debugContainer=None,**kwargs):
        '''
        constructor
        
        Args:
            lod(List[dict]): the table content
            headerMap(dict): a mapping for headers (if any)
            allowInput(bool): allow editing/input
            primaryKey(str): the column holding the primary key
        '''
        self.lod = lod
        self.primaryKey=primaryKey
        self.rowsByKey={}
        self.rows=[]
        self.allowInput=allowInput
        super().__init__(**kwargs)
        self.table = jp.Table(a=self)
        self.table.set_class(self.t_classes)
        #First row of values is header
        if self.lod and len(self.lod)>0:
            if headerMap is None:
                headerMap={}
                headerColumns = self.lod[0].keys()
                for headerColumn in headerColumns:
                    headerMap[headerColumn]=headerColumn
            thead = jp.Thead(a=self.table, classes=self.thead_classes)
            tr = jp.Tr(a=thead)
            for _column,header in headerMap.items():
                jp.Th(text=header, classes=self.th_classes, a=tr)    
            tbody = jp.Tbody(a=self.table)
            for _i, row in enumerate(self.lod):
                tableRow=TableRow(table=self,a=tbody, record=row, headerMap=headerMap)
                self.rows.append(tableRow)
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

    def __init__(self, table,record:dict, headerMap:dict,  **kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        self.table=table
        self.record = record
        self.headerMap=headerMap
        self.cellsMap = {}
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
            self.control = self.getInput()
            self.isControl=True
        else:
            self.inner_html=inputValue
            self.isControl=False
            
    def setControl(self,control):
        '''
        set a control
        '''
        self.control=control
        self.isControl=True
        
    def getControl(self):
        return self.control
            
    def setValue(self,value):
        '''
        set my value
        
        Args:
            value(object): the value to set
        '''
        self.inputValue=value
        if self.isInput:
            self.input.value=value
        elif self.isControl:
            # TODO -define value for controls
            pass
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



