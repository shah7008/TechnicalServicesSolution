# app/model/entities.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Customer:
    CustomerID: Optional[int]
    Name: str
    Phone: str
    Email: Optional[str]
    Address: Optional[str]
    CreatedAt: Optional[datetime] = None



