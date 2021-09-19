from flask_restful import Resource, reqparse
import json, traceback, base64, requests, os
import pandas as pd
from .conf import *
from .solicita_token import solicitaToken

class buscaDatosCajaPallet(Resource):
    def get(self, etiqueta):
        
        payload={}
        
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
            url = os.environ['URL']+"ZGW_ROBOT_SRV/I1_DETALLE_CAJASet/?$filter=Caja eq '{}' &$expand=I1DetalleCaja_To_AtributosCajaNav&$format=json".format(etiqueta)

            headers = {
                    'sap-client': '110',
                    'Authorization': 'Basic SU5URVJGQVo6SXBlc2EyMDIxKg==',
                    'x-csrf-token': token,  
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie':coockie_str
                }
            response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                
            if response.status_code == 200:
                    print("mensaje recibido")
                    respuesta=response.json()
                    msg=respuesta['d']['results'][0]
                   
                    # Tomo valores
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
                    return resultado,200
            else:
                    print("error mensaje paso 2")
                    return {"msg":response.text}, 400
        else:
            return {"msg":"No se puede obtener el token de seguridad"},400
            
    