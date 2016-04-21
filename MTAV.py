#!/usr/bin/env python3

import os
import sys
import time
import re
import csv 

class Menu:
	def presentar(self):
		presentacion = '''
Aplicación de programación matemática para distribución de viviendas 
en una cooperativa de ayuda mutua optimizando la satisfacción de los interesados 
(version 0.2)

----------------------------------------------------------------------
Estudiantes:
 - Ezequiel Sánchez (eze91@outlook.com)
 - Martín Prino (marpri3210@gmail.com)

Profesor Responsable:
 -Hector Cancela'''
		print(presentacion)

	def principal(self):
		principal = '''----------------------------------------------------------------------
Menu - Ingrese las letras del comando a ejecutar:
- (I)nstrucciones : pasos a seguir para realizar la asignación.
- (A)signar : ¿todo listo? Realiza la asignación final.
- (M)etodología : metodología utilizada para la asignación.
- (C)olaborar : ¿como puedo colaborar con el proyecto?
- (L)icencia : información sobre licencia del programa. 
- (S)alir

[I|A|M|C|L|S]:'''
		print(principal)

	def instrucciones(self):
		print(' >> Instrucciones se encuentra en documentacion/instrucciones.txt')


		os.system("open documentacion/instrucciones.txt")

	def metodologia(self):
		print(' >> Explicacion sobre metodologia utilizada en documentacion/metodologia.txt')


		os.system("open documentacion/metodologia.txt")

	def colaborar(self):
		print(' >> Explicación sobre como colaborar en documentacion/colaborar.txt')


		os.system("open documentacion/colaborar.txt")

	def licencia(self):
		print(' >> Detalles sobre la licencia en documentacion/licencia.txt')


		os.system("open documentacion/licencia.txt")

menu = Menu()
menu.presentar()

# funciones auxiliares
def is_expected_header(sentence):
	return "No. Column name       Activity     Lower bound   Upper bound" in sentence

def is_activity_one(sentence):
	return "*              1" in sentence

def is_asignation(sentence):
	if 'Objective:  s = ' in sentence or 'Objective:  resultado = ' in sentence:
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
		print("-------------------------------------------------------------")
		print("Comenzando con la asignacion.\n")
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
			print("(ERROR) - La cantidad de familias debe coincidir con la cantidad de viviendas")
		else:
			N = len(familias) ** 2
			preferencias = []
			for i in range(1, len(familias) + 1):
				listaPreferencias = preferencias_matrix[i][1:]
				familia = preferencias_matrix[i][0]
				valido_local = fila_valida(listaPreferencias, CANT_FINAL)
				if not valido_local:
					print("(ERROR) - Los datos para la familia %s no son consistentes." % familia)
					valido = False
				else:
					preferenciasProcesadas = []
					for elem in listaPreferencias:
						preferenciasProcesadas.append(int(elem))
					preferencias.append(('c' + str(i-1), preferenciasProcesadas))
			if not valido:
				print("\nNo se puede continuar porque hay datos inconsistentes. \nPor favor revise el archivo antes de continuar")
			else:
				file = open("utils_GLPK/datos/MTAV_pref.dat",'w') 
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
				os.system("glpsol --model utils_GLPK/modelos/MTAV.mod --data utils_GLPK/datos/MTAV_pref.dat --output utils_GLPK/soluciones/MTAV_inter.sol --log utils_GLPK/logs/ejecucion_primaria.log")
				#wait until the file is ready
				time.sleep(1)

				# read objective
				objective = 0
				file = open("utils_GLPK/soluciones/MTAV_inter.sol",'r')
				lines = file.read().split('\n')
				raw_asignaciones = []
				for line in lines:
					if is_asignation(line):
						objective = get_maximum(line)
						break

				file = open("utils_GLPK/datos/MTAV_pref_empate.dat",'w')   # Trying to create a new file or open one
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
				#call terminal
				os.system("glpsol --model utils_GLPK/modelos/MTAV_empate.mod --data utils_GLPK/datos/MTAV_pref_empate.dat --output utils_GLPK/soluciones/MTAV_asign.sol --log utils_GLPK/logs/ejecucion_secundaria.log")
				#wait until the file is ready
				time.sleep(1)

				os.system("clear")
				#parse file and output asignation
				file = open("utils_GLPK/soluciones/MTAV_asign.sol",'r')
				lines = file.read().split('\n')
				raw_asignaciones = []
				for i in range(0, len(lines) + 1):
					if is_expected_header(lines[i]):
						for j in range(i + 2, i + 4 + N):
							if is_activity_one(lines[j]):
								raw_asignaciones.append(get_asignacion(lines[j]))
						break
				file.close()
				minima = 0
				file = open("utils_GLPK/soluciones/MTAV_asign.sol",'r')
				for line in lines:
					if is_asignation(line):
						minima = get_maximum(line)
						break
				file.close()

				f = open('asignaciones_finales.txt','w')
				f.write("Asignaciones finales\n\nFamilias : vivienda asignada\n---------------------------------\n")
				for raw_asignacion in raw_asignaciones:
					f.write('%s : %s\n' % (familias[raw_asignacion[0]], viviendas[raw_asignacion[1]]))
				f.write('\n')
				f.write("Satisfacción\n---------------------------------\n")
				f.write('Global : %d\n' % objective)
				f.write('Promedio : %f\n' % (float(objective)/CANT_FINAL))
				f.write('Mínima : %d\n' % minima)
				f.close()	

				print("\nSE COMPLETÓ LA ASIGNACION.\nPor favor revise el archivo asignaciones_finales.txt\n")
				os.system("open asignaciones_finales.txt")

	else:
		print('''Comando no reconocido. Por favor intente nuevamente.''')


