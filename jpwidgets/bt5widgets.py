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
             
        