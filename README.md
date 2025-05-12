# 1996-Arbitrage-Model

## Context
In the world's currency market there exist an exchange rate between two currencies. It is always true that if you covert currency _A_ to currency _B_ you will end up with less money that what you started with. The implication here is that the product of exchange rates between any pair of countries is less than one. 
Under very particular circumstances we can create a chain of conversions that results in a net gain. This is known as arbitrage. A simple linear programming model can be used to find the exact exchanges needed where this sitution exist. 

## Data
Consider the table of exchange rates from the Wall Street Journal on Nov 10, 1996. 

|   | USD | Yen | Mark | Franc |
| - | --- | --- | ---- | ----- |
|USD|     |111.52|1.4987|5.852|
|Yen|.008966|   |.013493|.045593|
|Mark|.6659|73.964|   |3.3823|
|Franc|.1966|21.933|.29507|   |

### Solution
We will state the solution first and describe how we reached the solution below. The conversion from USD &rarr; Yen &rarr; Mark &rarr; makes $0.002 on each initial dollar. 

## Formulating the Problem

We can make a generalized network model, where the network flow models uses the currency exchange rate as the unit of flow that leaves one node and arrives at the next node. Each currency is represented as a node.  For example, one dollar flowing out of the USD node arrives at the Yen node as 111.52 Yen.

Let x<sup>ij</sup> denote the flow from node (currency) _i_ to _j_. This flow is measured in the currency of node _i_. 

We assign USD as the home node, at all other nodes must have a  flow balance. 

### Formulation in Gurobi 
Set up each initial node, this is done by creating a _directed edge_ from one currency to the next. 

```python
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
```
We write down the flow balance constraints at the 3 non-home nodes (Franc, Yen, Mark). In addition, we set the flow out at the home node to 1. 

```python
model.addConstr(111.52 * DY + 73.964 * MY + 21.933 * FY - YD - YM - YF == 0, name='Yen balance')
model.addConstr(1.4987 * DM + .013493 * YM + .29507 * FM - MD - MY - MF == 0, name='Mark balance')
model.addConstr(5.0852 * DF + .045593 * YF + 3.2823 * MF - FD - FY - FM == 0, name='Franc balance')
model.addConstr(DY + DM + DF == 1, name='Dollar flow out')
model.addConstrs((var >= 0 for var in model.getVars()), name='Flows non-negative')
```
We set our objective function to maximize the net inflow the home node. 
```python
model.setObjective(.008966* YD + .6659 * MD + .1966 * FD, GRB.MAXIMIZE)
model.write('Arbitrage96.lp')
```
## Result
We run our model in the gurobi library. Since our formulation is of a linear program, gurobi uses the dual simplex algorithm to solve. 

```python
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
```
While there are several arbitrage opportunities , some of the opportunities do not have a bound on the flow making the problem unbounded. 

Changing the Mark to Franc conversion rate from 3.3823 to 2.2823 leaves USD &rarr; Franc &rarr; Yen &rarr; Mark &rarr; USD as the optimal arbitrage opportunity, where the maximu return on one dollar is $1.0021289.

- Convert 1.0 Dollar to Franc
- Convert 5.0852 Franc to Yen
- Convert 111.53369160000001 to Mark
- Convert 1.504924107588001 Mark to Dollar 
