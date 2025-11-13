from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyomo.environ as pyo


def load_input_data() -> dict:
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    with (data_dir / "technology_params.json").open("r", encoding="utf-8") as f:
        technology_params = json.load(f)
    demand_df = pd.read_csv(data_dir / "demand_projection.csv")
    demand = {
        int(row["year"]): float(row["demand_twh"])
        for _, row in demand_df.iterrows()
    }
    return {"technology_params": technology_params, "demand": demand}


def extract_results(model: pyo.ConcreteModel) -> pd.DataFrame:
    rows = []
    for tech in model.TECHNOLOGIES:
        for year in model.YEARS:
            rows.append(
                {
                    "technology": tech,
                    "year": int(year),
                    "generation": pyo.value(model.generation[tech, year]),
                    "new_capacity": pyo.value(model.new_capacity[tech, year]),
                }
            )
    return pd.DataFrame(rows)


def save_results(df: pd.DataFrame) -> None:
    project_root = Path(__file__).resolve().parents[1]
    df.to_csv(project_root / "results.csv", index=False)
    df.to_json(project_root / "results.json", orient="records")
