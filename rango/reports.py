from datetime import datetime, timedelta

import rango
from .models import Medidor, Medidas

# FUNCIONES PARA RECUPERAR DATOS DE LA BASE DE DATOS
# LOS REPORTES NOS ARROJAN LOS DATOS QUE NECESITAMOS 

#--------------------------helper function --------------

import calendar
def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime(year,month,day)
#-----------------------------------------------------
#funcion de prueba para los highcharts
class ChartMes(object):
    @classmethod
    def get_month_power(cls, month, medidor_slug="", resumen=False):
        fecha_in = month - timedelta(days=month.day) #inicio del mes
        fecha_fin = add_months(fecha_in,1)
        dias = (fecha_fin - timedelta(days=1)).day
        print "----------------------"
        print "dias:"+ str(dias)
        print "----------------------"
        datos = []
        datos1 = []
        datos2 = []
        datos3 = []
        series = []
        anho = month.year
        mes = month.month

        if medidor_slug:
            medidores= Medidor.objects.get(slug=medidor_slug)
            datos.append(
                Medidas.objects.filter(
                medidor=medidores
                ).exclude(
                fecha__gte=fecha_fin    #fecha fin
                ).filter(
                fecha__gte=fecha_in  #fecha inicio
                )
            )
            

            for med in datos[0]:
                    datos1.append(med.kwh)
                #datos1.append(aux)
            for dia in range(dias):
                aux_dia = sum(datos1[dia:dia+24])
                datos2.append(aux_dia)

            series.append({
                    'name':medidores.nombre,
                    'data':datos2
                })
            #print "--........--"
            #print "dias en arreglo:" + str(len(datos2))
            #print "--........--"
        # si es que no pasan el parametro del medidor entonces retornamos 
        # los datos de TODOS los medidores
        else:
            medidores = Medidor.objects.all()
            for med in medidores:
                datos.append(
                    Medidas.objects.filter(
                    medidor=med
                    ).exclude(
                    fecha__gte=fecha_fin    #fecha fin
                    ).filter(
                    fecha__gte=fecha_in  #fecha inicio
                    )
                )

            for dato in datos:  #para cada queryset por cada medidor
                aux=[]
                datos2=[]
                for med in dato: #para cada arreglo
                    aux.append(med.kwh)  #obtenemos su kwh
                #print "--->horas: " + str(len(aux)) + " " + str(len(aux)/24)
                datos1.append(aux) 
		#variablea auxiliar para la suma del mes si nos piden un resumen
		sum_mes = 0
                for dia_ in range(len(aux)/24): #para los dias del mes consultado
                    aux_dia = sum(aux[dia_:dia_+24])
		    
		    #si es que es resumen se van sumando
                    if resumen:
			sum_mes += aux_dia
		    else:
		    #si no se aumentan a una lista
			datos2.append(aux_dia)

                if resumen:
		    datos2.append(sum_mes)

	        datos3.append(datos2)
                
            
	    
		    
            #print "--........--"
            #print "medidores:" + str(len(datos3)) +" dias en arreglo:" + str(len(datos3[0])) 
            #print "--........--"    
            for i,j in enumerate(medidores):
                series.append({
                    'name':medidores[i].nombre,
                    'data':datos3[i]
                })

        return series
  
######################################################

class ChartDia(object):
    @classmethod
    def get_day_power(cls, day, medidor_slug=""):
        fecha_in = day
        fecha_fin = day + timedelta(days=1)
        datos = []
        datos1=[]
        series = []
        anho= day.year
        mes = day.month
        dia_=day.day
        referencia = datetime(1970,1,1)
        tiempo = day - referencia
        #si nos pasan un slug entonces mostramos el resumen del ultimo dia 
        # solo del medidor que queremos
        if medidor_slug:
            medidores= Medidor.objects.get(slug=medidor_slug)
            datos.append(
                Medidas.objects.filter(
                medidor=medidores
                ).exclude(
                fecha__gte=fecha_fin    #fecha fin
                ).filter(
                fecha__gte=fecha_in  #fecha inicio
                )
            )

            for med in datos[0]:
                    datos1.append(med.kwh)
                #datos1.append(aux)

            series.append({
                    'name':medidores.nombre,
                    'data':datos1
                })

        # si es que no pasan el parametro del medidor entonces retornamos 
        # los datos de TODOS los medidores
        else:
            medidores = Medidor.objects.all()
            for med in medidores:
                datos.append(
                    Medidas.objects.filter(
                    medidor=med
                    ).exclude(
                    fecha__gte=fecha_fin    #fecha fin
                    ).filter(
                    fecha__gte=fecha_in  #fecha inicio
                    )
                )

            for dato in datos:
                aux=[]
		sum_dia=0	#para el resumen
                for med in dato:
		    if resumen:
			sum_dia += med.kwh
		    else:
			aux.append(med.kwh)

		if resumen:
		    aux.append(sum_dia)

                datos1.append(aux) 

            
            for i,j in enumerate(medidores):
                series.append({
                    'name':medidores[i].nombre,
                    'data':datos1[i]
                })


        
        #extrae datos entre 2 fechas desde la base de datos   
        
        return series

#class Resumen(object):
#    """este reporte retorna el resumen semanal, diario o mensual"""
#    @classmethod
#    def get_brief(self, )
        
