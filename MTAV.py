#!/usr/bin/env python3

import os
import sys
import time
import re
import csv 

class Menu:
	def presentar(self):
		presentacion = '''Aplicación de Programación Matemática 
para distribución de viviendas en una cooperativa de ayuda mutua 
optimizando la satisfacción de los interesados (version 0.2)

----------------------------------------------------------------
Estudiantes:
	Ezequiel Sánchez (eze91@outlook.com)
	Martín Prino (marpri3210@gmail.com)
Profesor Responsable:
	Hector Cancela
----------------------------------------------------------------
'''
		print(presentacion)

	def principal(self):
		principal = '''
Menu - Ingrese las letras de el comando a ejecutar
- (I)nstrucciones : pasos a seguir para realizar la asignación.
- (A)siganar : ¿todo listo? Realiza la asignación final.
- (M)etodología : metodología utilizada para la asignación.
- (C)olaborar : ¿como puedo colaborar en el proyecto?
- (L)icencia : información sobre licencia del programa. 
- (S)alir

[I|A|M|C|L|S]:'''
		print(principal)

	def instrucciones(self):
		instrucciones = '''Instrucciones:
1) Preparación del archivo
   -----------------------

El programa espera una tabla con los identificadores de las viviendas en la primera columna y con las familias en la primera fila. Luego, en la fila de cada familia se listan las preferencias de las familias por las viviendas. Estas preferencias se representan en forma numérica siendo el numero (natural) la preferencia por la vivienda.

El formato de entrada al programa es un archivo en formato CSV (Coma Separated Values), un formato estandar y soportado para exportar e importar por programas populares de planillas electrónicas como Microsoft Excel, OpenCalc y Google Sheets. El separador no necesariamente debe ser como, puede ser '.', ',', ';' o tabulador.

Lo puede crear en su editor de planillas eletronica de su preferencia y exportarlo en formato CSV con el combre 'preferencias.csv' guardandolo en la misma carpeta del programa (llamada MTAV)

Ejemplo en editor de planilla de cálculo:

                   |  101 | 102 | 201 | 202 |     <---- Identificares de vivienda
---------------------------------------------
Sanchez            |   4  |  3  |  1  |  2  |
---------------------------------------------
Pino               |   2  |  4  |  1  |  3  |
---------------------------------------------
Cancela            |   4  |  2  |  1  |  3  |
---------------------------------------------
Rodriquez Da´Silva |   3  |  1  |  4  |  2  |
---------------------------------------------

 ^
 |
 
Identificadores de familia

El siguiente ejemplo representa que la vivienda 201 es la preferida por la familia Sanchez, la 202 es la segunda y asi sucesivamente (sienda la 101 es la menos deseada por la familia Sanchez). Luego es igual para el resto de las familias.

Los cuidados que se deben tener (y que serán chequiados por el programa avisando en caso de algún tipo de anomalia) son:

- La cantidad de familais debe ser igual a la cantidad de viviendas (cantidad de filas igual a la cantidad de columnas).
- Las preferencias deben ser una permutacion de naturales de [1, 2, ..., CANTIDAD_VIVIENDAS] (sin repetidos ni salteados)

La tabla anterior exportada a CSV:

                   ,  101 , 102 , 201 , 202
Sanchez            ,  1  ,  3  ,  4  ,  2 
Pino               ,  2  ,  4  ,  1  ,  3 
Cancela            ,  4  ,  2  ,  1  ,  3 
Rodriquez Da´Silva ,  3  ,  1  ,  4  ,  2 

Se cuenta con un ejemplo de entrada ('preferencias_EJEMPLO.csv') para tomar como referencia.


2) Ejecutar comando Asignar
   ------------------------

Luego de creado el archivo como se detalla en el punto 1 seleccione el comando (A)signar. Luego el programa pedirá confirmacion para empezar la asignación. Si cree que el el archivo preferencias es correcto, acepte. En breves segundos la asignación debería estar completa.

3) Asignación final
   ----------------
'''
		print(instrucciones)

	def metodologia(self):
		print('''Info de metodología''')

	def colaborar(self):
		print('''Puede colaborar con este proyecto en GTIHUB_url''')

	def licencia(self):
		print('''El software tiene licencia MIT.

Copyright (c) 2016 MTAV

Por la presente se autoriza, de forma gratuita, a cualquier persona que haya obtenido una copia de este software y archivos de documentación asociados (el "Software"), a utilizar el Software sin restricción, incluyendo sin limitación los derechos de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender copias de este Software, y permitir lo mismo a las personas a las que se les proporcione el Software, de acuerdo con las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso tendrán que ser incluidos en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE ENTREGA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, YA SEA EXPRESA O IMPLÍCITA, INCLUYENDO, A MODO ENUNCIATIVO, CUALQUIER GARANTÍA DE COMERCIABILIDAD, IDONEIDAD PARA UN FIN PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT INCLUIDOS EN ESTE AVISO SERÁN RESPONSABLES DE NINGUNA rECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UN LITIGIO, AGRAVIO O DE OTRO MODO, RESULTANTES DE O EN CONEXION CON EL SOFTWARE, SU USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.''')

menu = Menu()
menu.presentar()

# funciones auxiliares
def is_expected_header(sentence):
	return "No. Column name       Activity     Lower bound   Upper bound" in sentence

def is_activity_one(sentence):
	return "*              1" in sentence

def is_asignation(sentence):
	if 'Objective:  s = ' in sentence:
		return True

def get_asignacion(sentence):
	m = re.search('\[c(\d+),v(\d+)\]', sentence)
	return (int(m.group(1)), int(m.group(2)))

def fila_valida(fila, n):
	fila_procesada = []
	for elem in fila:
		fila_procesada.append(int(elem))
	valido = len(fila) == n
	for i in range(1,n + 1):
		valido = valido and i in fila_procesada
		if not valido:
			break
	return valido

def get_maximum(line):
	m = re.search('= (\d+) \(', line)
	return int(m.group(1))

while True:
	menu.principal()
	comando = input('> ')
	print()
	if comando == 'M':
		menu.metodologia()
	elif comando == 'C':
		menu.colaborar()
	elif comando == 'L':
		menu.licencia()
	elif comando == 'S':
		break
	elif comando == 'I':
		menu.instrucciones()
	elif comando == 'A':
		print("Realizando la asignacion")
		#read csv
		preferencias_file = open('IngresoPreferenciasVivienda.csv', 'r')
		separador = max(map((lambda x : (preferencias_file.read().count(x), x)), ['.', ',', ';', "\t"]))[1]
		preferencias_file.close
		preferencias_file = open('IngresoPreferenciasVivienda.csv', 'r')
		preferencias_csv = csv.reader(preferencias_file, delimiter=separador)
		preferencias_matrix = []
		for line in preferencias_csv:
			preferencias_matrix.append(line)

		
		# book = xlrd.open_workbook('IngresoPreferencias_matrixVivienda.xls')
		viviendas = preferencias_matrix[0][1:]
		familias = list(map(lambda x: x[0], preferencias_matrix))[1:]
		CANT_FINAL = len(viviendas)

		valido = len(familias) == len(viviendas)
		if not valido:
			print("La cantidad de familias debe coincidir con la cantidad de viviendas")
		else:
			N = len(familias) ** 2
			print(N)
			preferencias = []
			for i in range(1, len(familias) + 1):
				listaPreferencias = preferencias_matrix[i][1:]
				familia = preferencias_matrix[i][0]
				valido_local = fila_valida(listaPreferencias, CANT_FINAL)
				if not valido_local:
					print("Los datos para la familia %s no son consistentes" % familia)
					valido = False
				else:
					preferenciasProcesadas = []
					for elem in listaPreferencias:
						preferenciasProcesadas.append(int(elem))
					preferencias.append(('c' + str(i-1), preferenciasProcesadas))

			print("PREFERENCIAS")		
			print(preferencias)		
			print('Termino de leer')
			if not valido:
				print("No se puede continuar porque hay datos inconsistentes. Por favor revise el archivo antes de continuar")
			else:
				file = open("MTAV_pref.dat",'w')   # Trying to create a new file or open one
				file.write('data;\n\n')
				numeroFamilias = 0
				familiasIN = ''
				viviendasIN = ''
				for preferencia in preferencias:
					familiasIN = familiasIN + ' ' + preferencia[0]
					viviendasIN = viviendasIN + ' v' + str(numeroFamilias)
					numeroFamilias += 1
				file.write('set C :=%s;\n\n' % familiasIN)
				file.write('set V :=%s;\n\n' % viviendasIN)
				file.write('param p :%s :=' %viviendasIN)
				for preferencia in preferencias:
					string_pref_array = map(str,preferencia[1])
					string_pref = ' '.join(string_pref_array)
					file.write("\n      %s %s" % (preferencia[0], string_pref))

				file.write(';\n\nend;')

				file.close()
				#call terminal
				os.system('ls')
				os.system("glpsol --model MTAV.mod --data MTAV_pref.dat --output MTAV_inter.sol")
				#wait until the file is ready
				time.sleep(2)

				# read objective
				objective = 0
				file = open("MTAV_inter.sol",'r')
				lines = file.read().split('\n')
				raw_asignaciones = []
				for line in lines:
					if is_asignation(line):
						objective = get_maximum(line)
						break
				print(objective)

				file = open("MTAV_pref_empate.dat",'w')   # Trying to create a new file or open one
				file.write('data;\n\n')
				numeroFamilias = 0
				familiasIN = ''
				viviendasIN = ''
				for preferencia in preferencias:
					familiasIN = familiasIN + ' ' + preferencia[0]
					viviendasIN = viviendasIN + ' v' + str(numeroFamilias)
					numeroFamilias += 1
				file.write('set C :=%s;\n\n' % familiasIN)
				file.write('set V :=%s;\n\n' % viviendasIN)
				file.write('param N := %d;\n\n' % CANT_FINAL)
				file.write('param S := %s;\n\n' % objective)

				file.write('param p :%s :=' %viviendasIN)
				for preferencia in preferencias:
					string_pref_array = map(str,preferencia[1])
					string_pref = ' '.join(string_pref_array)
					file.write("\n      %s %s" % (preferencia[0], string_pref))

				file.write(';\n\nend;')

				file.close()
				'''
				except:
			    	print('No se pudo crear el archivo')
			    	sys.exit(0) # quit Python
				'''
				#call terminal
				os.system('ls')
				os.system("glpsol --model MTAV_empate.mod --data MTAV_pref_empate.dat --output MTAV_asign.sol")
				#wait until the file is ready
				time.sleep(2)

				os.system("clear")
				#parse file and output asignation
				file = open("MTAV_asign.sol",'r')
				lines = file.read().split('\n')
				raw_asignaciones = []
				for i in range(0, len(lines) + 1):
					if is_expected_header(lines[i]):
						for j in range(i + 2, i + 4 + N):
							if is_activity_one(lines[j]):
								raw_asignaciones.append(get_asignacion(lines[j]))
						break
				f = open('asignaciones_finales.txt','w')
				f.write("Asignaciones finales\n\nFamilias : vivienda asignada\n---------------------------------\n")
				for raw_asignacion in raw_asignaciones:
					f.write('%s : %s\n' % (familias[raw_asignacion[0]], viviendas[raw_asignacion[1]]))
				f.write('\n')

				f.close()	

				print("Se hizo la asignacion. Revise el archivo asignaciones.txt")

	else:
		print('''Comando no reconocido. Por favor intente nuevamente.

''')


