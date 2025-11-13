from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_generation_mix(results_df: pd.DataFrame):
    pivot = (
        results_df.pivot_table(
            index="year", columns="technology", values="generation", aggfunc="sum"
        )
        .sort_index()
        .fillna(0.0)
    )
    ax = pivot.plot.area(stacked=True, figsize=(10, 6))
    ax.set_xlabel("Year")
    ax.set_ylabel("Generation")
    ax.set_title("Generation Mix by Technology")
    ax.legend(title="Technology", loc="upper left", bbox_to_anchor=(1.02, 1))
    fig = ax.get_figure()
    fig.tight_layout()
    return ax
