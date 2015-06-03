# script para poblar la base de datos
# se definen funciones auxiliares para la funcion principal
# NOTA
# este script utiliza los archivos mandados por el gateway de prueba

#importa los django settings para usar modulos de lproyecto
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_project.settings')

#importa los modulos correctamente
import django
django.setup()

from django.utils import timezone
#importa los modelos de la app rango
from rango.models import Category, Page, Medidor, Medidas

#utilidades para fecha y hora
from datetime import datetime, timedelta

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

def populate(datos):
    """ingresa los datos a la base de datos"""
    print "actualizando la base de datos"
    i=0
    for dato in datos[0]:
	nombre= "med"+str(i)
	print nombre
	med = add_medicion(nombre,dato, datos[1])
	i = i+1    
    
    #int out what we have added to the user.
    for m in Medidor.objects.all():
        for med in Medidas.objects.filter(medidor=m):
            print "- {0} - {1}".format(str(m), str(med))


#nueva funcion
def add_medicion(nombre_medidor,valor,fecha):
    medidor = Medidor.objects.get_or_create(nombre = nombre_medidor)[0]
    print medidor
    med = Medidas.objects.get_or_create(medidor = medidor,fecha = fecha)[0]
    print med
    #med.fecha=datetime.today()
    med.kwh = valor
    print "valor anadido"
    print valor
    med.save()
    print "valor actualizado"
    return med


# Start execution here!
if __name__ == '__main__':
   
    populate(extraer())
    print "terminado!"
