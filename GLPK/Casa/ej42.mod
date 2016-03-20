set Productos;

set Insumos;

set Escenarios;

param costo{p in Productos};
/* costo de producir el producto p */

param venta{p in Productos};
/* precio de venta del producto p */

param requerimientos{i in Insumos, p in Productos};
/* requerimientos de insumos para cada producto */

param demanda{p in Productos};
/* demanda de los productos para cada escenario */

param probabilidad{e in Escenarios};
/* probabilidad para cada escenario */

var x_p{p in Productos} >= 0, integer;
/* cantidad que produzco del producto p */

var x_c{i in Insumos} >= 0, integer;
/* cantidad de insumos i que compro */

var y_p{p in Productos} >= 0, integer;
/* cantidad que vendo del producto p por escenario e*/

maximize beneficio_total: sum{p in Productos} (venta[p] * y_p[p] - costo[p] * x_p[p]);  
/* beneficio total */

s.t. suministro{i in Insumos}: (sum{p in Productos} (x_p[p] * requerimientos[i,p])) <= x_c[i]; 
/* restringe suministro del insumo i */

s.t. mercado{p in Productos}: x_p[p] = demanda[p]; 
/* satisface demanda del mercado en cada escenario */