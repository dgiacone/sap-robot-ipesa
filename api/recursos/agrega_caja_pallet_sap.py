from flask_restful import Resource, reqparse
import json, traceback, base64, requests
from .conf import *
from .solicita_token import solicitaToken
from .logger import log	
from datetime import datetime


class agregaCajaPallet(Resource):
    def post(self, caja,pallet):
         # Calculo la fecha y la hora dd/mm/YY H:M:S
        now = datetime.now()
        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Este valor se utiliza para los mensajes de error
        etapa="Abre Pallet"
        
        payload={
                    "d": {
                        "Caja" :caja,
                            "Pallet" : pallet,
                            "I4AsignacionPallet_To_MensajesNav" :
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
            
            url = os.environ['URL']+"ZGW_ROBOT_SRV/I4_ASIGNACION_PALLETSet"
            log(url, "AGREGA CAJA PALLET")
            headers = {
                    'sap-client': os.environ['SAP-CLIENT'],
                    'Authorization':  os.environ['CLAVE'],
                    'x-csrf-token': token,  
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie':coockie_str,
                    'Cache-Control': 'no-cache'
                }
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            log(response.text, "AGREGA CAJA PALLET")
            if response.status_code == 201:
                    print("mensaje recibido")
                    
                    respuesta=response.json()
                    msg=respuesta['d']['I4AsignacionPallet_To_MensajesNav']['results'][0]
                   
                    # Tomo valores
                    resultado={}
                    resultado['key']=msg['Key']
                    resultado['type']=msg['Type']
                    resultado['number']=msg['Number']
                    resultado['id']=msg['Id']
                    resultado['message']=msg['Message']
                    resultado['MessageV1']=msg['MessageV1']
                    # agrego los datos para registro en el log
                       
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
                    log(resultado, "AGREGA CAJA PALLET")
                    
                    return resultado,200
            else:
                   
                    resultado={}
                    resultado['tipo']="ERROR"
                    resultado['status']="Error en el servicio de agregar caja a pallet SAP"
                    resultado['fecha_hora']=fecha_hora
                    resultado['etapa']=etapa
                    log(resultado, "AGREGA CAJA PALLET")
                    return {"msg":response.text}, 400
        else:
            resultado={}
            resultado['tipo']="ERROR"
            resultado['status']="No se puede obtener el token de seguridad"
            resultado['fecha_hora']=fecha_hora
            resultado['etapa']=etapa
            log(resultado, "AGREGA CAJA PALLET")
            return {"msg":"No se puede obtener el token de seguridad"},400
            
    