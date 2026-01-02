import logging
from typing import Dict, Tuple, Any
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, roc_auc_score, log_loss

from trendlab.domain.ports import MLModel

logger = logging.getLogger(__name__)

class ModelEngine(MLModel):
    
    def __init__(self, model_type: str = "logistic", random_state: int = 42):
        self.model_type = model_type
        self.random_state = random_state
        self.pipeline = self._build_pipeline()
        self.feature_cols: list[str] = []

    def _build_pipeline(self) -> Pipeline:
        if self.model_type == "logistic":
            clf = LogisticRegression(class_weight='balanced', random_state=self.random_state)
        elif self.model_type == "boosting":
            clf = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=self.random_state)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        return Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', clf)
        ])

    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Trains the model using TimeSeriesSplit cross-validation to ensure rigor.
        Returns aggregated metrics.
        """
        self.feature_cols = list(X.columns)
        tscv = TimeSeriesSplit(n_splits=5)
        
        metrics = {
            "accuracy": [],
            "precision": [],
            "auc": [],
            "log_loss": []
        }
        
        logger.info(f"Starting training with {self.model_type}...")
        
        for fold, (train_index, test_index) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            
            self.pipeline.fit(X_train, y_train)
            
            y_pred = self.pipeline.predict(X_test)
            y_prob = self.pipeline.predict_proba(X_test)[:, 1]
            
            metrics["accuracy"].append(accuracy_score(y_test, y_pred))
            metrics["precision"].append(precision_score(y_test, y_pred, zero_division=0))
            
            # ROC AUC requires both classes in test set
            if len(np.unique(y_test)) > 1:
                metrics["auc"].append(roc_auc_score(y_test, y_prob))
            
            metrics["log_loss"].append(log_loss(y_test, y_prob))

        # Final fit on all data for future inference
        self.pipeline.fit(X, y)
        
        avg_metrics = {k: float(np.mean(v)) if v else 0.0 for k, v in metrics.items()}
        logger.info(f"Training complete. Metrics: {avg_metrics}")
        return avg_metrics

    def predict(self, X: pd.DataFrame) -> pd.Series:
        return pd.Series(self.pipeline.predict(X), index=X.index)

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        probs = self.pipeline.predict_proba(X)
        return pd.DataFrame(probs, index=X.index, columns=self.pipeline.classes_)
