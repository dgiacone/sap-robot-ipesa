from datetime import date
from datetime import datetime
from pathlib import Path
def log(mensaje, tarea):
    #Fecha actual
    now = datetime.now()
    my_file = Path("logger.csv")
    '''
    Verifico si el archivo de log existe, si existe hago un update si no lo creo.
    '''
    if my_file.is_file():
        text_file = open("logger.csv", "a")
        msg="{};[{}];{} \r".format(now,tarea,mensaje)
        text_file.write(msg)
        text_file.close()
    else:
        text_file = open("logger.csv", "w")
        msg="{};[{}];{} \r".format(now,tarea,mensaje)
        text_file.write(msg)
        text_file.close()
        
   
    