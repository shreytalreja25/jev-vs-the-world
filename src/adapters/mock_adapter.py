"""
Mock adapter for offline tests and latency/cost simulations.
"""

import time
from typing import Dict, Any
from src.adapters.base import BaseModelAdapter
from src.models import BenchmarkItem, DecisionOutput


class MockAdapter(BaseModelAdapter):
    def __init__(self, model_name: str, model_info: Any):
        super().__init__(model_name, model_info)

    async def predict_decision(self, item: BenchmarkItem) -> DecisionOutput:
        start_time = time.perf_counter()
        
        is_fast = "fast" in self.model_name.lower()
        elapsed_ms = 75.0 if is_fast else 520.0
        
        input_tokens = len(str(item.input_state).split()) + 20
        output_tokens = 0 if self.model_info.is_system_one else 35
        
        h = hash(item.id + self.model_name) % 100
        is_correct = (h < 82)
        chosen = item.ground_truth if is_correct else item.candidate_choices[-1]
        confidence = 0.89 if is_correct else 0.58
        
        cost = (input_tokens / 1_000_000.0) * self.model_info.input_cost_per_1m + \
               (output_tokens / 1_000_000.0) * self.model_info.output_cost_per_1m
               
        return DecisionOutput(
            item_id=item.id,
            dataset_name=item.dataset_name,
            model_name=self.model_name,
            chosen_label=chosen,
            confidence_score=confidence,
            is_correct=is_correct,
            latency_ms=elapsed_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost_usd=cost,
            raw_response="mock_response"
        )
