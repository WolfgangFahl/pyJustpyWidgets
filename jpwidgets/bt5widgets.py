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

    def __init__(self,version,title:str=None,websockets=True):
        '''
        Constructor
        
        Args:
            version(Version): Version info
            title(str): optional title - if None use Version.description
            websockets(bool): if True use websockets(default)
        '''
        self.version=version
        if title is None:
            title=version.description
        self.title=title
        self.menu=""
        self.websockets=websockets
        
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
        jp.justpy(callback,host=self.host,port=self.port,websockets=self.websockets)
        
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
        
    def createSelect(self,text,value,change,a,**kwargs):
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
        select=jp.Select(a=a,classes="form-select",value=value,change=change,**kwargs)
        selectorLabel.for_component=select
        return select
    
    def createInput(self,text,placeholder,change,a,size:int=30, **kwargs):
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
        jpinput=jp.Input(a=a,classes="form-input",size=size,placeholder=placeholder, **kwargs)
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

class Link:
    '''
    a link
    '''
    @staticmethod
    def create(url,text,tooltip=None,target=None):
        '''
        create a link for the given url and text
        
        Args:
            url(str): the url
            text(str): the text
            tooltip(str): an optional tooltip
        '''
        title="" if tooltip is None else f" title='{tooltip}'"
        target="" if target is None else f" target=' {target}'"
        link=f"<a href='{url}'{title}{target}>{text}</a>"
        return link

             
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
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        classes = "spinner-border"
        kwargs["classes"] = f"{classes} {kwargs.get('classes', '')}"
        super(Spinner, self).__init__(role="status", **kwargs)
        self.span = jp.Span(a=self, classes="visually-hidden", text="Loading...")

class Alert(jp.Div):
    """
    Bootstrap 5 Alert
    see https://getbootstrap.com/docs/5.0/components/alerts/
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super(Alert, self).__init__(classes="alert alert-warning alert-dismissible fade show", role="alert", **kwargs)
        conf={
            "data-bs-dismiss":"alert",
            "classes":"btn-close",
            "aria-label":"Close"
        }
        self.btn = jp.Button(a=self, **conf)
        self.btn.on("click", self.delete_alert)

    def delete_alert(self, _msg):
        """
        delete the alert message
        """
        self.a.remove_component(self)
        
class Collapsible(jp.Div):
    """
    Collapsible div
    see https://getbootstrap.com/docs/4.0/components/collapse/

    use the body attribute to assign contents to the collapsible body
    """

    def __init__(self, label:str, collapsed:bool=False, **kwargs):
        '''
        constructor
        '''
        super().__init__(classes="accordion", **kwargs)
        self.div = jp.Div(a=self, classes="accordion-item")
        self.label = label
        self.btnClasses = "accordion-button"
        self.bodyClasses = "accordion-collapse"
        self.btn = jp.Button(a=self.div,
                             inner_html=self.label,
                             classes=self.btnClasses,
                             click=self.collapse)
        self.collapsibleDiv = jp.Div(a=self.div, classes=f"{self.bodyClasses} collapse show")
        self.body = jp.Div(a=self.collapsibleDiv, classes=f"accordion-body collapse show")
        self.collapsed=collapsed
        self.collapse(changeState=True)

    def collapse(self, changeState:bool=True):
        """
        change state of Collapsible body
        """
        if self.collapsed:
            self.btn.classes = f"{self.btnClasses}"
            self.collapsibleDiv.classes=f"{self.bodyClasses} collapse show"
        else:
            self.btn.classes = f"{self.btnClasses} collapsed"
            self.collapsibleDiv.classes = f"{self.bodyClasses} collapse"
        if changeState:
            self.collapsed = not self.collapsed

    def setCollapseState(self, collapsed:bool):
        """
        set the collapse state to the given state
        """
        self.collapsed = collapsed
        self.collapse(changeState=False)


class DebugOutput(jp.Div):
    """
    shows debug messages
    """
    def __init__(self, **kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        self.messages = []
        self.collapsible = Collapsible("Log", a=self)

    def react(self, _data):
        '''
        called on each event
        '''
        if self.collapsible:
            self.collapsible.body.delete()
        ul = jp.Ul(a=self.collapsible.body, classes="list-none")
        for msg in reversed(self.messages):
            jp.Li(a=ul, text=msg)

    def addMessage(self, msg:str):
        '''
        add message

        Args:
            msg(str): a message to add
        '''
        self.messages.append(msg)
