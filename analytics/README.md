# Module 2: Analytics & Machine Learning Pipeline (`/analytics`)

## Overview

This module profiles and models the Titanic dataset through a unified analytics and machine learning pipeline. The dataset is loaded locally from `analytics/data/titanic.csv` and processed through data profiling, cleaning, visualization, classification, class imbalance handling, hyperparameter tuning, and regression.

---

## Part A: Data Profiling & Visual Interpretation

### 1. Missing Value Strategy & Thresholds

* **`deck`:** The column contains a high percentage of missing values and was removed during preprocessing.

* **`age`:** Missing values were handled using **median imputation** to preserve the dataset while reducing the effect of extreme values.

* **`embarked`:** Rows with missing `embarked` values were removed because the number of missing records was very small.

* **`embark_town`:** Removed as a redundant representation of the `embarked` information.

### 2. Outliers & Skewness

* **Age Outliers:** Outliers were identified using the IQR rule (`Q1 - 1.5 × IQR` and `Q3 + 1.5 × IQR`).

* **Fare Outliers:** Fare contains noticeable high-value observations, which were identified using the IQR method.

* **Fare Skewness:** The mean fare is higher than the median fare, indicating a **right-skewed distribution** caused by relatively high fare values.

### 3. Correlation Matrix & Top 2 Off-Diagonal Features

The correlation matrix was calculated strictly on the six numeric columns (`survived`, `pclass`, `age`, `sibsp`, `parch`, `fare`):

1. **`pclass` & `fare`:** A negative relationship is observed between passenger class and fare. Lower class numbers are associated with higher fare values.

2. **`sibsp` & `parch`:** A positive relationship is observed, indicating that passengers traveling with siblings/spouses also tended to have parents/children recorded in the dataset.

### 4. Visual Data Story Conclusions

1. **Gender & Class:** Survival rates vary considerably across passenger gender and class groups.

2. **Class & Fare:** Passenger class and fare show noticeable relationships with survival outcomes.

3. **Age Distribution:** Survival patterns vary across different age groups.

4. **Family Size Dynamics:** Survival rates differ across passengers with different family-related characteristics represented by `sibsp` and `parch`.

---

## Part B: Predictive Modeling & Recommendations

### Combined Model Comparison Table

| Model Type     | Algorithm                          | Metric 1        | Metric 2         | Metric 3      | Metric 4        | Metric 5       |
| :------------- | :--------------------------------- | :-------------- | :--------------- | :------------ | :-------------- | :------------- |
| **Classifier** | **Logistic Regression**            | **Accuracy:** — | **Precision:** — | **Recall:** — | **F1-Score:** — | **ROC-AUC:** — |
| **Classifier** | **Decision Tree (Max Depth=4)**    | **Accuracy:** — | **Precision:** — | **Recall:** — | **F1-Score:** — | **ROC-AUC:** — |
| **Classifier** | **Random Forest (Tuned)**          | **Accuracy:** — | **Precision:** — | **Recall:** — | **F1-Score:** — | **ROC-AUC:** — |
| **Regressor**  | **Multivariate Linear Regression** | **MAE:** —      | **RMSE:** —      | **R²:** —     | **Adj R²:** —   | N/A            |

### Class Imbalance & Hyperparameter Tuning

* **Imbalance Handling:** The project compares a baseline Random Forest, class-weighted Random Forest, and SMOTE applied **only to the training data**.

* **GridSearchCV:** Hyperparameter tuning is performed using 5-fold cross-validation with F1-score as the scoring metric.

* **Random Forest OOB Score:** The Random Forest model uses out-of-bag evaluation to provide an additional validation measure.

* **Regression Residuals:** A residual plot is generated to examine the relationship between predicted and actual fare values and identify potential non-constant variance.

---

## Final Recommendation

The final model selection is based on the evaluation results produced by `02_modeling.ipynb`. Classification models are compared using Accuracy, Precision, Recall, F1-Score, and ROC-AUC, while the regression model is evaluated using MAE, RMSE, R², and Adjusted R².
