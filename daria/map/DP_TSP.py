# Modified code from https://github.com/phvargas/TSP-python/blob/master/TSP.py
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pandas as pd
from scipy.spatial import distance_matrix
import sys
import copy
import help_functions as fun
import matplotlib.pyplot as plt
import time  # Required library to calculate Computational Time


def main(mylist):
    n = len(mylist) - 1

    xlist = [xx[0] for xx in mylist]
    ylist = [yy[1] for yy in mylist]

    d = {"x": xlist, "y": ylist}
    df = pd.DataFrame(data=d)
    print(df)

    matrix = pd.DataFrame(
        distance_matrix(df[["x", "y"]].values, df[["x", "y"]].values),
        index=df.index,
        columns=df.index,
    ).values

    # print(matrix)
    # # print(distance_matrix)
    # exit()
    distance = 0

    all_sets = []
    g = {}
    p = []

    n = len(mylist)
    for x in range(1, n):
        g[x + 1, ()] = matrix[x][0]

    intTuple=()
    for i in range (2,n+1):
        intTuple += (i,)
    print(intTuple)
    # exit()
    # get_minimum(1, (2, 3, 4, 5, 6, 7, 8, 9, 10), g, p, matrix)
    start_time = time.time()  # Keeps the start time
    get_minimum(1, intTuple, g, p, matrix)

    prev=1
    print("\n\nSolution to TSP: {1, ", end="")
    solution = p.pop()
    sol = [1, solution[1][0]]
    print(solution[1][0], end=", ")
    for x in range(n - 2):
        for new_solution in p:
            if tuple(solution[1]) == new_solution[0]:
                solution = new_solution
                print(solution[1][0], end=", ")
                sol.append(solution[1][0])
                distance+=matrix[prev-1][solution[1][0]-1]
                prev=solution[1][0]
                break
    print("1}")
    comp_time = (
        time.time() - start_time
    )  # Subtracts the start time from the end time and keeps the result
    print(f"-> Computational Time: {comp_time} seconds")  # Prints computational time

    arr = [xx - 1 for xx in sol]
    print(arr)
    routes = [(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
    routes.append((arr[-1], arr[0]))

    # Visualization
    # PRINT DRONE ROUTE
    drone_route = [(i, (i + 1) % len(mylist)) for i in range(len(mylist))]

    d = {"x": [x[0] for x in mylist], "y": [x[1] for x in mylist]}
    # df = pd.DataFrame(data=d)
    drone_df = pd.DataFrame(data=d)
    print("drone_route: ", drone_route)
    # fun.DrawRealMap(drone_df, None, drone_route)

    # PRINT SOLUTION
    print("routes: ", routes)
    print(routes)
    fun.DrawRealMap(df, None, routes)
    return (
        len(mylist),
        round(comp_time,2), round(distance,2)
    )


def get_minimum(k, a, g, p, matrix):
    start_time=time.time()
    if (k, a) in g:
        # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
        return g[k, a]

    values = []
    all_min = []
    for j in a:
        set_a = copy.deepcopy(list(a))
        set_a.remove(j)
        all_min.append([j, tuple(set_a)])
        result = get_minimum(j, tuple(set_a), g, p, matrix)
        values.append(matrix[k - 1][j - 1] + result)

    # get minimun value from set as optimal solution for
    g[k, a] = min(values)
    p.append(((k, a), all_min[values.index(g[k, a])]))

    return g[k, a]


if __name__ == "__main__":
    print("DP_TSP")
    results = []
    for i in range(10,11):
        results.append(
            main(fun.generated_list_of_27[15])#fun.generated_list_of_27[i-1])#fun.shuffle_list(tmpList[:10]))
        )  # (generation number, number of individuals in a generation, Number of parent "pairs" to be selected in parent selection, crossover probability for a parent pair, mutation probability for a child solution)
        
    print(results)
    sys.exit(0)
