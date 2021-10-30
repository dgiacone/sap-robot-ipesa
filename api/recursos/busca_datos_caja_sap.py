from flask_restful import Resource, reqparse
from datetime import datetime
import json, traceback, base64, requests, os
import pandas as pd
from .conf import *
from .solicita_token import solicitaToken
from .logger import log

class buscaDatosCajaPallet(Resource):
    def get(self, etiqueta,peso):
        # dd/mm/YY H:M:S
        now = datetime.now()
        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
        etapa="Solicita datos caja"
        
        msg={
        "Caja" : str(etiqueta),
        "Peso" : str(peso),
        "I1LecturaLote_To_DetalleCajaNav" : [],
        "I1LecturaLote_To_AtributosCajaNav" : [],
        "I1LecturaLote_To_MensajesNav" : []
        }
        
        payload=json.dumps(msg)
         
        
        headers = {
            'sap-client': os.environ['SAP-CLIENT'],
            'Authorization':  os.environ['CLAVE'],
            'x-csrf-token': 'Fetch',
            'Cache-Control': 'no-cache'
        }

        solicita=solicitaToken()
        if solicita!="error":
            status=solicita["status"]
            token=solicita["token"]
            coockie_str=solicita["coockie"]
            
            if status==1:
                url = os.environ['URL']+"ZGW_ROBOT_SRV/I1_LECTURA_LOTESet"  
                headers = {
                        'sap-client': os.environ['SAP-CLIENT'],
                        'Authorization':  os.environ['CLAVE'],
                        'x-csrf-token': token,  
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Cookie':coockie_str,
                        'Cache-Control': 'no-cache'
                    }
                log(url, "BUSCA DATOS CAJA")
                response = requests.request("POST", url, headers=headers, data=payload, verify=False)   
                log(response.text, "BUSCA DATOS CAJA")
                if response.status_code == 201:
                    
                        print("mensaje recibido")
                        respuesta=response.json()
                        if len(respuesta['d']['I1LecturaLote_To_DetalleCajaNav']['results'])>0:
                             # Tomo valores
                            msg=respuesta['d']['I1LecturaLote_To_DetalleCajaNav']['results'][0]
                            resultado={}
                            resultado['posicion']=msg['Posicion']
                            resultado['caja']=msg['Caja']
                            resultado['descripcion']=msg['DescripMaterial']
                            resultado['familia_aduana']=msg['FamiliaAduana']
                            resultado['orden']=msg['Orden']
                            resultado['umtara']=msg['UmTara']
                            resultado['material']=msg['Material']
                            resultado['tara']=msg['Tara']    
                            resultado['fecha']=msg['Fecha']
                            resultado['anio']=msg['Anio']
                            resultado['hora']=msg['Hora']
                            # agrego los datos para registro en el log
                            resultado['tipo']="OK"
                            resultado['status']="La etiqueta {} se registro correctamente".format(msg['Caja'])
                            resultado['fecha_hora']=fecha_hora
                            resultado['etapa']=etapa
                            log(resultado, "BUSCA DATOS CAJA")
                            return resultado,200
                    
                        # capturo los mensajes de la respuesta en busca de un error
                        if len(respuesta['d']['I1LecturaLote_To_MensajesNav']['results'])>0:
                            msg_nav=respuesta['d']['I1LecturaLote_To_MensajesNav']['results'][0]
                            type=msg_nav["Type"]
                            mensaje=msg_nav["Message"]
                            key=msg_nav['Key']
                            mensaje="{};{}; ERROR ;key[{}] {} ".format(fecha_hora, etapa, key,mensaje )
                            log(mensaje, "BUSCA DATOS CAJA")
                            return mensaje ,400
                else:
                        # dd/mm/YY H:M:S
                        now = datetime.now()
                        fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
                        etapa="Solicita datos caja"
                        mensaje="Error de servivio SAP"
                        mensaje="{},{},{}".format(fecha_hora, etapa, mensaje)
                        log(mensaje, "BUSCA DATOS CAJA")
                        return mensaje ,400
            else:
                # dd/mm/YY H:M:S
                now = datetime.now()
                fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
                etapa="Solicita datos caja"
                mensaje="Error de seguridad"
                mensaje="{};{};ERROR;{}".format(fecha_hora, etapa, mensaje)
                log(mensaje, "BUSCA DATOS CAJA")
                return mensaje ,400
        else:
            # dd/mm/YY H:M:S
            now = datetime.now()
            fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
            etapa="Solicita datos caja"
            mensaje="Error solicitud token SAP"
            mensaje="{};{};ERROR;{}".format(fecha_hora, etapa, mensaje)
            log(mensaje, "BUSCA DATOS CAJA")
            return mensaje ,400
            
    