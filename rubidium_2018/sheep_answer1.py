from ortools.sat.python import cp_model

model = cp_model.CpModel()

# X = [0, 0, 10, 10]
# Y = [0, 10, 0, 10]
X = [1, 1, 8]
Y = [1, 6, 0]
d = model.NewIntVar(2, 100_000, "side_length")


for i in range(len(X) - 1):
    for j in range(i + 1, len(X)):
        if X[i] < X[j]:
            # print(f"X[{i}]={X[i]} < X[{j}]={X[j]}")
            model.add((X[i] + d) <= (X[j] - d))

        if Y[i] < Y[j]:
            # print(f"Y[{i}]={Y[i]} < Y[{j}]={Y[j]}")
            model.add((Y[i] + d) <= (Y[j] - d))

# Maximize the area of the shade
model.Maximize(d)

solver = cp_model.CpSolver()
# solver.parameters.log_search_progress = True
status = solver.Solve(model)


if status == cp_model.OPTIMAL:
    print(f"Shade side length: {solver.Value(d)}")
