# Baseline architecture adapted from the flask_2025 template
# Source: https://github.com/nighthawkcoders/flask_2025

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Material(Base):
    """
    Material Model

    Rows with identical chemistry are treated as one element to avoid duplication
    
    Attributes:
        material_id (Column): An integer representing the materials unique identifier
        cu_wt_pct ... c_wt_pct (Column): wt% of each element 
    """

    __tablename__ = 'materials'

    __table_args__ = (
        UniqueConstraint(
            "cu_wt_pct", "ni_wt_pct", "mn_wt_pct", "p_wt_pct", "si_wt_pct", "c_wt_pct",
            name="uq_material_chemistry",
        ),
    )

    material_id = Column(Integer, primary_key=True)
    cu_wt_pct = Column(Float, nullable=False)
    ni_wt_pct = Column(Float, nullable=False)
    mn_wt_pct = Column(Float, nullable=False)
    p_wt_pct = Column(Float, nullable=False)
    si_wt_pct = Column(Float, nullable=False)
    c_wt_pct = Column(Float, nullable=False)

    results = relationship("Result", back_populates="material")

class Source(Base):
    """
    Source Model

    Where a group of rows came from. This was labeled as 'datatype' in the raw xlsx file

    Attributes:
        source_id (Column): An integer representing the source's unique identifier
        datatype (Column): Label from the raw file (e.g. 'Plotter')
        description (Column): Description of the source
        dataset_doi (Column): DOI of the dataset the file came from
    """
    __tablename__ = "sources"

    source_id = Column(Integer, primary_key=True)
    datatype = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    dataset_doi = Column(String, nullable=False)

    results = relationship("Result", back_populates="source")

class Result(Base):
    """
    Result Model

    Each row in the raw xlsx file is a result. Each result is linked to a source and a material.

    Attributes:
        result_id (Column): An integer representing the result's unique identifier
        source_id (Column): Foreign key to the source table
        material_id (Column): Foreign key to the material table
    """

    __tablename__ = "results"

    result_id = Column(Integer, primary_key=True)

    source_id = Column(
        Integer,
        ForeignKey("sources.source_id"),
        nullable=False,
    )

    material_id = Column(
        Integer,
        ForeignKey("materials.material_id"),
        nullable=False,
    )


    raw_row_number = Column(Integer, unique=True, nullable=False)
    irradiation_temp_c = Column(Float, nullable=False)
    log10_fluence_n_cm2 = Column(Float, nullable=False)
    log10_flux_n_cm2_s = Column(Float, nullable=False)
    delta_t41j_c = Column(Float, nullable=False)

    source = relationship("Source", back_populates="results")
    material = relationship("Material", back_populates="results")