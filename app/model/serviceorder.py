from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ServiceOrder:
    OrderID: Optional[int]
    CustomerID: int
    TechnicianID: Optional[int]
    ServiceType: str
    Description: Optional[str]
    Status: str
    ScheduledAt: Optional[datetime]
    CreatedAt: Optional[datetime] = None
    UpdatedAt: Optional[datetime] = None