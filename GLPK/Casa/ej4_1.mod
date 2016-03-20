set Productos;

set Insumos;

set Escenarios;

param costo{p in Productos};
/* costo de producir el producto p */

param venta{p in Productos};
/* precio de venta del producto p */

param requerimientos{i in Insumos, p in Productos};
/* requerimientos de insumos para cada producto */

param demanda{e in Escenarios, p in Productos};
/* demanda de los productos para cada escenario */

param probabilidad{e in Escenarios};
/* probabilidad para cada escenario */

var x_p{p in Productos, e in Escenarios} >= 0, integer;
/* cantidad que produzco del producto p por escenario e*/

var x_c{i in Insumos, e in Escenarios} >= 0, integer;
/* cantidad de insumos i que compro por escenario e*/

var y_p{p in Productos, e in Escenarios} >= 0, integer;
/* cantidad que vendo del producto p por escenario e*/

minimize costo_total: sum{p in Productos, e in Escenarios} (costo[p] * x_p[p,e] - venta[p] * y_p[p,e]) * probabilidad[e]; 
/* costo total */

s.t. suministro{i in Insumos, e in Escenarios}: (sum{p in Productos} (x_p[p,e] * requerimientos[i,p])) <= x_c[i,e];
/* restringe suministro del insumo i */
