'''
Created on 2022-08-03

@author: wf
'''
import justpy as jp
import sys
from jpwidgets.bt5widgets import App, ComboBox
import urllib.request, json 

class Version(object):
    '''
    Version handling for bootstrap5 example
    '''
    name="jpComboBox demo example"
    version='0.0.1'
    date = '2022-08-03'
    updated = '2022-08-03'
    description='jpComboBox example'
    authors='Wolfgang Fahl'
    license=f'''Copyright 2022 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.'''
    longDescription=f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""

class JpComboBoxDemo(App):
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
        self.addMenuLink(text='Source',icon='file-code',href="https://github.com/WolfgangFahl/pyJustpyWidgets/blob/main/jpdemo/examples/jpComboBoxDemo.py")
        
    def getCountries(self):
        countriesUrl="https://raw.githubusercontent.com/stefangabos/world_countries/master/data/countries/en/countries.json"
        with urllib.request.urlopen(countriesUrl) as url:
            jsonText=url.read().decode()
            countries = json.loads(jsonText)
        return countries
        
    async def content(self):
        '''
        show the content
        '''
        head_html="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">"""
        wp=self.getWp(head_html)    
        rowA=jp.Div(classes="row",a=self.contentbox)
        self.colA1=jp.Div(classes="col-3",a=rowA)
        self.colA2=jp.Div(classes="col-3",a=rowA)
        self.colA3=jp.Div(classes="col-6",a=rowA)
        comboBox=self.createComboBox(labelText="Country",a=self.colA1,placeholder="Please enter a country")
        for country in self.getCountries():
            comboBox.dataList.add(jp.Option(value=country["alpha2"],text=country["name"]))
            print(country)
        return wp
       
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    app=JpComboBoxDemo(Version)
    sys.exit(app.mainInstance())