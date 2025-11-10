from __future__ import annotations

import pyomo.environ as pyo


def add_constraints(model: pyo.ConcreteModel) -> None:
    if not hasattr(model, "renewable_share_target"):
        model.renewable_share_target = pyo.Param(
            initialize=0.3,
            within=pyo.PercentFraction,
            mutable=True,
        )

    def demand_rule(m: pyo.ConcreteModel, y: int) -> pyo.Expression:
        return sum(m.generation[t, y] for t in m.TECHNOLOGIES) >= m.demand[y]

    model.demand_constraint = pyo.Constraint(model.YEARS, rule=demand_rule)

    def capacity_rule(m: pyo.ConcreteModel, t: str, y: int) -> pyo.Expression:
        return m.generation[t, y] <= m.new_capacity[t, y] * m.capacity_factor[t] * 8760

    model.capacity_constraint = pyo.Constraint(
        model.TECHNOLOGIES,
        model.YEARS,
        rule=capacity_rule,
    )

    def emissions_rule(m: pyo.ConcreteModel) -> pyo.Expression:
        return sum(
            m.emissions[t] * m.generation[t, y]
            for t in m.TECHNOLOGIES
            for y in m.YEARS
        ) <= 500_000_000

    model.emissions_cap = pyo.Constraint(rule=emissions_rule)

    def renewable_share_rule(m: pyo.ConcreteModel) -> pyo.Expression:
        renewable_generation = sum(
            m.generation[t, y] * m.renewable[t]
            for t in m.TECHNOLOGIES
            for y in m.YEARS
        )
        total_generation = sum(
            m.generation[t, y] for t in m.TECHNOLOGIES for y in m.YEARS
        )
        return renewable_generation >= m.renewable_share_target * total_generation

    model.renewable_share = pyo.Constraint(rule=renewable_share_rule)
