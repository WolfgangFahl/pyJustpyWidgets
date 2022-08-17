'''
Created on 2022-08-17

@author: th
'''
import sys
import justpy as jp
from jpwidgets.bt5widgets import Alert, App, Link, Login, Logout, SimpleAuthApi


class Version(object):
    '''
    Version handling for bootstrap5 example
    '''
    name = "justpy bootstrap5 example"
    version = '0.0.1'
    date = '2022-08-17'
    updated = '2022-08-17'
    description = 'justpy bootstrap5 login example'
    authors = 'th'
    license = f'''Copyright 2022 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.'''
    longDescription = f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""


class Bootstrap5LoginExampleApp(App):
    '''
    example Application for Bootstrap5
    '''

    def __init__(self, version):
        '''
        Constructor

        Args:
            version(Version): the version info for the app
        '''
        App.__init__(self, version, title="Bootstrap5 example")
        self.addMenuLink(text='Home', icon='home', href="/")
        self.addMenuLink(text='github', icon='github', href="https://github.com/WolfgangFahl/pyJustpyWidgets")
        self.addMenuLink(text='Documentation', icon='file-document',
                         href="https://wiki.bitplan.com/index.php/PyJustpyWidgets")
        self.addMenuLink(text='Source', icon='file-code',
                         href="https://github.com/WolfgangFahl/pyJustpyWidgets/blob/main/jpdemo/examples/bootstrap5app.py")
        self.addMenuLink(text='Login', icon="login", href="/login")
        self.addMenuLink(text='Logout', icon="logout", href="/logout")
        self.authApi = SimpleAuthApi("/tmp/pyJustpyWidgets/logindemo.yaml")
        self.authApi.addUser("user", "user")
        # Routes
        jp.Route('/login', self.login)
        jp.Route('/logout', self.logout)
        jp.Route('/protected', self.protected)

    def setup(self):
        self.wp = self.getWp()

    async def content(self):
        wp = self.getWp()
        jp.Link(a=self.contentbox, href="/protected", text="Link to login protected site")
        return wp

    async def login(self):
        """show login"""
        self.setup()
        Alert(a=self.contentbox, alertType="primary", text="This is a demo login use 'user' as username and password")
        Login(a=self.contentbox, authApi=self.authApi, wp=self.wp)
        return self.wp

    async def logout(self):
        """show login"""
        self.setup()
        Logout(a=self.contentbox, authApi=self.authApi, wp=self.wp)
        return self.wp

    async def protected(self, req):
        """show protected site if logged-in"""
        self.setup()
        # refactor as wrapper
        if not self.authApi.isLoggedIn(req.session_id):
            self.wp.redirect = "/login"
            return self.wp
        # -------------------
        jp.H1(a=self.contentbox, text="Login protected site")
        return self.wp


DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    app=Bootstrap5LoginExampleApp(Version)
    sys.exit(app.mainInstance())