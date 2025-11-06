from __future__ import annotations

import pyomo.environ as pyo


def build_parameters(model: pyo.ConcreteModel, data: dict) -> None:
    tech_params = data["technology_params"]
    demand = {int(year): float(value) for year, value in data["demand"].items()}

    model.capital_cost = pyo.Param(
        model.TECHNOLOGIES,
        initialize={tech: params["capital_cost"] for tech, params in tech_params.items()},
        within=pyo.NonNegativeReals,
    )
    model.variable_cost = pyo.Param(
        model.TECHNOLOGIES,
        initialize={tech: params["variable_cost"] for tech, params in tech_params.items()},
        within=pyo.NonNegativeReals,
    )
    model.capacity_factor = pyo.Param(
        model.TECHNOLOGIES,
        initialize={tech: params["capacity_factor"] for tech, params in tech_params.items()},
        within=pyo.PercentFraction,
    )
    model.emissions = pyo.Param(
        model.TECHNOLOGIES,
        initialize={tech: params["emissions"] for tech, params in tech_params.items()},
        within=pyo.NonNegativeReals,
    )
    model.renewable = pyo.Param(
        model.TECHNOLOGIES,
        initialize={tech: params["renewable"] for tech, params in tech_params.items()},
        within=pyo.Binary,
    )
    model.demand = pyo.Param(
        model.YEARS,
        initialize=demand,
        within=pyo.NonNegativeReals,
    )
