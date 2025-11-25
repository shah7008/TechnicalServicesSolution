# app/services/service.py
from typing import List, Optional
from datetime import datetime
from app.config import VALID_STATUSES, SERVICE_TYPES
from app.model.customer import Customer


from app.model.CURDoperations import CustomerRepository, TechnicianRepository, ServiceOrderRepository

class CustomerServiceManager:
    def __init__(self):
        self.customers = CustomerRepository()
        self.techs = TechnicianRepository()
        self.orders = ServiceOrderRepository()

    # Customers
    def create_customer(self, name: str, phone: str, email: Optional[str], address: Optional[str]) -> int:
        if not name or not phone:
            raise ValueError("Name and phone are required")
        c = Customer(CustomerID=None, Name=name.strip(), Phone=phone.strip(),
                     Email=(email.strip() if email else None),
                     Address=(address.strip() if address else None))
        return self.customers.create(c)

    def list_customers(self, search: Optional[str] = None, limit: int = 100) -> List[Customer]:
        return self.customers.list(search=search, limit=limit)

    def update_customer(self, customer_id: int, name: str, phone: str, email: Optional[str], address: Optional[str]) -> None:
        c = Customer(CustomerID=customer_id, Name=name.strip(), Phone=phone.strip(),
                     Email=(email.strip() if email else None),
                     Address=(address.strip() if address else None))
        self.customers.update(c)

    def delete_customer(self, customer_id: int) -> None:
        self.customers.delete(customer_id)

