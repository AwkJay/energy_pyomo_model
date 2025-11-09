from __future__ import annotations

import pyomo.environ as pyo


def add_objective(model: pyo.ConcreteModel) -> None:
    def total_cost_rule(m: pyo.ConcreteModel) -> pyo.Expression:
        return sum(
            m.capital_cost[t] * m.new_capacity[t, y]
            + m.variable_cost[t] * m.generation[t, y]
            for t in m.TECHNOLOGIES
            for y in m.YEARS
        )

    model.total_cost = pyo.Objective(rule=total_cost_rule, sense=pyo.minimize)
