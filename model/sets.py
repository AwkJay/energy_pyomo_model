from __future__ import annotations

import pyomo.environ as pyo


def build_sets(model: pyo.ConcreteModel, data: dict) -> None:
    technologies = sorted(data["technology_params"].keys())
    years = sorted(int(year) for year in data["demand"].keys())
    model.TECHNOLOGIES = pyo.Set(initialize=technologies, ordered=True)
    model.YEARS = pyo.Set(initialize=years, ordered=True)
