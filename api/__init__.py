from flask import Flask
from flask_restful import Api
import os


app = Flask(__name__)

from api.recursos.abre_pallet_sap import abrePalletSap
from api.recursos.agrega_caja_pallet_sap import agregaCajaPallet
from api.recursos.busca_datos_caja_sap import buscaDatosCajaPallet
from api.recursos.envia_peso_sap import enviaPesoPallet
from api.recursos.cierra_pallet_sap import cierraPallet

api = Api(app)
api.add_resource(abrePalletSap, "/abre/pallet/<caja>")
api.add_resource(agregaCajaPallet, "/agrega/caja/pallet/<caja>/<pallet>")
api.add_resource(buscaDatosCajaPallet, "/busca/datos/caja/<etiqueta>")
api.add_resource(enviaPesoPallet, "/envia/peso/<caja>/<peso>")
api.add_resource(cierraPallet, "/cierra/pallet/<pallet>")