from ortools.sat.python import cp_model


# Callback
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:

        self.__solution_count += 1
        print(f"SOL {self.__solution_count}:", end=" ")
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count


# Initialize the model
model = cp_model.CpModel()


vars_list = [model.NewIntVar(1, 8, f"x{i}") for i in range(1, 9)]


# Constraints
# Function to enforce non-consecutive neighbor rule
def add_non_consecutive_constraints(node1, neighbors):
    for neighbor in neighbors:
        model.add(vars_list[node1] - vars_list[neighbor] != 1)
        model.add(vars_list[node1] - vars_list[neighbor] != -1)


# Each node must be different
model.AddAllDifferent(vars_list)
# Neighboring nodes cant me consecutive
# 1 is neighbor with 2, 3, and 4
add_non_consecutive_constraints(0, [1, 2, 3])
# 2 is neighbor with 1, 3, 5, and 6
add_non_consecutive_constraints(1, [0, 2, 4, 5])
# 3 is neighbor with 1, 2, 4, 5, 6, and 7
add_non_consecutive_constraints(2, [0, 1, 3, 4, 5, 6])
# 4 is neighbor with 1, 3, 6, and 7
add_non_consecutive_constraints(3, [0, 2, 5, 6])
# 5 is neighbor with 2, 3, 6, and 8
add_non_consecutive_constraints(4, [1, 2, 5, 7])
# 6 is neighbor with 2, 3, 4, 5, 7, and 8
add_non_consecutive_constraints(5, [1, 2, 3, 4, 6, 7])
# 7 is neighbor with 3, 4, 6, and 8
add_non_consecutive_constraints(6, [2, 3, 5, 7])
# 8 is neighbor with 5, 6, and 7
add_non_consecutive_constraints(7, [4, 5, 6])

# Initialize the solver
solver = cp_model.CpSolver()

# Solve the model
status = solver.Solve(model, VarArraySolutionPrinter(vars_list))

# Check if the solution is feasible or optimal
# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     # Print values for each variable
#     for i in range(len(vars_list)):
#         print(f"x{i+1} = {solver.Value(vars_list[i])}")
# else:
#     print("No solution found.")
