# Bài tập 2 — Cài đặt và đánh giá Logistic Regression

Môn học: **Nhận dạng mẫu** (Pattern Recognition) — Cao học
Hình thức: làm cá nhân

## Đề bài

Trên một bộ dữ liệu thực tế, cài đặt Logistic Regression bằng NumPy (không dùng mô hình/bộ tối ưu có sẵn) và so sánh với `sklearn.linear_model.LogisticRegression`. Đánh giá bằng accuracy, precision, recall, F1, ROC-AUC, log loss và ma trận nhầm lẫn.

## Bộ dữ liệu

**Breast Cancer Wisconsin (Diagnostic)** (built-in trong `sklearn.datasets`) — 569 mẫu, 30 đặc trưng, 2 lớp (malignant / benign). Không cần tải dữ liệu từ mạng ngoài.

## Cấu trúc thư mục

```
baitap2-logistic-regression/
├── main.py              # Script chạy toàn bộ pipeline từ đầu đến cuối
├── notebook.ipynb       # Jupyter notebook tương đương, có sẵn output/biểu đồ
├── make_report.py       # Script sinh báo cáo PDF từ kết quả trong outputs/
├── BaoCao_BaiTap2.pdf   # Báo cáo hoàn chỉnh (≥ 14 trang, tiếng Việt có dấu)
├── outputs/             # Hình ảnh (.png), bảng số liệu (.csv) và summary.json sau khi chạy
├── requirements.txt
└── README.md
```

## Cách chạy

```bash
# 1. Tạo môi trường ảo (khuyến nghị)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3a. Chạy bằng script (nhanh, tái tạo toàn bộ outputs/)
python main.py

# 3b. Hoặc mở và chạy notebook
jupyter notebook notebook.ipynb   # Kernel → Run All

# 4. (Tuỳ chọn) Sinh lại báo cáo PDF sau khi có outputs/ mới
python make_report.py
```

Không cần kết nối mạng để tải dữ liệu — `load_breast_cancer()` có sẵn trong scikit-learn.

## Phương pháp tóm tắt

1. Chia train/test (80/20, stratified) + `StandardScaler`.
2. **`LogisticRegressionNumpy`** (trong `main.py`): tự cài đặt sigmoid, log loss, gradient descent (learning rate 0.1, tối đa 3000 vòng lặp, dừng sớm khi `Δloss < 1e-7`).
3. Huấn luyện `sklearn.linear_model.LogisticRegression` trên cùng dữ liệu đã chuẩn hoá.
4. So sánh accuracy, precision, recall, F1, ROC-AUC, log loss; vẽ ma trận nhầm lẫn và ROC curve của cả hai mô hình.

## Kết quả chính

Xem chi tiết trong `BaoCao_BaiTap2.pdf` hoặc `outputs/summary.json`. Tóm tắt: cả hai cách cài đặt đạt accuracy và ROC-AUC trên 97%, chênh lệch trọng số chủ yếu do khác thuật toán tối ưu và scikit-learn có sẵn regularization L2.

## Hướng dẫn sử dụng mã nguồn

### 1. Yêu cầu hệ thống
- Python từ 3.9 trở lên (đã kiểm thử với Python 3.12).
- Thư viện trong `requirements.txt`: numpy, pandas, matplotlib, scikit-learn (từ 1.4), jupyter, ipykernel, reportlab, pypdf.
- Không cần mạng khi chạy vì dữ liệu có sẵn trong scikit-learn.

### 2. Cài đặt môi trường
Mở terminal tại thư mục bài tập:

```bash
python -m venv venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Chạy chương trình

| Mục đích | Lệnh | Kết quả |
|---|---|---|
| Chạy toàn bộ pipeline | `python main.py` | In tiến trình; ghi hình, CSV, `summary.json` vào `outputs/` |
| Sinh lại báo cáo PDF | `python make_report.py` | Tạo lại PDF từ `outputs/` (phải chạy `main.py` trước) |
| Chạy từng bước tương tác | `jupyter notebook` | Mở `notebook.ipynb`, chọn Kernel, Restart & Run All |

Thứ tự khuyến nghị: `main.py` rồi `make_report.py`.

### 4. Tệp kết quả trong `outputs/`

| Tệp | Nội dung |
|---|---|
| `comparison_metrics.csv` | Accuracy, Precision, Recall, F1, ROC-AUC, Log loss của hai cài đặt |
| `weight_comparison.csv` | Trọng số 30 đặc trưng ở hai mô hình và độ chênh lệch |
| `01_class_distribution.png` | Phân bố số mẫu theo lớp |
| `02_convergence_numpy.png` | Đường cong log loss theo vòng lặp (bản NumPy) |
| `03_confusion_matrices.png` | Ma trận nhầm lẫn của hai mô hình |
| `04_roc_curve.png` | Đường cong ROC |
| `summary.json` | Bias, chênh lệch trọng số, số vòng lặp, ma trận nhầm lẫn, các chỉ số |

### 5. Tham số có thể điều chỉnh

| Tham số | Vị trí | Ý nghĩa |
|---|---|---|
| `lr` | `LogisticRegressionNumpy` | Learning rate, mặc định 0.1 |
| `n_iters` | `LogisticRegressionNumpy` | Số vòng lặp tối đa, mặc định 3000 |
| `tol` | `LogisticRegressionNumpy` | Ngưỡng dừng sớm, mặc định 1e-7 |
| `threshold` | `predict()` | Ngưỡng quyết định, mặc định 0.5 (hạ thấp để ưu tiên recall) |
| `max_iter` | `LogisticRegression` | Số vòng lặp tối đa của bản scikit-learn |

Ví dụ dùng riêng lớp cài đặt NumPy:

```python
from main import LogisticRegressionNumpy
model = LogisticRegressionNumpy(lr=0.05, n_iters=5000, tol=1e-8)
model.fit(X_train_scaled, y_train)
proba = model.predict_proba(X_test_scaled)
pred = model.predict(X_test_scaled, threshold=0.4)
```

### 6. Các hàm và lớp chính trong `main.py`
- `sigmoid()`: hàm sigmoid, có `np.clip` để tránh tràn số.
- `compute_log_loss()`: log loss, cắt xác suất trong [1e-12, 1-1e-12].
- `LogisticRegressionNumpy`: `fit()` chạy gradient descent, `predict_proba()` và `predict()` dự báo.
- `evaluate()`: tính 6 chỉ số đánh giá từ nhãn và xác suất dự báo.
- `main()`: điều phối toàn bộ quy trình.

### 7. Lỗi thường gặp

| Hiện tượng | Cách khắc phục |
|---|---|
| `ModuleNotFoundError` | Kích hoạt lại venv và chạy `pip install -r requirements.txt` |
| PowerShell chặn lệnh activate | `Set-ExecutionPolicy -Scope Process RemoteSigned` hoặc dùng Command Prompt |
| `make_report.py` báo thiếu ảnh/CSV | Chạy `python main.py` trước |
| PDF bị ô vuông, mất dấu | Cài matplotlib (kèm font DejaVu Sans) hoặc đặt `DejaVuSans*.ttf` cạnh `make_report.py` |
| Jupyter không thấy kernel | `python -m ipykernel install --user` |

## Tác giả

Làm cá nhân — [Điền tên / MSSV của bạn tại đây].
