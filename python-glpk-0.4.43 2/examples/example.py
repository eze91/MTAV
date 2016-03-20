import glpk

print "starting..."
example = glpk.glpk("example.mod")
example.update()
example.solve()
print "solution:", example.solution()
print "solution is also here: x =", example.x, "y =", example.y

