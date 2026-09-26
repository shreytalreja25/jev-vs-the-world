"""
Base model adapter abstract class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.models import BenchmarkItem, DecisionOutput


class BaseModelAdapter(ABC):
    def __init__(self, model_name: str, model_info: Any):
        self.model_name = model_name
        self.model_info = model_info

    @abstractmethod
    async def predict_decision(self, item: BenchmarkItem) -> DecisionOutput:
        """
        Executes a decision query for a given benchmark item.
        Returns a DecisionOutput object with chosen label, confidence, latency, tokens, and cost.
        """
        pass
