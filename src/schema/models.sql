-- Product_ID,Product_Name, Merchant_ID, Cluster_ID, Cluster_Label, Category_ID,Category,Price,StockQuantity,Description,Rating
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL
    merchant_id INTEGER NOT NULL,
    cluster_id INTEGER NOT NULL,
    cluster_label TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    description TEXT,
    rating DECIMAL(3, 2)
);

-- Merchant ID,MerchantName,MerchantLocation,MerchantRating
CREATE TABLE Orders (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    order_status TEXT NOT NULL,
    return_eligible BOOLEAN NOT NULL,
    shipping_date DATE NOT NULL
);


-- Vectorizes columns to create a search index, which will help the model query on partial text.
ALTER TABLE "products" ADD COLUMN "search" tsvector GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(product_name, '') || ' ' || coalesce(description, ''))
) STORED;



CREATE INDEX "idx_search_gin" ON "products" USING GIN ("search")


ALTER TABLE "orders" ADD COLUMN "search" tsvector GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(product_name, '') || ' ' || coalesce(category, ''))
) STORED;



CREATE INDEX "idx_search_gin" ON "orders" USING GIN ("search")

-- Ensure you have the Database created in RDS, and is publicly accessible.
-- install pgadmin (Postgres DB Client) and create a new server connection. Specify db endpoint, port, username, password.
-- Run the above SQL statements in PGADMIN SQL Editor, to create the tables.
-- Once the tables are created, import the data from the CSV files into the tables.
-- Test the queries in the SQL Editor, to ensure the data is imported correctly.



