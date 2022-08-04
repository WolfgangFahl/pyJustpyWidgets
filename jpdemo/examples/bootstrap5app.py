'''
Created on 2022-07-25

@author: wf
'''
import sys
import justpy as jp
from jpwidgets.bt5widgets import App, ProgressBar, Spinner, Alert


class Version(object):
    '''
    Version handling for bootstrap5 example
    '''
    name="justpy bootstrap5 example"
    version='0.0.1'
    date = '2022-07-25'
    updated = '2022-07-25'
    description='justpy bootstrap5 example'
    authors='Wolfgang Fahl'
    license=f'''Copyright 2022 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.'''
    longDescription=f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""
class Bootstrap5ExampleApp(App):
    '''
    example Application for Bootstrap5
    '''

    def __init__(self,version):
        '''
        Constructor
        
        Args:
            version(Version): the version info for the app
        '''
        App.__init__(self, version,title="Bootstrap5 example")
        self.addMenuLink(text='Home',icon='home', href="/")
        self.addMenuLink(text='github',icon='github', href="https://github.com/WolfgangFahl/pyJustpyWidgets")
        self.addMenuLink(text='Documentation',icon='file-document',href="https://wiki.bitplan.com/index.php/PyJustpyWidgets")
        self.addMenuLink(text='Source',icon='file-code',href="https://github.com/WolfgangFahl/pyJustpyWidgets/blob/main/jpdemo/examples/bootstrap5app.py")
        self.rows=3
        self.cols=3
        
    def onRowSelected(self,msg):
        self.rows=int(msg.value)
        self.showRowsAndCols()
        
    def onColSelected(self,msg):
        self.cols=int(msg.value)
        self.showRowsAndCols()
        
    def showRowsAndCols(self):
        try:
            self.feedback.text=f"{self.rows} rows x {self.cols} cols"
            self.grid.delete_components()
            for row in range(1,self.rows+1):
                rowDiv=jp.Div(classes="row",a=self.grid)
                for col in range(1,self.cols+1):
                    clazz=f"col-{12/self.cols:.0f}"
                    print (clazz)
                    colDiv=jp.Div(classes=f"{clazz} h1",a=rowDiv)
                    colDiv.text=f"{row}-{col}"
        except Exception as ex:
            self.handleException(ex)
        
    async def content(self):
        '''
        show the content
        '''
        head="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">
<link rel="stylesheet" href="/static/css/pygments.css">
"""
        wp=self.getWp(head)
        rowA=jp.Div(classes="row",a=self.contentbox)
        colA1=jp.Div(classes="col-1",a=rowA)
        colA2=jp.Div(classes="col-1",a=rowA)
        colA3=jp.Div(classes="col-1",a=rowA)
        colA4=jp.Div(classes="col-9",a=rowA)
        self.grid=jp.Div(a=self.contentbox)
        self.feedback=jp.Div(a=colA3)
        self.errors=jp.Span(a=colA4,style='color:red')
        rowSelector=self.createSelect("rows",self.rows, self.onRowSelected, a=colA1)
        for row in range(9):
            rowSelector.add(jp.Option(value=row+1,text=str(row+1)))
        colSelector=self.createSelect("cols",self.cols, self.onColSelected, a=colA2)
        for col in [1,2,3,4,6,12]:
            colSelector.add(jp.Option(value=col,text=str(col)))
        self.showRowsAndCols()

        self.widgets = ShowBootstrap5Widgets(a=self.contentbox)
        return wp

class ShowBootstrap5Widgets(jp.Div):
    """
    Bootstrap 5 Widget Demos
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super(ShowBootstrap5Widgets, self).__init__(**kwargs)
        self.sectionHeader = jp.H2(a=self,  text="Bootstrap 5 Widgets")
        self.subSectionHeader = jp.H3(a=self, text="Progress Indication Widgets")
        self.button = jp.Button(a=self, text="Press to progress", classes="btn btn-primary")
        self.button.on("click", self.progress_demo)
        self.progress_count = 0
        self.progressGrid = jp.Div(a=self, classes="d-grid gap-4")
        self.progressDivs = [jp.Div(a=self.progressGrid, classes="p-2 d-flex justify-content-center"),
                             jp.Div(a=self.progressGrid, classes="p-2"),
                             jp.Div(a=self.progressGrid, classes="p-2"),
                             jp.Div(a=self.progressGrid, classes="p-2"),]
        self.spinner = Spinner(a=self.progressDivs[0])
        self.progressBar = ProgressBar(a=self.progressDivs[1])
        self.progressBarAnimated = ProgressBar(a=self.progressDivs[2], animated=True)
        self.progressBarWithKillSwitch = ProgressBar(a=self.progressDivs[3], withKillSwitch=True)
        self.progressBarWithKillSwitch.onStop(callback=self.stop_progress)

    def stop_progress(self, msg):
        """
        stop the progress
        """
        self.progressBarWithKillSwitch.updateProgress(0)
        Alert(a=self, text="Process was stopped!!!")

    def progress_demo(self, msg):
        """
        update progress bars of the demo
        """
        value = 18
        for progressBar in [self.progressBar, self.progressBarAnimated, self.progressBarWithKillSwitch]:
            if progressBar.value < 100:
                progressBar.incrementProgress(value)
            if progressBar.value >= 100:
                Alert(a=self, text="Demo process completed!!!  → resetting demo...")
                progressBar.updateProgress(0)

    
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    app=Bootstrap5ExampleApp(Version)
    sys.exit(app.mainInstance())