# app/view/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.config import APP_TITLE, DEFAULT_PAGE_SIZE, VALID_STATUSES, SERVICE_TYPES
from app.services.customerServiceManager import CustomerServiceManager
from app.services.technicianServiceManager import TechnicianServiceManager
from app.services.serviceorderServiceManager import ServiceorderServiceManager

class ACServiceDeskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x650")
        self.customer_mgr = CustomerServiceManager()
        self.technician_mgr = TechnicianServiceManager()
        self.serviceorder_mgr = ServiceorderServiceManager()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.customers_tab = ttk.Frame(self.notebook)
        self.techs_tab = ttk.Frame(self.notebook)
        self.orders_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.customers_tab, text="Customers")
        self.notebook.add(self.techs_tab, text="Technicians")
        self.notebook.add(self.orders_tab, text="Service Orders")

        self._build_customers_tab()
        self._build_technicians_tab()
        self._build_orders_tab()

    # Customers UI
    def _build_customers_tab(self):
        form = ttk.LabelFrame(self.customers_tab, text="Add / Update Customer")
        form.pack(fill=tk.X, padx=10, pady=10)

        self.c_id_var = tk.StringVar()
        self.c_name_var = tk.StringVar()
        self.c_phone_var = tk.StringVar()
        self.c_email_var = tk.StringVar()
        self.c_address_var = tk.StringVar()
        self.c_search_var = tk.StringVar()

        ttk.Label(form, text="ID (for update):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.c_id_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Name:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.c_name_var, width=25).grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Phone:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.c_phone_var, width=15).grid(row=0, column=5, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.c_email_var, width=25).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Address:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.c_address_var, width=50).grid(row=1, column=3, columnspan=3, sticky="w", padx=5, pady=5)

        ttk.Button(form, text="Create", command=self._create_customer).grid(row=2, column=0, padx=5, pady=8)
        ttk.Button(form, text="Update", command=self._update_customer).grid(row=2, column=1, padx=5, pady=8)
        ttk.Button(form, text="Delete", command=self._delete_customer).grid(row=2, column=2, padx=5, pady=8)

        search_frame = ttk.LabelFrame(self.customers_tab, text="Search")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Entry(search_frame, textvariable=self.c_search_var, width=40).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(search_frame, text="Refresh", command=self._refresh_customers).pack(side=tk.LEFT, padx=5)

        self.customers_tree = ttk.Treeview(self.customers_tab, columns=("id","name","phone","email","address","created"), show="headings", height=15)
        for col, text, w in [
            ("id", "ID", 60),
            ("name", "Name", 180),
            ("phone", "Phone", 120),
            ("email", "Email", 180),
            ("address", "Address", 250),
            ("created", "CreatedAt", 140),
        ]:
            self.customers_tree.heading(col, text=text)
            self.customers_tree.column(col, width=w, anchor=tk.W)
        self.customers_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._refresh_customers()

    def _create_customer(self):
        try:
            new_id = self.customer_mgr.create_customer(
                self.c_name_var.get(), self.c_phone_var.get(),
                self.c_email_var.get() or None, self.c_address_var.get() or None
            )
            messagebox.showinfo("Success", f"Customer created with ID {new_id}")
            self._refresh_customers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_customer(self):
        try:
            cid = int(self.c_id_var.get())
            self.customer_mgr.update_customer(
                cid, self.c_name_var.get(), self.c_phone_var.get(),
                self.c_email_var.get() or None, self.c_address_var.get() or None
            )
            messagebox.showinfo("Success", "Customer updated")
            self._refresh_customers()
        except ValueError:
            messagebox.showerror("Error", "Valid Customer ID required")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete_customer(self):
        try:
            cid = int(self.c_id_var.get())
            self.customer_mgr.delete_customer(cid)
            messagebox.showinfo("Success", "Customer deleted")
            self._refresh_customers()
        except ValueError:
            messagebox.showerror("Error", "Valid Customer ID required")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh_customers(self):
        self.customers_tree.delete(*self.customers_tree.get_children())
        rows = self.customer_mgr.list_customers(search=self.c_search_var.get() or None, limit=DEFAULT_PAGE_SIZE)
        for c in rows:
            self.customers_tree.insert("", tk.END, values=(c.CustomerID, c.Name, c.Phone, c.Email or "", c.Address or "", c.CreatedAt))

    # Technicians UI
    def _build_technicians_tab(self):
        form = ttk.LabelFrame(self.techs_tab, text="Add Technician")
        form.pack(fill=tk.X, padx=10, pady=10)

        self.t_name_var = tk.StringVar()
        self.t_phone_var = tk.StringVar()
        self.t_skill_var = tk.StringVar(value="Junior")
        self.t_active_var = tk.BooleanVar(value=True)

        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.t_name_var, width=25).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Phone:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.t_phone_var, width=15).grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Skill Level:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.t_skill_var, values=["Junior","Mid","Senior"], width=12, state="readonly").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Checkbutton(form, text="Active", variable=self.t_active_var).grid(row=1, column=2, sticky="w", padx=5, pady=5)

        ttk.Button(form, text="Create", command=self._create_technician).grid(row=2, column=0, padx=5, pady=8)
        ttk.Button(form, text="Set Active/Inactive", command=self._toggle_technician_active).grid(row=2, column=1, padx=5, pady=8)

        self.techs_tree = ttk.Treeview(self.techs_tab, columns=("id","name","phone","skill","active","created"), show="headings", height=18)
        for col, text, w in [
            ("id", "ID", 60),
            ("name", "Name", 180),
            ("phone", "Phone", 120),
            ("skill", "Skill", 120),
            ("active", "Active", 80),
            ("created", "CreatedAt", 140),
        ]:
            self.techs_tree.heading(col, text=text)
            self.techs_tree.column(col, width=w, anchor=tk.W)
        self.techs_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        actions = ttk.Frame(self.techs_tab)
        actions.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(actions, text="Refresh (Active only)", command=lambda: self._refresh_technicians(True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="Refresh (All)", command=lambda: self._refresh_technicians(False)).pack(side=tk.LEFT, padx=5)

        self._refresh_technicians(True)

    def _create_technician(self):
        try:
            new_id = self.technician_mgr.create_technician(self.t_name_var.get(), self.t_phone_var.get(), self.t_skill_var.get(), self.t_active_var.get())
            messagebox.showinfo("Success", f"Technician created with ID {new_id}")
            self._refresh_technicians(True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _toggle_technician_active(self):
        sel = self.techs_tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a technician row")
            return
        item = self.techs_tree.item(sel[0])["values"]
        tech_id, _, _, _, active, _ = item
        try:
            self.technician_mgr.set_technician_active(int(tech_id), not bool(active))
            self._refresh_technicians(False)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh_technicians(self, active_only: bool):
        self.techs_tree.delete(*self.techs_tree.get_children())
        rows = self.technician_mgr.list_technicians(active_only=active_only, limit=DEFAULT_PAGE_SIZE)
        for t in rows:
            self.techs_tree.insert("", tk.END, values=(t.TechnicianID, t.Name, t.Phone, t.SkillLevel, int(t.Active), t.CreatedAt))

    # Orders UI
    def _build_orders_tab(self):
        form = ttk.LabelFrame(self.orders_tab, text="Create Service Order")
        form.pack(fill=tk.X, padx=10, pady=10)

        self.o_customer_id_var = tk.StringVar()
        self.o_service_type_var = tk.StringVar(value=SERVICE_TYPES[0])
        self.o_desc_var = tk.StringVar()
        self.o_sched_var = tk.StringVar()

        ttk.Label(form, text="Customer ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.o_customer_id_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Service Type:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.o_service_type_var, values=SERVICE_TYPES, width=14, state="readonly").grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.o_desc_var, width=50).grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        ttk.Label(form, text="Scheduled At (YYYY-MM-DD HH:MM):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.o_sched_var, width=25).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(form, text="Create Order", command=self._create_order).grid(row=2, column=2, padx=5, pady=8)

        actions = ttk.LabelFrame(self.orders_tab, text="Assignment / Status")
        actions.pack(fill=tk.X, padx=10, pady=10)

        self.o_order_id_var = tk.StringVar()
        self.o_technician_id_var = tk.StringVar()
        self.o_status_var = tk.StringVar(value="Pending")

        ttk.Label(actions, text="Order ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(actions, textvariable=self.o_order_id_var, width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(actions, text="Technician ID:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(actions, textvariable=self.o_technician_id_var, width=10).grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Button(actions, text="Assign Technician", command=self._assign_technician).grid(row=0, column=4, padx=5, pady=8)

        ttk.Label(actions, text="Status:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(actions, textvariable=self.o_status_var, values=VALID_STATUSES, width=14, state="readonly").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(actions, text="Update Status", command=self._update_status).grid(row=1, column=2, padx=5, pady=8)

        filter_frame = ttk.Frame(self.orders_tab)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        self.o_filter_status_var = tk.StringVar(value="")
        ttk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.o_filter_status_var, values=[""] + VALID_STATUSES, width=14, state="readonly").pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Refresh", command=self._refresh_orders).pack(side=tk.LEFT, padx=5)

        self.orders_tree = ttk.Treeview(self.orders_tab, columns=("id","customer","tech","type","desc","status","scheduled","created","updated"), show="headings", height=16)
        for col, text, w in [
            ("id", "OrderID", 70),
            ("customer", "CustomerID", 90),
            ("tech", "TechnicianID", 100),
            ("type", "ServiceType", 110),
            ("desc", "Description", 260),
            ("status", "Status", 100),
            ("scheduled", "ScheduledAt", 160),
            ("created", "CreatedAt", 140),
            ("updated", "UpdatedAt", 140),
        ]:
            self.orders_tree.heading(col, text=text)
            self.orders_tree.column(col, width=w, anchor=tk.W)
        self.orders_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._refresh_orders()

    def _parse_dt(self, s: str):
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Use YYYY-MM-DD HH:MM")
            return None

    def _create_order(self):
        try:
            cid = int(self.o_customer_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "Valid Customer ID required")
            return
        scheduled = self._parse_dt(self.o_sched_var.get())
        if self.o_sched_var.get() and not scheduled:
            return
        try:
            new_id = self.serviceorder_mgr.create_order(
                customer_id=cid,
                service_type=self.o_service_type_var.get(),
                description=self.o_desc_var.get() or None,
                scheduled_at=scheduled
            )
            messagebox.showinfo("Success", f"Order created with ID {new_id}")
            self._refresh_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _assign_technician(self):
        try:
            oid = int(self.o_order_id_var.get())
            tid = int(self.o_technician_id_var.get())
            self.serviceorder_mgr.assign_technician(oid, tid)
            messagebox.showinfo("Success", "Technician assigned")
            self._refresh_orders()
        except ValueError:
            messagebox.showerror("Error", "Valid Order ID and Technician ID required")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_status(self):
        try:
            oid = int(self.o_order_id_var.get())
            status = self.o_status_var.get()
            self.serviceorder_mgr.update_order_status(oid, status)
            messagebox.showinfo("Success", "Order status updated")
            self._refresh_orders()
        except ValueError:
            messagebox.showerror("Error", "Valid Order ID required")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh_orders(self):
        self.orders_tree.delete(*self.orders_tree.get_children())
        status = self.o_filter_status_var.get() or None
        rows = self.serviceorder_mgr.list_orders(status=status, limit=DEFAULT_PAGE_SIZE)
        for o in rows:
            self.orders_tree.insert("", tk.END, values=(o.OrderID, o.CustomerID, o.TechnicianID or "", o.ServiceType, o.Description or "", o.Status, o.ScheduledAt, o.CreatedAt, o.UpdatedAt))

def main():
    app = ACServiceDeskApp()
    app.mainloop()

if __name__ == "__main__":
    main()