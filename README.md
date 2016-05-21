# MTAV
Sistema de maximizacion del beneficio en la asignación de viviendas.

##Instalación.

Antes de ejecutar el programa asegurase de tener instalado:
* Python 3  (>= 3.5)
* GLPK      (>= 4.5)

Instale Python3 (https://www.python.org/downloads/). Se testeo con Python 3.5.1 (no es necesaria instalar ninguna biblioteca de python adicional).

Instale GLPK (https://en.wikibooks.org/wiki/GLPK) y cheque que este instalado correctamente ejecutando.
```
$ glpsol --version
```
El programa esta testeado con la versión 4.52.

Luego de instaladas estas dependencias ejecute el programa posicionado en la carpeta MTAV de la siguiente forma:
```
$ python3 MTAV.py
```
Por mas información recurra a la carpeta 'documentacion'.

## Instrucciones:

### Preparación del archivo

El programa espera una tabla con los identificadores de las viviendas en la primera columna y con las familias en la primera fila. En la fila de cada familia se listan las preferencias de las familias por las viviendas. Estas preferencias se representan en forma numérica siendo el numero (natural) la preferencia por la vivienda.

El formato de entrada al programa es un archivo en formato CSV (Coma Separated Values), un formato estándar y soportado para exportar e importar por programas populares de planillas electrónicas como Microsoft Excel, OpenCalc y Google Sheets. El separador no necesariamente debe ser una coma, pudiendo también ser '.', ',', ';' o tabulador.

Lo puede crear en su editor de planillas electrónicas de su preferencia y exportarlo en formato CSV con el nombre 'preferencias.csv' guardandolo en la misma carpeta del programa (llamada MTAV)

Ejemplo en editor de planilla de cálculo:

|                   | 101 | 102 | 201 | 202 |
| ----------------- | --- | ----| --- | --- |
|Sanchez            |  4  |  3  |  1  |  2  |
|Pino               |  2  |  4  |  1  |  3  |
|Cancela            |  4  |  2  |  1  |  3  |
|Rodriquez Da´Silva |  3  |  1  |  4  |  2  |


El siguiente ejemplo representa que la vivienda 201 es la preferida por la familia Sanchez, la 202 es la segunda y así sucesivamente (siendo la 101 la menos deseada por la familia Sanchez). Es de forma análoga para el resto de las familias.

Los cuidados que se deben tomar (y que serán chequeados por el programa avisando en caso de algún tipo de anomalía) son:

- La cantidad de familias debe ser igual a la cantidad de viviendas (cantidad de filas igual a la cantidad de columnas).
- Las preferencias deben ser una permutación de naturales de [1, 2, ..., CANTIDAD_VIVIENDAS] (sin repetidos ni salteados)

ATENCIÓN: para evitar complicaciones con el formato del texto evite caracteres especiales no estándares del ingles (como la letra Ñ, tilde, etc.).

La tabla anterior exportada a CSV:
```
                   ,  101 , 102 , 201 , 202
Sanchez            ,  1  ,  3  ,  4  ,  2 
Pino               ,  2  ,  4  ,  1  ,  3 
Cancela            ,  4  ,  2  ,  1  ,  3 
Rodriquez Da´Silva ,  3  ,  1  ,  4  ,  2 
```

Se cuenta con un ejemplo de entrada ('preferencias_EJEMPLO.csv') para tomar como referencia.


### Ejecutar comando Asignar

Luego de creado el archivo como se detalla en el punto 1 y cuando crea que el archivo de preferencias es correcto, seleccione el comando (A)signar. 

Si se encuentra alguna inconsistencia con los datos (como se detalla en el punto anterior), se le notificará sobre ello. Corrija el archivo (preferencias.csv) en caso de ser necesario. Si no existe ningún error el programa terminará de realizar la asignación en breves segundos, mostrándose el progreso en pantalla (lo que es desplegado en pantalla se guardará en la carpeta ‘logs’).


### Asignación final

Cuando el programa termine de ejecutar, se abriría automáticamente el archivo que contiene las asignaciones finales. Puede encontrarlo en MTAV/asignaciones_finales.txt.

ATENCIÓN: al ejecutar nuevamente el programa este archivo se sobre escribirá. Cámbiele el nombre si desea conservarlo.

## Metodología

La metodología aplicada (en dos pasos secuenciales) es la siguiente:
* Como primer paso se busca minimizar la insatisfacción de cada uno de los cooperativistas, es decir, se busca una de las asignaciones en la que la peor asignación sea la mejor posible.
* Tomando como cota superior el nivel de insatisfacción que se obtiene de la solución dada por el modelo anterior, se busca la asignación que maximice la satisfacción global respetando esa cota.

## Colaboración

Si quiere colaborar lo alentamos a que lo haga.

El repositorio central se encuentra en: https://github.com/eze91/MTAV

Puede:
 * señalar issues
 * corregir issues
 * depurar el código
 * sugerir nuevas funcionalidades
 * agregar nuevas funcionalidades
 * cualquier cosa para mejorar el programa y dejar contentos a los cooperativistas

Para colaborar como desarrollador realice un Pull Request que lo mercaremos a la brevedad luego de probarlo.


## Licencia

Por la presente se autoriza, de forma gratuita, a cualquier persona que haya obtenido una copia de este software y archivos de documentación asociados (el "Software"), a utilizar el Software sin restricción, incluyendo sin limitación los derechos de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender copias de este Software, y permitir lo mismo a las personas a las que se les proporcione el Software, de acuerdo con las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso tendrán que ser incluidos en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE ENTREGA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, YA SEA EXPRESA O IMPLÍCITA, INCLUYENDO, A MODO ENUNCIATIVO, CUALQUIER GARANTÍA DE COMERCIABILIDAD, IDONEIDAD PARA UN FIN PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT INCLUIDOS EN ESTE AVISO SERÁN RESPONSABLES DE NINGUNA rECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UN LITIGIO, AGRAVIO O DE OTRO MODO, RESULTANTES DE O EN CONEXION CON EL SOFTWARE, SU USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.''')