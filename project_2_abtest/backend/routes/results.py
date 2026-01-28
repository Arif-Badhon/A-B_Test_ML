from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{experiment_id}", response_model=List[schemas.Result])
def read_results(experiment_id: int, db: Session = Depends(get_db)):
    results = db.query(models.Result).filter(models.Result.experiment_id == experiment_id).order_by(models.Result.computed_at.desc()).all()
    return results
