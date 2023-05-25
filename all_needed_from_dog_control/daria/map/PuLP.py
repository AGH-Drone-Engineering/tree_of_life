# https://avinashnavlani.medium.com/solving-linear-programming-using-python-pulp-3d3b6189d0a2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import help_functions as fun

import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import pulp

import warnings

warnings.filterwarnings("ignore")


# # prepare data
# tmpList = [
#     (4920, -581),
#     (5054, -531),
#     (5327, -767),
#     (5400, -730),
#     (5120, -460),
#     (5207, -396),
#     (5499, -722),
#     (5586, -663),
#     (5301, -333),
#     (5173, -304),
#     (4920, -581),
# ]
# tmpList=[(774, 330),(513, 209),(602, 206),(663, 278),(540, 86),(589, 390),(395, 235),(492, 317),(689, 366)]

# print(tmpList)

def main(mylist):
    if len(mylist)==1:
        return (
            len(mylist),0,0, 'Optimal'
        )
    xlist = []
    ylist = []

    xlist = [xx[0] for xx in mylist]
    ylist = [yy[1] for yy in mylist]

    d = {"x": xlist, "y": ylist}
    df = pd.DataFrame(data=d)
    print(df)
    routes=[(0, 21), (1, 3), (2, 16), (3, 20), (4, 6), (5, 15), (6, 1), (7, 5), (8, 0), (9, 4), (10, 19), (11, 13), (12, 18), (13, 8), (14, 24), (15, 10), (16, 23), (17, 25), (18, 17), (19, 14), (20, 11), (21, 2), (22, 9), (23, 7), (24, 12), (25, 22)]
    # routes2=[(0, 8), (8, 3), (3, 2), (2, 1), (1, 7), (7, 5), (5, 6), (6, 4)]
    # routes3=[(0, 21), (21, 16), (16, 11), (11, 26), (26, 25), (25, 12), (12, 1), (1, 24), (24, 3), (3, 5), (5, 2), (2, 15), (15, 6), (6, 10), (10, 9), (9, 4), (4, 13), (13, 23), (23, 20), (20, 14), (14, 8), (8, 18), (18, 7), (7, 17), (17, 19), (19, 22)]
    routes4=[(0, 21), (21, 16), (16, 26), (26, 25), (25, 15), (15, 11), (11, 24), (24, 12), (12, 6), (6, 18), (18, 10), (10, 9), (9, 23), (23, 20), (20, 14), (14, 13), (13, 4), (4, 8), (8, 7), (7, 19), (19, 22), (22, 17), (17, 1), (1, 5), (5, 3), (3, 2), (2, 0)]

    fun.DrawRealMap3(df, None, routes4)
    exit()


    n_point = min(len(xlist), len(ylist))

    # # get edge coords
    BBox = (df.x.min(), df.x.max(), df.y.min(), df.y.max())
    print(BBox)

    # visualization
    fun.DrawRealMap(df, None)

    # Find shortest way by solving TSP using PuLP
    # get distance matrix

    distances = pd.DataFrame(
        distance_matrix(df[["x", "y"]].values, df[["x", "y"]].values),
        index=df.index,
        columns=df.index,
    ).values


    # set problem
    problem = pulp.LpProblem("tsp_mip", pulp.LpMinimize)

    # set valiables
    x = pulp.LpVariable.dicts(
        "x",
        ((i, j) for i in range(n_point) for j in range(n_point)),
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    # we need to keep track of the order in the tour to eliminate the possibility of subtours
    u = pulp.LpVariable.dicts(
        "u", (i for i in range(n_point)), lowBound=1, upBound=n_point, cat="Integer"
    )

    # set objective function
    problem += pulp.lpSum(
        distances[i][j] * x[i, j] for i in range(n_point) for j in range(n_point)
    )

    # set constrains
    for i in range(n_point):
        problem += x[i, i] == 0

    for i in range(n_point):
        problem += pulp.lpSum(x[i, j] for j in range(n_point)) == 1
        problem += pulp.lpSum(x[j, i] for j in range(n_point)) == 1

    # eliminate subtour
    for i in range(n_point):
        for j in range(n_point):
            if i != j and (i != 0 and j != 0):
                problem += u[i] - u[j] <= n_point * (1 - x[i, j]) - 1

    # solve problem (stop after maxSeconds)
    status = problem.solve(pulp.PULP_CBC_CMD(maxSeconds=60, msg=0, fracGap=0))

    # output status, value of objective function
    print(
        status,
        pulp.LpStatus[status],
        pulp.LpStatus,
        pulp.value(problem.objective),
        problem.solutionTime,
    )
    print(problem.solutionTime)
    # exit()

    # check TSP problem and optimized route
    routes = [
        (i, j)
        for i in range(n_point)
        for j in range(n_point)
        if pulp.value(x[i, j]) == 1
    ]
    drone_route = [(i, (i + 1) % len(mylist)) for i in range(len(mylist))]

    d = {"x": [x[0] for x in mylist], "y": [x[1] for x in mylist]}
    # df = pd.DataFrame(data=d)
    drone_df = pd.DataFrame(data=d)
    print("drone_route: ", drone_route)
    # fun.DrawRealMap(drone_df, None, drone_route)

    # PRINT SOLUTION
    sorted_data = sorted(routes, key=lambda x: x[1])
    result = [sorted_data[0]]

    for i in range(len(sorted_data) - 1):
        current_tuple = result[i]
        next_tuple = [t for t in sorted_data if t[0] == current_tuple[1]][0]
        result.append(next_tuple)
    routes=result
    
    print (routes)
    print("routes: ", routes)
    fun.DrawRealMap3(df, None, routes4)
    return (
        len(mylist),
        round(problem.solutionTime, 2),
        round(pulp.value(problem.objective), 2),
        pulp.LpStatus[status],
    )
    
    
    

print("PuLP")
results = []
for i in range(10,11):
    results.append(
        main(fun.generated_list_of_27[26])
    )  # (generation number, number of individuals in a generation, Number of parent "pairs" to be selected in parent selection, crossover probability for a parent pair, mutation probability for a child solution)
    print(results[-1])
print(results)

# POINT \(([.\d]+) ([.\d]+)\),(.*),(.*)?
