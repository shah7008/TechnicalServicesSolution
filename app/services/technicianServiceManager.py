from typing import List, Optional
from app.model.technician import Technician
from datetime import datetime
from app.config import VALID_STATUSES, SERVICE_TYPES
from app.model.CURDoperations import TechnicianRepository


class TechnicianServiceManager:
    def __init__(self):

        self.techs = TechnicianRepository()

# Technicians
    def create_technician(self, name: str, phone: str, skill_level: str, active: bool = True) -> int:
        if not name or not phone or not skill_level:
            raise ValueError("Name, phone, and skill level are required")
        t = Technician(TechnicianID=None, Name=name.strip(), Phone=phone.strip(), SkillLevel=skill_level.strip(), Active=active)
        return self.techs.create(t)

    def list_technicians(self, active_only: bool = True, limit: int = 100) -> List[Technician]:
        return self.techs.list(active_only=active_only, limit=limit)

    def set_technician_active(self, technician_id: int, active: bool) -> None:
        self.techs.set_active(technician_id, active)

