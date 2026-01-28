from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func
from database import Base

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    t_statistic = Column(Float)
    p_value = Column(Float)
    effect_size = Column(Float)
    ci_lower = Column(Float)
    ci_upper = Column(Float)
    conclusion = Column(String(255))
    computed_at = Column(DateTime, server_default=func.now())
