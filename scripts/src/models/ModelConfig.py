from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class TAConfig:
    candle_data: List[str]
    config: dict[str, Any]
    func: str
    name: str

@dataclass
class ModelConfig:
    candle_data: List[str]
    func_M: str
    func_S: str
    func_Y: str
    model: dict[str, Any]
    model_inputs: Optional[List[str]] = field(default_factory=list)
    ta: Optional[List[TAConfig]] = field(default_factory=list)
