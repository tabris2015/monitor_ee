# script para poblar la base de datos con datos aleatorios
# se definen funciones auxiliares para la funcion principal
# NOTA
# este script genera valores de fechas

#importa los django settings para usar modulos de lproyecto
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitor_ee.settings')

#importa los modulos correctamente
import django
django.setup()

from django.utils import timezone
#importa los modelos de la app rango
from rango.models import Category, Page, Medidor, Medidas

#utilidades para fecha y hora
from datetime import datetime, timedelta
import random

#funcion para poblar la base de datos
# TODO:
# probar el funcionamiento de manera separada y crear el modelo 'medidas'
def extraer():
    """abre el archivo y extrae los datos de fecha y medicion"""
    print "extrayendo informacion..."
    # nota: poner full path al archivo!
    archivo= open('/home/pi/django_projects/tango_project/datos_temp/datos.txt','r')
    f_raw = archivo.readline().split() #lista con los datos de fecha y hora
    print f_raw
    corr= timedelta(hours=4) #correccion para la hora de la base de datos - resolver
    fecha = datetime(int(f_raw[0]),int(f_raw[1]),int(f_raw[2]),int(f_raw[3]),int(f_raw[4]),)
    print fecha
    fecha = fecha - corr
    datos = archivo.readline().split() # lista de valores de las lecturas
    archivo.close()			#cerramos archivo
    
    return datos,fecha		#devuelve una tupla con la lista de los valores y la fecha


def generar_valor(instante, v_min=40, medidor=0):
    """genera un valor aleatorio dentro de rangos establecidos
        que varia segun la fecha y hora del acontecimiento
        ejemplo:
	    print generar_valor(datetime.today())
	    >> 120
 	el valor retornado depende tanto de la hora del dia
	del dia de la semana y del mes del anho
    """
    #pesos de horas: [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23]
    w_horas =	     [5,5,5,6,40,40,30,30,6,7,8, 8, 80,80,80,90,70, 8, 7, 6, 9, 9, 9,8]
    norm = sum(w_horas)
    #normalizamos el vector	
    for elemento in w_horas:
        w_horas[w_horas.index(elemento)]=elemento/float(norm)
    
    #pesos de dias   [L,M,M,J,V,S,D]
    w_dia_semana=    [4,4,10,24,20,2,1]
    norm = sum(w_dia_semana)
    for dia in w_dia_semana:
	w_dia_semana[w_dia_semana.index(dia)]=dia/float(norm)

    #pesos de mes: 	[E,F,M,A,M,J,J,A,S,O,N,D]
    w_mes=	 	[3,3,3,4,4,4,4,4,4,3,3,3]
    norm = sum(w_mes)
    for mes in w_mes:
	w_mes[w_mes.index(mes)] = mes/float(norm)
    
    #pesos del medidor
    w_medidor = [1,1,0.7,0.7,0.8,0.4,0.5,1]*2
    #pesos por tiempo:  		Hora, Dia, mes
    base_hora, base_dia, base_mes  =  	1100,  60, 20
    
    valor = v_min + base_hora*w_horas[instante.hour]*random.uniform(0.5,2.5)\
	+ base_dia*w_dia_semana[instante.weekday()]*random.uniform(0.4,1.2)\
	+ base_mes*w_mes[instante.month-1]*random.uniform(0.3,1.1)
    
    return int(valor*w_medidor[medidor])

def generar_lista(fecha, med):
    """genera una lista de medidas para cada medidor"""
    medidas = []
    for i in range(med):
	medidas.append(generar_valor(instante=fecha, medidor = i))
    
    return medidas, fecha


def ingresar(datos):
    """ingresa los datos a la base de datos"""
    print "actualizando la base de datos"
    i=0
    for dato in datos[0]:
	nombre= "med"+str(i)
	med = add_medicion(nombre,dato, datos[1])
	i = i+1    
    print "ingresados " + str(len(datos[0])) + " registros en fecha" + datos[1].strftime('%d, %b %Y')
    

#nueva funcion
def add_medicion(nombre_medidor,valor,fecha):
    medidor = Medidor.objects.get_or_create(nombre = nombre_medidor)[0]
    #print medidor
    med = Medidas.objects.get_or_create(medidor = medidor,fecha = fecha)[0]
    #print med
    #med.fecha=datetime.today()
    med.kwh = valor
    #print "valor anadido"
    #print valor
    med.save()
    #print "valor actualizado"
    return med


# Start execution here!
if __name__ == '__main__':
    
    #fecha_in=datetime(2012,1,1)
    tiempo = timedelta(days=120)
    fecha_in = datetime.today()-timedelta(days=1)#-tiempo
    for i in range(100*24):
        delta= timedelta(hours=i)
	ingresar(generar_lista(fecha_in+delta, 4))
    print "terminado!"
