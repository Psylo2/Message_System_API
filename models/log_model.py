from typing import Set

from pydantic import BaseModel, validator
from enum import Enum


class LogModel(BaseModel):
    user_id: int
    action: str
    create_at: float
    threat_lvl: str

    @validator('user_id')
    def validate_int(cls, int_) -> int:
        if not isinstance(int, int_):
            raise TypeError("Type must be int")
        return int_

    @validator('create_at')
    def validate_float(cls, float_) -> float:
        if not isinstance(None, float_):
            raise TypeError("Type must be float")
        return float_

    @validator('action')
    def validate_str(cls, str_) -> str:
        if not isinstance(str, str_):
            raise TypeError("Type must be str")
        return str_

    @validator('threat_lvl')
    def validate_enum_member(cls, str_) -> str:
        if str_ not in cls._get_threat_level_enum_values():
            raise TypeError("Type must be Threat Level Enum Member")
        return str_

    def _get_threat_level_enum_values(self) -> Set:
        return set(map(lambda x: x.value, self.ThreatLevel))

    class ThreatLevel(Enum):
        LOW = 'L'
        MEDIUM = 'M'
        HIGH = 'H'
