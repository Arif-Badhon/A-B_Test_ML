from fastapi import APIRouter
from typing import List, Dict
from services.power import PowerAnalyzer

router = APIRouter(prefix="/power", tags=["power"])

@router.get("/sample-size")
def calculate_sample_size(effect_size: float, alpha: float = 0.05, power: float = 0.8):
    n = PowerAnalyzer.sample_size(effect_size, alpha, power)
    return {"required_sample_size": n}

@router.get("/power")
def calculate_power(n: int, effect_size: float, alpha: float = 0.05):
    p = PowerAnalyzer.power(n, effect_size, alpha)
    return {"power": p}

@router.get("/mde")
def calculate_mde(n: int, power: float = 0.8, alpha: float = 0.05):
    mde = PowerAnalyzer.minimum_detectable_effect(n, power, alpha)
    return {"mde": mde}
