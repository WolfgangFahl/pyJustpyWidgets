'''
@author Tim Holzheim
2022-06
'''
from datetime import datetime

from jpwidgets.jpTable import Table, EchoButtonColumn, EchoTwiceButtonColumn, EchoTwiceInputDisabledButtonColumn

import justpy as jp
import sys
from jpwidgets.bt5widgets import App

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
        self.rows=3
        self.cols=3
        
    async def content(self):
        '''
        show the content
        '''
        head_html="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">"""
        wp=self.getWp(head_html)
        lod=[{
                    "pageTitle": "WebSci 2019",
                    "acronym": "WebSci 2019",
                    "ordinal": 11,
                    "homepage": "http://websci19.webscience.org/",
                    "title": "11th ACM Conference on Web Science",
                    "eventType": "Conference",
                    "startDate": datetime.fromisoformat("2019-06-30"),
                    "endDate": datetime.fromisoformat("2019-07-03"),
                    "inEventSeries": "WebSci",
                    "country": "USA",
                    "region": "US-MA",
                    "city": "Boston",
                    "acceptedPapers": 41,
                    "submittedPapers": 120,
                    "presence": "online",
                    "wikicfpId": 891,
                    "tibKatId":"1736060724",
                    "subject": "Software engineering",
                    "ISBN":"9781450370707",
                    "gndId":"1221636014"
                }
        ]
        cellValidationMap = {
            'beer_servings': lambda value: value.isnumeric()
        }
        self.table = Table(lod=[{"index":i, **lod[0]} for i in range(5)],
                      editable=True,
                      cellValidationMap=cellValidationMap,
                      a=self.contentbox,
                      actionColumns=[
                          EchoButtonColumn(name="Echo"),
                          EchoTwiceButtonColumn(name="EchoTwice"),
                          EchoTwiceInputDisabledButtonColumn(name="EchoTwiceDisableInput")
                      ])
        return wp


def main(argv=None): # IGNORE:C0111
    '''main program.'''

    if argv is None:
        argv=sys.argv[1:]
        
    app=JpTableDemo(Version)
    app.cmdLine(argv,app.content)

    
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())