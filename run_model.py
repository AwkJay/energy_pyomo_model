from __future__ import annotations

import pyomo.environ as pyo

from model.constraints import add_constraints
from model.objective import add_objective
from model.parameters import build_parameters
from model.sets import build_sets
from model.variables import add_variables
from utils.results import load_input_data


def main() -> None:
    data = load_input_data()
    model = pyo.ConcreteModel()
    build_sets(model, data)
    build_parameters(model, data)
    add_variables(model)
    add_objective(model)
    add_constraints(model)

    solver = pyo.SolverFactory("glpk")
    results = solver.solve(model, tee=False)
    print("Solver Status:", results.solver.status)
    print("Termination Condition:", results.solver.termination_condition)

    print("\nGeneration Results:")
    for t in model.TECHNOLOGIES:
        for y in model.YEARS:
            val = model.generation[t, y].value
            if val is not None and val > 0:
                print(f"{t} | {y} | {val:.2f}")


if __name__ == "__main__":
    main()
