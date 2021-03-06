from PySimpleGUI import Text, Button, Window, Output, VerticalSeparator, Column
from math import modf

no: dict = {'size':(6,2), 'font':('Franklin Gothic Book', 24),'border_width':1, 'button_color':("black","#f9f9f9")}
opr: dict = {'size':(6,2), 'font':('Franklin Gothic Book', 24),'border_width':1, 'button_color':("black","#d6d6d6")}
eq: dict = {'size':(12,2), 'font':('Franklin Gothic Book', 24),'border_width':1, 'button_color':("black","#66a6ff")}
col = [
    [Button('C',**opr), Button('CE',**opr), Button('β',**opr), Button("/",**opr)],
    [Button('7',**no), Button('8',**no), Button('9',**no), Button("*",**opr),],
    [Button('4',**no), Button('5',**no), Button('6',**no), Button("-",**opr)],
    [Button('1',**no), Button('2',**no), Button('3',**no), Button("+",**opr)],    
    [Button('0',**no), Button('.',**no), Button('=',**eq)],
]
layout:list = [
    [Text('Babylon Upgraded Calculator', size=(98,1), justification='center', background_color="#d1d1d1",text_color='black', font=('Franklin Gothic Book', 14, 'bold'))],
    [Text('0.0000', size=(20,1),pad=(0,0), justification='right', background_color='#d1d1d1', text_color='black',font=('Franklin Gothic Book',48), relief='sunken', key="_DISPLAY_")],
    [Column(col),VerticalSeparator(pad=14),Output(size=(80, 20))],
    [Text('Whole number', size=(22,1),pad=(0,0), justification='right', background_color='#d1d1d1', text_color='black',font=('Franklin Gothic Book',36), relief='sunken', key="_DISPLAY1_")],
    [Text('Fractional part', size=(22,1),pad=(0,0), justification='left', background_color='#d1d1d1', text_color='black',font=('Franklin Gothic Book',36), relief='sunken', key="_DISPLAY2_")]
]

window: object = Window('Made by Efe', layout=layout,element_padding=(0,0),background_color="#d1d1d1", size=(800, 720), return_keyboard_events=True)


var: dict = {'front':[], 'back':[], 'decimal':False, 'x_val':0.0, 'y_val':0.0, 'result':0.0, 'operator':''}


def format_number() -> float:
    return float(''.join(var['front']).replace(',','') + '.' + ''.join(var['back']))


def update_display(display_value: str):
    try:
        window['_DISPLAY_'].update(value='{:,.4f}'.format(display_value))
    except:
        window['_DISPLAY_'].update(value=display_value)

        
def number_click(event: str):
    global var
    if var['decimal']:
        var['back'].append(event)
    else:
        var['front'].append(event)
    update_display(format_number())


def clear_click():
    global var
    var['front'].clear()
    var['back'].clear()
    var['decimal'] = False 


def operator_click(event: str):
    global var
    var['operator'] = event
    try:
        var['x_val'] = format_number()
    except:
        var['x_val'] = var['result']
    clear_click()


def calculate_click():
    global var
    try:
        var['y_val'] = format_number()
    except ValueError: # When Equals is pressed without any input
        var['x_val'] = var['result']
    try:
        var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
        update_display(var['result'])
        print('   '+str(var['operator'])+'    '+str(var['y_val']))
        clear_click()    
    except:
        update_display("ERROR! DIV/0")
        clear_click()


def sixtize(event: float):
    if(event<0):
        event= event*(-1)
    res=[0,0,0,0,0]
    pec=[0,0,0,0,0,0,0]
    frac, whole = modf(event)
    x=4
    while(whole!=0):
        res[x]=int(whole%60)
        whole=((whole-res[x])/60)
        x=x-1
    window['_DISPLAY1_'].update(value=(res))
    x,b=0,0
    while(frac!=0):
        a,b=modf(frac*60)
        frac=round(a,1)
        pec[x]=int(b)
        x=x+1
        if x>6:
            frac=0
    window['_DISPLAY2_'].update(value=(pec))
    
while True:
    event, values = window.read()
    if event is None:
        break
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        number_click(event)
    if event in ['Escape:27','C','CE']: 
        clear_click()
        update_display(0.0)
        var['result'] = 0.0
    if event in ['+','-','*','/']:
        operator_click(event)
        print('     '+str(var['x_val']))
    if event == '=':
        calculate_click()
        print(' ¯¯¯¯¯¯¯¯¯\n      '+str(var['result'])+'\n')
    if event == '.':
        var['decimal'] = True
    if event == 'β':
        sixtize(var['result'])

