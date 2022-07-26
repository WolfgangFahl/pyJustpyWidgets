'''
@author Tim Holzheim
2022-06
'''
import asyncio
from datetime import datetime
import justpy as jp
from jpwidgets.jpTable import Table,TableRow,TableData
import sys
from jpwidgets.bt5widgets import App, Link,  DebugOutput

class Version(object):
    '''
    Version handling for bootstrap5 example
    '''
    name="jpTable demo example"
    version='0.0.2'
    date = '2022-05-09'
    updated = '2022-07-25'
    description='jpTable bootstrap5 example'
    authors='Tim Holzheim, Wolfgang Fahl'
    license=f'''Copyright 2022 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.'''
    longDescription=f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""
  
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
  
class EchoClick():
    
    @classmethod
    def getContext(cls,msg):
        target=msg["target"]
        cell=target.a # convention - the target is a control of the cell
        row=cell.row
        table=row.table
        return cell,row,table,table.debugContainer 
        

    @classmethod
    async def onClick(cls,msg):
        _cell,row,table,debugContainer=cls.getContext(msg)
        print(msg)
        print(row.record)
        if debugContainer is not None:
            table.debugContainer.addMessage(str(row.record))
            await msg.page.update()

class EchoTwiceClick():

    @classmethod
    async def onClick(cls,msg):
        _cell,_row,_table,debugContainer=EchoClick.getContext(msg)
        await EchoClick.onClick(msg)
        if debugContainer is not None:
            debugContainer.addMessage("Echoing in 5 seconds again")
            await msg.page.update()
        await asyncio.sleep(5)
        await EchoClick.onClick(msg)

class JpTableDemo(App):
    '''
    demonstration for jpTable widget
    '''
    
    def __init__(self,version):
        '''
        Constructor
        
        Args:
            version(Version): the version info for the app
        '''
        App.__init__(self, version)
        self.addMenuLink(text='Home',icon='home', href="/")
        self.addMenuLink(text='github',icon='github', href="https://github.com/WolfgangFahl/pyJustpyWidgets")
        self.addMenuLink(text='Documentation',icon='file-document',href="https://wiki.bitplan.com/index.php/PyJustpyWidgets")
        self.addMenuLink(text='Source',icon='file-code',href="https://github.com/WolfgangFahl/pyJustpyWidgets/blob/main/jpdemo/examples/jpTableDemo.py")
       
    async def onWdLinks(self,msg):
        '''
        replace cell content with links
        '''
        try:
            target=msg["target"]
            target.disabled=True
            for rowKey in self.table2.rowsByKey.keys():
                wikidataLink=self.table2.getCellValue(rowKey,"president")
                itemId=wikidataLink.replace("http://www.wikidata.org/entity/","")
                link=Link.create(url=wikidataLink,text=itemId)
                self.table2.updateCell(rowKey, "president",link)
        except Exception as ex:
            self.handleException(ex)
            
    def addButtonColumn(self,table,column,onClick):
        '''
        add a button column
        '''
        for row in table.rows:
            cell=row.cellsMap[column]
            cell.delete_components()
            button=jp.Button(text=column,classes="btn btn-primary", a=cell,click=onClick)
            cell.setControl(button)
            
    async def content(self):
        '''
        show the content
        '''
        head_html="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">"""
        wp=self.getWp(head_html)
        lod=[
  {
    "dateOfBirth": datetime.fromisoformat("1988-04-14 00:00:00"),
    "familyName": "Modeste",
    "givenName": "Anthony",
    "league": "Bundesliga",
    "nationalOf": "France",
    "position": "forward",
    "speaks": "French",
    "team": "1. FC K\u00f6ln"
  },
  {
    "dateOfBirth": datetime.fromisoformat("1990-10-14 00:00:00"),
    "familyName": "Ujah",
    "givenName": "Anthony",
    "league": "Bundesliga",
    "nationalOf": "Nigeria",
    "position": "forward",
    "speaks": "Nigerian Pidgin",
    "team": "1. FC Union Berlin"
  },
  {
    "dateOfBirth": datetime.fromisoformat("1991-10-13 00:00:00"),
    "familyName": "Riley",
    "givenName": "Joe",
    "league": "EFL League One",
    "nationalOf": "United Kingdom",
    "position": "defender",
    "speaks": "English",
    "team": "Bury F.C."
  },
  {
    "dateOfBirth": datetime.fromisoformat("1995-02-08 00:00:00"),
    "familyName": "Kimmich",
    "givenName": "Joshua",
    "league": "Bundesliga",
    "nationalOf": "Germany",
    "position": "midfielder",
    "speaks": "German",
    "team": "FC Bayern Munich"
  },
  {
    "dateOfBirth": datetime.fromisoformat("2000-07-21 00:00:00"),
    "familyName": "Haaland",
    "givenName": "Erling",
    "league": "Premier League",
    "nationalOf": "Norway",
    "position": "forward",
    "speaks": "Norwegian",
    "team": "Manchester City F.C."
  },
  {
    "dateOfBirth": datetime.fromisoformat("1996-12-06 00:00:00"),
    "familyName": "Riley",
    "givenName": "Joe",
    "league": "Premier League",
    "nationalOf": "United Kingdom",
    "position": "fullback",
    "speaks": "English",
    "team": "Manchester United F.C."
  },
  {
    "dateOfBirth": datetime.fromisoformat("1987-06-24 00:00:00"),
    "familyName": "Messi",
    "givenName": "Lionel",
    "league": "Ligue 1",
    "nationalOf": "Argentina",
    "position": "forward",
    "speaks": "Spanish",
    "team": "Paris Saint-Germain F.C."
  },
  {
    "dateOfBirth": datetime.fromisoformat("1998-12-20 00:00:00"),
    "familyName": "Mbapp\u00e9",
    "givenName": "Kylian",
    "league": "Ligue 1",
    "nationalOf": "France",
    "position": "forward",
    "speaks": "French",
    "team": "Paris Saint-Germain F.C."
  },
  {
    "dateOfBirth": datetime.fromisoformat("1990-10-14 00:00:00"),
    "familyName": "Ujah",
    "givenName": "Anthony",
    "league": "2. Bundesliga",
    "nationalOf": "Nigeria",
    "position": "forward",
    "speaks": "English",
    "team": "SV Werder Bremen"
  }
]
        rowA=jp.Div(classes="row",a=self.contentbox)
        rowB=jp.Div(classes="row",a=self.contentbox)  
        rowC=jp.Div(classes="row",a=self.contentbox)  
        rowD=jp.Div(classes="row",a=self.contentbox)     
        colD1=jp.Div(classes="col-1",a=rowD)
        debugContainer = DebugOutput(a=rowB)
        for record in lod:
            record["echo"]=""
            record["echo2"]=""
        self.table1 = Table(lod=lod,
                      allowInput=True,
                      a=rowA,
                      debugContainer=debugContainer)
        self.addButtonColumn(self.table1,"echo",EchoClick.onClick)
        self.addButtonColumn(self.table1,"echo2",EchoTwiceClick.onClick)
        plod=[
  {
    "nickNames": "American Fabius",
    "president": "http://www.wikidata.org/entity/Q23",
    "presidentLabel": "George Washington"
  },
  {
    "nickNames": "Barry",
    "president": "http://www.wikidata.org/entity/Q76",
    "presidentLabel": "Barack Obama"
  },
  {
    "nickNames": "The Comeback Kid,Slick Willie",
    "president": "http://www.wikidata.org/entity/Q1124",
    "presidentLabel": "Bill Clinton"
  },
  {
    "nickNames": "Joe",
    "president": "http://www.wikidata.org/entity/Q6279",
    "presidentLabel": "Joe Biden"
  },
  {
    "nickNames": "Jack",
    "president": "http://www.wikidata.org/entity/Q9696",
    "presidentLabel": "John F. Kennedy"
  },
  {
    "nickNames": "Ike",
    "president": "http://www.wikidata.org/entity/Q9916",
    "presidentLabel": "Dwight D. Eisenhower"
  },
  {
    "nickNames": "Dick Nixon",
    "president": "http://www.wikidata.org/entity/Q9588",
    "presidentLabel": "Richard Nixon"
  },
  {
    "nickNames": "Old Kinderhook",
    "president": "http://www.wikidata.org/entity/Q11820",
    "presidentLabel": "Martin Van Buren"
  },
  {
    "nickNames": "Old Tippecanoe",
    "president": "http://www.wikidata.org/entity/Q11869",
    "presidentLabel": "William Henry Harrison"
  },
  {
    "nickNames": "Old Hickory",
    "president": "http://www.wikidata.org/entity/Q11817",
    "presidentLabel": "Andrew Jackson"
  },
  {
    "nickNames": "Old Rough and ready",
    "president": "http://www.wikidata.org/entity/Q11896",
    "presidentLabel": "Zachary Taylor"
  },
  {
    "nickNames": "The Donald",
    "president": "http://www.wikidata.org/entity/Q22686",
    "presidentLabel": "Donald Trump"
  },
  {
    "nickNames": "Teddy",
    "president": "http://www.wikidata.org/entity/Q33866",
    "presidentLabel": "Theodore Roosevelt"
  },
  {
    "nickNames": "\u201cUnconditional Surrender\u201d Grant",
    "president": "http://www.wikidata.org/entity/Q34836",
    "presidentLabel": "Ulysses S Grant"
  }
]
        self.table2 = Table(lod=plod,
                      allowInput=False,
                      primaryKey='president',
                      a=rowC)
        _wdLinks=jp.Button(text="Wikidata Links",classes="btn btn-primary",a=colD1,click=self.onWdLinks)
        return wp

DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    app=JpTableDemo(Version)
    sys.exit(app.mainInstance())