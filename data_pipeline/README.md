# Module 1: Data Engineering Pipeline

## Overview

This module builds an end-to-end data engineering pipeline using data scraped from `books.toscrape.com`.

The pipeline:

* Scrapes books from **Travel, Mystery, and Historical Fiction**
* Cleans and transforms the data
* Converts GBP prices to INR using the required fixed rate
* Stores the data in a normalized SQLite database
* Runs SQL validation queries
* Compares SQL results with equivalent Pandas operations

**Verified records: 69**

---

## Data Processing

### Categories

* Travel
* Mystery
* Historical Fiction

### Price Conversion

The required fixed conversion rate is:

```text
1 GBP = 105.50 INR
```

```text
price_inr = price_gbp × 105.50
```

Prices are rounded to two decimal places.

### Rating Conversion

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

### Availability Conversion

```text
In Stock     → 1
Not In Stock → 0
```

---

## SQLite Database

Database:

```text
zepto_store.db
```

The database contains two normalized tables.

### `categories`

```text
category_id     PRIMARY KEY
category_name
```

### `books`

```text
book_id         PRIMARY KEY
title
price_gbp
price_inr
rating
in_stock
category_id     FOREIGN KEY
```

The relationship is:

```text
categories.category_id
        ↓
books.category_id
```

---

## SQL Validation

The pipeline executes five SQL queries covering the required operations.

### Query 1 — SELECT / WHERE / LIMIT

```sql
SELECT title, price_gbp, price_inr, rating
FROM books
WHERE rating = 5
LIMIT 5;
```

### Query 2 — ORDER BY / LIMIT

```sql
SELECT title, price_inr, rating
FROM books
ORDER BY price_inr DESC
LIMIT 5;
```

### Query 3 — DISTINCT

```sql
SELECT DISTINCT rating
FROM books
ORDER BY rating ASC;
```

### Query 4 — BETWEEN / IN

```sql
SELECT title, price_gbp, rating
FROM books
WHERE price_gbp BETWEEN 10.0 AND 30.0
  AND rating IN (4, 5)
LIMIT 5;
```

### Query 5 — JOIN

```sql
SELECT b.title, c.category_name, b.price_inr, b.rating
FROM books b
JOIN categories c
    ON b.category_id = c.category_id
WHERE b.rating = 5
ORDER BY b.price_inr DESC
LIMIT 5;
```

---

## Query Results

The following outputs should be copied from the **latest execution of `data_pipeline.py`**.

### Query 1

```text
PASTE ACTUAL QUERY 1 OUTPUT HERE
```

### Query 2

```text
PASTE ACTUAL QUERY 2 OUTPUT HERE
```

### Query 3

```text
PASTE ACTUAL QUERY 3 OUTPUT HERE
```

### Query 4

```text
PASTE ACTUAL QUERY 4 OUTPUT HERE
```

### Query 5

```text
PASTE ACTUAL QUERY 5 OUTPUT HERE
```

---

## SQL vs Pandas Validation

The pipeline verifies the SQL JOIN using both SQL and Pandas.

**SQL:**

```python
pd.read_sql()
```

**Pandas:**

```python
pd.merge()
```

The results are compared directly.

Expected validation output:

```text
Outputs Match Exactly? --> True
```

---

## Project Structure

```text
data_pipeline/
│
├── README.md
├── data_pipeline.py
└── zepto_store.db
```

---

## How to Run

From the `data_pipeline` directory:

```bash
python data_pipeline.py
```

Pipeline flow:

```text
Web Scraping
     ↓
Data Cleaning
     ↓
Rating & Availability Conversion
     ↓
GBP → INR Conversion
     ↓
SQLite Database
     ↓
SQL Validation
     ↓
Pandas Validation
```

The SQLite database is recreated on each run to provide a fresh, reproducible dataset and prevent duplicate records.

---

## Technology Stack

* Python
* Requests
* BeautifulSoup
* Pandas
* SQLite
* SQL
* Regular Expressions

---

## Final Validation

Module 1 demonstrates:

* Web scraping from `books.toscrape.com`
* Three required book categories
* Data cleaning and transformation
* Fixed GBP-to-INR conversion
* Normalized SQLite database
* Primary and foreign keys
* Five SQL validation queries
* SQL JOIN
* SQL/Pandas equivalence validation
* Reproducible database generation
* 69 verified processed records
