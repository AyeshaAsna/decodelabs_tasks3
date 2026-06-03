# decodelabs_tasks3
Use SQL queries to extract meaningful insights from a dataset and demonstrate the application of SQL fundamentals for data analysis.

# Project-3: SQL Data Analysis

## Goal

Use SQL queries to extract meaningful insights from a dataset and demonstrate the application of SQL fundamentals for data analysis.

## Project Objective

The objective of this project is to load a dataset into a SQLite database and perform SQL-based analysis using filtering, sorting, grouping, and aggregation techniques to generate business insights.

## Key Requirements

- Write SELECT queries
- Use WHERE clause
- Use ORDER BY clause
- Use GROUP BY clause
- Perform aggregations using:
  - COUNT()
  - SUM()
  - AVG()

## Key Skills Demonstrated

- SQL Fundamentals
- Data Querying
- Data Filtering
- Data Grouping
- Data Aggregation
- Database Management
- Analytical Thinking

## Technologies Used

- Python
- SQLite
- Pandas

## Features Implemented

### Dataset Loading
- Reads dataset from Excel file
- Loads data into SQLite database
- Creates a structured SQL table for analysis

### SQL Query Operations

#### 1. SELECT Query
Displays sample records from the dataset.

```sql
SELECT *
FROM orders_data
LIMIT 10;
```

#### 2. WHERE + ORDER BY
Filters high-value orders and sorts them.

```sql
SELECT *
FROM orders_data
WHERE TotalPrice > 1000
ORDER BY TotalPrice DESC;
```

#### 3. GROUP BY + COUNT
Counts the number of orders for each product.

```sql
SELECT Product,
COUNT(*) AS OrderCount
FROM orders_data
GROUP BY Product;
```

#### 4. GROUP BY + SUM + AVG
Calculates revenue and average order values by payment method.

```sql
SELECT PaymentMethod,
COUNT(*),
SUM(TotalPrice),
AVG(TotalPrice)
FROM orders_data
GROUP BY PaymentMethod;
```

#### 5. WHERE + GROUP BY + AVG
Analyzes average order value by order status.

```sql
SELECT OrderStatus,
AVG(TotalPrice)
FROM orders_data
WHERE TotalPrice >= 500
GROUP BY OrderStatus;
```

## Outputs Generated

### SQLite Database
`project3_dataset.db`

Stores the dataset in SQL format.

### SQL Summary Report
`project3_sql_summary.txt`

Contains:
- Query observations
- Key findings
- Business insights

### Query Result Files

- q1_basic_select.csv
- q2_where_orderby.csv
- q3_groupby_count.csv
- q4_groupby_aggregations.csv
- q5_filtered_group_avg.csv

Each CSV stores the result of a SQL query.

## Workflow

1. Load Excel dataset
2. Create SQLite database
3. Import data into SQL table
4. Execute SQL queries
5. Perform filtering and grouping
6. Generate aggregations
7. Save query outputs
8. Summarize insights

## Learning Outcomes

Through this project, the following concepts were applied:

- SQL Query Writing
- Data Filtering with WHERE
- Data Sorting with ORDER BY
- Data Grouping with GROUP BY
- Aggregation Functions
- Database Analysis
- Business Insight Generation

## How to Run

Install required libraries:

```bash
pip install pandas openpyxl
```

Run the script:

```bash
python project3.py
```

## Author

Ayesha Asna

DecodeLabs Internship
