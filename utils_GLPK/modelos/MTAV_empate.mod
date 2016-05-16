set C;
/* cooperativistas */

set V;
/* viviendas */

param S;
/* satisfacción */

param p{c in C, v in V};
/* prioridades de los cooperativistas por las viviendas */

var x{c in C, v in V}, binary;
/* indica si el cooperativista c es asignado a la vivienda v */

minimize s: sum{c in C, v in V} p[c,v] * x[c,v];
/* preferencias acumuladas */

s.t. unicaAsignacionCoperativista_mayorIgual{c in C}: sum{v in V} x[c,v] >= 1;
s.t. unicaAsignacionCoperativista_menorIgual{c in C}: sum{v in V} x[c,v] <= 1;
/* el cooperativista c solo tiene una vivienda asignada */

s.t. unicaAsignacionCasa_mayorIgual{v in V}: sum{c in C} x[c,v] >= 1;
s.t. unicaAsignacionCasa_menorIgual{v in V}: sum{c in C} x[c,v] <= 1;
/* la vivienda v solo tiene un cooperativista asignado */

s.t. z_menorIgual{c in C}: sum{v in V} p[c,v] * x[c,v] <= S;
/* nivel de satisfacción */