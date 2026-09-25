import os
import re
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
BASE_URL = "https://books.toscrape.com/"
GBP_TO_INR = 105.50  # Required fixed baseline conversion rate (1 GBP = 105.50 INR)
DB_PATH = os.path.join(os.path.dirname(__file__), "zepto_store.db")

# Standard Browser Headers to bypass HTTP 403 Forbidden
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Categories to scrape (guarantees ≥ 60 books across ≥ 3 categories)
TARGET_CATEGORIES = [
    {"name": "Travel", "url": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"},
    {"name": "Mystery", "url": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"},
    {"name": "Historical Fiction", "url": "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"}
]

# ==========================================
# 1. SCRAPING MODULE
# ==========================================
def scrape_category_books():
    print("--- [1/5] Scraping books across target categories ---")
    raw_records = []

    for cat in TARGET_CATEGORIES:
        cat_name = cat["name"]
        current_url = cat["url"]
        
        while current_url:
            response = requests.get(current_url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Failed to load URL {current_url} | Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article", class_="product_pod")

            for article in articles:
                # Title
                title_tag = article.h3.find("a")
                title = title_tag["title"] if title_tag and "title" in title_tag.attrs else title_tag.text

                # Price
                price_text = article.find("p", class_="price_color").text

                # Star Rating
                rating_classes = article.find("p", class_="star-rating")["class"]
                rating_text = [c for c in rating_classes if c != "star-rating"][0] if len(rating_classes) > 1 else None

                # Availability Status
                availability_text = article.find("p", class_="instock availability").text.strip()

                raw_records.append({
                    "title": title,
                    "price_raw": price_text,
                    "rating_raw": rating_text,
                    "availability_raw": availability_text,
                    "category_name": cat_name
                })

            # Handle Pagination within Category
            next_button = soup.find("li", class_="next")
            if next_button and next_button.find("a"):
                next_rel_path = next_button.find("a")["href"]
                # Build correct relative URL for nested category paths
                parent_path = current_url.rsplit("/", 1)[0]
                current_url = f"{parent_path}/{next_rel_path}"
            else:
                current_url = None

    df_raw = pd.DataFrame(raw_records)
    print(f"Successfully scraped {len(df_raw)} raw rows across {df_raw['category_name'].nunique()} categories.")
    return df_raw

# ==========================================
# 2. DATA CLEANING & CONVERSION MODULE
# ==========================================
def clean_and_transform_data(df):
    print("\n--- [2/5] Cleaning raw fields and applying currency conversion ---")

    # A. Strip Currency Symbol and Parse Price (float)
    df["price_gbp"] = df["price_raw"].apply(lambda x: re.sub(r"[^\d.]", "", str(x)))
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")

    # Median Imputation Strategy for Numeric Parsing Failures
    if df["price_gbp"].isnull().any():
        median_price = df["price_gbp"].median()
        df["price_gbp"].fillna(median_price, inplace=True)
        print(f"Applied median imputation for missing prices: {median_price:.2f} GBP")

    # B. Map Rating Text to Integer (1-5)
    df["rating"] = df["rating_raw"].map(RATING_MAP)
    if df["rating"].isnull().any():
        mode_rating = df["rating"].mode()[0]
        df["rating"].fillna(mode_rating, inplace=True)
        print(f"Applied mode imputation for missing ratings: {mode_rating}")
    df["rating"] = df["rating"].astype(int)

    # C. Parse Availability into Boolean Integer (1 = In Stock, 0 = Out of Stock)
    df["in_stock"] = df["availability_raw"].apply(lambda x: 1 if "In stock" in str(x) else 0)

    # D. Compute price_inr using required fixed baseline conversion (1 GBP = 105.50 INR)
    df["price_inr"] = (df["price_gbp"] * GBP_TO_INR).round(2)

    cleaned_df = df[["title", "price_gbp", "price_inr", "rating", "in_stock", "category_name"]]
    print(f"Cleaned dataset ready with {len(cleaned_df)} verified rows.")
    return cleaned_df

# ==========================================
# 3. RELATIONAL DATABASE MODULE (SQLite)
# ==========================================
def populate_relational_database(df):
    print("\n--- [3/5] Setting up 2-Table Foreign Key SQLite Schema ---")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Table 1: Primary Dimension Table
    cursor.execute("""
    CREATE TABLE categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    );
    """)

    # Table 2: Fact/Entity Table with Foreign Key
    cursor.execute("""
    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price_gbp REAL NOT NULL,
        price_inr REAL NOT NULL,
        rating INTEGER NOT NULL,
        in_stock INTEGER NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    );
    """)

    # Populate categories
    unique_cats = df["category_name"].unique()
    for cat in unique_cats:
        cursor.execute("INSERT INTO categories (category_name) VALUES (?);", (cat,))
    conn.commit()

    # Map category names to foreign keys
    cat_mapping = pd.read_sql("SELECT * FROM categories", conn).set_index("category_name")["category_id"].to_dict()
    df["category_id"] = df["category_name"].map(cat_mapping)

    # Insert into books table
    books_data = df[["title", "price_gbp", "price_inr", "rating", "in_stock", "category_id"]]
    books_data.to_sql("books", conn, if_exists="append", index=False)

    conn.close()
    print("Database zepto_store.db created and populated successfully.")

# ==========================================
# 4. EXECUTING REQUIRED SQL QUERIES
# ==========================================
def execute_sql_queries():
    print("\n--- [4/5] Executing 5 SQL Queries (Covering all required clauses) ---")
    conn = sqlite3.connect(DB_PATH)

    queries = {
        "Query 1 (SELECT/WHERE/LIMIT - 5-star books)": """
            SELECT title, price_gbp, price_inr, rating 
            FROM books 
            WHERE rating = 5 
            LIMIT 5;
        """,
        "Query 2 (ORDER BY/LIMIT - Highest Price in INR)": """
            SELECT title, price_inr, rating 
            FROM books 
            ORDER BY price_inr DESC 
            LIMIT 5;
        """,
        "Query 3 (DISTINCT - Unique Ratings in Store)": """
            SELECT DISTINCT rating 
            FROM books 
            ORDER BY rating ASC;
        """,
        "Query 4 (IN / BETWEEN - Price Range & High Rating)": """
            SELECT title, price_gbp, rating 
            FROM books 
            WHERE price_gbp BETWEEN 10.0 AND 30.0 
              AND rating IN (4, 5) 
            LIMIT 5;
        """,
        "Query 5 (JOIN - Multi-Table Category Relational Join)": """
            SELECT b.title, c.category_name, b.price_inr, b.rating
            FROM books b
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.rating = 5
            ORDER BY b.price_inr DESC
            LIMIT 5;
        """
    }

    for description, sql_str in queries.items():
        print(f"\n>>> {description}")
        res_df = pd.read_sql(sql_str, conn)
        print(res_df.to_string(index=False))

    conn.close()

# ==========================================
# 5. PANDAS vs SQL EQUIVALENCE CHECK
# ==========================================
def verify_pandas_sql_equivalence():
    print("\n--- [5/5] Demonstrating Equivalence between pd.read_sql and pd.merge ---")
    conn = sqlite3.connect(DB_PATH)

    join_query = """
    SELECT b.book_id, b.title, c.category_name, b.price_inr, b.rating
    FROM books b
    JOIN categories c ON b.category_id = c.category_id
    WHERE b.rating = 5
    ORDER BY b.price_inr DESC
    LIMIT 5;
    """

    # Approach A: Direct SQL via pd.read_sql
    df_sql = pd.read_sql(join_query, conn)

    # Approach B: Pure In-Memory Pandas pd.merge
    df_books = pd.read_sql("SELECT * FROM books", conn)
    df_categories = pd.read_sql("SELECT * FROM categories", conn)

    df_merged = pd.merge(df_books, df_categories, on="category_id")
    df_merged = df_merged[df_merged["rating"] == 5]
    df_merged = df_merged.sort_values(by="price_inr", ascending=False).head(5)
    df_pandas = df_merged[["book_id", "title", "category_name", "price_inr", "rating"]].reset_index(drop=True)

    print("\n[Method A: pd.read_sql output]:")
    print(df_sql.to_string(index=False))

    print("\n[Method B: pd.merge in-memory output]:")
    print(df_pandas.to_string(index=False))

    # Strict Equality Assertion
    are_equal = df_sql.equals(df_pandas)
    print(f"\nOutputs Match Exactly? --> {are_equal}")
    conn.close()

if __name__ == "__main__":
    df_raw = scrape_category_books()
    df_clean = clean_and_transform_data(df_raw)
    populate_relational_database(df_clean)
    execute_sql_queries()
    verify_pandas_sql_equivalence()