# app/model/repositories.py
from typing import List, Optional, Tuple
from datetime import datetime
from app.model.dbconnection import get_connection
from app.model.customer import Customer
from app.model.technician import Technician
from app.model.serviceorder import ServiceOrder


class CustomerRepository:
    def create(self, customer: Customer) -> int:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                INSERT INTO Customers (Name, Phone, Email, Address)
                VALUES (?, ?, ?, ?);
                """,
                (customer.Name, customer.Phone, customer.Email, customer.Address),
            )
            cur.execute("SELECT SCOPE_IDENTITY();")
            new_id = int(cur.fetchone()[0])
            cn.commit()
            return new_id

    def list(self, search: Optional[str] = None, limit: int = 100) -> List[Customer]:
        with get_connection() as cn:
            cur = cn.cursor()
            if search:
                cur.execute(
                    """
                    SELECT TOP (?) CustomerID, Name, Phone, Email, Address, CreatedAt
                    FROM Customers
                    WHERE Name LIKE ? OR Phone LIKE ? OR Email LIKE ?
                    ORDER BY CustomerID DESC;
                    """,
                    (limit, f"%{search}%", f"%{search}%", f"%{search}%"),
                )
            else:
                cur.execute(
                    """
                    SELECT TOP (?) CustomerID, Name, Phone, Email, Address, CreatedAt
                    FROM Customers
                    ORDER BY CustomerID DESC;
                    """,
                    (limit,),
                )
            rows = cur.fetchall()
            return [
                Customer(r.CustomerID, r.Name, r.Phone, r.Email, r.Address, r.CreatedAt)
                for r in rows
            ]

    def update(self, customer: Customer) -> None:
        if not customer.CustomerID:
            raise ValueError("CustomerID required for update")
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                UPDATE Customers
                SET Name = ?, Phone = ?, Email = ?, Address = ?
                WHERE CustomerID = ?;
                """,
                (customer.Name, customer.Phone, customer.Email, customer.Address, customer.CustomerID),
            )
            cn.commit()

    def delete(self, customer_id: int) -> None:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM Customers WHERE CustomerID = ?;", (customer_id,))
            cn.commit()

class TechnicianRepository:
    def create(self, tech: Technician) -> int:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                INSERT INTO Technicians (Name, Phone, SkillLevel, Active)
                VALUES (?, ?, ?, ?);
                """,
                (tech.Name, tech.Phone, tech.SkillLevel, int(tech.Active)),
            )
            cur.execute("SELECT SCOPE_IDENTITY();")
            new_id = int(cur.fetchone()[0])
            cn.commit()
            return new_id

    def list(self, active_only: bool = True, limit: int = 100) -> List[Technician]:
        with get_connection() as cn:
            cur = cn.cursor()
            if active_only:
                cur.execute(
                    """
                    SELECT TOP (?) TechnicianID, Name, Phone, SkillLevel, Active, CreatedAt
                    FROM Technicians
                    WHERE Active = 1
                    ORDER BY TechnicianID DESC;
                    """,
                    (limit,),
                )
            else:
                cur.execute(
                    """
                    SELECT TOP (?) TechnicianID, Name, Phone, SkillLevel, Active, CreatedAt
                    FROM Technicians
                    ORDER BY TechnicianID DESC;
                    """,
                    (limit,),
                )
            rows = cur.fetchall()
            return [
                Technician(r.TechnicianID, r.Name, r.Phone, r.SkillLevel, bool(r.Active), r.CreatedAt)
                for r in rows
            ]

    def set_active(self, technician_id: int, active: bool) -> None:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                "UPDATE Technicians SET Active = ? WHERE TechnicianID = ?;",
                (int(active), technician_id),
            )
            cn.commit()

class ServiceOrderRepository:
    def create(self, order: ServiceOrder) -> int:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                INSERT INTO ServiceOrders (CustomerID, TechnicianID, ServiceType, Description, Status, ScheduledAt)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (order.CustomerID, order.TechnicianID, order.ServiceType, order.Description, order.Status, order.ScheduledAt),
            )
            cur.execute("SELECT SCOPE_IDENTITY();")
            new_id = int(cur.fetchone()[0])
            cn.commit()
            return new_id

    def list(self, status: Optional[str] = None, limit: int = 100) -> List[ServiceOrder]:
        with get_connection() as cn:
            cur = cn.cursor()
            if status:
                cur.execute(
                    """
                    SELECT TOP (?) OrderID, CustomerID, TechnicianID, ServiceType, Description,
                           Status, ScheduledAt, CreatedAt, UpdatedAt
                    FROM ServiceOrders
                    WHERE Status = ?
                    ORDER BY OrderID DESC;
                    """,
                    (limit, status),
                )
            else:
                cur.execute(
                    """
                    SELECT TOP (?) OrderID, CustomerID, TechnicianID, ServiceType, Description,
                           Status, ScheduledAt, CreatedAt, UpdatedAt
                    FROM ServiceOrders
                    ORDER BY OrderID DESC;
                    """,
                    (limit,),
                )
            rows = cur.fetchall()
            return [
                ServiceOrder(
                    r.OrderID, r.CustomerID, r.TechnicianID, r.ServiceType, r.Description,
                    r.Status, r.ScheduledAt, r.CreatedAt, r.UpdatedAt
                )
                for r in rows
            ]

    def assign_technician(self, order_id: int, technician_id: int) -> None:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                UPDATE ServiceOrders
                SET TechnicianID = ?, Status = CASE WHEN Status = 'Pending' THEN 'Assigned' ELSE Status END,
                    UpdatedAt = SYSUTCDATETIME()
                WHERE OrderID = ?;
                """,
                (technician_id, order_id),
            )
            cn.commit()

    def update_status(self, order_id: int, status: str) -> None:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute(
                """
                UPDATE ServiceOrders
                SET Status = ?, UpdatedAt = SYSUTCDATETIME()
                WHERE OrderID = ?;
                """,
                (status, order_id),
            )
            cn.commit()

    def delete(self, order_id: int) -> None:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM ServiceOrders WHERE OrderID = ?;", (order_id,))
            cn.commit()