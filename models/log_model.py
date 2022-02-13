from typing import Set, Optional

from pydantic import BaseModel, validator
from enum import Enum


class LogModel(BaseModel):
    id: Optional[int]
    user_id: int
    action: str
    create_at: float
    threat_lvl: str

    @validator('user_id')
    def validate_int(cls, v) -> int:
        if not isinstance(v, int):
            raise TypeError("Type must be int")
        return v

    @validator('create_at')
    def validate_float(cls, v) -> float:
        if not isinstance(v, float):
            raise TypeError("Type must be float")
        return v

    @validator('action')
    def validate_str(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError("Type must be str")
        return v

    @validator('threat_lvl')
    def validate_enum_member(cls, v) -> str:
        if v not in cls._get_threat_level_enum_values():
            raise TypeError("Type must be Threat Level Enum Member")
        return v

    def _get_threat_level_enum_values(self) -> Set:
        return set(map(lambda x: x.value, self.ThreatLevel))

    class ThreatLevel(Enum):
        LOW = 'L'
        MEDIUM = 'M'
        HIGH = 'H'
