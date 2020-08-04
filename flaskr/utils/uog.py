from bs4 import BeautifulSoup
import pandas as pd
import requests

def getKeys(header):
    cookie = {}
    
    keySections = header['Set-Cookie'].split(", ")
    
    for x in keySections:
        cookie[x.split('=')[0]] = x.split('=')[1]
        
    return cookie


def webadvisorQuery(params):
    try:
        getURL = 'https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?CONSTITUENCY=WBST&type=P&pid=ST-WESTS12A&TOKENIDX='
        r = requests.get(getURL)
        cookie = getKeys(r.headers)

        getURL = 'https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?CONSTITUENCY=WBST&type=P&pid=ST-WESTS12A&TOKENIDX=' + cookie['LASTTOKEN']
        r = requests.get(getURL, cookies=cookie)
        cookie = getKeys(r.headers)

        postURL = 'https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?TOKENIDX=' + cookie['LASTTOKEN'] + '&SS=1&APP=ST&CONSTITUENCY=WBST'
        postfields = {"VAR1":'', "VAR10":"", "VAR11":"","VAR12":"", "VAR13":"", "VAR14":"", "VAR15":"", "VAR16":"", "DATE.VAR1":"", "DATE.VAR2":"", "LIST.VAR1_CONTROLLER":"LIST.VAR1", "LIST.VAR1_MEMBERS":"LIST.VAR1*LIST.VAR2*LIST.VAR3*LIST.VAR4", "LIST.VAR1_MAX":"5", "LIST.VAR2_MAX":"5", "LIST.VAR3_MAX":"5", "LIST.VAR4_MAX":"5", "LIST.VAR1_1":"", "LIST.VAR2_1":"", "LIST.VAR3_1":"", "LIST.VAR4_1":"", "LIST.VAR1_2":"", "LIST.VAR2_2":"", "LIST.VAR3_2":"", "LIST.VAR4_2":"", "LIST.VAR1_3":"", "LIST.VAR2_3":"", "LIST.VAR3_3":"", "LIST.VAR4_3":"", "LIST.VAR1_4":"", "LIST.VAR2_4":"", "LIST.VAR3_4":"", "LIST.VAR4_4":"", "LIST.VAR1_5":"", "LIST.VAR2_5":"", "LIST.VAR3_5":"", "LIST.VAR4_5":"", "VAR7":"", "VAR8":"", "VAR3":"", "VAR6":"", "VAR21":"", "VAR9":"", "SUBMIT_OPTIONS":""}
        postfields.update(params)
        r = requests.post(postURL, data=postfields, cookies=cookie)
        f = r.text

        webadvisor=BeautifulSoup(f, 'lxml')

        course_table = pd.read_html(str(webadvisor),header=1, attrs = {'summary': 'Sections'}, keep_default_na=False)[0]

        return {"success": True, "data": course_table.to_dict(orient='index')}
    except:
        return {"success": False, "data": ""}