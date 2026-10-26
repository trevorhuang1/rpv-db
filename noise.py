import pandas as pd
from sqlalchemy import create_engine

# pull db and read the tables
DB = 'sqlite:///data/rpv.db'
engine = create_engine(DB)
results = pd.read_sql_table("results", engine)
sources = pd.read_sql_table("sources", engine)
df = results.merge(sources[["source_id", "datatype"]], on="source_id")
print("rows:", len(df))

# list of conditions that must be the same to be considered the same test
conditions = ["datatype", "material_id", "irradiation_temp_c",
              "log10_fluence_n_cm2", "log10_flux_n_cm2_s"]

# one row per group of same-condition measurements
stats = df.groupby(conditions)["delta_t41j_c"].agg(["count", "min", "max", "std"]).reset_index()
stats["spread"] = stats["max"] - stats["min"]

# we only want groups that were measured more than once
repeats = stats[stats["count"] >= 2].copy()
print("groups with repeats:", len(repeats), "| rows in them:", repeats["count"].sum())

# pooling the standard deviations
repeats["dof"] = repeats["count"] - 1
repeats["ss"] = repeats["dof"] * repeats["std"] ** 2
pooled_sd = (repeats["ss"].sum() / repeats["dof"].sum()) ** 0.5
print("overall pooled SD (C):", round(pooled_sd, 1))

# 6. The same thing per source
by_source = repeats.groupby("datatype").agg(
    n_groups=("count", "size"),
    n_rows=("count", "sum"),
    mean_spread=("spread", "mean"),
    ss=("ss", "sum"),
    dof=("dof", "sum"),
)
by_source["pooled_sd"] = (by_source["ss"] / by_source["dof"]) ** 0.5
print(by_source[["n_groups", "n_rows", "mean_spread", "pooled_sd"]].round(1))