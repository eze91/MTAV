Problem:    MTAV_empate
Rows:       18
Columns:    10 (10 integer, 9 binary)
Non-zeros:  67
Status:     INTEGER OPTIMAL
Objective:  resultado = 2 (MINimum)

   No.   Row name        Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 resultado                   2                             
     2 z_menorIgual[c0]
                                   0            -0               
     3 z_menorIgual[c1]
                                   1            -0               
     4 z_menorIgual[c2]
                                   0            -0               
     5 unicaAsignacionCoperativista_mayorIgual[c0]
                                   1             1               
     6 unicaAsignacionCoperativista_mayorIgual[c1]
                                   1             1               
     7 unicaAsignacionCoperativista_mayorIgual[c2]
                                   1             1               
     8 unicaAsignacionCoperativista_menorIgual[c0]
                                   1                           1 
     9 unicaAsignacionCoperativista_menorIgual[c1]
                                   1                           1 
    10 unicaAsignacionCoperativista_menorIgual[c2]
                                   1                           1 
    11 unicaAsignacionCasa_mayorIgual[v0]
                                   1             1               
    12 unicaAsignacionCasa_mayorIgual[v1]
                                   1             1               
    13 unicaAsignacionCasa_mayorIgual[v2]
                                   1             1               
    14 unicaAsignacionCasa_menorIgual[v0]
                                   1                           1 
    15 unicaAsignacionCasa_menorIgual[v1]
                                   1                           1 
    16 unicaAsignacionCasa_menorIgual[v2]
                                   1                           1 
    17 s_mayorIgual                5             5               
    18 s_menorIgual                5                           5 

   No. Column name       Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 x[c0,v0]     *              0             0             1 
     2 x[c0,v1]     *              1             0             1 
     3 x[c0,v2]     *              0             0             1 
     4 x[c1,v0]     *              1             0             1 
     5 x[c1,v1]     *              0             0             1 
     6 x[c1,v2]     *              0             0             1 
     7 x[c2,v0]     *              0             0             1 
     8 x[c2,v1]     *              0             0             1 
     9 x[c2,v2]     *              1             0             1 
    10 z            *              2                             

Integer feasibility conditions:

KKT.PE: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

KKT.PB: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

End of output
