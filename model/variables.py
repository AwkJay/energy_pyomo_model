from __future__ import annotations

import pyomo.environ as pyo


def add_variables(model: pyo.ConcreteModel) -> None:
    model.new_capacity = pyo.Var(
        model.TECHNOLOGIES,
        model.YEARS,
        within=pyo.NonNegativeReals,
    )
    model.generation = pyo.Var(
        model.TECHNOLOGIES,
        model.YEARS,
        within=pyo.NonNegativeReals,
    )
