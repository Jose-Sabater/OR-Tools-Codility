from ortools.sat.python import cp_model

model = cp_model.CpModel()

H = [3, 1, 4]


start_rectangle_1 = model.NewIntVar(0, 10_000, "start_1")
end_rectangle_1 = model.NewIntVar(0, 10_000, "end_1")
height_rectangle_1 = model.NewIntVar(0, 10_000, "height_1")
start_rectangle_2 = model.NewIntVar(0, 100_000, "start_2")
end_rectangle_2 = model.NewIntVar(0, 100_000, "end_2")
height_rectangle_2 = model.NewIntVar(0, 10_000, "height_2")
area_1 = model.NewIntVar(0, 1_000_000_000, "area_1")

# sum of the widths must be the length of the strip
model.add(
    (end_rectangle_1 - start_rectangle_1) + (end_rectangle_2 - start_rectangle_2)
    == len(H) - 1
)

# The second rectangle, if exists must start where the first one ends
model.add(start_rectangle_2 > end_rectangle_1)

# All elements of H must be within either of the rectangles
# We could frame it as element belongs to rectangle 1 or element belongs to rectangle 2
belongs_1 = []
belongs_2 = []
for i in range(len(H)):
    belongs_1.append(model.NewBoolVar(f"belongs_to_rectangle_1_{i}"))
    belongs_2.append(model.NewBoolVar(f"belongs_to_rectangle_2_{i}"))

    model.add(end_rectangle_1 >= i).OnlyEnforceIf(belongs_1[i])
    model.add(height_rectangle_1 >= H[i]).OnlyEnforceIf(belongs_1[i])

    model.add(start_rectangle_2 <= i).OnlyEnforceIf(belongs_2[i])
    model.add(height_rectangle_2 >= H[i]).OnlyEnforceIf(belongs_2[i])

model.AddMultiplicationEquality(
    area_1, [end_rectangle_1 - start_rectangle_1, height_rectangle_1]
)
area_2 = model.NewIntVar(0, 1_000_000_000, "area_2")
model.AddMultiplicationEquality(
    area_2, [end_rectangle_2 - start_rectangle_2, height_rectangle_2]
)

# Minimize the rectangle areas
model.Minimize(area_1 + area_2)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print(
        f"Rectangle 1: {solver.Value(start_rectangle_1)}, {solver.Value(end_rectangle_1)}, {solver.Value(height_rectangle_1)}"
    )
    print(
        f"Rectangle 2: {solver.Value(start_rectangle_2)}, {solver.Value(end_rectangle_2)}, {solver.Value(height_rectangle_2)}"
    )
    print(f"Area: {solver.ObjectiveValue()}")
