"""
Pydantic data models for benchmark tasks, model responses, and aggregated metrics.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class BenchmarkItem(BaseModel):
    id: str
    dataset_name: str
    input_state: Dict[str, Any]
    question_key: str
    question_instruction: str
    candidate_choices: List[str]
    ground_truth: str
    metadata: Optional[Dict[str, Any]] = None


class DecisionOutput(BaseModel):
    item_id: str
    dataset_name: str
    model_name: str
    chosen_label: str
    confidence_score: float  # Calibrated probability [0.0, 1.0]
    is_correct: bool
    latency_ms: float
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    raw_response: Optional[str] = None
    error: Optional[str] = None


class AggregateMetric(BaseModel):
    model_name: str
    total_samples: int
    accuracy: float
    macro_f1: float
    mean_latency_ms: float
    p50_latency_ms: float
    p90_latency_ms: float
    p99_latency_ms: float
    total_cost_usd: float
    cost_per_1k_decisions: float
    expected_calibration_error: float
    total_input_tokens: int
    total_output_tokens: int
