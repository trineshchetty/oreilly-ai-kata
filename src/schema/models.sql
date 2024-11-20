-- Product_ID,Product_Name, Merchant_ID, Cluster_ID, Cluster_Label, Category_ID,Category,Price,StockQuantity,Description,Rating
CREATE TABLE Products (
    Product_ID INTEGER PRIMARY KEY,
    Product_Name TEXT NOT NULL,
    Merchant_ID INTEGER NOT NULL,
    Cluster_ID INTEGER NOT NULL,
    Cluster_Label TEXT NOT NULL,
    Category_ID INTEGER NOT NULL,
    Category TEXT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    StockQuantity INTEGER NOT NULL,
    Description TEXT,
    Rating DECIMAL(3, 2)
);

-- Merchant ID,MerchantName,MerchantLocation,MerchantRating
CREATE TABLE Orders (
    Product_ID INTEGER PRIMARY KEY,
    ProductName TEXT NOT NULL,
    Category TEXT NOT NULL,
    Category_ID INTEGER NOT NULL,
    Order_ID INTEGER NOT NULL,
    Customer_ID INTEGER NOT NULL,
    Order_Status TEXT NOT NULL,
    Return_Eligible BOOLEAN NOT NULL,
    ShippingDate DATETIME NOT NULL
);

-- Ensure you have the Database created in RDS, and is publicly accessible.
-- install pgadmin (Postgres DB Client) and create a new server connection. Specify db endpoint, port, username, password.
-- Run the above SQL statements in PGADMIN SQL Editor, to create the tables.
-- Once the tables are created, import the data from the CSV files into the tables.
-- Test the queries in the SQL Editor, to ensure the data is imported correctly.
