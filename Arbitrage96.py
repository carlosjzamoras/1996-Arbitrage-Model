from gurobipy import *

#------------------Defining the model---------------------------

# Initialization. The name is arbitrary
model = Model('Arbitrage96')

# Adding new variables
DY = model.addVar(vtype=GRB.CONTINUOUS, name='Dollar to Yen')
DM = model.addVar(vtype=GRB.CONTINUOUS, name='Dollar to Mark')
DF = model.addVar(vtype=GRB.CONTINUOUS, name='Dollar to Franc')
YD = model.addVar(vtype=GRB.CONTINUOUS, name='Yen to Dollar')
YM = model.addVar(vtype=GRB.CONTINUOUS, name='Yen to Mark')
YF = model.addVar(vtype=GRB.CONTINUOUS, name='Yen to Franc')
MD = model.addVar(vtype=GRB.CONTINUOUS, name='Mark to Dollar')
MY = model.addVar(vtype=GRB.CONTINUOUS, name='Mark to Yen')
MF = model.addVar(vtype=GRB.CONTINUOUS, name='Mark to Franc')
FD = model.addVar(vtype=GRB.CONTINUOUS, name='Franc to Dollar')
FY = model.addVar(vtype=GRB.CONTINUOUS, name='Franc to Yen')
FM = model.addVar(vtype=GRB.CONTINUOUS, name='Franc to Mark')

model.update()

model.addConstr(111.52 * DY + 73.964 * MY + 21.933 * FY - YD - YM - YF == 0, name='Yen balance')
model.addConstr(1.4987 * DM + .013493 * YM + .29507 * FM - MD - MY - MF == 0, name='Mark balance')
model.addConstr(5.0852 * DF + .045593 * YF + 3.2823 * MF - FD - FY - FM == 0, name='Franc balance')
model.addConstr(DY + DM + DF == 1, name='Dollar flow out')
model.addConstrs((var >= 0 for var in model.getVars()), name='Flows non-negative')
#model.addConstrs((var <= 1000 for var in model.getVars()), name='Flows non-negative')


model.setObjective(.008966* YD + .6659 * MD + .1966 * FD, GRB.MAXIMIZE)
model.write('Arbitrage96.lp')

model.optimize()

model.printAttr('X')
[DY_sol, DM_sol, DF_sol, YD_sol, YM_sol, YF_sol, MD_sol, MY_sol, MF_sol, FD_sol, FY_sol, FM_sol] = model.getAttr("X", [DY, DM, DF, YD, YM, YF, MD, MY, MF, FD, FY, FM])
optimal_objective = model.getObjective().getValue()

print('\nOut custom output:\n')
print("Maximum inflow is", optimal_objective, "dollars")

print("Convert {}  {}!".format(DY_sol, DY.varName))
print("Convert {}  {}!".format(DM_sol, DM.varName))
print("Convert {}  {}!".format(DF_sol, DF.varName))
print("Convert {}  {}!".format(YD_sol, YD.varName))
print("Convert {}  {}!".format(YM_sol, YM.varName))
print("Convert {}  {}!".format(YF_sol, YF.varName))
print("Convert {}  {}!".format(MD_sol, MD.varName))
print("Convert {}  {}!".format(MY_sol, MY.varName))
print("Convert {}  {}!".format(MF_sol, MF.varName))
print("Convert {}  {}!".format(FD_sol, FD.varName))
print("Convert {}  {}!".format(FY_sol, FY.varName))
print("Convert {}  {}!".format(FM_sol, FM.varName))
