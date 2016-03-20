import os
import sys
import time
import re
import xlrd

print('''Aplicación de Programación Matemática 
para distribución de viviendas en una cooperativa de ayuda mutua 
optimizando la satisfacción de los interesados (version 0.1)
----------------------------------------------------------------
Estudiantes:
Ezequiel Sánchez (eze91@outlook.com)
Martín Prino (marpri3210@gmail.com)
Profesor Responsable:
Hector Cancela
----------------------------------------------------------------
''')

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
		fila_procesada.append(int(elem.value))
	valido = len(fila) == n
	for i in range(1,n + 1):
		valido = valido and i in fila_procesada
		if not valido:
			break
	return valido

comando = input('''Ingrese el comando que desee ejecutar
- asignar: asignar las viviendas
- ayuda: informacion general
''')

if comando == 'ayuda':
	print("Texto de Ayuda")
else:
	print("Realizando la asignacion")
	#read excel
	book = xlrd.open_workbook('IngresoPreferenciasVivienda.xls')
	first_sheet = book.sheet_by_index(0)

	familias = first_sheet.col(0)
	familias.pop(0)
	viviendas = first_sheet.row(0)
	viviendas.pop(0)
	CANT_FINAL = len(viviendas)
	valido = len(familias) == len(viviendas)
	if not valido:
		print("La cantidad de familias debe coincidir con la cantidad de viviendas")
	else:
		N = len(familias) ** 2
		print(N)
		preferencias = []
		for i in range(1, len(familias) + 1):
			listaPreferencias = first_sheet.row(i)
			familia = listaPreferencias.pop(0)
			valido_local = fila_valida(listaPreferencias, CANT_FINAL)
			if not valido_local:
				print("Los datos para la familia %s no son consistentes" % familia)
				valido = False
			else:
				preferenciasProcesadas = []
				for elem in listaPreferencias:
					preferenciasProcesadas.append(int(elem.value))
				preferencias.append(('c' + str(i-1), preferenciasProcesadas))

		print("PREFERENCIAS")		
		print(preferencias)		
		print('Termino de leer')
		# OLD : preferencias = [("Rodriguez",[1,2,3]), ("Sanchez",[2,3,1]), ("Garcia",[3,1,2])] for test purpose
		#preferencias = [(0,[1,2,3]), (1,[2,3,1]), (2,[3,1,2])] for test purpose
		#create file
		#try:
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
			'''
			except:
		    	print('No se pudo crear el archivo')
		    	sys.exit(0) # quit Python
			'''
			#call terminal
			os.system('ls')
			os.system("glpsol --model MTAV.mod --data MTAV_pref.dat --output MTAV_asign.sol --log tsp.log")
			#wait until the file is ready
			time.sleep(2)
			file = open("MTAV_asign.sol",'r')
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


			print(raw_asignaciones)
			print(familias)
			print(viviendas)
			os.system("clear")
			print(file.read())
			f = open('asignaciones_finales.txt','w')
			f.write("Asignaciones finales\n\nFamilias : vivienda asignada\n---------------------------------\n")
			for raw_asignacion in raw_asignaciones:
				f.write('%s : %s\n' % (familias[raw_asignacion[0]].value, viviendas[raw_asignacion[1]].value))
			f.write('\n')

			f.close()	

			print("Se hizo la asignacion. Revise el archivo asignaciones.txt")



	






