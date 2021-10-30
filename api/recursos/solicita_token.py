import requests, os
from .conf import *
from .logger import log

def solicitaToken():   
        
        '''
        Funcion que solicita el token y el cookie de sesion a SAP.
        Este proceso es necesario siempre antes de llamar a cualquier servicio de SAP
        el TOKEN dura 30 minutos por eso lo pedimos cada ve que enviamos para asi evitar tener que 
        evitar controlar el tiempo del token.
        '''
            
        url = os.environ['URL']+"/ZGW_ROBOT_SRV/?$format=json"
       
        payload={}
        headers = {
            'sap-client': os.environ['SAP-CLIENT'],
            'Authorization': os.environ['CLAVE'],
            'x-csrf-token': 'Fetch',
            'Cache-Control': 'no-cache'
        }
        log(url, "SOLICITA TOKEN")
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        log(response.text, "SOLICITA TOKEN")
        
        if response.status_code==200:
            centro=os.environ['SAP-CLIENT']
            a=response.cookies
          
            b=list(a)
             
          
         
            cookie=b[0].value
            token=response.headers['x-csrf-token']
            coockie_str='sap-usercontext=sap-client={}; SAP_SESSIONID_DEV_{}={}'.format(centro,centro,cookie)
        
            if response.status_code == 200:
                msg={
                    "status":1,
                    "token":token,
                    "coockie":coockie_str
                }
            else:
                msg={
                    "status":0,
                    "token":"",
                    "coockie":""
                }
        else:
            msg="error"
        log(msg, "SOLICITA TOKEN")
        return msg