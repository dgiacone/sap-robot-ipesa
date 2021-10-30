from flask_restful import Resource, reqparse
import json, traceback, base64, requests
from .conf import *
from .solicita_token import solicitaToken
from .logger import log	
from datetime import datetime


class cierraPallet(Resource):
    def post(self, pallet):
        # Calculo la fecha y la hora dd/mm/YY H:M:S
        now = datetime.now()
        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Este valor se utiliza para los mensajes de error
        etapa="Cierra Pallet"
        payload={
                    "d" : {
                        "Pallet" : pallet,
                        "I5CierrePallet_To_MensajesNav" :
                        {
                            "results" : [ ]
                            }
                    }
                }
                    
        payload=json.dumps(payload) 
        
       
        headers = {
            'sap-client': os.environ['SAP-CLIENT'],
            'Authorization':  os.environ['CLAVE'],
            'x-csrf-token': 'Fetch',
            'Cache-Control': 'no-cache'
        }

        solicita=solicitaToken()
        status=solicita["status"]
        token=solicita["token"]
        coockie_str=solicita["coockie"]

      
        
        if status==1:
            url = os.environ['URL']+"ZGW_ROBOT_SRV/I5_CIERRE_PALLETSet"
            

            headers = {
                    'sap-client': os.environ['SAP-CLIENT'],
                    'Authorization':  os.environ['CLAVE'],
                    'x-csrf-token': token,  
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie':coockie_str,
                    'Cache-Control': 'no-cache'
                }
            log(url, "CERRAR PALLET")
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            log(response.text, "CERRAR PALLET")
            if response.status_code == 201:
                    
                    
                    respuesta=response.json()
                    msg=respuesta['d']['I5CierrePallet_To_MensajesNav']['results'][0]
                   
                    # Tomo valores
                    resultado={}
                    resultado['key']=msg['Key']
                    resultado['type']=msg['Type']
                    resultado['number']=msg['Number']
                    resultado['id']=msg['Id']
                    resultado['message']=msg['Message']
                    resultado['messageV1']=msg['MessageV1']
                    if msg['Type']!='S':
                        resultado['tipo']="ERROR"
                        resultado['status']="key [{}] {}".format(msg['Key'] ,msg['Message'] )
                        resultado['fecha_hora']=fecha_hora
                        resultado['etapa']=etapa
                    else:
                        resultado['tipo']="OK"
                        resultado['status']="  Pallet {} abierto correctamente".format(msg['Number'])
                        resultado['fecha_hora']=fecha_hora
                        resultado['etapa']=etapa
                    log(resultado, "CERRAR PALLET")
                    return resultado,200
            else:
                    resultado={}
                    resultado['tipo']="ERROR"
                    resultado['status']="Error al cerrar el pallet"
                    resultado['fecha_hora']=fecha_hora
                    resultado['etapa']=etapa
                    log(resultado, "CERRAR PALLET")
                    return {"msg":response.text}, 400
        else:
            resultado={}
            resultado['tipo']="ERROR"
            resultado['status']="No se puede obtener el token de seguridad"
            resultado['fecha_hora']=fecha_hora
            resultado['etapa']=etapa
            log(resultado, "CERRAR PALLET")
            return {"msg":"No se puede obtener el token de seguridad"},400