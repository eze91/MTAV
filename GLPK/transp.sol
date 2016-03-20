Problem:    transp
Rows:       6
Columns:    6 (6 integer, 0 binary)
Non-zeros:  18
Status:     INTEGER OPTIMAL
Objective:  cost = 153.675 (MINimum)

   No.   Row name        Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 cost                  153.675                             
     2 supply[Seattle]
                                 350                         350 
     3 supply[San-Diego]
                                 550                         600 
     4 demand[New-York]
                                 325           325               
     5 demand[Chicago]
                                 300           300               
     6 demand[Topeka]
                                 275           275               

   No. Column name       Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 x[Seattle,New-York]
                    *             50             0               
     2 x[Seattle,Chicago]
                    *            300             0               
     3 x[Seattle,Topeka]
                    *              0             0               
     4 x[San-Diego,New-York]
                    *            275             0               
     5 x[San-Diego,Chicago]
                    *              0             0               
     6 x[San-Diego,Topeka]
                    *            275             0               

Integer feasibility conditions:

KKT.PE: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

KKT.PB: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

End of output
