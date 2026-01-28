from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..services import statistics

router = APIRouter(prefix="/experiments", tags=["experiments"])

@router.post("/", response_model=schemas.Experiment)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    db_experiment = models.Experiment(**experiment.model_dump())
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment

@router.get("/", response_model=List[schemas.Experiment])
def read_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiments = db.query(models.Experiment).order_by(models.Experiment.created_at.desc()).offset(skip).limit(limit).all()
    return experiments

@router.get("/{experiment_id}", response_model=schemas.Experiment)
def read_experiment(experiment_id: int, db: Session = Depends(get_db)):
    db_experiment = db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return db_experiment

@router.post("/{experiment_id}/run", response_model=schemas.Result)
def run_experiment(
    experiment_id: int, 
    control_data: List[float], 
    treatment_data: List[float], 
    db: Session = Depends(get_db)
):
    db_experiment = db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    try:
        stats_results = statistics.welch_ttest(control_data, treatment_data)
        
        db_result = models.Result(
            experiment_id=experiment_id,
            t_statistic=stats_results["t_statistic"],
            p_value=stats_results["p_value"],
            effect_size=stats_results["effect_size"],
            ci_lower=stats_results["ci_lower"],
            ci_upper=stats_results["ci_upper"],
            conclusion=stats_results["conclusion"]
        )
        
        db_experiment.status = "completed"
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return db_result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
