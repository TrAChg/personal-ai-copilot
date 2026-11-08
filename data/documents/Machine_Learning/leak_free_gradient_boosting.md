# Leak-Free Machine Learning Pipeline: HistGradientBoostingRegressor & Out-of-Fold Preprocessing

## Core Principles
1. **Target Transformation**:
   In skewed price/valuation regression, apply `y_trans = log1p(y)` prior to fitting. The inverse transform `expm1(y_pred)` recovers true scale while optimizing for relative percentage error (RMSLE).

2. **Preventing Data Leakage**:
   All imputers, standardizers, and one-hot encoders must be fitted strictly on the training fold within a Scikit-Learn `Pipeline`. Fitting transformers on the full dataset before cross-validation produces optimistic test metric contamination.

3. **HistGradientBoosting vs XGBoost**:
   `HistGradientBoostingRegressor` discretizes continuous variables into 256 integer bins (histogram-based), reducing computation time from $O(N \cdot M)$ to $O(\text{bins} \cdot M)$ with native support for categorical features and missing values.

