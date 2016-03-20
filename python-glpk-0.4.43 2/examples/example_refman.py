from glpk.glpkpi import *
size = 1000+1
ia = intArray(size)
ja = intArray(size)
ar = doubleArray(size)
prob = glp_create_prob()

glp_set_prob_name(prob, "sample")
glp_set_obj_dir(prob, GLP_MAX)
glp_add_rows(prob, 3)
glp_set_row_name(prob, 1, "p")
glp_set_row_bnds(prob, 1, GLP_UP, 0.0, 100.0)
glp_set_row_name(prob, 2, "q")
glp_set_row_bnds(prob, 2, GLP_UP, 0.0, 600.0)
glp_set_row_name(prob, 3, "r")
glp_set_row_bnds(prob, 3, GLP_UP, 0.0, 300.0)
glp_add_cols(prob, 3)
glp_set_col_name(prob, 1, "x1")
glp_set_col_bnds(prob, 1, GLP_LO, 0.0, 0.0)
glp_set_obj_coef(prob, 1, 10.0)
glp_set_col_name(prob, 2, "x2")
glp_set_col_bnds(prob, 2, GLP_LO, 0.0, 0.0)
glp_set_obj_coef(prob, 2, 6.0)
glp_set_col_name(prob, 3, "x3")
glp_set_col_bnds(prob, 3, GLP_LO, 0.0, 0.0)
glp_set_obj_coef(prob, 3, 4.0)
ia[1] = 1; ja[1] = 1; ar[1] =  1.0	# /* a[1,1] =  1 */
ia[2] = 1; ja[2] = 2; ar[2] =  1.0	# /* a[1,2] =  1 */
ia[3] = 1; ja[3] = 3; ar[3] =  1.0	# /* a[1,3] =  1 */
ia[4] = 2; ja[4] = 1; ar[4] = 10.0	# /* a[2,1] = 10 */
ia[5] = 3; ja[5] = 1; ar[5] =  2.0	# /* a[3,1] =  2 */
ia[6] = 2; ja[6] = 2; ar[6] =  4.0	# /* a[2,2] =  4 */
ia[7] = 3; ja[7] = 2; ar[7] =  2.0	# /* a[3,2] =  2 */
ia[8] = 2; ja[8] = 3; ar[8] =  5.0	# /* a[2,3] =  5 */
ia[9] = 3; ja[9] = 3; ar[9] =  6.0	# /* a[3,3] =  6 */

glp_load_matrix(prob, 9, ia, ja, ar)
glp_simplex(prob, None)
Z = glp_get_obj_val(prob)
x1 = glp_get_col_prim(prob, 1)
x2 = glp_get_col_prim(prob, 2)
x3 = glp_get_col_prim(prob, 3)
print "\nZ = %g; x1 = %g; x2 = %g; x3 = %g\n" %(Z, x1, x2, x3)
del prob
