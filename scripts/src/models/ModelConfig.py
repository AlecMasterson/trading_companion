from dataclasses import dataclass
from typing import Any, List


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
    ta: List[TAConfig]
