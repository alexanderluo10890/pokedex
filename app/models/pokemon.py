from pydantic import BaseModel
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
    next_evolution: Optional[List[Evolution]]

class UpdatePokemon(BaseModel):
    num: Optional[str] = None
    name: Optional[str] = None
    img: Optional[str] = None
    type: Optional[List[str]] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    weaknesses: Optional[List[str]] = None
    next_evolution: Optional[List[Evolution]] = None

    class Config:
        extra = 'forbid'  # Use literal value 'forbid' to reject extra keys
