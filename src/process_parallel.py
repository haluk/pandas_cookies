#!/usr/bin/env pythondocker
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use("ggplot")


def violinplot(df, i, id_var, prefix="chunk_", suffix=".png"):
    print(f"chunk {i+1}")
    fname = f"{prefix}{i+1}{suffix}"
    value_vars = list(set(df.columns) - set([id_var])).sort()
    df_melt = pd.melt(df, id_vars=id_var, value_vars=value_vars, value_name="expr")
    order = df_melt[id_var].value_counts().index
    g = sns.FacetGrid(
        df_melt, col=id_var, col_wrap=5, row_order=order, height=2.0, aspect=2
    )
    g.map(sns.violinplot, "expr", cut=0, order=value_vars)

    g.savefig(fname)
    plt.close()


def process_parallel(data, func, id_var, worker=2, **kwargs):
    with ProcessPoolExecutor(max_workers=worker) as executor:
        future_to_square = {
            executor.submit(func, chunk, i, id_var): (i, chunk)
            for (i, chunk) in enumerate(data)
        }
        for future in as_completed(future_to_square):
            future_to_square[future]
        try:
            future.result()
        except Exception as exc:
            print(exc)


if __name__ == "__main__":
    df = pd.read_csv("brca/xena_mirna_hiseq.tsv", sep="\t")

    df_split = np.array_split(df, 50)

    process_parallel(df_split, violinplot, "mirna", multiprocessing.cpu_count())
