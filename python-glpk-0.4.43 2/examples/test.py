from glpk import *

def problem0():
    print "\n>>problem 0:\n"    
    problem = glpk("models/samp1.mps")
    problem.solve()
    
    print problem.solution()
    problem = glpk("models/plan.lp")
    problem.solve()
    print problem.solution()

def problem1():
    print "\n>>problem 1:\n"
    problem = glpk("models/net3.mod","models/net3.dat")
    problem.solve()
    sol1 = problem.solution()
    
    problem.pd_cap['NE'] = 10000
    problem.dw_cap['NE', 'BOS'] = 50
    problem.p_supply = 450
    problem.update()
    problem.solve()
    sol2 = problem.solution()
    
    print "solution1:", sol1
    print "solution2:", sol2

def problem2():
    print "\n>>problem 2:\n"
    problem = glpk("models/multi.mod","models/multi.dat")
    problem.update()
    problem.solve()
    print problem.supply['GARY','bands']
    print "solution:", problem.solution()

def problem3():
    print "\n>>problem 3:\n"
    problem = glpk("models/steel.mod","models/steel.dat")
    problem.update()
    problem.solve()
    print "solution:", problem.solution()
    print "problem.total_profit =", problem.total_profit
    print "problem.Make =", problem.Make
    
def problem4():
    print "\n>>problem 4:\n"
    problem = glpk("models/steel.mod")
    problem.PROD = ['bands', 'coils']
    problem.rate['bands'] = 200
    problem.rate['coils'] = 140
    problem.profit['bands'] = 25
    problem.profit['coils'] = 30
    problem.market['bands'] = 6000
    problem.market['coils'] = 4000
    problem.avail = 40
    problem.update()
    problem.solve()
    print "problem.solution() =", problem.solution()
    print "problem.sets() =", problem.sets()
    print "problem.parameters() =", problem.parameters()
    print "problem.variables() =", problem.variables()
    print "problem.constraints() =", problem.constraints()
    print "problem.objectives() =", problem.objectives()
    print "problem.Make =", problem.Make
    print "problem.Make['bands'] =", problem.Make['bands']
    print "problem.Make['bands'].value() =", problem.Make['bands'].value()    
    print "problem.total_profit =", problem.total_profit
    print "problem.total_profit.value() =", problem.total_profit.value()
    problem.Make >= 10
    problem.Make['coils'] <= 100
    0 <= problem.total_profit <= 100000

    problem.Make <= 15
    problem.Make['bands'] <= 10
    print problem.Make['bands']._bounds()
    #problem.Time <= 10
    
    
    print "problem.total_profit =", problem.total_profit    
    problem.solve()
    #print "problem.Make.bounds() =", problem.Make._bounds()
    #print "problem.Make['coils'].bounds() =", problem.Make['coils']._bounds()
    #print "problem.Make['bands'].bounds() =", problem.Make['bands']._bounds()       
    print "problem.solution() =", problem.solution()

if __name__ == "__main__":
    problem0()
    problem1()
    problem2()
    problem3()
    problem4()

