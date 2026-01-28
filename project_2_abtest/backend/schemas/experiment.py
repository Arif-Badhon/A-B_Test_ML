from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExperimentBase(BaseModel):
    name: str
    description: Optional[str] = None
    control_group_name: str
    treatment_group_name: str
    metric_name: str
    metric_type: str
    created_by: Optional[str] = None

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
