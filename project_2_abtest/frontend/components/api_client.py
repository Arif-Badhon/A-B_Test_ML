import requests
import os
from typing import List, Dict, Any, Optional

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000/api")

    def get_experiments(self) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/experiments")
        response.raise_for_status()
        return response.json()

    def create_experiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/experiments/", json=data)
        response.raise_for_status()
        return response.json()

    def run_experiment(self, experiment_id: int, control: List[float], treatment: List[float]) -> Dict[str, Any]:
        params = {
            "control_data": control,
            "treatment_data": treatment
        }
        response = requests.post(f"{self.base_url}/experiments/{experiment_id}/run", json=params)
        response.raise_for_status()
        return response.json()

    def get_results(self, experiment_id: int) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/results/{experiment_id}")
        response.raise_for_status()
        return response.json()

    def calculate_sample_size(self, effect_size: float, alpha: float, power: float) -> Dict[str, Any]:
        params = {"effect_size": effect_size, "alpha": alpha, "power": power}
        response = requests.get(f"{self.base_url}/power/sample-size", params=params)
        response.raise_for_status()
        return response.json()

    def calculate_power(self, n: int, effect_size: float, alpha: float) -> Dict[str, Any]:
        params = {"n": n, "effect_size": effect_size, "alpha": alpha}
        response = requests.get(f"{self.base_url}/power/power", params=params)
        response.raise_for_status()
        return response.json()

    def calculate_mde(self, n: int, power: float, alpha: float) -> Dict[str, Any]:
        params = {"n": n, "power": power, "alpha": alpha}
        response = requests.get(f"{self.base_url}/power/mde", params=params)
        response.raise_for_status()
        return response.json()

api_client = APIClient()
