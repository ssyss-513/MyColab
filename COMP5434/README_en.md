# Earthquake Alert Level Prediction with Custom KNN

## 1. Project Overview

This project focuses on predicting earthquake alert levels using a dataset of seismic measurements. The primary goal is to build an effective machine learning model that can classify the severity of an earthquake (`label`) based on various features.

The entire analytical process is documented in the `5434_task1.ipynb` notebook, covering everything from data exploration and preprocessing to the implementation and evaluation of a custom K-Nearest Neighbors (KNN) model.

## 2. Workflow

The project follows a structured machine learning workflow:

### Step 1: Data Acquisition & Exploration (EDA)
- **Load Data**: The training (`train.csv`) and testing (`test.csv`) datasets are loaded using pandas.
- **Exploratory Data Analysis**:
    - **Histograms**: To understand the distribution of each feature (`magnitude`, `depth`, `cdi`, `mmi`, `sig`).
    - **Boxplots**: To visualize the relationship between each feature and the target `label`.
    - **Pairplots**: To observe interactions and correlations between features.

### Step 2: Data Preprocessing
- **Outlier Removal**: Outliers were identified using the Z-score method with a threshold of 3. Samples containing outliers were removed to create a cleaner dataset.
- **Feature Transformation**: A logarithmic transformation (`np.log1p`) was applied to the `depth` feature to normalize its highly skewed distribution.
- **Feature Scaling**: The `depth` and `sig` features were standardized using `StandardScaler` to ensure they have a mean of 0 and a standard deviation of 1, which is crucial for distance-based algorithms like KNN.

### Step 3: Model Implementation (Custom KNN)
A `CustomKNN` classifier was implemented from scratch with the following key capabilities:
- **Manhattan Distance**: Uses Manhattan distance for calculating neighbor proximity.
- **Feature Weighting**: Allows assigning different weights to each feature, enabling the model to prioritize more important features.
- **Distance-Weighted Voting**: Instead of simple majority voting, predictions are weighted by the inverse of the distance from the neighbors. Closer neighbors have a stronger influence on the outcome.

### Step 4: Hyperparameter Tuning
- A custom function, `find_best_k`, was created to perform 5-fold stratified cross-validation.
- This function iterates through a range of `k` values (from 1 to 20) to find the optimal number of neighbors that maximizes the **Macro-F1 score**.

### Step 5: Model Evaluation
- The performance of the final trained KNN model was assessed on a held-out test set.
- Key evaluation metrics included:
    - **Macro-F1 Score**: The primary metric for this multi-class classification problem.
    - **Classification Report**: Provides precision, recall, and F1-score for each class.
    - **Confusion Matrix**: Visualizes the model's performance in distinguishing between the different alert levels.

### Step 6: Prediction and Submission
- The same preprocessing steps were applied to the official test data (`test.csv`).
- The trained `CustomKNN` model was used to predict the labels for the test set.
- The final predictions were saved to `submission.csv` in the required format.

## 3. How to Run

1.  Ensure you have a Python environment with the necessary dependencies installed.
2.  Place the `train.csv` and `test.csv` files in the same directory as the notebook.
3.  Open and run the `5434_task1.ipynb` Jupyter Notebook from top to bottom. The notebook will automatically perform all steps and generate the `submission.csv` file.

## 4. Dependencies

- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `seaborn`
