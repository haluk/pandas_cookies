#!/usr/bin/env python3
import sys

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, SmallInteger, String
from tqdm import tqdm

from utils import read_config


def create_postgre_engine(config):
    host = config["SERVER"]["host"]
    port = config["SERVER"]["port"]
    user = config["SERVER"]["user"]
    password = config["SERVER"]["password"]
    db = config["SERVER"]["db"]
    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db}")

    return engine


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def import_dataframe(df, engine, table, dtype):
    chunksize = len(df) // 10  # 10%
    try:
        with tqdm(total=len(df)) as pbar:
            for i, cdf in enumerate(chunker(df, chunksize)):
                replace = "replace" if i == 0 else "append"
                cdf.to_sql(table, engine, if_exists=replace,
                           index=False, dtype=dtype, method="multi")
                pbar.update(chunksize)
    except Exception as e:
        print(e)


def read_mirna_gene_clip(fname):
    df = pd.read_csv(fname, sep="\t")
    dtypes = {
        "id": Integer(),
        "miRNAname": String(),
        "geneID": String(),
        "geneName": String(),
        "geneType": String(),
        "chromosome": String(length=5),
        "strand": String(length=1),
        "clipExpNum": SmallInteger(),
        "degraExpNum": SmallInteger(),
        "RBP": String(),
        "pancancerNum": SmallInteger(),
        "cellLine": String()
    }

    return df, dtypes


def main(args):
    config = read_config("config.ini")
    engine = create_postgre_engine(config)
    df, dtypes = read_mirna_gene_clip(args[0])
    import_dataframe(df, engine, "breast_cancer", dtypes)


if __name__ == "__main__":
    main(sys.argv[1:])
