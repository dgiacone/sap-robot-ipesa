import requests, os
from .conf import *

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
            'sap-client': '110',
            'Authorization': 'Basic SU5URVJGQVo6SXBlc2EyMDIxKg==',
            'x-csrf-token': 'Fetch',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        
        a=response.cookies
        b=list(a)
        cookie=b[1].value
        token=response.headers['x-csrf-token']
        coockie_str='sap-usercontext=sap-client=110; SAP_SESSIONID_DEV_110={}'.format(cookie)
        
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
            
        return msg