from flask_restful import Resource, reqparse
import json, traceback, base64, requests, os
import pandas as pd
from .conf import *



class healt(Resource):
    def get(self):
       return 200