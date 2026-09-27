# Module 2: Analytics & Machine Learning Pipeline

## Overview

This module performs exploratory data analysis and machine learning on the Titanic dataset. It covers data profiling, missing-value handling, outlier analysis, visualization, classification, class-imbalance handling, Random Forest hyperparameter tuning, and a fare regression task.

The committed `titanic.csv` file is used as the offline dataset for modeling.

---

## Part A: Data Profiling & Visual Interpretation

### Dataset

- Dataset: Titanic
- Total rows: 891
- Classification target: `survived`
- Class 0 — Died: 549 (61.62%)
- Class 1 — Survived: 342 (38.38%)

### Missing Value Strategy

- `deck`: removed because of its high percentage of missing values.
- `age`: median imputation is used because its missing percentage falls within the 5%–30% range.
- `embarked`: rows with missing values are removed because the missing percentage is below 5%.
- `embark_town`: not used because it duplicates the information represented by `embarked`.

For the classification pipeline:

- Numerical features use median imputation.
- Categorical features use most-frequent imputation.

### Outliers & Skewness

- Age and fare outliers were identified using the IQR method.
- Fare mean, median, and mode were compared to assess skewness.
- Fare contains high-value observations that are also reflected in the regression residual analysis.

### Correlation Analysis

The correlation matrix uses exactly:

`survived`, `pclass`, `age`, `sibsp`, `parch`, `fare`

The strongest absolute off-diagonal correlations are identified and interpreted in `01_eda.ipynb`.

### Visual Analysis

The analysis includes:

- Survival by sex
- Survival by passenger class
- Survival by sex and passenger class
- Age distribution
- Fare distribution
- Family-related variables
- Correlation analysis

---

## Part B: Predictive Modeling

### Data Preparation

Classification features:

```text
pclass
sex
age
sibsp
parch
fare
embarked
```

Target:

```text
survived
```

A stratified 80/20 train-test split was used:

```text
Training rows: 712
Testing rows : 179
```

The split uses:

```text
random_state=42
stratify=y
```

### Preprocessing & Standardization

Numerical features:

```text
pclass
age
sibsp
parch
fare
```

Processing:

```text
Median Imputation
       ↓
StandardScaler
```

Categorical features:

```text
sex
embarked
```

Processing:

```text
Most-Frequent Imputation
       ↓
One-Hot Encoding
```

Preprocessing is fitted only on the training data and then applied to the test data to prevent data leakage.

### Classification Models

Three classification models were trained:

- Logistic Regression
- Decision Tree
- Random Forest

### Classification Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8045 | 0.7931 | 0.6667 | 0.7244 | 0.8437 |
| Decision Tree | 0.7933 | 0.8636 | 0.5507 | 0.6726 | 0.8292 |
| Random Forest | 0.8156 | 0.8000 | 0.6957 | 0.7442 | 0.8287 |

### Confusion Matrices

The confusion matrices from the current modeling notebook are:

**Logistic Regression**

```text
[[98, 12],
 [23, 46]]
```

**Decision Tree**

```text
[[104, 6],
 [31, 38]]
```

**Random Forest**

```text
[[98, 12],
 [21, 48]]
```

Class labels:

```text
0 = Died
1 = Survived
```

### ROC Curves

ROC curves were generated for all three classification models.

ROC-AUC values:

- Logistic Regression: `0.8437`
- Decision Tree: `0.8292`
- Random Forest: `0.8287`

The ROC curve is saved as:

```text
outputs/roc_curves.png
```

### Random Forest OOB Score

The baseline Random Forest OOB score is:

```text
0.8034
```

---

## Class Imbalance

The classification target is moderately imbalanced:

```text
Class 0: 549
Class 1: 342
```

Training-set distribution:

```text
Class 0: 439
Class 1: 273
```

Three Random Forest approaches were compared:

1. Baseline Random Forest
2. Random Forest with `class_weight="balanced"`
3. Random Forest with `SMOTE`

SMOTE was applied only to the training data after the train-test split.

After SMOTE:

```text
Class 0: 439
Class 1: 439
```

### Imbalance Results

| Strategy | Precision | Recall | F1 Score |
|---|---:|---:|---:|
| Baseline | 0.8000 | 0.6957 | 0.7442 |
| Balanced Class Weight | 0.7463 | 0.7246 | 0.7353 |
| SMOTE | 0.7463 | 0.7246 | 0.7353 |

The complete imbalance analysis is implemented in `02_modeling.ipynb`.

---

## Random Forest Hyperparameter Tuning

`GridSearchCV` was used for Random Forest hyperparameter tuning.

Configuration:

```text
Cross-validation: 5-fold
Scoring metric: F1 Score
```

### Parameter Grid

```text
n_estimators: [50, 100]
max_depth: [3, 5, 10]
max_features: ["sqrt", "log2"]
```

### Best Parameters

The best configuration selected by GridSearchCV was:

```text
{
    'classifier__max_depth': 3,
    'classifier__max_features': 'sqrt',
    'classifier__n_estimators': 50
}
```

### Best Cross-Validation F1

```text
0.7472
```

### Tuned Random Forest Test Results

| Metric | Value |
|---|---:|
| Accuracy | 0.8045 |
| Precision | 0.8036 |
| Recall | 0.6522 |
| F1 Score | 0.7200 |
| ROC-AUC | 0.8323 |

### Tuned Random Forest OOB Score

```text
0.8076
```

### Tuned Random Forest Confusion Matrix

```text
[[99, 11],
 [24, 45]]
```

The tuned model is the classifier saved by the modeling pipeline after GridSearchCV.

---

## Fare Regression

### Regression Task

A Linear Regression model was used to predict:

```text
fare
```

The target variable `fare` is not used as an input feature.

Regression features:

```text
pclass
sex
age
sibsp
parch
embarked
```

The regression dataset contains 891 rows.

### Regression Preprocessing

Numerical features:

```text
pclass
age
sibsp
parch
```

Processing:

```text
Median Imputation
       ↓
StandardScaler
```

Categorical features:

```text
sex
embarked
```

Processing:

```text
Most-Frequent Imputation
       ↓
One-Hot Encoding
```

A `LinearRegression` model is fitted after preprocessing.

### Regression Results

| Metric | Value |
|---|---:|
| MAE | 20.8094 |
| RMSE | 30.4731 |
| R² | 0.3999 |
| Adjusted R² | 0.3679 |

---

## Residual Analysis & Heteroscedasticity

A residual plot was created by plotting predicted fare against regression residuals.

### Conclusion

The residual plot shows **evidence of heteroscedasticity**. The spread of residuals is not constant across the range of predicted fare values, and the residuals become more widely dispersed at higher predicted fare values.

Therefore:

```text
The fare regression residuals show evidence of heteroscedasticity.
```

The residual plot is saved as:

```text
outputs/fare_regression_residuals.png
```

### Actual vs Predicted Fare

An actual-versus-predicted fare plot is also generated to compare observed and predicted fare values.

Saved as:

```text
outputs/actual_vs_predicted_fare.png
```

---

## Saved Model Artifacts

### Classification Pipeline

The saved classification pipeline is:

```text
models/best_titanic_classifier.joblib
```

It contains the preprocessing steps and the final Random Forest classifier.

### Regression Pipeline

The saved regression pipeline is:

```text
models/fare_regression_pipeline.joblib
```

### Saved Model Verification

The classification pipeline was reloaded using `joblib` and tested using raw input.

Example input:

```text
pclass   = 1
sex      = female
age      = 28.0
sibsp    = 0
parch    = 0
fare     = 100.0
embarked = S
```

The reloaded pipeline successfully accepted the raw input and produced:

```text
Predicted class: 1
Predicted survival probability: 0.8610
```

This verifies that the saved classification pipeline can be reloaded and used with raw feature values.

---

## Final Model Recommendation

The final saved classifier is the **tuned Random Forest pipeline** selected through 5-fold `GridSearchCV` using F1 scoring. The selected hyperparameters are `max_depth=3`, `max_features="sqrt"`, and `n_estimators=50`, with a cross-validation F1 score of `0.7472`. On the held-out test set, the tuned Random Forest achieved an accuracy of `0.8045`, F1 score of `0.7200`, and ROC-AUC of `0.8323`. The baseline Random Forest had a higher held-out F1 score of `0.7442`, while Logistic Regression had the highest ROC-AUC of `0.8437`; these differences are reported explicitly to keep the model selection and evaluation results transparent.

---

## Project Files

```text
analytics/
│
├── README.md
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
│
├── models/
│   ├── best_titanic_classifier.joblib
│   └── fare_regression_pipeline.joblib
│
└── outputs/
    ├── classification_results.csv
    ├── imbalance_results.csv
    ├── grid_search_results.csv
    ├── regression_results.csv
    ├── roc_curves.png
    ├── decision_tree.png
    ├── fare_regression_residuals.png
    ├── actual_vs_predicted_fare.png
    ├── confusion_matrix_logistic_regression.png
    ├── confusion_matrix_decision_tree.png
    ├── confusion_matrix_random_forest.png
    └── tuned_random_forest_confusion_matrix.png
```

---

## How to Run

From the repository root:

```bash
cd analytics
```

Open the notebooks in this order:

```text
01_eda.ipynb
02_modeling.ipynb
```

Run `01_eda.ipynb` first and then run `02_modeling.ipynb`.

The modeling notebook performs:

1. Dataset loading
2. Feature and target preparation
3. Stratified train-test splitting
4. Missing-value handling
5. Standardization and one-hot encoding
6. Classification model training
7. Classification evaluation
8. Confusion-matrix generation
9. ROC curve generation
10. Class-imbalance analysis
11. SMOTE oversampling
12. Random Forest hyperparameter tuning
13. Fare regression
14. Residual analysis
15. Model serialization
16. Saved-model reload and verification

---

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- imbalanced-learn
- Joblib
- Jupyter Notebook

---

## Module Summary

```text
Titanic Dataset
      ↓
Data Profiling & EDA
      ↓
Missing-Value Handling
      ↓
Outlier & Correlation Analysis
      ↓
Feature Preprocessing
      ↓
Standardization & Encoding
      ↓
Classification
      ↓
Class-Imbalance Analysis
      ↓
SMOTE
      ↓
Random Forest Hyperparameter Tuning
      ↓
Fare Regression
      ↓
Residual Analysis
      ↓
Saved ML Pipelines
```