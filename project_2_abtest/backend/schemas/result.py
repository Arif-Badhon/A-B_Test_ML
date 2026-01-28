from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResultBase(BaseModel):
    experiment_id: int
    t_statistic: Optional[float] = None
    p_value: Optional[float] = None
    effect_size: Optional[float] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    conclusion: Optional[str] = None

class ResultCreate(ResultBase):
    pass

class Result(ResultBase):
    id: int
    computed_at: datetime

    class Config:
        from_attributes = True
