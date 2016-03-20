set C;
/* cooperativistas */

set V;
/* viviendas */

param N;
/* cantidad de cooperativistas y viviendas */

param S;
/* satisfacción */

param p{c in C, v in V};
/* prioridades de los cooperativistas por las viviendas */

var x{c in C, v in V}, binary;
/* indica si el cooperativista c es asignado a la vivienda v */

var z, integer;
/* variable auxiliar para representar la mínima satisfacción */

/* minimize d: sum{c in C, v in V} (abs(S/N - (N - p[c,v]))) * x[c,v]; */
maximize resultado: z;
/* dispersión entre la satisfacción promedio y la individual*/

s.t. z_menorIgual{c in C}: z <= sum{v in V} (N - p[c,v]) * x[c,v];
/* busco que z sea menor o igual que la satisfacción de cada cooperativista c */

s.t. unicaAsignacionCoperativista_mayorIgual{c in C}: sum{v in V} x[c,v] >= 1;
s.t. unicaAsignacionCoperativista_menorIgual{c in C}: sum{v in V} x[c,v] <= 1;
/* el cooperativista c solo tiene una vivienda asignada */

s.t. unicaAsignacionCasa_mayorIgual{v in V}: sum{c in C} x[c,v] >= 1;
s.t. unicaAsignacionCasa_menorIgual{v in V}: sum{c in C} x[c,v] <= 1;
/* la vivienda v solo tiene un cooperativista asignado */

s.t. s_mayorIgual: sum{c in C, v in V} (N - p[c,v]) * x[c,v] >= S;
s.t. s_menorIgual: sum{c in C, v in V} (N - p[c,v]) * x[c,v] <= S;
/* nivel de satisfacción */
