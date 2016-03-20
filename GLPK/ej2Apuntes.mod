set TipoInversiones;

set Periodos;

set Periodos2;

set Escenarios;

param b;

param G;

param q;

param r;

param probabilidad;

/* param retornos{i in TipoInversiones, e in Escenarios}; */
/* retorno del tipo de inversión i para cada escenario s */

/* param probabilidad{s in Escenarios}; */
/* probabilidad para cada escenario s */

/***************************/

param ind{t in Periodos, s2 in Escenarios, s1 in Escenarios};

/* Los condicionales sobre las sumatorias de cada restricción
se pueden implementar con un parámetro indicatriz (binario),
por ejemplo "param ind{T,S,S}", donde el primer
indice en S se utiliza en las sumatorias y el segundo es el
recorrido de las restricciones.
Los valores de dicho parámetro se usan como un coeficiente binario
que al multiplicar las expresiones seleccionan, para el recoorido
de todos sus índices, {T,S,S}, aquellas que se suman. */

param E{i in TipoInversiones, t in Periodos, s1 in Escenarios};

/**************************/

/* var E{i in TipoInversiones, t in Periodos, s1 in Escenarios} >= 0, integer; */ /* no se si tiene que ser entero */
/* retorno para el tipo de inversión i en el período p y el escenario s */

var x{i in TipoInversiones, t in Periodos, s1 in Escenarios} >= 0, integer;
/* inversión para el tipo de inversión i en el período t y el escenario s */

var w{s1 in Escenarios} >= 0, integer;
/* déficit para el escenario s */

var y{s1 in Escenarios} >= 0, integer;
/* superávit para el escenario s */

/**************************/

maximize resultado: sum{s1 in Escenarios} probabilidad * (-r * w[s1] + q * y[s1]);
/* función objetivo */

/**************************/

s.t. inicial{s1 in Escenarios}: (sum{i in TipoInversiones} x[i,1,s1]) = b;
/* Inicialmente sólo se puede invertir b */ 

s.t. capital{s1 in Escenarios, t in Periodos2}: ( (sum{i in TipoInversiones} -E[i,t-1,s1] * x[i,t-1,s1]) + (sum{i in TipoInversiones} x[i,t,s1]) ) = 0;
/* Para cada período invierto lo que dispongo, que depende de los retornos e inversiones previas */

s.t. ganancia{s1 in Escenarios}: (sum{i in TipoInversiones} E[i,3,s1] * x[i,3,s1] + w[s1] - y[s1]) = G;
/* Garantizo la ganancia G */ 

s.t. no_anticipatividad{i in TipoInversiones, t in Periodos, s1 in Escenarios}: ( sum{s2 in Escenarios} ind[t,s2,s1] * x[i,t,s2] ) = ( ( sum{s2 in Escenarios} ind[t,s2,s1] ) * x[i,t,s1] );
/* Control de vínculos entre los escenarios */
