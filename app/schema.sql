-- schema.sql
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Phone NVARCHAR(30) NOT NULL,
    Email NVARCHAR(100) NULL,
    Address NVARCHAR(200) NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE Technicians (
    TechnicianID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Phone NVARCHAR(30) NOT NULL,
    SkillLevel NVARCHAR(50) NOT NULL, -- e.g., "Junior", "Senior"
    Active BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE ServiceOrders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    TechnicianID INT NULL,
    ServiceType NVARCHAR(50) NOT NULL, -- e.g., "Repair", "Tuning", "Installation"
    Description NVARCHAR(400) NULL,
    Status NVARCHAR(30) NOT NULL DEFAULT 'Pending', -- Pending, Assigned, In Progress, Completed, Canceled
    ScheduledAt DATETIME2 NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_ServiceOrders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    CONSTRAINT FK_ServiceOrders_Technicians FOREIGN KEY (TechnicianID) REFERENCES Technicians(TechnicianID)
);

-- Helpful indexes
CREATE INDEX IX_ServiceOrders_Status ON ServiceOrders(Status);
CREATE INDEX IX_ServiceOrders_CustomerID ON ServiceOrders(CustomerID);
CREATE INDEX IX_ServiceOrders_TechnicianID ON ServiceOrders(TechnicianID);
