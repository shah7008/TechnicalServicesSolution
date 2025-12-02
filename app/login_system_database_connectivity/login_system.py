import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import os
import subprocess
import sys
import webbrowser


# ==================== CHECK ODBC DRIVER ====================
def check_odbc_driver():
    """Check if ODBC driver is installed and install if not"""
    try:
        # List available ODBC drivers
        drivers = pyodbc.drivers()
        print("Available ODBC Drivers:", drivers)

        # Check for common SQL Server drivers
        desired_drivers = [
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server",
            "ODBC Driver 13 for SQL Server"
        ]

        available_driver = None
        for driver in desired_drivers:
            if driver in drivers:
                available_driver = driver
                break

        if not available_driver:
            # No driver found, offer to download
            response = messagebox.askyesno(
                "ODBC Driver Not Found",
                "Microsoft ODBC Driver for SQL Server is not installed.\n\n"
                "This driver is required to connect to SQL Server.\n\n"
                "Would you like to download it now?"
            )

            if response:
                webbrowser.open(
                    "https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")

            return None
        else:
            print(f"Using driver: {available_driver}")
            return available_driver

    except Exception as e:
        print(f"Error checking drivers: {e}")
        return None


# ==================== DATABASE CONNECTION ====================
def connect_db():
    # First check for ODBC driver
    driver_name = check_odbc_driver()
    if not driver_name:
        return None

    # Try different connection configurations
    connection_configs = [
        # Try with named instance
        {
            "name": "Named Instance",
            "conn_str": f"DRIVER={{{driver_name}}};"
                        "SERVER=DESKTOP-G8NIUM3\\SQLEXPRESS;"
                        "DATABASE=master;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;"
        },
        # Try with localhost
        {
            "name": "Localhost",
            "conn_str": f"DRIVER={{{driver_name}}};"
                        "SERVER=localhost\\SQLEXPRESS;"
                        "DATABASE=master;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;"
        },
        # Try with dot (local instance)
        {
            "name": "Dot Instance",
            "conn_str": f"DRIVER={{{driver_name}}};"
                        "SERVER=.\\SQLEXPRESS;"
                        "DATABASE=master;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;"
        },
        # Try without instance name (default instance)
        {
            "name": "Default Instance",
            "conn_str": f"DRIVER={{{driver_name}}};"
                        "SERVER=DESKTOP-G8NIUM3;"
                        "DATABASE=master;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;"
        },
        # Try with TCP/IP
        {
            "name": "TCP/IP Localhost",
            "conn_str": f"DRIVER={{{driver_name}}};"
                        "SERVER=tcp:localhost\\SQLEXPRESS,1433;"
                        "DATABASE=master;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;"
        }
    ]

    conn = None
    errors = []

    for config in connection_configs:
        try:
            print(f"\nTrying connection: {config['name']}")
            print(f"Connection string: {config['conn_str'][:100]}...")

            conn = pyodbc.connect(config['conn_str'], timeout=5, autocommit=True)
            print(f"✅ Success with: {config['name']}")

            # Test the connection
            cursor = conn.cursor()
            cursor.execute("SELECT @@version")
            version = cursor.fetchone()[0]
            print(f"SQL Server Version: {version[:100]}...")

            return conn

        except pyodbc.Error as e:
            error_msg = f"{config['name']}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ Failed: {error_msg}")
            if conn:
                conn.close()
            continue

    # If all connections failed, show detailed error
    error_message = "All connection attempts failed:\n\n"
    error_message += "\n".join(errors[:5])  # Show first 5 errors
    error_message += "\n\n🔧 Troubleshooting Steps:\n"
    error_message += "1. Check if SQL Server is running (SQL Server Configuration Manager)\n"
    error_message += "2. Verify SQL Server Browser service is running\n"
    error_message += "3. Try using 'localhost' instead of PC name\n"
    error_message += "4. Check if SQL Server Express is installed\n"
    error_message += "5. Enable TCP/IP in SQL Server Configuration Manager"

    messagebox.showerror("Database Connection Failed", error_message)
    return None


# ==================== DATABASE SETUP ====================
def setup_database():
    """Create database and table if they don't exist"""
    driver_name = check_odbc_driver()
    if not driver_name:
        return False

    try:
        # Try multiple connection methods for setup
        setup_configs = [
            f"DRIVER={{{driver_name}}};SERVER=.\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;Encrypt=no;",
            f"DRIVER={{{driver_name}}};SERVER=localhost\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;Encrypt=no;",
            f"DRIVER={{{driver_name}}};SERVER=DESKTOP-G8NIUM3\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;Encrypt=no;"
        ]

        conn = None
        for conn_str in setup_configs:
            try:
                conn = pyodbc.connect(conn_str, timeout=10, autocommit=True)
                break
            except:
                continue

        if not conn:
            messagebox.showerror("Setup Error", "Cannot connect to SQL Server for setup")
            return False

        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'LoginSystemDB')
            BEGIN
                CREATE DATABASE LoginSystemDB;
                PRINT 'Database created successfully';
            END
            ELSE
                PRINT 'Database already exists';
        """)
        conn.commit()

        # Switch to the new database
        cursor.execute("USE LoginSystemDB")

        # Create Users table if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users')
            BEGIN
                CREATE TABLE Users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(50) UNIQUE NOT NULL,
                    password NVARCHAR(100) NOT NULL,
                    created_at DATETIME DEFAULT GETDATE()
                );
                PRINT 'Users table created';
            END
            ELSE
                PRINT 'Users table already exists';
        """)

        # Check if table is empty and add test users
        cursor.execute("SELECT COUNT(*) FROM Users")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
                INSERT INTO Users (username, password) 
                VALUES ('admin', 'admin123');
                INSERT INTO Users (username, password) 
                VALUES ('user1', 'password123');
            """)
            print("Test users created")

        conn.commit()

        # Verify setup
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'LoginSystemDB'")
        db_exists = cursor.fetchone()

        cursor.execute("USE LoginSystemDB")
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]

        conn.close()

        if db_exists:
            messagebox.showinfo("Database Setup Complete",
                                f"✅ Setup successful!\n\n"
                                f"Database: LoginSystemDB\n"
                                f"Users in table: {user_count}\n\n"
                                f"Test credentials:\n"
                                f"• admin / admin123\n"
                                f"• user1 / password123")
            return True
        else:
            messagebox.showerror("Setup Failed", "Database was not created")
            return False

    except pyodbc.Error as e:
        messagebox.showerror("Database Setup Error",
                             f"Failed to setup database:\n\n{str(e)}")
        return False
    except Exception as e:
        messagebox.showerror("Setup Error", f"Unexpected error: {str(e)}")
        return False


# ==================== SIMPLE LOGIN (for testing) ====================
def simple_login():
    """Simplified login for testing without database"""
    username = entry_username.get().strip()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Input Required", "Please enter both username and password!")
        return

    # For testing without database
    test_users = {
        'admin': 'admin123',
        'user1': 'password123',
        'test': 'test123'
    }

    if username in test_users and test_users[username] == password:
        messagebox.showinfo("Success", f"Welcome {username}!\n\n(Using simulated login - database not connected)")

        # Simulate main window
        root.withdraw()
        open_simulated_window(username)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")


# ==================== SIMULATED MAIN WINDOW ====================
def open_simulated_window(username):
    """Open main window without database connection"""
    main = tk.Toplevel()
    main.title(f"Application - {username} (Simulation Mode)")
    main.geometry("600x400")
    main.configure(bg="#f0f0f0")

    main.transient(root)
    main.grab_set()

    tk.Label(
        main,
        text="⚠️ Simulation Mode",
        font=("Helvetica", 20, "bold"),
        bg="#f0f0f0",
        fg="#e67e22"
    ).pack(pady=30)

    tk.Label(
        main,
        text=f"Welcome, {username}!",
        font=("Arial", 18),
        bg="#f0f0f0",
        fg="#2c3e50"
    ).pack(pady=10)

    tk.Label(
        main,
        text="Database is not connected.\nRunning in simulation mode.",
        font=("Arial", 12),
        bg="#f0f0f0",
        fg="#7f8c8d"
    ).pack(pady=20)

    # Info frame
    info_frame = tk.Frame(main, bg="#e8f4f8", bd=2, relief=tk.GROOVE)
    info_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)

    tk.Label(
        info_frame,
        text="To enable database connection:",
        font=("Arial", 11, "bold"),
        bg="#e8f4f8",
        fg="#2c3e50"
    ).pack(pady=10)

    steps = [
        "1. Install ODBC Driver 18 from Microsoft",
        "2. Ensure SQL Server is running",
        "3. Click 'Setup Database' button",
        "4. Restart the application"
    ]

    for step in steps:
        tk.Label(
            info_frame,
            text=step,
            font=("Arial", 10),
            bg="#e8f4f8",
            fg="#34495e",
            justify=tk.LEFT
        ).pack(anchor="w", padx=20, pady=2)

    # Buttons
    button_frame = tk.Frame(main, bg="#f0f0f0")
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Download ODBC Driver",
        font=("Arial", 10, "bold"),
        bg="#3498db",
        fg="white",
        command=lambda: webbrowser.open(
            "https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        button_frame,
        text="Setup Database",
        font=("Arial", 10, "bold"),
        bg="#9b59b6",
        fg="white",
        command=setup_database
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        button_frame,
        text="Logout",
        font=("Arial", 10, "bold"),
        bg="#e74c3c",
        fg="white",
        command=lambda: [main.destroy(), root.deiconify()]
    ).pack(side=tk.LEFT, padx=5)

    def on_closing():
        main.destroy()
        root.deiconify()

    main.protocol("WM_DELETE_WINDOW", on_closing)


# ==================== MAIN LOGIN FUNCTION ====================
def login():
    username = entry_username.get().strip()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Input Required", "Please enter both username and password!")
        return

    # Try database login first
    if use_database_var.get():
        # Show loading
        login_button.config(state='disabled', text="Connecting...")
        status_label.config(text="Attempting database connection...", fg="#3498db")
        root.update()

        try:
            driver_name = check_odbc_driver()
            if not driver_name:
                status_label.config(text="❌ ODBC Driver not found", fg="#e74c3c")
                login_button.config(state='normal', text="LOGIN")
                return

            # Try to connect to our database
            conn_str = f"DRIVER={{{driver_name}}};SERVER=.\\SQLEXPRESS;DATABASE=LoginSystemDB;Trusted_Connection=yes;Encrypt=no;"
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()

            # Check if table exists
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'Users'
            """)
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                messagebox.showwarning("Table Missing", "Users table not found. Please run Setup Database first.")
                login_button.config(state='normal', text="LOGIN")
                conn.close()
                return

            # Perform login query
            query = "SELECT username FROM Users WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                root.withdraw()
                open_main_window(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            conn.close()
            status_label.config(text="✅ Database login complete", fg="#27ae60")

        except pyodbc.Error as e:
            error_msg = str(e)
            if "LoginSystemDB" in error_msg:
                # Database doesn't exist
                if messagebox.askyesno("Database Not Found",
                                       "LoginSystemDB database not found.\n\nWould you like to create it now?"):
                    setup_database()
            else:
                messagebox.showerror("Database Error",
                                     f"Cannot connect to database:\n\n{error_msg}\n\nSwitching to simulation mode.")
                # Fall back to simple login
                simple_login()
        finally:
            login_button.config(state='normal', text="LOGIN")
    else:
        # Use simple login (no database)
        simple_login()


# ==================== MAIN APPLICATION WINDOW ====================
def open_main_window(username):
    main = tk.Toplevel()
    main.title(f"Main Application - {username}")
    main.geometry("700x500")
    main.configure(bg="#f4f6f9")

    main.transient(root)
    main.grab_set()

    tk.Label(
        main,
        text="✅ Login Successful!",
        font=("Helvetica", 24, "bold"),
        bg="#f4f6f9",
        fg="#27ae60"
    ).pack(pady=30)

    tk.Label(
        main,
        text=f"Welcome, {username}!",
        font=("Arial", 18),
        bg="#f4f6f9",
        fg="#2c3e50"
    ).pack(pady=10)

    tk.Label(
        main,
        text="Connected to SQL Server Database",
        font=("Arial", 12),
        bg="#f4f6f9",
        fg="#7f8c8d"
    ).pack(pady=5)

    # Content frame
    content_frame = tk.Frame(main, bg="#f4f6f9")
    content_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)

    # Display database info
    info_text = """Application Features:

    • Secure database authentication
    • User management system
    • Data persistence
    • SQL Server integration
    • Encrypted connections

    Status: Connected to LoginSystemDB
    Authentication: Windows Integrated Security
    """

    tk.Label(
        content_frame,
        text=info_text,
        font=("Courier", 10),
        bg="#f4f6f9",
        fg="#2c3e50",
        justify=tk.LEFT
    ).pack(anchor="w", pady=10)

    # Logout button
    tk.Button(
        main,
        text="Logout",
        font=("Arial", 12, "bold"),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        command=lambda: [main.destroy(), root.deiconify()],
        width=15,
        height=2
    ).pack(pady=30)

    def on_closing():
        main.destroy()
        root.deiconify()

    main.protocol("WM_DELETE_WINDOW", on_closing)


# ==================== GUI - LOGIN WINDOW ====================
root = tk.Tk()
root.title("SQL Server Login System")
root.geometry("500x600")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Title
title_frame = tk.Frame(root, bg="#2c3e50")
title_frame.pack(pady=30)

tk.Label(
    title_frame,
    text="🔐 Database Login System",
    font=("Helvetica", 26, "bold"),
    fg="#ecf0f1",
    bg="#2c3e50"
).pack()

tk.Label(
    title_frame,
    text="SQL Server Authentication",
    font=("Arial", 12),
    fg="#bdc3c7",
    bg="#2c3e50"
).pack(pady=5)

# Mode Selection
mode_frame = tk.Frame(root, bg="#2c3e50")
mode_frame.pack(pady=10)

use_database_var = tk.BooleanVar(value=True)
tk.Checkbutton(
    mode_frame,
    text="Use Database Authentication",
    variable=use_database_var,
    font=("Arial", 10),
    fg="#ecf0f1",
    bg="#2c3e50",
    selectcolor="#2c3e50",
    activebackground="#2c3e50"
).pack()

tk.Label(
    mode_frame,
    text="(Uncheck for simulation mode without database)",
    font=("Arial", 8),
    fg="#95a5a6",
    bg="#2c3e50"
).pack()

# Input Frame
input_frame = tk.Frame(root, bg="#34495e", bd=2, relief=tk.GROOVE)
input_frame.pack(pady=20, padx=50, fill=tk.X)

# Username
tk.Label(input_frame, text="Username", font=("Arial", 11, "bold"),
         fg="#ecf0f1", bg="#34495e").pack(pady=(10, 5))
entry_username = tk.Entry(input_frame, font=("Arial", 14),
                          width=25, justify="center", bd=2, relief=tk.SUNKEN)
entry_username.pack(pady=(0, 15))

# Password
tk.Label(input_frame, text="Password", font=("Arial", 11, "bold"),
         fg="#ecf0f1", bg="#34495e").pack(pady=(0, 5))
entry_password = tk.Entry(input_frame, font=("Arial", 14),
                          width=25, show="•", justify="center", bd=2, relief=tk.SUNKEN)
entry_password.pack(pady=(0, 20))

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#2c3e50")
buttons_frame.pack(pady=10)

# Login Button
login_button = tk.Button(
    buttons_frame,
    text="LOGIN",
    font=("Arial", 14, "bold"),
    bg="#27ae60",
    fg="white",
    activebackground="#2ecc71",
    command=login,
    height=2,
    width=15
)
login_button.pack(pady=5)

# Setup Button
tk.Button(
    buttons_frame,
    text="🔧 Setup Database",
    font=("Arial", 10),
    bg="#8e44ad",
    fg="white",
    command=setup_database,
    height=1,
    width=15
).pack(pady=5)

# Test Button
tk.Button(
    buttons_frame,
    text="🎯 Test Connection",
    font=("Arial", 10),
    bg="#3498db",
    fg="white",
    command=lambda: [check_odbc_driver(), connect_db()],
    height=1,
    width=15
).pack(pady=5)

# Status Label
status_label = tk.Label(
    root,
    text="Ready...",
    font=("Arial", 9),
    fg="#bdc3c7",
    bg="#2c3e50"
)
status_label.pack(pady=10)

# Test credentials
creds_frame = tk.Frame(root, bg="#2c3e50", bd=1, relief=tk.SUNKEN)
creds_frame.pack(pady=10, padx=30, fill=tk.X)

tk.Label(
    creds_frame,
    text="Test Credentials:",
    font=("Arial", 9, "bold"),
    fg="#ecf0f1",
    bg="#2c3e50"
).pack(pady=(5, 2))

tk.Label(
    creds_frame,
    text="admin / admin123  |  user1 / password123",
    font=("Arial", 9),
    fg="#95a5a6",
    bg="#2c3e50"
).pack(pady=(0, 5))

# Auto-focus
entry_username.focus()
entry_password.bind("<Return>", lambda event: login())

# Initial driver check
root.after(1000, lambda: check_odbc_driver())

root.mainloop()