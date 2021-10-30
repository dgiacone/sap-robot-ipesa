from flask_restful import Resource, reqparse
import json, traceback, base64, requests
from .conf import *
from datetime import datetime
from .solicita_token import solicitaToken
from .logger import log


class abrePalletSap(Resource):
    def post(self, caja):
        # Calculo la fecha y la hora dd/mm/YY H:M:S
        now = datetime.now()
        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Este valor se utiliza para los mensajes de error
        etapa="Abre Pallet"
        
        
        
        payload={
                "d" : {
                    "Caja" : caja,
                    "ePallet" : "",
                    "I3AperturaPallet_To_MensajeNav" :
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

        # Solicito token SAP
        solicita=solicitaToken()
        
        # Extraigo los datos del token y del coockie
        status=solicita["status"]
        token=solicita["token"]
        coockie_str=solicita["coockie"]
        
        if status==1:
            url = os.environ['URL']+"ZGW_ROBOT_SRV/I3_APERTURA_PALLETSet"

            headers = {
                    'sap-client': os.environ['SAP-CLIENT'],
                    'Authorization':  os.environ['CLAVE'],
                    'x-csrf-token': token,  
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie':coockie_str,
                    'Cache-Control': 'no-cache'
                }
            log(url, "ABRE PALLET")
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            log(response.text, "ABRE PALLET")
            if response.status_code == 201:
        
                    respuesta=response.json()
                    if len(respuesta['d']['I3AperturaPallet_To_MensajeNav']['results'])>0:
                        msg=respuesta['d']['I3AperturaPallet_To_MensajeNav']['results'][0]
                        # Tomo valores
                        resultado={}
                        resultado['key']=msg['Key']
                        resultado['type']=msg['Type']
                        resultado['number']=msg['MessageV1']
                        resultado['id']=msg['Id']
                        resultado['message']=msg['Message']
                        resultado['numero_pallet']=msg['MessageV1']
                        
                        # agrego los datos para registro en el log
                       
                        if msg['Type']!='S':
                            resultado['tipo']="ERROR"
                            resultado['status']="key [{}] {}".format(msg['Key'] ,msg['Message'] )
                            resultado['fecha_hora']=fecha_hora
                            resultado['etapa']=etapa
                        else:
                            resultado['tipo']="OK"
                            resultado['status']="  Nuevo Pallet creado Nro: {}  correctamente".format(msg['MessageV1'])
                            resultado['fecha_hora']=fecha_hora
                            resultado['etapa']=etapa
                            
                        log(resultado, "ABRE PALLET")
                        return resultado,200
                        
            else:
                resultado={}
                resultado['tipo']="ERROR"
                resultado['status']="Error en el servicio de apertura de pallet SAP"
                resultado['fecha_hora']=fecha_hora
                resultado['etapa']=etapa
                log(resultado, "ABRE PALLET")
                return resultado, 400
        else:
            
            resultado={}
            resultado['tipo']="ERROR"
            resultado['status']="Error al obtener el token de seguridad de  SAP"
            resultado['fecha_hora']=fecha_hora
            resultado['etapa']=etapa
            log(resultado, "ABRE PALLET")
            return resultado, 400
           
            
    