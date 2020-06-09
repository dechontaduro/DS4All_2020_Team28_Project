# importing the requests library 
import requests 
import json
import time
import pandas as pd
import numpy as np

import base64

#https://www.toptal.com/python/in-depth-python-logging#:~:text=Python%20Logging%20Best%20Practices&text=Here%20are%20the%20best%20practices,root%20logger%20behind%20the%20scene.
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(LOG_FORMATTER_CONSOLE)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.suffix = "%Y-%m-%d.txt"
   file_handler.setFormatter(LOG_FORMATTER_FILE)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger

#create a zip file with the information downloaded from IDEAM site
def decodeZip(base64File, fileName, file):
	try:
		log.info(f"decode ... -{file}")
		file_content=base64.b64decode(base64File)
		base64_result = open(fileName, 'wb')
		base64_result.write(file_content)
		log.info('#'*100)
		return True
	except:
		log.error(f"error decode ... -{file}{fileName}")
		log.debug('*'*100)
		log.debug(base64File)
		log.debug('*'*100)
		return False

def hook_process_file_factory(*factory_args, **factory_kwargs):
	def hook_process_file(result, *request_args, **request_kwargs): #def process_file(result, **kwargs):
		file = factory_kwargs["file"]
		r = json.loads(result.text)
		log.info(f"procesando ... -{file}")
		decodeZip(r['value'], FILE_BASE + '{}_{}.zip'.format(file, round(time.time())), file)
		return None
	return hook_process_file


def hook_response_factory(*factory_args, **factory_kwargs):
	def hook_response(result, *request_args, **request_kwargs): #def do_something(result, **kwargs):
		file = factory_kwargs["file"]

		if result.status_code == 404:
			log.error(f"error 404 {file}")
			return -1

		r = json.loads(result.text)
		jobId = r['jobId']
		log.info(f"consultando ... -{file}-{jobId}-{r['jobStatus']}")
		url2=f"http://dhime.ideam.gov.co/server/rest/services/AtencionCiudadano/DescargarArchivo/GPServer/DescargarArchivo/jobs/{jobId}"

		if (r['jobStatus'] == "esriJobSubmitted" or r['jobStatus'] == "esriJobExecuting"):
			time.sleep(5)
		
		ts = time.time()
		params = {
			'f':"json",
			'dojo.preventCache': round(ts*1000)
		}

		if (r['jobStatus'] == "esriJobSucceeded"):
			url2 += '/results/Archivo'
			params['returnType'] = 'data'
		r = requests.get(url = url2, params = params, 
					hooks = {'response' : [hook_response_factory(file=file)] 
											if r['jobStatus'] != "esriJobSucceeded" 
											else [hook_process_file_factory(file=file)]})
		return None
	return hook_response

#############################################################################################################
######################################---------- ---MAIN--- -----------######################################
#############################################################################################################

LOG_FORMATTER_CONSOLE = logging.Formatter("%(asctime)s—%(levelname)s— %(message)s", datefmt='%H:%M:%S')
LOG_FORMATTER_FILE = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")


LOG_FILE = "ideam_scrapping"
log = get_logger("IDEAM")

URL = "http://dhime.ideam.gov.co/server/rest/services/AtencionCiudadano/DescargarArchivo/GPServer/DescargarArchivo/submitJob"

etiquetas = \
	{'CAUDAL': ['Q_MX_D', 'Q_MEDIA_D', 'Q_MN_D'],
	'PRECIPITACION': ['PT_10_TT_D', 'PTPM_TT_M'],
	'PRECIPITACION2': ['PTPM_CON'],
	'PRECIPITACION3': ['PT_10_TT_D'],
	'TEMPERATURA': ['TMX_CON', 'TMN_CON']
	}

print ('{:░<100}'.format(''))
print ('{:░^100}'.format('PROGRAMA PARA LA AUTOMATIZACION DE CONSULTAS AL IDEAM'))

print ('{:░^100}'.format('░░░░░░░░░░░░░░░░░░░░░░'))
print ('{:░^100}'.format('░░░░░░░▄█▄▄▄█▄░░░░░░░░'))
print ('{:░^100}'.format('▄▀░░░░▄▌─▄─▄─▐▄░░░░▀▄░'))
print ('{:░^100}'.format('█▄▄█░░▀▌─▀─▀─▐▀░░█▄▄█░'))
print ('{:░^100}'.format('░▐▌░░░░▀▀███▀▀░░░░▐▌░░'))
print ('{:░^100}'.format('████░▄█████████▄░████░'))
print ('{:░>100}'.format(''))


print ('{}'.format(r'                                                                                '))
print ('{}'.format(r' _____    _____  _    _     _____   __   __        ____   ____     ____   ____  '))
print ('{}'.format(r'(_____)  (_____)(_)  (_)   (_____) (__) (__)     _(____) (____)  _(____) (____) '))
print ('{}'.format(r'(_)  (_)(_)___  (_)__(_)_ (_)___(_) (_)  (_)    (_) _(_)(_)  (_)(_) _(_)(_)  (_)'))
print ('{}'.format(r'(_)  (_)  (___)_(________)(_______) (_)  (_)      _(_)  (_)  (_)  _(_)  (_)  (_)'))
print ('{}'.format(r'(_)__(_)  ____(_)    (_)  (_)   (_) (_)  (_)     (_)___ (_)__(_) (_)___ (_)__(_)'))
print ('{}'.format(r'(_____)  (_____)     (_)  (_)   (_)(___)(___)   (______) (____) (______) (____) '))
print ('{}'.format(r'                                                                                '))
print ('{}'.format(r'                                                                                '))
print('\n'*2)


archivo = r"C:\Users\juanc\Google Drive\DS4All_Team28\Listado Estaciones IDEAM 1990-2020\est_limnimetrica.csv"
parametro = "CAUDAL"
linea_desde = 489

#archivo = input('Ingrese la ruta del archivo que desea procesar(ej: d:\\temp\\archivo.csv): ')
#parametro = input('Ingrese el parametro que desea consultar (ej: PRECIPITACION, PRECIPITACION2 (PluvioMétrica), CAUDAL, TEMPERATURA):')

FILE_BASE = "\\".join(archivo.split("\\")[:-1])+"\\data\\"
FILE_NAME = archivo.split("\\")[-1]
FILE_NAME = FILE_NAME.split(".")[0]

#import sys
#sys.exit() 

etiquetaLst = etiquetas[parametro]
parametro = 'PRECIPITACION' if 'PRECIPITACION' in parametro else parametro

log.info(f"Archivo:{archivo} Línea inicial:{linea_desde}")
log.info(f"Parametro:{parametro} Variables:{','.join(etiquetaLst)}")

df = pd.read_csv(archivo, usecols=['codigo'])

peticiones = df.codigo.count() * len(etiquetaLst)
log.info(f"Estaciones:{df.codigo.count()} Variables:{len(etiquetaLst)} Peticiones:{peticiones}")

peticion = linea_desde * len(etiquetaLst)
log.info(f"Petición inicial :{peticion}")
#import sys
#sys.exit() 

for i, codigo in enumerate(df[linea_desde:].codigo):
	log.info(f"línea:{i + linea_desde} estación:{codigo}")
	#continue

	for j, etiqueta in enumerate(etiquetaLst):
		peticion += 1
		log.info(f"p:{peticion}/{peticiones} {100.0 * peticion / peticiones:.1f}% :{i + linea_desde} v:{etiqueta}")

		filtro = f"sort=&filter=((IdParametro~eq~'{parametro}'and~Etiqueta~eq'{etiqueta}'and~IdEstacion~eq'{codigo}'))&group=&fechaInicio=1991-1-1T05%3A00%3A00.000Z&fechaFin=2020-5-31T05%3A00%3A00.000Z&mostrarGrado=true&mostrarCalificador=true&mostrarNivelAprobacion=true"
		items = f'[{{"IdParametro":"{parametro}","Etiqueta":"{etiqueta}","EsEjeY1":false,"EsEjeY2":false,"EsTipoLinea":false,"EsTipoBarra":false,"TipoSerie":"Estandard","Calculo":""}}]'

		PARAMS = {
			'f' : "json",
			'Filtro' : filtro,
			'Items' : items
		}
		
		file=f"{FILE_NAME}_{codigo}_{parametro}_{etiqueta}"
		r = requests.get(url = URL, params = PARAMS, 
						hooks = {'response' : [hook_response_factory(file=file)]})


