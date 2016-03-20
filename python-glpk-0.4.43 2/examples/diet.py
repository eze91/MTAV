from glpk import *

# create an LP as an instance of class "glpk",
# based on the model "diet.mod" (coming in glpk's "examples")
problem = glpk("models/diet.mod")

# solve
problem.solve()
print "\n\nsolution:", problem.solution()

# define/modify problem data:
# "F" and "a" are, respectively, a "set" and a "param" in "diet.mod";
# now, they can be accessed in Python as members of the "glpk" instance
problem.F += ['Bacalhau']	# add a new food
problem.a['Bacalhau','Calorie']    = 87.3	# nutrients
problem.a['Bacalhau','Protein']	   = 98.7
problem.a['Bacalhau','Calcium']	   = 17.3
problem.a['Bacalhau','Iron']	   = 12.3
problem.a['Bacalhau','Vitamin-A']  = 12.3	

# update and solve
problem.update()
problem.solve()
print "\n\nsolution:", problem.solution()

# one more update
problem.F.remove('Bacalhau')	# remove food
for key in problem.a.keys():
    if 'Bacalhau' in key:
        del problem.a[key]

# update and solve
problem.update()
problem.solve()
print "\n\nsolution:", problem.solution()
