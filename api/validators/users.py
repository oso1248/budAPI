from pydantic import BaseModel
from typing import Optional  # Optional[int]


class User(BaseModel):
    name: str
    content: str
