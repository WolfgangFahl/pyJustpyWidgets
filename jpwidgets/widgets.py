'''
Created on 2022-05-22

@author: wf
'''
import justpy as jp
import pandas as pd

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
        
    def load_lod(self,lod:list):
        '''
        load the given list of dicts
        '''
        # https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
        df=pd.DataFrame(lod)
        self.load_pandas_frame(df)
        
        
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
        