from __future__ import annotations

import copy

import pandas as pd
import pyomo.environ as pyo

from model.constraints import add_constraints
from model.objective import add_objective
from model.parameters import build_parameters
from model.sets import build_sets
from model.variables import add_variables
from utils.results import extract_results, load_input_data


def build_model(data: dict, renewable_share_target: float) -> pyo.ConcreteModel:
    model = pyo.ConcreteModel()
    build_sets(model, data)
    build_parameters(model, data)
    add_variables(model)
    add_objective(model)
    add_constraints(model)
    model.renewable_share_target.set_value(renewable_share_target)
    return model


def apply_carbon_tax(data: dict, carbon_tax: float) -> None:
    for params in data["technology_params"].values():
        params["variable_cost"] = params["variable_cost"] + params["emissions"] * carbon_tax


def run_all_scenarios() -> pd.DataFrame:
    base_data = load_input_data()
    scenarios = [
        {"name": "baseline", "carbon_tax": 0.0, "renewable_share": 0.3},
        {"name": "high_carbon_tax", "carbon_tax": 50.0, "renewable_share": 0.3},
        {"name": "high_renewables", "carbon_tax": 0.0, "renewable_share": 0.6},
    ]

    summaries = []
    for scenario in scenarios:
        data = copy.deepcopy(base_data)
        if scenario["carbon_tax"] > 0:
            apply_carbon_tax(data, scenario["carbon_tax"])
        model = build_model(data, scenario["renewable_share"])
        solver = pyo.SolverFactory("glpk")
        solver.solve(model, tee=False)
        results_df = extract_results(model)
        summaries.append(
            {
                "scenario": scenario["name"],
                "total_generation": results_df["generation"].sum(),
                "total_new_capacity": results_df["new_capacity"].sum(),
                "total_cost": pyo.value(model.total_cost),
            }
        )

    return pd.DataFrame(summaries)
