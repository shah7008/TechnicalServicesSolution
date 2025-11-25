from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Technician:
    TechnicianID: Optional[int]
    Name: str
    Phone: str
    SkillLevel: str
    Active: bool = True
    CreatedAt: Optional[datetime] = None