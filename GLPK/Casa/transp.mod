# Problema de Transporte
#
# Determina el envio de costo minimo que cumple
# con los requisitos de demanda de mercados y
# suministro de fabricas.
# Dantzig, G B., Linear Programming and Extensions
# Princeton University Press, Princeton, New Jersey,
# 1963,# Chapter 3-3.

set I;
/* plantas */

set J;
/* mercados */

param a{i in I};
/* capacidad de planta i en cajas */

param b{j in J};
/* demanda de mercado j en cajas */

param d{i in I, j in J};
/* distancia desde plantas a mercados en millas */

param f;
/* flete en pesos por caja por distancia */

param c{i in I, j in J} := f * d[i,j] / 1000;
/* costo del transporte en miles de pesos por caja */

var x{i in I, j in J} >= 0, integer;
/* cantidad de envio en cajas */

minimize cost: sum{i in I, j in J} c[i,j] * x[i,j];
/* costo total de transporte en miles de pesos */

s.t. supply{i in I}: sum{j in J} x[i,j] <= a[i];
/* restringe suministro en planta i */

s.t. demand{j in J}: sum{i in I} x[i,j] >= b[j];
/* satisface demanda en mercado j */
