# Classical Machine Learning and Tabular AI: Scikit-Learn, XGBoost, Cross-Validation and Leakage Prevention

**Category**: `machine_learning_core` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Tabular ML Decision Rule (SY09): On structured/tabular datasets (<1M rows), Gradient Boosted Decision Trees (XGBoost, LightGBM, CatBoost) outperform Deep Learning. Core engineering rules: (1) Prevent Data Leakage by fitting StandardScaler, Imputer, and TargetEncoder strictly inside sklearn.pipeline.Pipeline on X_train only during Stratified K-Fold Cross-Validation. (2) Bias-Variance and Regularization: L1 (Lasso) induces sparsity for feature selection; L2 (Ridge) shrinks collinear weights; PCA/SVD projects orthogonal maximum-variance axes. (3) Class Imbalance: Use PR-AUC and F1/F-beta instead of ROC-AUC or accuracy; tune scale_pos_weight and probability thresholds. (4) Explainability: Use SHAP values for global and local feature attribution.

## Connected GraphRAG Entities

- `Classical_ML_XGBoost`
- `Deep_Learning_PyTorch_UNet`
