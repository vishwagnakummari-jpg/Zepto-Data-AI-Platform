# Module 2: Analytics & Machine Learning Pipeline

## Overview

This module performs exploratory data analysis and machine learning on the Titanic dataset. It covers data profiling, missing-value handling, outlier analysis, visualization, classification, class-imbalance handling, Random Forest tuning, and a fare regression task.

The committed `titanic.csv` file is used as the offline dataset for modeling.

---

## Part A: Data Profiling & Visual Interpretation

### Missing Value Strategy

- `deck`: removed because of its high percentage of missing values.
- `age`: median imputation was used because its missing percentage falls within the 5%–30% range.
- `embarked`: rows with missing values were removed because the missing percentage is below 5%.
- `embark_town`: not used because it duplicates the information represented by `embarked`.

### Outliers & Skewness

- Age and fare outliers were identified using the IQR method.
- Fare mean, median, and mode were compared to assess its skewness.

### Correlation Analysis

The correlation matrix uses exactly:

`survived`, `pclass`, `age`, `sibsp`, `parch`, `fare`

The strongest absolute off-diagonal correlations are identified and interpreted in `01_eda.ipynb`.

### Visual Analysis

The analysis includes:

- Survival by sex
- Survival by passenger class
- Survival by sex and passenger class
- Age and fare distributions
- Family-related variables
- Correlation analysis

---

## Part B: Predictive Modeling

### Data Preparation

Classification features:

`pclass`, `sex`, `age`, `sibsp`, `parch`, `fare`, `embarked`

A stratified 80/20 train-test split was used.

Numerical features were median-imputed and standardized. Categorical features were imputed using the most frequent value and one-hot encoded.

Preprocessing was fitted on the training data and applied to the test data.

### Classification Models

- Logistic Regression
- Decision Tree
- Random Forest

### Classification Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | **0.8090** | **0.7833** | **0.6912** | **0.7344** | **0.8610** |
| Decision Tree | **0.8090** | **0.8148** | **0.6471** | **0.7200** | Reported in notebook |
| Random Forest | **0.8202** | **0.7813** | **0.7353** | **0.7576** | Reported in notebook |

### Confusion Matrices

- Logistic Regression: `[[97, 13], [21, 47]]`
- Decision Tree: `[[100, 10], [24, 44]]`
- Random Forest: `[[96, 14], [18, 50]]`

---

## Class Imbalance

Three Random Forest approaches were compared:

1. Baseline Random Forest
2. Random Forest with `class_weight="balanced"`
3. Custom SMOTE-style oversampling applied only to the training data

SMOTE-style oversampling was performed after the train/test split, using only the training data.

The Accuracy, Precision, Recall, F1 Score, and ROC-AUC results are reported in `02_modeling.ipynb`.

---

## Random Forest Hyperparameter Tuning

`GridSearchCV` was used with 5-fold cross-validation and F1 Score as the scoring metric.

### Best Parameters

```text
{
    'max_depth': 5,
    'max_features': 'sqrt',
    'n_estimators': 50
}