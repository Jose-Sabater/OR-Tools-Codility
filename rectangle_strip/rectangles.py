from ortools.sat.python import cp_model


# # Callback
# class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
#     """Print intermediate solutions."""

#     def __init__(self, variables: list[cp_model.IntVar]):
#         cp_model.CpSolverSolutionCallback.__init__(self)
#         self.__variables = variables
#         self.__solution_count = 0

#     def on_solution_callback(self) -> None:

#         self.__solution_count += 1
#         print(f"SOL {self.__solution_count}:", end=" ")
#         for v in self.__variables:
#             print(f"{v}={self.value(v)}", end=" ")
#         print()

#     @property
#     def solution_count(self) -> int:
#         return self.__solution_count


# Initialize the model
model = cp_model.CpModel()


# Two lists of nrs

# A = [2, 3, 2, 3, 5]
# B = [3, 4, 2, 4, 2]
# A = [2, 3, 1, 3]
# B = [2, 3, 1, 3]

A = [2, 10, 4, 1, 4]
B = [4, 1, 2, 2, 5]
# Rectangles are of size A[i] x B[i]

# Variables
strip_height = model.new_int_var(1, 1_000_000_000, "strip_height")
in_strip_vars = []
rotated_strip_vars = []
# For the rectangle, do I use the rectangle?
for i in range(len(A)):
    in_strip_vars.append(model.new_bool_var(f"rectangle_{i}_in_strip"))
    rotated_strip_vars.append(model.new_bool_var(f"rectangle_{i}_rotated"))
    model.add(A[i] == strip_height).OnlyEnforceIf(in_strip_vars[i])
    model.add(B[i] == strip_height).OnlyEnforceIf(rotated_strip_vars[i])
# Do I use the rectangle as is or do I rotate it?

model.maximize(sum(in_strip_vars + rotated_strip_vars))


solver = cp_model.CpSolver()

# solution_printer = VarArraySolutionPrinter(
#     [strip_height] + in_strip_vars + rotated_strip_vars
# )

# solver.parameters.log_search_progress = True
status = solver.solve(model)

if status == cp_model.OPTIMAL:
    for i in range(len(A)):
        if solver.value(in_strip_vars[i]):
            print(f"Rectangle {i} is in the strip with size {A[i]} x {B[i]}")
        elif solver.value(rotated_strip_vars[i]):
            print(f"Rectangle {i} is in the strip with size {B[i]} x {A[i]}")

    print("Optimal solution found")
