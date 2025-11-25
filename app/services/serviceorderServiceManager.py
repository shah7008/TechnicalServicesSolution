from typing import List, Optional
from app.model.serviceorder import ServiceOrder
from app.model.CURDoperations import ServiceOrderRepository
from datetime import datetime
from app.config import VALID_STATUSES, SERVICE_TYPES

class ServiceorderServiceManager:
    def __init__(self):

        self.orders = ServiceOrderRepository()
# Service orders
    def create_order(self, customer_id: int, service_type: str, description: Optional[str], scheduled_at: Optional[datetime]) -> int:
        if service_type not in SERVICE_TYPES:
            raise ValueError(f"Invalid service type. Allowed: {SERVICE_TYPES}")
        order = ServiceOrder(
            OrderID=None, CustomerID=customer_id, TechnicianID=None,
            ServiceType=service_type, Description=(description.strip() if description else None),
            Status="Pending", ScheduledAt=scheduled_at
        )
        return self.orders.create(order)

    def list_orders(self, status: Optional[str] = None, limit: int = 100) -> List[ServiceOrder]:
        if status and status not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Allowed: {VALID_STATUSES}")
        return self.orders.list(status=status, limit=limit)

    def assign_technician(self, order_id: int, technician_id: int) -> None:
        # Basic consistency checks could be added here (e.g., tech active)
        self.orders.assign_technician(order_id, technician_id)

    def update_order_status(self, order_id: int, status: str) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Allowed: {VALID_STATUSES}")
        self.orders.update_status(order_id, status)

    def delete_order(self, order_id: int) -> None:
        self.orders.delete(order_id)