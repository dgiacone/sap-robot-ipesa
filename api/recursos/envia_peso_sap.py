from flask_restful import Resource, reqparse
import json, traceback, base64, requests, os
import pandas as pd
from .conf import *
from .solicita_token import solicitaToken


class enviaPesoPallet(Resource):
    def post(self,caja,peso):
        
        payload={
                        "d" : {
                            "Caja" : caja,
                            "Peso" : peso,
                            "I2RegistroPeso_To_MensajesNav" :
                            {
                                "results" : [ ]
                                }
                        }
                    }
        payload=json.dumps(payload) 
        
       
        headers = {
            'sap-client': '110',
            'Authorization': 'Basic SU5URVJGQVo6SXBlc2EyMDIxKg==',
            'x-csrf-token': 'Fetch',
        }

        solicita=solicitaToken()
        status=solicita["status"]
        token=solicita["token"]
        coockie_str=solicita["coockie"]
        
        if status==1:
            url = os.environ['URL']+"ZGW_ROBOT_SRV/I2_REGISTRO_PESOSet"

            headers = {
                    'sap-client': '110',
                    'Authorization': 'Basic SU5URVJGQVo6SXBlc2EyMDIxKg==',
                    'x-csrf-token': token,  
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie':coockie_str
                }
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
           
            if response.status_code == 201:
                    print("mensaje recibido")
                    respuesta=response.json()
                    msg=respuesta['d']['I2RegistroPeso_To_MensajesNav']['results'][0]
                   
                    # Tomo valores
                    resultado={}
                    resultado['key']=msg['Key']
                    resultado['type']=msg['Type']
                    resultado['number']=msg['Number']
                    resultado['id']=msg['Id']
                    resultado['message']=msg['Message']
                    return resultado,200
            else:
                    print("error en registro de peso")
                    return {"msg":response.text}, 400
        else:
            return {"msg":"No se puede obtener el token de seguridad"},400
            
    