# Earthquake Alert Level Prediction: A Comparative Study

## 1. Project Overview

This project tackles the prediction of earthquake alert levels from seismic data. It documents a comprehensive machine learning workflow, from initial data analysis to the implementation and evaluation of two distinct modeling strategies:
1.  A **Custom K-Nearest Neighbors (KNN)** model with feature weighting.
2.  A **Custom XGBoost** model enhanced with advanced feature engineering and **SMOTE** for handling class imbalance.

The entire process is captured in the `5434_task1.ipynb` and `5434_task1_test.ipynb` notebooks, showcasing a full cycle of model development, iteration, and optimization.

## 2. Common Workflow Steps

Both modeling approaches share a common foundation of data preparation.

### Step 1: Data Acquisition & Exploration (EDA)
- **Load Data**: The `train.csv` and `test.csv` datasets are loaded.
- **Exploratory Data Analysis**: Feature distributions and their relationships with the target `label` are visualized using histograms, boxplots, and pairplots to guide subsequent preprocessing and feature engineering decisions.

### Step 2: Data Preprocessing
- **Outlier Removal**: Outliers are identified using the Z-score method and removed to create a cleaner, more robust dataset.
- **Feature Transformation**: A logarithmic transformation (`np.log1p`) is applied to the `depth` feature to normalize its skewed distribution.
- **Feature Scaling**: `StandardScaler` is used to standardize the `depth` and `sig` features, ensuring they have a consistent scale.

---

## 3. Modeling Approach 1: Custom K-Nearest Neighbors (KNN)

This approach focuses on a from-scratch implementation of the KNN algorithm, enhanced with several custom features.

### 3.1. Model Implementation (Custom KNN)
A `CustomKNN` classifier was built with the following key capabilities:
- **Manhattan Distance**: Uses Manhattan distance for calculating neighbor proximity.
- **Feature Weighting**: Allows assigning different weights to each feature, enabling the model to prioritize more important features during distance calculation.
- **Distance-Weighted Voting**: Predictions are weighted by the inverse of the distance from the neighbors. Closer neighbors have a stronger influence on the final prediction, making the model more robust.

### 3.2. Hyperparameter Tuning
- A custom function, `find_best_k`, performs 5-fold stratified cross-validation to find the optimal number of neighbors (`k`).
- The best `k` is selected based on the value that maximizes the **Macro-F1 score**.

### 3.3. Evaluation and Submission
- The final KNN model is trained on the preprocessed data and evaluated on a held-out test set.
- Predictions for the official test data are generated and saved to `submission.csv`.

---

## 4. Modeling Approach 2: Custom XGBoost with SMOTE

This approach uses a more complex, gradient-based model and tackles the problem of class imbalance directly.

### 4.1. Advanced Feature Engineering
In addition to the common preprocessing, specific features were engineered to boost the XGBoost model's performance:
- **Interaction Feature**: `cdi_mmi_interaction` (`cdi` * `mmi`)
- **Polynomial Features**: `cdi_sq` (`cdi`^2) and `mmi_sq` (`mmi`^2)

### 4.2. Handling Class Imbalance with SMOTE
- To counteract the model's potential bias towards majority classes, **SMOTE (Synthetic Minority Over-sampling Technique)** is used.
- SMOTE synthetically creates new samples for the minority classes in the training set, resulting in a balanced dataset that allows the model to learn all class characteristics effectively.

### 4.3. Model Implementation (Custom XGBoost)
A `CustomXGBoost` classifier is implemented from scratch.
- **Core Logic**: It is built on gradient boosting principles, using second-order derivatives (gradients and Hessians) for optimization.
- **Base Learners**: It sequentially builds a series of `DecisionTree` regressors, where each new tree corrects the errors of the previous ones.
- **Multi-Class Strategy**: A **One-vs-Rest** approach is used, where a separate set of trees is trained for each class.

### 4.4. Hyperparameter Tuning
- A **Grid Search** is performed to find the optimal hyperparameters for the `CustomXGBoost` model.
- The search is conducted by training on the **SMOTE-balanced data** and validating on the original, unbalanced validation set to ensure real-world generalization.

### 4.5. Evaluation and Submission
- The final XGBoost model is trained on a fully resampled dataset using the best hyperparameters.
- Its performance is evaluated on the untouched test set, and final predictions are saved to `submission_xgb_final.csv`.

## 5. How to Run

1.  Ensure you have a Python environment with all dependencies installed.
2.  Place `train.csv` and `test.csv` in the same directory.
3.  Open and run either `5434_task1.ipynb` (for KNN) or `5434_task1_test.ipynb` (for XGBoost) to reproduce the results for each approach.

## 6. Dependencies

- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `imbalanced-learn` (for the XGBoost approach)
