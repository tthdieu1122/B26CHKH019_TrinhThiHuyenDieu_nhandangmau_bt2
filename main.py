"""
Bai tap 2 - Cai dat va danh gia Logistic Regression
Mon: Nhan dang mau (Pattern Recognition) - Cao hoc

Chay:
    python main.py

Dau ra: cac hinh (.png) va bang ket qua (.csv/.json) trong thu muc outputs/
"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, log_loss, confusion_matrix, ConfusionMatrixDisplay, roc_curve,
)

RANDOM_STATE = 42
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)
np.random.seed(RANDOM_STATE)


def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def compute_log_loss(y_true, p, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)
    return -np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p))


class LogisticRegressionNumpy:
    """Logistic Regression cai dat thuan NumPy, toi uu bang gradient descent."""

    def __init__(self, lr=0.1, n_iters=3000, tol=1e-7):
        self.lr = lr
        self.n_iters = n_iters
        self.tol = tol
        self.w = None
        self.b = None
        self.loss_history = []

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0
        prev_loss = np.inf

        for it in range(self.n_iters):
            z = X @ self.w + self.b
            p = sigmoid(z)
            loss = compute_log_loss(y, p)
            self.loss_history.append(loss)

            error = p - y
            dw = (X.T @ error) / n_samples
            db = np.mean(error)

            self.w -= self.lr * dw
            self.b -= self.lr * db

            if abs(prev_loss - loss) < self.tol:
                print(f"  Hoi tu som o vong lap {it + 1}, log loss = {loss:.6f}")
                break
            prev_loss = loss
        else:
            print(f"  Dat so vong lap toi da ({self.n_iters}), log loss cuoi = {loss:.6f}")
        return self

    def predict_proba(self, X):
        return sigmoid(X @ self.w + self.b)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


def evaluate(name, y_true, y_pred, y_proba):
    return {
        "Model": name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1": f1_score(y_true, y_pred),
        "ROC-AUC": roc_auc_score(y_true, y_proba),
        "LogLoss": log_loss(y_true, y_proba),
    }


def main():
    # 1. Du lieu
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target
    print(f"[1] Du lieu: {X.shape[0]} mau, {X.shape[1]} dac trung, 2 lop {list(data.target_names)}")
    print("    Ti le lop:\n", y.value_counts(normalize=True).to_string())

    fig, ax = plt.subplots(figsize=(4, 4))
    y.value_counts().rename(index={0: "malignant", 1: "benign"}).plot(
        kind="bar", color=["indianred", "steelblue"], ax=ax
    )
    ax.set_title("Phân bố lớp")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "01_class_distribution.png"), dpi=150)
    plt.close(fig)

    # 2. Train/test + chuan hoa
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y.values, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"[2] Train: {X_train_scaled.shape}, Test: {X_test_scaled.shape}")

    # 3. NumPy Logistic Regression
    print("[3] Huan luyen Logistic Regression (NumPy)...")
    model_np = LogisticRegressionNumpy(lr=0.1, n_iters=3000, tol=1e-7)
    model_np.fit(X_train_scaled, y_train)

    fig, ax = plt.subplots()
    ax.plot(model_np.loss_history)
    ax.set_xlabel("Vòng lặp"); ax.set_ylabel("Log loss (train)")
    ax.set_title("Đường cong hội tụ - Logistic Regression (NumPy)")
    ax.grid(alpha=0.3)
    fig.savefig(os.path.join(OUT_DIR, "02_convergence_numpy.png"), dpi=150)
    plt.close(fig)

    # 4. sklearn Logistic Regression
    print("[4] Huan luyen Logistic Regression (scikit-learn)...")
    model_sk = LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)
    model_sk.fit(X_train_scaled, y_train)
    print(f"    So vong lap sklearn dung: {model_sk.n_iter_[0]}")

    # 5. Danh gia
    y_pred_np = model_np.predict(X_test_scaled)
    y_proba_np = model_np.predict_proba(X_test_scaled)
    y_pred_sk = model_sk.predict(X_test_scaled)
    y_proba_sk = model_sk.predict_proba(X_test_scaled)[:, 1]

    results = pd.DataFrame([
        evaluate("NumPy (from scratch)", y_test, y_pred_np, y_proba_np),
        evaluate("scikit-learn", y_test, y_pred_sk, y_proba_sk),
    ]).set_index("Model")
    results.to_csv(os.path.join(OUT_DIR, "comparison_metrics.csv"))
    print("[5] Bang so sanh:\n", results.round(4))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    cm_np = confusion_matrix(y_test, y_pred_np)
    ConfusionMatrixDisplay(cm_np, display_labels=data.target_names).plot(ax=axes[0], colorbar=False, cmap="Blues")
    axes[0].set_title("Ma trận nhầm lẫn - NumPy")
    cm_sk = confusion_matrix(y_test, y_pred_sk)
    ConfusionMatrixDisplay(cm_sk, display_labels=data.target_names).plot(ax=axes[1], colorbar=False, cmap="Greens")
    axes[1].set_title("Ma trận nhầm lẫn - scikit-learn")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "03_confusion_matrices.png"), dpi=150)
    plt.close(fig)

    fpr_np, tpr_np, _ = roc_curve(y_test, y_proba_np)
    fpr_sk, tpr_sk, _ = roc_curve(y_test, y_proba_sk)
    fig, ax = plt.subplots()
    ax.plot(fpr_np, tpr_np, label=f"NumPy (AUC={results.loc['NumPy (from scratch)','ROC-AUC']:.3f})")
    ax.plot(fpr_sk, tpr_sk, label=f"sklearn (AUC={results.loc['scikit-learn','ROC-AUC']:.3f})", linestyle="--")
    ax.plot([0, 1], [0, 1], color="gray", linestyle=":")
    ax.set_xlabel("Tỉ lệ dương tính giả (FPR)"); ax.set_ylabel("Tỉ lệ dương tính thật (TPR)")
    ax.set_title("Đường cong ROC")
    ax.legend()
    fig.savefig(os.path.join(OUT_DIR, "04_roc_curve.png"), dpi=150)
    plt.close(fig)

    w_compare = pd.DataFrame({
        "w_numpy": model_np.w,
        "w_sklearn": model_sk.coef_[0],
    }, index=X.columns)
    w_compare["abs_diff"] = (w_compare["w_numpy"] - w_compare["w_sklearn"]).abs()
    w_compare.to_csv(os.path.join(OUT_DIR, "weight_comparison.csv"))

    summary = {
        "bias_numpy": float(model_np.b),
        "bias_sklearn": float(model_sk.intercept_[0]),
        "mean_abs_weight_diff": float(w_compare["abs_diff"].mean()),
        "sklearn_n_iter": int(model_sk.n_iter_[0]),
        "numpy_n_iter": len(model_np.loss_history),
        "confusion_matrix_numpy": cm_np.tolist(),
        "confusion_matrix_sklearn": cm_sk.tolist(),
        "metrics": results.round(4).to_dict(orient="index"),
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nHoan tat. Ket qua duoc luu trong: {OUT_DIR}")


if __name__ == "__main__":
    main()
