# -*- coding: utf-8 -*-
"""vehicle_routing_problem_Gurobi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1R579E7SjSJKldTkqx1vDLyOozWZxY-t1
"""

from gurobipy import Model, GRB, quicksum

def solve_model(demand_override=None):
    customers = [0,1,2,3,4,5,6]
    demand = {
        0:0, 1:10, 2:15, 3:20, 4:25, 5:30, 6:35
    }
    if demand_override is not None:
        for k,v in demand_override.items():
            demand[k] = v

    vehicle_count = 4
    vehicle_capacity = 60

    # Gerçek mesafe matrisi
    distance_data = [
    [0, 8, 12, 20, 15, 30, 25],
    [8, 0, 5, 18, 9, 22, 11],
    [12, 5, 0, 10, 7, 20, 13],
    [20, 18, 10, 0, 5, 14, 10],
    [15, 9, 7, 5, 0, 10, 8],
    [30, 22, 20, 14, 10, 0, 5],
    [25, 11, 13, 10, 8, 5, 0],
    ]

    distance = {
        (i, j): distance_data[i][j]
        for i in customers for j in customers if i != j
    }

    model = Model("CVRP")

    x = model.addVars(distance.keys(), vtype=GRB.BINARY, name="x")
    u = model.addVars(customers, vtype=GRB.CONTINUOUS, lb=0, name="u")

    model.setObjective(quicksum(distance[i,j]*x[i,j] for i,j in distance), GRB.MINIMIZE)

    for j in customers[1:]:
        model.addConstr(quicksum(x[i,j] for i in customers if i!=j) == 1)
        model.addConstr(quicksum(x[j,k] for k in customers if k!=j) == 1)

    model.addConstr(quicksum(x[0,j] for j in customers if j!=0) == vehicle_count)
    model.addConstr(quicksum(x[i,0] for i in customers if i!=0) == vehicle_count)

    for i in customers[1:]:
        for j in customers[1:]:
            if i!=j:
                model.addConstr(u[i]-u[j] + vehicle_capacity*x[i,j] <= vehicle_capacity - demand[j])

    for i in customers[1:]:
        model.addConstr(u[i] >= demand[i])
        model.addConstr(u[i] <= vehicle_capacity)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return model.objVal
    else:
        return None