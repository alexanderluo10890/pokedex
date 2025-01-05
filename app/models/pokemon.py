from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class Evolution(BaseModel):
    num: str
    name: str

class Pokemon(BaseModel):
    id: int
    num: str
    name: str
    img: str
    type: List[str]
    height: str
    weight: str
    weaknesses: List[str]
    prev_evolution: Optional[List[Evolution]] = None
    next_evolution: Optional[List[Evolution]] = None
    
    model_config = ConfigDict(json_schema_extra={'exclude_none': True})

class UpdatePokemon(BaseModel):
    num: Optional[str] = None
    name: Optional[str] = None
    img: Optional[str] = None
    type: Optional[List[str]] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    weaknesses: Optional[List[str]] = None
    prev_evolution: Optional[List[Evolution]] = None
    next_evolution: Optional[List[Evolution]] = None
    
    model_config = ConfigDict(extra='forbid')