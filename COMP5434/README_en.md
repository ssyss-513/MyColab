# Earthquake Alert Level Prediction with Custom XGBoost and SMOTE

## 1. Project Overview

This project focuses on predicting earthquake alert levels using a dataset of seismic measurements. The primary goal is to build and optimize an effective machine learning model that can classify the severity of an earthquake (`label`).

The entire analytical process is documented in the `5434_task1_test.ipynb` notebook. This project implements a **custom XGBoost (Extreme Gradient Boosting) model from scratch** and employs advanced techniques like **feature engineering** and **SMOTE (Synthetic Minority Over-sampling Technique)** to handle class imbalance.

## 2. Workflow

The project follows a structured machine learning workflow:

### Step 1: Data Acquisition & Exploration (EDA)
- **Load Data**: The training (`train.csv`) and testing (`test.csv`) datasets are loaded.
- **Exploratory Data Analysis**: The distributions of features (`magnitude`, `depth`, `cdi`, `mmi`, `sig`) and their relationships with the target `label` are visualized using histograms, boxplots, and pairplots.

### Step 2: Data Preprocessing & Feature Engineering
- **Outlier Removal**: Outliers are identified using the Z-score method and removed to create a cleaner dataset.
- **Feature Transformation**: A logarithmic transformation (`np.log1p`) is applied to the `depth` feature to normalize its distribution.
- **Feature Scaling**: `StandardScaler` is used on the `depth` and `sig` features.
- **Advanced Feature Engineering**: Based on EDA insights, new features are created to capture more complex relationships:
    - **Interaction Feature**: `cdi_mmi_interaction` (`cdi` * `mmi`)
    - **Polynomial Features**: `cdi_sq` (`cdi`^2) and `mmi_sq` (`mmi`^2)

### Step 3: Handling Class Imbalance with SMOTE
- The training data exhibits a significant class imbalance, which can bias the model.
- To address this, **SMOTE** from the `imbalanced-learn` library is applied to the training set (`X_train`).
- SMOTE synthetically generates new samples for the minority classes, resulting in a balanced training dataset (`X_resampled`, `y_resampled`). This helps the model learn the characteristics of all classes more effectively.

### Step 4: Model Implementation (Custom XGBoost)
A `CustomXGBoost` classifier is implemented from scratch.
- **Core Logic**: It is built on the principles of gradient boosting, using second-order derivatives (gradients and Hessians) for optimization, which is the hallmark of XGBoost.
- **Base Learners**: A series of `DecisionTree` regressors are built sequentially, where each new tree corrects the errors of the previous ones.
- **Multi-Class Strategy**: The model handles the multi-class problem using a **One-vs-Rest** approach, training a separate set of trees for each class.

### Step 5: Hyperparameter Tuning
- A **Grid Search** is performed to find the optimal hyperparameters for the `CustomXGBoost` model.
- The search is conducted by training the model on the **SMOTE-balanced data** (`X_resampled`) and evaluating its performance on the original, unbalanced validation set (`X_valid`). This ensures the model's generalization ability is tested on a realistic data distribution.
- The best combination of `learning_rate`, `max_depth`, `n_estimators`, etc., is selected based on the highest **Macro-F1 score**.

### Step 6: Final Training & Evaluation
- The final `CustomXGBoost` model is trained using the best hyperparameters on a fully resampled dataset (combining the original training and validation sets, then applying SMOTE).
- The model's performance is evaluated on the untouched test set (`X_test`) using a classification report and a confusion matrix.

### Step 7: Prediction and Submission
- The same preprocessing and feature engineering steps are applied to the official test data (`test.csv`).
- The final trained `CustomXGBoost` model is used to predict labels for the test set.
- The predictions are saved to `submission_xgb_final.csv`.

## 3. How to Run

1.  Ensure you have a Python environment with the necessary dependencies installed.
2.  Place `train.csv` and `test.csv` in the same directory as the notebook.
3.  Open and run the `5434_task1_test.ipynb` Jupyter Notebook from top to bottom. The notebook will automatically perform all steps and generate the `submission_xgb_final.csv` file.

## 4. Dependencies

- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `imbalanced-learn`
