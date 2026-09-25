# Module 1: Data Engineering Pipeline

## Overview

This module builds the data pipeline for the Zepto project. The pipeline collects book data from the public practice website `books.toscrape.com`, cleans and transforms the scraped data, converts the prices from GBP to INR using the given fixed conversion rate, and stores the final data in a normalized SQLite database.

The pipeline also runs SQL queries to check the stored data and verify that the database is working correctly.

## What I Built

The pipeline performs the following steps:

1. Scrapes books from the required categories.
2. Extracts the book title, price, rating, category and other required fields.
3. Cleans the scraped data.
4. Converts the rating from words such as `One`, `Two`, `Three`, `Four`, and `Five` into numbers.
5. Converts GBP prices into INR using:

   `1 GBP = 105.50 INR`

6. Creates a SQLite database.
7. Stores the data using two related tables:
   - `categories`
   - `books`
8. Uses a foreign key to connect books with their categories.
9. Runs SQL queries to verify and test the database.
10. Performs final validation of the processed data.

## Categories Used

The pipeline collects books from:

- Travel
- Mystery
- Historical Fiction

The pipeline produced **69 verified records** after cleaning and validation.

## Project Structure

```text
data_pipeline/
│
├── README.md
├── data_pipeline.py
└── zepto_store.db
