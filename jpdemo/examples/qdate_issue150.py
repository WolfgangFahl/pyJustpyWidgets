'''
Created on 20.08.2022

@author: wf
'''
import justpy as jp

class QInputDateTime(jp.QInput):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = '####-##-## ##:##'
        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD HH:mm', name='date', a=c2,
                             locale={
                                 'days': 'Neděle_Pondělí_Úterý_Středa_Čtvrtek_Pátek_Sobota'.split('_'),
                                 'daysShort': 'Ne_Po_Út_St_Čt_Pá_So'.split('_'),
                                 'months': 'Leden_Únor_Březen_Duben_Květen_Červen_Červenec_Srpen_Září_Říjen_Listopad_Prosinec'.split(
                                     '_'),
                                 'monthsShort': 'Led_Úno_Bře_Dub_Kvě_Čvn_Čvc_Srp_Zář_Říj_Lis_Pro'.split('_')
                             },
                             )

        time_slot = jp.QIcon(name='access_time', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=time_slot)
        self.time = jp.QTime(mask='YYYY-MM-DD HH:mm', format24h=True, name='time', a=c2)

        self.date.parent = self
        self.time.parent = self
        self.date.value = self.value
        self.time.value = self.value
        self.prepend_slot = date_slot
        self.append_slot = time_slot
        self.date.on('input', self.date_time_change)
        self.time.on('input', self.date_time_change)
        self.on('input', self.input_change)

    @staticmethod
    def date_time_change(self, msg):
        print(self.value)
        self.parent.value = self.value
        self.parent.date.value = self.value
        self.parent.time.value = self.value

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value
        self.time.value = self.value


def input_test():
    wp = jp.QuasarPage()
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2020-03-01 12:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2021-04-01 14:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2022-05-01 18:44')
    return wp


from  jpdemo.examples.basedemo import Demo
Demo('QDate issue 150',input_test)