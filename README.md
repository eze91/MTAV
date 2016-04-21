# MTAV
Sistema de maximizacion del beneficio de asignación para cooperativas de viviendas.

##Instalación.

El programa depende de la instalacion de GLPK.
* Python 3 3.5.1
* GLPK 4.52

Para poder ejecutar instale Python3 (https://www.python.org/downloads/). Se testeo con Python 3.5.1.

Antes de ejecutarlo instale el GLPK (https://en.wikibooks.org/wiki/GLPK) y cheque que este instalado correctamente ejecutando:
```
$ glpsol --version
```

El programa esta testeado con la version v4.52.

Luego de instaladas estas dependencias ejecute el programa de la siguiente forma:
```
$ python3 MTAV.py
```
Por mas informacion recurra a la carpeta 'documentacion'.

## Instrucciones:

### 1) Preparación del archivo

El programa espera una tabla con los identificadores de las viviendas en la primera columna y con las familias en la primera fila. Luego, en la fila de cada familia se listan las preferencias de las familias por las viviendas. Estas preferencias se representan en forma numérica siendo el numero (natural) la preferencia por la vivienda.

El formato de entrada al programa es un archivo en formato CSV (Coma Separated Values), un formato estandar y soportado para exportar e importar por programas populares de planillas electrónicas como Microsoft Excel, OpenCalc y Google Sheets. El separador no necesariamente debe ser como, puede ser '.', ',', ';' o tabulador.

Lo puede crear en su editor de planillas eletronica de su preferencia y exportarlo en formato CSV con el combre 'preferencias.csv' guardandolo en la misma carpeta del programa (llamada MTAV)

Ejemplo en editor de planilla de cálculo:

|                   | 101 | 102 | 201 | 202 |
| ----------------- | --- | ----| --- | --- |
|Sanchez            |  4  |  3  |  1  |  2  |
|Pino               |  2  |  4  |  1  |  3  |
|Cancela            |  4  |  2  |  1  |  3  |
|Rodriquez Da´Silva |  3  |  1  |  4  |  2  |


El siguiente ejemplo representa que la vivienda 201 es la preferida por la familia Sanchez, la 202 es la segunda y asi sucesivamente (sienda la 101 es la menos deseada por la familia Sanchez). Luego es igual para el resto de las familias.

Los cuidados que se deben tener (y que serán chequiados por el programa avisando en caso de algún tipo de anomalia) son:

- La cantidad de familais debe ser igual a la cantidad de viviendas (cantidad de filas igual a la cantidad de columnas).
- Las preferencias deben ser una permutacion de naturales de [1, 2, ..., CANTIDAD_VIVIENDAS] (sin repetidos ni salteados)

La tabla anterior exportada a CSV:
```
                   ,  101 , 102 , 201 , 202
Sanchez            ,  1  ,  3  ,  4  ,  2 
Pino               ,  2  ,  4  ,  1  ,  3 
Cancela            ,  4  ,  2  ,  1  ,  3 
Rodriquez Da´Silva ,  3  ,  1  ,  4  ,  2 
```
Se cuenta con un ejemplo de entrada ('preferencias_EJEMPLO.csv') para tomar como referencia.


### 2) Ejecutar comando Asignar

Luego de creado el archivo como se detalla en el punto 1 seleccione el comando (A)signar. Luego el programa pedirá confirmacion para empezar la asignación. Si cree que el el archivo preferencias es correcto, acepte. En breves segundos la asignación debería estar completa.

### 3) Asignación final

## Metodología

## Colaboración

## Licencia

El software disponde de licencia MIT.

Por la presente se autoriza, de forma gratuita, a cualquier persona que haya obtenido una copia de este software y archivos de documentación asociados (el "Software"), a utilizar el Software sin restricción, incluyendo sin limitación los derechos de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender copias de este Software, y permitir lo mismo a las personas a las que se les proporcione el Software, de acuerdo con las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso tendrán que ser incluidos en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE ENTREGA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, YA SEA EXPRESA O IMPLÍCITA, INCLUYENDO, A MODO ENUNCIATIVO, CUALQUIER GARANTÍA DE COMERCIABILIDAD, IDONEIDAD PARA UN FIN PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT INCLUIDOS EN ESTE AVISO SERÁN RESPONSABLES DE NINGUNA rECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UN LITIGIO, AGRAVIO O DE OTRO MODO, RESULTANTES DE O EN CONEXION CON EL SOFTWARE, SU USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.''')