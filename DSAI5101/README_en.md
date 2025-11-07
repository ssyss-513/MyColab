# LoL Esports Match Outcome Prediction

This project aims to predict the outcome of professional League of Legends matches using machine learning models. It explores various feature engineering methods and classification models, with detailed performance evaluations.

## 📁 Project Directory Structure

```text
.
├── Esports dataset
│   ├── my        # Data and code
│   ├── pic       # Images or visualizations
│   └── data      # Raw data files
├── player_winrate_over10.csv
├── position_stats_combined.csv
└── README.md
```

## 🚀 Core Project Workflow

The project workflow is primarily divided into the following steps, all implemented in the `randomForest_XGB.ipynb` file:

1.  **Data Loading and Merging**: Load match data, player solo queue data, and global champion statistics.
2.  **Feature Engineering**: Construct key features from the raw data to quantify the skill gap between the two teams.
3.  **Model Training**: Train various machine learning models (Random Forest, XGBoost, Logistic Regression, SVM).
4.  **Model Evaluation**: Evaluate model performance using accuracy, F1-score, confusion matrices, and 10-fold cross-validation.

## 📊 Data Sources

This project uses three types of data:

| Filename | Path | Description |
| :--- | :--- | :--- |
| `2021_worlds_kda_with_result.csv` | `./data/` | Detailed match data from the 2021 World Championship, including teams, players, and champions used. |
| `pro_player_champion_stats.xlsx` | `./data/` | Global statistics for each champion in different positions in professional play, such as pick rate and win rate. |
| `solo_stats.csv` | `./data/` | Solo queue data for professional players during the competition period, including win rates and games played on specific champions. |

## 🛠️ Feature Engineering

Feature engineering is the core of this project. We constructed features that reflect the skill difference between teams through the following steps:

1.  **Data Matching**:
    *   For each player in every match, match their **global champion data** (e.g., the champion's general win rate in professional play).
    *   For each player in every match, match their **personal solo queue data** (e.g., the player's solo queue win rate with that champion).

2.  **Team-Level Aggregation**:
    *   Aggregate player-level features (like global win rate, solo queue win rate) at the team level to calculate the **average feature value** for each team.

3.  **Calculating Difference Features**:
    *   Merge the data for the two teams in the same match and calculate the **difference** in their average features. These differences are the final input features for model training, for example:
        *   `winrate_diff`: The difference in the average global champion win rates between the two teams.
        *   `picks_diff`: The difference in the average global champion pick counts between the two teams.
        *   `solo_winrate_diff`: The difference in the average solo queue win rates of the players on the two teams.

## 🤖 Modeling and Analysis

We used four different classification models to predict the match outcome (the `A_win` column, where 1 means Team A wins, and 0 means Team B wins).

### 1. Random Forest
*   **Characteristics**: An ensemble learning model that is robust and less prone to overfitting.
*   **Handling Imbalanced Data**: Automatically adjusts weights to address the imbalance between wins and losses by setting `class_weight='balanced'`.

### 2. XGBoost
*   **Characteristics**: An efficient, flexible, and powerful gradient boosting framework.
*   **Handling Imbalanced Data**: Balances the weights of positive and negative samples by calculating and setting the `scale_pos_weight` parameter.

### 3. Logistic Regression
*   **Characteristics**: A classic linear classification model that is simple, highly interpretable, and serves as an excellent baseline model.

### 4. Support Vector Machine (SVM)
*   **Characteristics**: Performs well on small to medium-sized datasets and is adept at handling complex non-linear boundaries.
*   **Data Standardization**: Since SVM is sensitive to feature scaling, we used `StandardScaler` to standardize all features (to a mean of 0 and a variance of 1) and integrated it seamlessly with the model training process using a `Pipeline` to prevent data leakage.

## 📈 Model Evaluation

To comprehensively evaluate model performance, we used the following methods:

*   **Basic Performance Metrics**: Quick evaluation on the test set using `accuracy_score` and `f1_score`.
*   **Confusion Matrix**: Visualizes the model's prediction performance on each class, intuitively showing the number of true positives, false positives, true negatives, and false negatives.
*   **10-Fold Cross-Validation**: To obtain a more robust and reliable performance assessment, we performed 10-fold stratified cross-validation (`StratifiedKFold`) for each model and calculated the average accuracy.

## ⚙️ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
    ```

2.  **Prepare Data**:
    *   Ensure all data files (`.csv`, `.xlsx`) are located in the `./data/` directory.
    *   Ensure helper scripts like `champion_map_zh2en.py` are in the same directory as the main notebook file.

3.  **Run the Notebook**:
    *   Open and execute all cells in `DSAI5101/Esports dataset/my/randomForest_XGB.ipynb` in order.

## 💡 Conclusions and Reflections

*   **Feature Importance**: The feature importance analysis from Random Forest and XGBoost shows that features based on individual player performance (like `solo_winrate_diff`) are more predictive of match outcomes than features based on global champion performance (like `winrate_diff`).
*   **Data Timeliness and Concept Drift**: The experiment revealed a sharp decline in model performance when using 2021 data to predict 2024 matches. This is because the game version (heroes, items, map) and player form are constantly changing, rendering old data less effective. To achieve accurate predictions, **it is essential to train the model on data that is close in time to the target prediction period**.

---
