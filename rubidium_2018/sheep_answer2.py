from ortools.sat.python import cp_model

model = cp_model.CpModel()

X = [0, 0, 10, 10]
Y = [0, 10, 0, 10]
# X = [1, 1, 8]
# Y = [1, 6, 0]
d = model.NewIntVar(2, 100_000, "side_length")
twice_d = model.NewIntVar(4, 200_000, "twice_side_length")
model.add(twice_d == 2 * d)

width_intervals = []
height_intervals = []
for i in range(len(X)):
    left = model.NewIntVar(-100_000, 100_000, f"left")
    model.Add(left == X[i] - d)
    right = model.NewIntVar(-100_000, 100_000, f"right")
    model.Add(right == X[i] + d)
    width_iv = model.NewIntervalVar(left, twice_d, right, f"width_{i}")
    top = model.NewIntVar(-100_000, 100_000, f"top")
    model.Add(top == Y[i] + d)
    bottom = model.NewIntVar(-100_000, 100_000, f"bottom")
    model.Add(bottom == Y[i] - d)
    height_iv = model.NewIntervalVar(bottom, twice_d, top, f"height_{i}")
    width_intervals.append(width_iv)
    height_intervals.append(height_iv)

# Add Constraints
model.add_no_overlap_2d(width_intervals, height_intervals)
# Maximize the area of the shade
model.Maximize(d)

solver = cp_model.CpSolver()
# solver.parameters.log_search_progress = True
status = solver.Solve(model)


if status == cp_model.OPTIMAL:
    print(f"Shade side length: {solver.Value(d)}")
