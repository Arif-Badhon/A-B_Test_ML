from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    control_group_name = Column(String(100))
    treatment_group_name = Column(String(100))
    metric_name = Column(String(100))
    metric_type = Column(String(50))  # 'continuous', 'categorical', 'binary'
    status = Column(String(50), default="running")
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String(100))
