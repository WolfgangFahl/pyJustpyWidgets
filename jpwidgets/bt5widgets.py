'''
Created on 2022-07-24

@author: wf

Bootstrap5Widgets to be used with 
https://getbootstrap.com/docs/5.0/getting-started/introduction/
 
'''
import asyncio
import hashlib
import pathlib
from datetime import datetime, timedelta
from typing import Callable

import justpy as jp
import os
import yaml
import socket
import sys
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from justpy.htmlcomponents import JustpyBaseComponent
from dataclasses import dataclass

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
        self.menu={}
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
            menuHtml=""
            for menuEntry in self.menu.values():
                menuHtml+=menuEntry.asHtml()
            html=f"""<div name='containerbox'>
        <!--  common menu -->
<div name='headerbox' id='headerbox'>
{menuHtml}
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
        wp.debug = getattr(self, "debug", False)
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
        
    def clearErrors(self):
        '''
        clear the Error area
        '''
        self.errors.inner_html=""

    def getLanguages(self):
        # see https://github.com/sahajsk21/Anvesha/blob/master/src/components/topnav.js
        languages= [
                ["ar", "&#1575;&#1604;&#1593;&#1585;&#1576;&#1610;&#1577;"],
                ["arz", "&#1605;&#1589;&#1585;&#1609;"],
                ["ast", "Asturianu"],
                ["az", "Az&#601;rbaycanca"],
                ["azb", "&#1578;&#1734;&#1585;&#1705;&#1580;&#1607;"],
                ["be", "&#1041;&#1077;&#1083;&#1072;&#1088;&#1091;&#1089;&#1082;&#1072;&#1103;"],
                ["bg", "&#1041;&#1098;&#1083;&#1075;&#1072;&#1088;&#1089;&#1082;&#1080;"],
                ["bn", "&#2476;&#2494;&#2434;&#2482;&#2494;"],
                ["ca", "Catal&agrave;"],
                ["ce", "&#1053;&#1086;&#1093;&#1095;&#1080;&#1081;&#1085;"],
                ["ceb", "Sinugboanong Binisaya"],
                ["cs", "&#268;e&scaron;tina"],
                ["cy", "Cymraeg"],
                ["da", "Dansk"],
                ["de", "Deutsch"],
                ["el", "&Epsilon;&lambda;&lambda;&eta;&nu;&iota;&kappa;&#940;"],
                ["en", "English"],
                ["eo", "Esperanto"],
                ["es", "Espa&ntilde;ol"],
                ["et", "Eesti"],
                ["eu", "Euskara"],
                ["fa", "&#1601;&#1575;&#1585;&#1587;&#1740;"],
                ["fi", "Suomi"],
                ["fr", "Fran&ccedil;ais"],
                ["gl", "Galego"],
                ["he", "&#1506;&#1489;&#1512;&#1497;&#1514;"],
                ["hi", "&#2361;&#2367;&#2344;&#2381;&#2342;&#2368;"],
                ["hr", "Hrvatski"],
                ["hu", "Magyar"],
                ["hy", "&#1344;&#1377;&#1397;&#1381;&#1408;&#1381;&#1398;"],
                ["id", "Bahasa Indonesia"],
                ["it", "Italiano"],
                ["ja", "&#26085;&#26412;&#35486;"],
                ["ka", "&#4325;&#4304;&#4320;&#4311;&#4323;&#4314;&#4312;"],
                ["kk", "&#1178;&#1072;&#1079;&#1072;&#1179;&#1096;&#1072; / Qazaq&#351;a / &#1602;&#1575;&#1586;&#1575;&#1602;&#1588;&#1575;"],
                ["ko", "&#54620;&#44397;&#50612;"],
                ["la", "Latina"],
                ["lt", "Lietuvi&#371;"],
                ["lv", "Latvie&scaron;u"],
                ["min", "Bahaso Minangkabau"],
                ["ms", "Bahasa Melayu"],
                ["nan", "B&acirc;n-l&acirc;m-g&uacute; / H&#333;-l&oacute;-o&#275;"],
                ["nb", "Norsk (bokm&aring;l)"],
                ["nl", "Nederlands"],
                ["nn", "Norsk (nynorsk)"],
                ["pl", "Polski"],
                ["pt", "Portugu&ecirc;s"],
                ["ro", "Rom&acirc;n&#259;"],
                ["ru", "&#1056;&#1091;&#1089;&#1089;&#1082;&#1080;&#1081;"],
                ["sh", "Srpskohrvatski / &#1057;&#1088;&#1087;&#1089;&#1082;&#1086;&#1093;&#1088;&#1074;&#1072;&#1090;&#1089;&#1082;&#1080;"],
                ["sk", "Sloven&#269;ina"],
                ["sl", "Sloven&scaron;&#269;ina"],
                ["sr", "&#1057;&#1088;&#1087;&#1089;&#1082;&#1080; / Srpski"],
                ["sv", "Svenska"],
                ["ta", "&#2980;&#2990;&#3007;&#2996;&#3021;"],
                ["tg", "&#1058;&#1086;&#1207;&#1080;&#1082;&#1251;"],
                ["th", "&#3616;&#3634;&#3625;&#3634;&#3652;&#3607;&#3618;"],
                ["tr", "T&uuml;rk&ccedil;e"],
                ["tt", "&#1058;&#1072;&#1090;&#1072;&#1088;&#1095;&#1072; / Tatar&ccedil;a"],
                ["uk", "&#1059;&#1082;&#1088;&#1072;&#1111;&#1085;&#1089;&#1100;&#1082;&#1072;"],
                ["ur", "&#1575;&#1585;&#1583;&#1608;"],
                ["uz", "O&#699;zbekcha / &#1038;&#1079;&#1073;&#1077;&#1082;&#1095;&#1072;"],
                ["vi", "Ti&#7871;ng Vi&#7879;t"],
                ["vo", "Volap&uuml;k"],
                ["war", "Winaray"],
                ["yue", "&#31925;&#35486;"],
                ["zh", "&#20013;&#25991;"],
            ]
        return languages

    def createSelectorGroupWithLabel(self,a,text:str,classes=""):
        '''
        create a selector Group with the given label
        '''
        # 
        # https://getbootstrap.com/docs/4.0/components/input-group/
        #<div class="input-group-prepend">
        #<span class="input-group-text" id="">First and last name</span>
        #</div>
        #selectorLabel=jp.Label(text=text,a=a,classes="form-label label")
        selectorGroup=jp.Div(a=a,classes=f"input-group {classes}")
        selectorGroupPrepend=jp.Div(a=selectorGroup,classes="input-group-prepend")
        selectorLabel=jp.Span(text=text,a=selectorGroupPrepend,classes="input-group-text")
        return selectorGroup,selectorLabel
        
    def createSelect(self,labelText,value,change,a,groupClasses="",**kwargs):
        '''
        create a select control with a label with the given text, the default value
        and a change onChange function having the parent a
        
        Args:
            labelText(str): the text for the label
            value(str): the selected value
            change(func): an onChange function
            a(object): the parent component of the Select control
        '''
        selectorGroup,_selectorLabel=self.createSelectorGroupWithLabel(a, text=labelText,classes=groupClasses)
        select=jp.Select(a=selectorGroup,classes="form-select",value=value,change=change,**kwargs)
        return select
    
    def createComboBox(self,labelText,placeholder,change,a,size:int=30,groupClasses="",**kwargs):
        '''
        create a combobox with a label with the given text
        a placeholder text and a change onChange function having the parent a
        
        Args:
            labelText(str): the text for the label
            placeholder(str): a placeholder value
            change(func): an onChange function
            a(object): the parent component of the Select control
            size(int). the size of the input
        '''
        selectorGroup,selectorLabel=self.createSelectorGroupWithLabel(a, text=labelText,classes=groupClasses)
        jpinput=ComboBox(a=selectorGroup,classes="form-input",size=size,placeholder=placeholder, **kwargs)
        jpinput.on('input', change)
        selectorLabel.for_component=jpinput
        return jpinput
    
    def createInput(self,labelText,placeholder,change,a,size:int=30,groupClasses="",**kwargs):
        '''
        create an input control with a label with the given text
        a placeholder text and a change onChange function having the parent a
        
        Args:
            labelText(str): the text for the label
            placeholder(str): a placeholder value
            change(func): an onChange function
            a(object): the parent component of the Select control
            size(int). the size of the input
        '''
        selectorGroup,selectorLabel=self.createSelectorGroupWithLabel(a, text=labelText,classes=groupClasses)
        jpinput=jp.Input(a=selectorGroup,classes="form-input",size=size,placeholder=placeholder, **kwargs)
        jpinput.on('input', change)
        selectorLabel.for_component=jpinput
        return jpinput
    
    def createCheckbox(self,labelText,a,groupClasses="",**kwargs):
        '''
        create an checkBox control with a label with the given text
        having the parent a
        
        Args:
            labelText(str): the text for the label
            a(object): the parent component of the Select control
            size(int). the size of the input
        '''
        selectorGroup,selectorLabel=self.createSelectorGroupWithLabel(a, text=labelText,classes=groupClasses)
        jpinput=jp.Input(a=selectorGroup,type="checkbox",classes="form-check-input", **kwargs)
        selectorLabel.for_component=jpinput
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
        
    def addMenuLink(self,text,icon,href,target=None):
        '''
         add a menu entry
         
         text(str)
         icon(str): see https://materialdesignicons.com/ for possible icons
         href(str): the link
         target(str): "_blank" or None
        '''
        self.menu[text]=MenuEntry(text,icon,href,target)

class About(jp.Div):
    """
    About Div for a given vresion
    """

    def __init__(self,version,a,**kwargs):
        """
        construct an about Div for the given version
        """
        jp.Div.__init__(self,a=a,**kwargs)

        jp.Div(text=f"{version.description}",a=self)
        jp.Div(text=f"version: {version.version}",a=self)
        jp.Div(text=f"updated: {version.updated}",a=self)
        jp.Div(text=f"authors: {version.authors}",a=self)
        # url,text,tooltip=None,target=None,style:str=None
        jp.Div(inner_html=Link.create(url=version.doc_url,text="documentation",target="_blank"),a=self)
        jp.Div(inner_html=Link.create(url=version.chat_url,text="discussion",target="_blank"),a=self)
        jp.Div(inner_html=Link.create(url=version.cm_url,text="source",target="_blank"),a=self)


class MenuEntry:
    '''
    a menu entry
    '''
    def __init__(self,text,icon,href,target):
        self.text=text
        self.icon=icon
        self.href=href
        self.target=target
        
    def asHtml(self):
        target="" if self.target is None else f" target=' {self.target}'"
        html=f"""
  <!-- {self.text} --><a
    href='{self.href}'
    title='{self.text}'{target}>
    <i class='mdi mdi-{self.icon} headerboxicon'></i>
  </a>
"""   
        return html     
        
class Link:
    '''
    a link
    '''
    @staticmethod
    def create(url,text,tooltip=None,target=None,style:str=None):
        '''
        create a link for the given url and text
        
        Args:
            url(str): the url
            text(str): the text
            tooltip(str): an optional tooltip
            target(str): e.g. _blank
            style(str): any style to be applied
        '''
        title="" if tooltip is None else f" title='{tooltip}'"
        target="" if target is None else f" target=' {target}'"
        style="" if style is None else f" style='{style}'"
        link=f"<a href='{url}'{title}{target}{style}>{text}</a>"
        return link

class DataList(jp.Div):
    '''
    a DataList
    '''
    html_tag = 'datalist'
    
    def __init__(self,**kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        cls = JustpyBaseComponent
        self.id = cls.next_id
        
    def clear(self):
        self.inner_html=""
        
    def addOption(self,text,value):
        self.inner_html+=f"""<option value="{value}">{text}</option>"""
                 
class ComboBox(jp.Input):
    '''
    combo box with attached datalist
    '''
    
    def __init__(self,**kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs)
        self.attributes.append("list")
        self.dataList=DataList(a=self)
        self.list=self.dataList.id

class SimpleCheckbox(jp.Div):
    """
    a simple Checkbox
    """
    def __init__(self,a,labelText,classes="col-1",**kwargs):
        """
        create a simple checkbox with the given label
        """
        jp.Div.__init__(self,a=a,classes=classes,data={'checked': False},**kwargs)
        self.checkbox=jp.Input(a=self,type="checkbox", classes="form-check-input",model=[self, 'checked'],**kwargs)
        self.label=jp.Label(a=self,text=labelText)

    def check(self,checked:bool):
        self.data["checked"]=checked

    def isChecked(self)->bool:
        return self.data["checked"]

class ProgressBar(jp.Div):
    """
    Displays a progressbar
    see https://getbootstrap.com/docs/5.0/components/progress/
    """

    def __init__(self, animated:bool=False, withKillSwitch:bool=False, **kwargs):
        '''
        constructor
        '''
        super().__init__(classes="row align-items-center", **kwargs)
        if withKillSwitch:
            self.stopButton:jp.Button = jp.Button(a=self, text="Stop", classes="btn btn-danger col-1")
        colClass = "col-11" if withKillSwitch else "col-12"
        self.progressContainer = jp.Div(a=self, classes=colClass)
        self.progressDiv = jp.Div(a=self.progressContainer, classes="progress")
        self.animated = animated
        self.value = 0
        self.bar = self.getBar()

    def onStop(self, *, callback:Callable):
        """
        Callback for the kill switch / stop button
        """
        if getattr(self, "stopButton") is not None and isinstance(self.stopButton, jp.Button):
            self.stopButton.on("click", callback)

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
        return jp.Div(a=self.progressDiv, classes=classes, **valueProps)

    def updateProgress(self, value:int=1):
        """
        update progress bar to the given value
        """
        if value >=0 and value <= 100:
            self.value = value
            self.progressDiv.delete_components()
            self.bar = self.getBar()

    def incrementProgress(self, value: int):
        """
        increment the progress bar by the given value
        """
        self.updateProgress(min(100, self.value + value))

@dataclass
class State:
    value:bool


class Switch(jp.Input):
    '''
    a switch
    https://mdbootstrap.com/docs/standard/forms/switch/
    '''
    
    def __init__(self,a,labelText:str,state:State=None,div_classes:str="",**kwargs):
        '''
        construct a Switch
        
        Args:
            labelText(str): the text for the label
            kwargs(): keyword arguments
        '''
        self.div=jp.Div(a=a,classes = f"form-check form-switch {div_classes}")
        classes="form-check-input"
        kwargs["classes"] = f"{classes} {kwargs.get('classes', '')}"
        super().__init__(a=self.div,type="checkbox",role="switch",**kwargs)
        if state:
            self.state=state
            self.checked=self.state.value
            self.on("input",self.onChangeState)

        self.switchLabel = jp.Label(
                a=self.div,
                text=labelText,
                classes="form-check-label"
        )
        self.switchLabel.for_component = self

    def onChangeState(self,msg):
        self.state.value=msg.checked

    def update_label(self, label:str):
        """
        update the label of the switch
        Args:
            label: new label of the switch
        """
        self.switchLabel.text = label

class IconButton(jp.Button):
    '''
    a button with an icon
     see https://www.w3schools.com/howto/howto_css_icon_buttons.asp 
    '''
    def __init__(self,iconName,**kwargs):
        classes = "btn"
        kwargs["classes"] = f"{classes} {kwargs.get('classes', '')}"
        super().__init__(**kwargs)
        self.icon=jp.I(a=self,classes=f'mdi mdi-{iconName} headerboxicon')     

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

    def __init__(self, alertType:str=None, **kwargs):
        """
        constructor
        """
        if alertType is None:
            alertType = "warning"
        alertType = f"alert-{alertType}"
        super(Alert, self).__init__(classes=f"alert {alertType} alert-dismissible fade show", role="alert", **kwargs)
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
    see https://getbootstrap.com/docs/5.0/components/accordion/

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


class AuthApiInterface:
    """AuthenticationApi interface defining the methods needed for the login widget"""

    def __init__(self):
        """constructor"""
        self.sessions = {}

    def addUser(self, name:str, password:str) -> bool:
        """
        creates a new user entry with the given information
        Args:
            name: name of the user
            password: password of the user

        Returns:
            True if the user creation was successful otherwise False
        """
        return NotImplemented

    def existsUser(self, name:str) -> bool:
        """Returns True if the user exists otherwise False"""

    def removeUser(self, name:str) -> bool:
        """
        Remove the user under the given name
        Args:
            user: user to remove

        Returns:
            True if the user removal was successful otherwise False
        """
        return NotImplemented

    def isAuthenticated(self, name:str, password:str):
        """
        Check if the given name is known and the given password corresponds to the user
        Args:
            name: name of the user
            password: password of the user

        Returns:
            True if the user is known and the password is correct otherwise False
        """
        return NotImplemented

    def login(self, sessionId:str, userName:str=None):
        """
        set the given sessionId as logged in
        Args:
            sessionId: sessionId of the user
            userName: name of the user
        """
        self.sessions[sessionId] = {
            "user": userName,
            "logged_in_at": datetime.now(),
            "logged_in": True
        }

    def logout(self, sessionId:str):
        """logout give sessionId"""
        del self.sessions[sessionId]

    def isLoggedIn(self, sessionId:str) -> bool:
        """
        Checks if the given sessionId is loggedIn
        """
        loggedId = False
        if sessionId in self.sessions:
            loggedInSince: timedelta = datetime.now() - self.sessions[sessionId].get("logged_in_at")
            if loggedInSince < timedelta(days=7):
                loggedId = self.sessions[sessionId].get("logged_in", False)
        return loggedId


class SimpleAuthApi(AuthApiInterface):
    """A simple authentication api based on YAML"""

    def __init__(self, filepath:str):
        """
        constructor
        Args:
            filepath: filepath to the yaml containing the authentication information
        """
        super().__init__()
        self.filepath = filepath
        self.users = {}
        self._readAuthFile()

    def addUser(self, name:str, password:str) -> bool:
        if self.existsUser(name):
            print("User already exists")
            return False
        else:
            self.users[name] = {
                "name": name,
                "password_hash": self._hashPassword(password)
            }
            self._writeAuthFile()
            return True

    def _hashPassword(self, password:str):
        """Hash the given password"""
        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    def existsUser(self, name:str) -> bool:
        return name in self.users

    def removeUser(self, name:str) -> bool:
        if self.existsUser(name):
            del self.users[name]
            self._writeAuthFile()
            # remove user sessions
            self.sessions = {k:v for k,v in self.sessions.items() if v.get("user") != name}
            return True
        else:
            print("Tried to delete a user that does not exist")
            return False

    def isAuthenticated(self, name:str, password:str) -> bool:
        isAuthenticated = False
        if self.existsUser(name):
            user = self.users.get(name)
            pwdHash = self._hashPassword(password)
            if user.get("password_hash") == pwdHash:
                isAuthenticated = True
        return isAuthenticated


    def _readAuthFile(self):
        """read the auth file and store as user information"""
        pathlib.Path(self.filepath).parent.mkdir(parents=True, exist_ok=True)
        if os.path.isfile(self.filepath):
            with open(self.filepath, "r") as fp:
                try:
                    users = yaml.safe_load(fp)
                    if isinstance(users, dict):
                        self.users = users
                    else:
                        raise Exception("Authentication yaml file has not the expected format")
                except yaml.YAMLError as exc:
                    print(exc)
                except Exception as exc:
                    print(exc)
        else:
            # file currently does not exist → create empty file
            with open(self.filepath, "w") as fp:
                print("", file=fp)

    def _writeAuthFile(self):
        """write user information to yaml file"""
        pathlib.Path(self.filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w") as fp:
            yaml.dump(self.users, fp)


class Login(jp.Div):
    """
    login form
    """

    def __init__(self, authApi:AuthApiInterface, wp:jp.WebPage, label:str=None, redirectPath:str=None, **kwargs):
        """
        constructor
        Args:
            authApi: api to handle the authentication
            wp: WebPage used to handle the redirect
            label: label for the username input field
            redirectPath: after successful login redirect to this path
        """
        if label is None:
            label="User"
        if redirectPath is None:
            redirectPath = "/"
        self.wp=wp
        super(Login, self).__init__(classes="container", **kwargs)
        self.authApi = authApi
        self.redirectPath = redirectPath
        self.rowA = jp.Div(a=self, classes="row")
        self.rowB = jp.Div(a=self, classes="row")
        self.rowC = jp.Div(a=self, classes="row")
        self.colA1 = jp.Div(a=self, classes="col-12")
        self.colB1 = jp.Div(a=self, classes="col-12")
        self.colC1 = jp.Div(a=self, classes="col-12")
        self.header = jp.H2(a=self.colA1, text="Login")
        self.form = jp.Form(a=self.colC1)
        # user field
        self.userContainer = jp.Div(a=self, classes="mb-3")
        self.userLabel = jp.Label(a=self.userContainer, classes="form-label", text=label)
        self.userInput = jp.Input(a=self.userContainer, classes="form-control")
        # password field
        self.pwdContainer = jp.Div(a=self, classes="mb-3")
        self.pwdLabel = jp.Label(a=self.pwdContainer, classes="form-label", text="Password")
        self.pwdInput = jp.Input(a=self.pwdContainer, classes="form-control", type="password")
        # login button
        self.submit = jp.Button(a=self, classes="btn btn-primary", type="submit", text="Login", click=self.loginClick)

    async def loginClick(self, msg):
        user = self.userInput.value
        password = self.pwdInput.value
        isValid = self.authApi.isAuthenticated(user, password)
        if isValid:
            Alert(a=self.colB1, alertType="success", text="Login successful. You are now logged in")
            self.authApi.login(msg.session_id, user)
            await self.wp.update()
            await asyncio.sleep(1)
            self.wp.redirect = self.redirectPath
            return
        else:
            Alert(a=self.colB1, text="Login not successful")


class Logout(jp.Div):
    """Logout widget"""

    def __init__(self, authApi:AuthApiInterface, wp:jp.WebPage, redirectPath:str=None, **kwargs):
        """
        constructor
        Args:
            authApi: api to handle the authentication
            wp: WebPage used to handle the redirect
            redirectPath: after successful login redirect to this path
        """
        if redirectPath is None:
            redirectPath = "/"
        super().__init__(**kwargs)
        self.wp=wp
        self.authApi = authApi
        self.redirectPath = redirectPath
        self.logoutBtn =  jp.Button(a=self, classes="btn btn-danger", text="Logout", click=self.logoutClick)

    async def logoutClick(self, msg):
        """handle logout click"""
        sessionId = msg.session_id
        self.authApi.logout(sessionId)
        Alert(a=self, alertType="success", text="Logout successful. You are now logged out")
        await self.wp.update()
        await asyncio.sleep(1)
        self.wp.redirect = self.redirectPath
        return
