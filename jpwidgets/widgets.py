'''
Created on 2022-05-22

@author: wf
'''
from typing import List, Union, Tuple

import justpy as jp

class LodGrid(jp.AgGrid):
    '''
    agGrid wrapper to be loaded from list of dicts
    '''
    
    def __init__(self, options:dict={},**kwargs):
        '''
        constructor
        
        Args:
            grid_options(dict): AgGrid options
        '''
        # set up the aggrid
        lodGrid_options={
            'enableCellTextSelection':True,
            # enable sorting on all columns by default
            'defaultColDef': {
                'sortable': True
            },
        }
        grid_options = {**options, **lodGrid_options}
        
        super().__init__(options=grid_options,**kwargs)
        
        
class MenuButton(jp.QBtn):
    '''
    a menu button
    '''
    def __init__(self, **kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs,color='primary')
    
class MenuLink(MenuButton):
    '''
    a menu link
    '''
    def __init__(self, **kwargs):
        '''
        constructor
        '''
        super().__init__(**kwargs,type="a",target="_blank")
        
class QPasswordDialog(jp.QDialog):
    '''
    a Quasar framework based password dialog
    '''
    password_dialog_html="""
<q-card>
  <q-card-section>
      <q-form class="q-gutter-md">
        <q-input clearable type='text' name="user" label="User"/>
        <q-input clearable type='password' name="password" label="Password">
          <q-icon name="visibility_off"/>
        </q-input>
      </q-form> 
  </q-card-section>

  <q-card-actions align="right">
    <q-btn flat name="Login" label="Login" color="primary" v-close-popup></q-btn>
    <q-btn flat name="Cancel" label="Cancel" color="primary" v-close-popup></q-btn>
  </q-card-actions>
</q-card>
"""
    def onVisibilityClick(self,_msg):
        #print(msg)
        vt=self.visibilityToggle
        if vt.name=="visibility_off":
            vt.name="visibility"
            self.passwordInput.type="text"
        else:
            vt.name="visibility_off"
            self.passwordInput.type="password"
                
    def __init__(self,**kwargs):
        '''
        constructor
        '''
        jp.QDialog.__init__(self,**kwargs)
        self.card=jp.parse_html(QPasswordDialog.password_dialog_html,a=self)
        self.loginButton=self.card.name_dict["Login"]
        self.cancelButton=self.card.name_dict["Cancel"]
        self.userInput=self.card.name_dict["user"]
        self.passwordInput=self.card.name_dict["password"]
        self.visibilityToggle=self.card.name_dict["visibility_off"]
        self.visibilityToggle.on("click",self.onVisibilityClick)
 
class QAlert(jp.QDialog):
    '''
    alert dialog
    '''
    alert_dialog_html = """
<q-card>
  <q-card-section>
    <div name="alertTitle" class="text-h6">Alert</div>
  </q-card-section>

  <q-card-section name="alertContent">
  </q-card-section>

  <q-card-actions align="right">
    <q-btn flat label="OK" color="primary" v-close-popup />
  </q-card-actions>
</q-card>
"""
    def __init__(self,**kwargs):
        '''
        constructor
        '''
        jp.QDialog.__init__(self,**kwargs)
        self.card=jp.parse_html(QAlert.alert_dialog_html,a=self)
        self.alertTitle=self.card.name_dict["alertTitle"]
        self.alertContent=self.card.name_dict["alertContent"]


class QuasarColorPalette:
    """
    Provides the Quasar color palette

    see https://quasar.dev/style/color-palette
    """

    colors = ["red", "pink","purple", "deep-purple", "indigo", "blue", "light-blue", "cyan", "teal", "green",
              "light-green", "lime", "yellow", "amber", "orange", "deep-orange", "brown", "grey", "blue-grey"]

    @classmethod
    def colorPalette(cls):
        palette = []
        for color in cls.colors:
            colors = [f"{color}-{i}" for i in range(1,15)]
            palette.append(color)
            palette.extend(colors)
        return palette

    @classmethod
    def getBackgroundColor(cls, color:str):
        return f"bg-{color}"

    @classmethod
    def getTextColor(cls, color:str):
        return f"text-{color}"

    @classmethod
    def getAllBackgroundColors(cls):
        return [cls.getBackgroundColor(color) for color in cls.colorPalette()]

    @classmethod
    def getAllTextColors(cls):
        return [cls.getTextColor(color) for color  in cls.colorPalette()]


class Token(jp.QDiv):
    """
    Displays a token and its label in a given color
    """
    TOKEN_CLASSES = "rounded-borders text-center row inline flex-center brand-color shadow-4 q-mx-xs"
    TOKEN_VALUE_CLASSES = "q-pa-xs"
    TOKEN_LABEL_CLASSES = "text-italic text-weight-light text-white q-pa-xs"

    def __init__(self, label:str, value:str, color:str=None, **kwargs):
        """
        constructor
        Args:
            label: label of the token (token name in NER)
            value: value of the token
            color: background color of the token Should be in QuasarColorPalette.colorPalette()
            **kwargs:
        """
        if color is None:
            color = "primary"
        classes = f"{self.TOKEN_CLASSES} bg-{color}"
        super(Token, self).__init__(classes=classes, **kwargs)
        self.label = label
        self.value = value
        self.valueWrapper = jp.QDiv(a=self, classes=self.TOKEN_VALUE_CLASSES)
        jp.QDiv(a=self.valueWrapper, text=self.value, classes="col")
        self.labelWrapper = jp.QDiv(a=self, classes=self.TOKEN_LABEL_CLASSES)
        jp.QDiv(a=self.labelWrapper, text=self.label, classes="col")


class TokenSequence(jp.QDiv):
    """
    Displays the sequence of given tokens.
    If the Token is a tuple of the form (label, value) the token value is displayed with its label.

    inspired by https://github.com/tvst/st-annotated-text
    """

    def __init__(self, tokens:List[Union[str,Tuple[str,str]]], colorMap:dict=None, **kwargs):
        super(TokenSequence, self).__init__(classes="q-pr-md q-ma-lg row justify-start", **kwargs)
        if colorMap is None:
            colorMap={}
            labels = {token[0] for token in tokens if isinstance(token, tuple)}
            colors = [ color for color in QuasarColorPalette.colorPalette() if '4' in color]
            totalColors=len(colors)
            for i, label in enumerate(labels):
                colorIndex = label.__hash__() % totalColors
                colorMap[label]=colors[colorIndex]
        for token in tokens:
            if isinstance(token, str):
                jp.QDiv(a=self, text=token, classes="q-mx-xs text-center q-pa-xs")
            else:
                label, value = token
                Token(label, value, color=colorMap.get(label),a=self)

class HideShow(jp.Div):
    """
    Create a Div with visibility (hid/show) toogle 
    """
    TRIANGLE_LEFT = "◀"
    TRIANGLE_DOWN = "▼"

    def __init__(
        self,
        hide_show_label: tuple,
        show_content: bool = True,
        **kwargs):
        """
        constructor
        
        Args:
            content: justpy component with the content to hide/show
            hide_show_label: labels to be shown if the content is hidden/shown.       
            show_content: If True show the content at page load otherwise the content is hidden.
            **kwargs: additional justpy arguments
        """
        # first add the hide/show button to my parent
        a=kwargs.get("a")
        self.label_if_shown, self.label_if_hidden = hide_show_label
        self.btn = jp.Button(a=a, text=self._getStatusLabel(show_content), on_click=self.toggleHideShow)
        # then create a div component
        jp.Div.__init__(self,**kwargs)
        self._setShowContent(show_content)
        
    def _setShowContent(self,show_content:bool):
        """
        set my show_content state via my data container
        """
        self.data["show_content"]=show_content
        self.hidden(not show_content)

    def _getStatusLabel(self,show_content:bool) -> str:
        """
        Returns the Icon of the current status
        """
        if show_content:
            icon = self.TRIANGLE_DOWN
            label = self.label_if_shown
        else:
            icon = self.TRIANGLE_LEFT
            label = self.label_if_hidden if self.label_if_hidden is not None else self.label_if_shown
        return f"{label} {icon}"      

    def toggleHideShow(self, _msg:dict):
        """
        Toggle the visibility status of the content
        """
        show_content = not self.data["show_content"]
        self._setShowContent(show_content)
        self.btn.text = self._getStatusLabel(show_content)