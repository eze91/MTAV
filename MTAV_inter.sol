Problem:    MTAV
Rows:       13
Columns:    9 (9 integer, 9 binary)
Non-zeros:  45
Status:     INTEGER OPTIMAL
Objective:  s = 5 (MINimum)

   No.   Row name        Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 s                           5                             
     2 unicaAsignacionCoperativista_mayorIgual[c0]
                                   1             1               
     3 unicaAsignacionCoperativista_mayorIgual[c1]
                                   1             1               
     4 unicaAsignacionCoperativista_mayorIgual[c2]
                                   1             1               
     5 unicaAsignacionCoperativista_menorIgual[c0]
                                   1                           1 
     6 unicaAsignacionCoperativista_menorIgual[c1]
                                   1                           1 
     7 unicaAsignacionCoperativista_menorIgual[c2]
                                   1                           1 
     8 unicaAsignacionCasa_mayorIgual[v0]
                                   1             1               
     9 unicaAsignacionCasa_mayorIgual[v1]
                                   1             1               
    10 unicaAsignacionCasa_mayorIgual[v2]
                                   1             1               
    11 unicaAsignacionCasa_menorIgual[v0]
                                   1                           1 
    12 unicaAsignacionCasa_menorIgual[v1]
                                   1                           1 
    13 unicaAsignacionCasa_menorIgual[v2]
                                   1                           1 

   No. Column name       Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 x[c0,v0]     *              1             0             1 
     2 x[c0,v1]     *              0             0             1 
     3 x[c0,v2]     *              0             0             1 
     4 x[c1,v0]     *              0             0             1 
     5 x[c1,v1]     *              1             0             1 
     6 x[c1,v2]     *              0             0             1 
     7 x[c2,v0]     *              0             0             1 
     8 x[c2,v1]     *              0             0             1 
     9 x[c2,v2]     *              1             0             1 

Integer feasibility conditions:

KKT.PE: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

KKT.PB: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

End of output
