from ortools.sat.python import cp_model

model = cp_model.CpModel()

H = [3, 1, 4]
H = [5, 3, 2, 4]
H = [5, 3, 5, 2, 1]
H = [7, 7, 3, 7, 7]
H = [1, 1, 7, 6, 6, 6]
max_height = max(H)

banner_1_width = model.NewIntVar(1, len(H), "banner_1_width")
banner_1_height = model.NewIntVar(0, max_height, "banner_1_height")
banner_2_width = model.NewIntVar(0, len(H), "banner_2_width")
model.add(banner_2_width == len(H) - banner_1_width)
banner_2_height = model.NewIntVar(0, max_height, "banner_2_height")

banner_1_area = model.NewIntVar(1, max_height * len(H), "banner_1_area")
banner_2_area = model.NewIntVar(0, max_height * len(H), "banner_2_area")

model.AddMultiplicationEquality(banner_1_area, [banner_1_width, banner_1_height])
model.AddMultiplicationEquality(banner_2_area, [banner_2_width, banner_2_height])

banner_1_recs = []
banner_2_recs = []
for x, h in enumerate(H):
    banner_1_recs.append(model.NewBoolVar(f"belongs_to_banner_1_{x}"))
    banner_2_recs.append(model.NewBoolVar(f"belongs_to_banner_2_{x}"))
    model.AddBoolXOr([banner_1_recs[x], banner_2_recs[x]])
    model.add(banner_1_width >= x + 1).OnlyEnforceIf(banner_1_recs[x])
    model.add(banner_1_height >= h).OnlyEnforceIf(banner_1_recs[x])

    model.add(banner_2_height >= h).OnlyEnforceIf(banner_2_recs[x])
    model.add(banner_2_width >= sum(banner_2_recs)).OnlyEnforceIf(banner_2_recs[x])


# Minimize the areas
model.Minimize(banner_1_area + banner_2_area)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True

status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    print(
        f"Banner 1: Width: {solver.Value(banner_1_width)}, Height: {solver.Value(banner_1_height)}"
    )
    print(
        f"Banner 2: Width: {solver.Value(banner_2_width)}, Height: {solver.Value(banner_2_height)}"
    )
    print(f"Area 1: {solver.Value(banner_1_area) + solver.Value(banner_2_area)}")
