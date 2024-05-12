from ortools.sat.python import cp_model

model = cp_model.CpModel()

initial_grid = [
    [0, 6, 0, 0, 5, 0, 0, 2, 0],
    [0, 0, 0, 3, 0, 0, 0, 9, 0],
    [7, 0, 0, 6, 0, 0, 0, 1, 0],
    [0, 0, 6, 0, 3, 0, 4, 0, 0],
    [0, 0, 4, 0, 7, 0, 1, 0, 0],
    [0, 0, 5, 0, 9, 0, 8, 0, 0],
    [0, 4, 0, 0, 0, 1, 0, 0, 6],
    [0, 3, 0, 0, 0, 8, 0, 0, 0],
    [0, 2, 0, 0, 4, 0, 0, 5, 0],
]

# i = rows, j = columns

grid = [[model.NewIntVar(1, 9, f"cell_{i}_{j}") for j in range(9)] for i in range(9)]


# Row constraints , all different
for i in range(9):
    model.add_all_different(grid[i])

# Each column has different values
for j in range(9):
    model.add_all_different([grid[i][j] for i in range(9)])

# 3x3 constraint all different
for i in range(0, 9, 3):
    rows = grid[i : i + 3]
    for j in range(0, 7, 3):
        grid_3x3 = []
        for row in rows:
            grid_3x3.append(row[j : j + 3])
        grid_3x3_lst = [el for cell in grid_3x3 for el in cell]
        model.add_all_different(grid_3x3_lst)


# Add initial values constraint
for i in range(9):
    for j in range(9):
        if initial_grid[i][j] != 0:
            model.add(grid[i][j] == initial_grid[i][j])


solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    for i in range(9):
        print(" ".join(str(solver.Value(grid[i][j])) for j in range(9)))
else:
    print("No solution found.")
