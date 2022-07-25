'''
Created on 2022-07-24

@author: wf

Bootstrap5Widgets to be used with 
https://getbootstrap.com/docs/5.0/getting-started/introduction/
 
'''
import justpy as jp
import os
import socket
import sys
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

class App(object):
    '''
    a Justpy App
    '''

    def __init__(self,version,title:str=None):
        '''
        Constructor
        
        Args:
            version(Version): Version info
            title(str): optional title - if None use Version.description
        '''
        self.version=version
        if title is None:
            title=version.description
        self.title=title
        self.menu=""
        
    def mainInstance(self,argv=None,callback=None): # IGNORE:C0111
        '''main program.'''
        if argv is None:
            argv=sys.argv[1:]
        if callback is None:
            if hasattr(self, "content"):
                if callable(self.content):
                    callback=self.content
        if callback is None:
            raise Exception("no callback defined and callable content function not declared")
        self.cmdLine(argv,callback)
        
    def getParser(self):
        '''
        get the argument parser
        '''
        description=f"{self.version.longDescription}\n{self.version.license}"
        parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--debug", dest="debug",   action="store_true", help="set debug [default: %(default)s]")
        parser.add_argument('--host',default=socket.getfqdn())
        parser.add_argument('--port',type=int,default=8000)
        parser.add_argument('-V', '--version', action='version', version=self.version.longDescription)
        return parser
    
    def getMenu(self):
        return self.menu
    
    def pageHtml(self,level):
        '''
        get the page level html
        '''
        if level=="head":
            html=f"""
        <title>{self.title}</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=yes">
        <!--  Material Design https://material.io/develop/web/getting-started  -->
        <link href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css" rel="stylesheet">
        <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
        <!-- bootstrap 5.2 https://getbootstrap.com/docs/5.2/getting-started/introduction/ -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
        <!--  Material design icons see https://materialdesignicons.com/getting-started -->
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.9.96/css/materialdesignicons.min.css" media="all" rel="stylesheet" type="text/css">
"""
        elif level=="body":
            html="""<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>"""
        elif level == "container":
            html=f"""<div name='containerbox'>
        <!--  common menu -->
<div name='headerbox' id='headerbox'>
{self.menu}
</div>
        <div name="navigationbox" id="navigationbox" title="{self.title}">{self.title}</div>
        <div name="contentbox" class="container-fluid" id="contentbox">
        <div name="footerbox"></div>
        </div><!--  end of main content box -->
</div><!--  end of container box -->
"""
        return html
    
    def getWp(self,headExtra=""):
        '''
        '''
        wp = jp.WebPage()
        head=self.pageHtml(level="head")
        # any extra head 
        head+=headExtra
        wp.head_html=head
        wp.body_html=self.pageHtml(level="body")
        self.containerbox=jp.parse_html(self.pageHtml(level="container"),a=wp)
        self.headerbox=self.containerbox.name_dict["headerbox"]
        self.contentbox=self.containerbox.name_dict["contentbox"]
        wp.debug = self.debug
        return wp
    
    def start(self,callback):
        '''
        start the reactive justpy webserver
        '''
        jp.justpy(callback,host=self.host,port=self.port)
        
    def handleException(self,ex):
        '''
        handle the given exception
        
        Args:
            ex(Exception): the exception to handle
        '''
        errorMsg=str(ex)
        trace=""
        if self.debug:
            trace=traceback.format_exc()
        if self.debug:
            print(errorMsg)
            print(trace)
        errorMsgHtml=f"{errorMsg}<pre>{trace}</pre>"
        self.errors.inner_html=errorMsgHtml
        
    def createSelect(self,text,value,change,a):
        '''
        create a select control with a label with the given text, the default value
        and a change onChange function having the parent a
        
        Args:
            text(str): the text for the label
            value(str): the selected value
            change(func): an onChange function
            a(object): the parent component of the Select control
        '''
        selectorLabel=jp.Label(text=text,a=a,classes="form-label label")
        select=jp.Select(a=a,classes="form-select",value=value,change=change)
        selectorLabel.for_component=select
        return select
    
    def createInput(self,text,placeholder,change,a,size:int=30):
        '''
        create an input control with a label with the given text
        a placeholder text and a change onChange function having the parent a
        
        Args:
            text(str): the text for the label
            placeholder(str): a placeholder value
            change(func): an onChange function
            a(object): the parent component of the Select control
            size(int). the size of the input
        '''
        inputLabel=jp.Label(text=text,a=a,classes="form-label label")
        jpinput=jp.Input(a=a,classes="form-input",size=size,placeholder=placeholder)
        jpinput.on('input', change)
        inputLabel.for_component=inputLabel
        return jpinput
        
    def cmdLine(self,argv,callback):
        '''
        cmdLine (main)
        
        Args:
             argv(list): command line arguments
            callback(func): the function to run justpy with
        '''
        try:
            # Setup argument parser
            parser = self.getParser()
            args = parser.parse_args(argv)
            self.args=args
            self.host=args.host
            self.port=args.port
            self.debug=args.debug
            self.start(callback)
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            return 1
        except Exception as e:
            if self.debug:
                raise(e)
            program_name = os.path.basename(__file__)
            indent = len(program_name) * " "
            sys.stderr.write(program_name + ": " + repr(e) + "\n")
            print(traceback.format_exc())
            sys.stderr.write(indent + "  for help use --help")
            return 2
        
    def addMenuLink(self,text,icon,href):
        '''
         add a menu entry
         
         text(str)
         icon(str): see https://materialdesignicons.com/ for possible icons
         href(str): the link
        '''
        self.menu+=f"""
  <!-- {text} --><a
    href='{href}'
    title='{text}'>
    <i class='mdi mdi-{icon} headerboxicon'></i>
  </a>
"""        
             
class ComboBox(jp.Input):
    '''
    combo box with attached datalist
    '''
    
    def __init__(self,**kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        self.clearOptions()
        
    def clearOptions(self):
        self.datalist=[]
        
    def addOption(self,option):
        self.datalist.append(option)


class ProgressBar(jp.Div):
    """
    Displays a progressbar
    see https://getbootstrap.com/docs/5.0/components/progress/
    """

    def __init__(self, animated:bool=False, **kwargs):
        '''
        constructor
        '''
        super().__init__(classes="progress", **kwargs)
        self.animated = animated
        self.value = 0
        self.bar = self.getBar()

    def getBar(self):
        """
        generate the actual bar based on the progress
        """
        classes = "progress-bar"
        if self.animated:
            classes += " progress-bar-striped progress-bar-animated"
        valueProps = {
            "aria-valuemin": "0",
            "aria-valuemax": "100",
            "aria-valuenow": self.value,
            "style":f"width: {self.value}%"
        }
        return jp.Div(a=self, classes=classes, **valueProps)

    def updateProgress(self, value:int=1):
        """
        update progress bar to the given value
        """
        if value >=0 and value <= 100:
            self.value = value
            self.delete_components()
            self.bar = self.getBar()

    def incrementProgress(self, value: int):
        """
        increment the progress bar by the given value
        """
        self.updateProgress(min(100, self.value + value))


class Spinner(jp.Div):
    """
    bootstrap5 spinner
    see https://getbootstrap.com/docs/5.0/components/spinners/
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super(Spinner, self).__init__(classes="spinner-border", role="status", **kwargs)
        self.span = jp.Span(a=self, classes="visually-hidden", text="Loading...")