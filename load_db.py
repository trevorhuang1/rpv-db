import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Base, Material, Result, Source

# Constants
PATH = 'data/raw/rpv.xlsx'
DB = 'sqlite:///data/rpv.db'
DATASET_DOI = '10.18126/3zkm-yd51'

SOURCE_INFO = {
    "Plotter": "Surveillance data from power-plant programs (Charpy shifts)",
    "Plotter-15 MTR": "Test-reactor data from the earlier PLOTTER-15 release, mostly Charpy shifts",
    "IVAR": "UCSB test-reactor experiment, hardening data",
    "BR2": "UCSB test-reactor experiment, hardening data, higher flux",
    "ATR2": "UCSB test-reactor experiment, hardening data, high fluence",
    "RADAMO": "Separate test-reactor database, tensile hardening data",
}
RENAME = {
    "temperature_C": "irradiation_temp_c",
    "wt_percent_Cu": "cu_wt_pct",
    "wt_percent_Ni": "ni_wt_pct",
    "wt_percent_Mn": "mn_wt_pct",
    "wt_percent_P": "p_wt_pct",
    "wt_percent_Si": "si_wt_pct",
    "wt_percent_C": "c_wt_pct",
    "log(fluence_n_cm2)": "log10_fluence_n_cm2",
    "log(flux_n_cm2_sec)": "log10_flux_n_cm2_s",
    "Measured DT41J [C]": "delta_t41j_c",  # the raw header has two spaces; collapsed below
    "datatype": "datatype",
}
COMPOSITIONS = ["cu_wt_pct", "ni_wt_pct", "mn_wt_pct", "p_wt_pct", "si_wt_pct", "c_wt_pct"]

# Database set up. SQLite ignores foreign keys unless this runs on every connection.
engine = create_engine(DB)

@event.listens_for(engine, "connect")
def foreign_keys_on(dbapi_conn, _record):
    dbapi_conn.execute("PRAGMA foreign_keys = ON")

Path(DB).unlink(missing_ok=True)
Base.metadata.create_all(engine)

# Cleaning and reading the raw xlsx
df = pd.read_excel(PATH)
df.columns = [" ".join(c.split()) for c in df.columns]
df = df.rename(columns=RENAME) # rename all the columns to fit the tables in models.py