from sqlalchemy import Column, Float, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Material(Base):
    """
    Rows with identical chemistry are treated as one element, with different
    
    Attributes:
        material_id (Column): Each unique element
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

class 