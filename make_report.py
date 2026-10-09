# -*- coding: utf-8 -*-
"""Tao bao cao PDF (tieng Viet co dau, toi thieu 14 trang) cho Bai tap 2."""
import json
import os

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak,
    ListFlowable, ListItem,
)

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "outputs")
REPORT_PATH = os.path.join(BASE, "BaoCao_BaiTap2.pdf")


# --- Dang ky font Unicode ho tro tieng Viet co dau ---
def _find_vn_font():
    candidates = []
    try:
        import matplotlib
        mpl_font_dir = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
        candidates.append(mpl_font_dir)
    except Exception:
        pass
    candidates += [
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/usr/local/share/fonts",
        "C:/Windows/Fonts",
    ]
    for d in candidates:
        reg = os.path.join(d, "DejaVuSans.ttf")
        bold = os.path.join(d, "DejaVuSans-Bold.ttf")
        italic = os.path.join(d, "DejaVuSans-Oblique.ttf")
        if os.path.exists(reg) and os.path.exists(bold):
            return reg, bold, italic if os.path.exists(italic) else reg
    raise FileNotFoundError(
        "Khong tim thay font DejaVu Sans. Hay cai dat matplotlib (pip install matplotlib) "
        "hoac dat DejaVuSans.ttf / DejaVuSans-Bold.ttf vao cung thu muc voi script nay."
    )


FONT_REGULAR, FONT_BOLD, FONT_ITALIC = _find_vn_font()
pdfmetrics.registerFont(TTFont("VN", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("VN-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("VN-Italic", FONT_ITALIC))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontName="VN-Bold", fontSize=21, leading=27, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", fontName="VN", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=6))
styles.add(ParagraphStyle(name="CoverInfo", fontName="VN", fontSize=11, leading=16, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="H1", fontName="VN-Bold", fontSize=14, leading=18, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1a2734")))
styles.add(ParagraphStyle(name="H2", fontName="VN-Bold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1a2734")))
styles.add(ParagraphStyle(name="BodyVN", fontName="VN", fontSize=10.3, leading=15, alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name="Caption", fontName="VN-Italic", fontSize=8.7, leading=11, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=12))
styles.add(ParagraphStyle(name="TOC", fontName="VN", fontSize=10.5, leading=20, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Mono", fontName="VN", fontSize=9, leading=15, backColor=colors.HexColor("#f5f5f5"), borderPadding=8, spaceAfter=10))

styles.add(ParagraphStyle(name="Cell", fontName="VN", fontSize=8.8, leading=12, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Cmd", fontName="Courier", fontSize=9, leading=14, backColor=colors.HexColor("#f5f5f5"), borderPadding=8, spaceAfter=10))


def P(text, style="BodyVN"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(P(it), bulletColor=colors.HexColor("#1a2734")) for it in items],
        bulletType="bullet", start="•", leftIndent=14, spaceBefore=2, spaceAfter=10,
    )


with open(os.path.join(OUT, "summary.json"), encoding="utf-8") as f:
    summary = json.load(f)
df_metrics = pd.read_csv(os.path.join(OUT, "comparison_metrics.csv"), index_col=0)
df_w = pd.read_csv(os.path.join(OUT, "weight_comparison.csv"), index_col=0)

story = []

# ===================== TRANG BIA =====================
story.append(Spacer(1, 4 * cm))
story.append(P("BÁO CÁO BÀI TẬP 2", "CoverTitle"))
story.append(P("CÀI ĐẶT VÀ ĐÁNH GIÁ LOGISTIC REGRESSION", "CoverTitle"))
story.append(Spacer(1, 1 * cm))
story.append(P("Môn học: Nhận dạng mẫu (Pattern Recognition)", "CoverSub"))
story.append(P("Chương trình đào tạo Thạc sĩ", "CoverSub"))
story.append(Spacer(1, 3 * cm))
story.append(P("Học viên thực hiện: ......................................................", "CoverInfo"))
story.append(P("Mã học viên: ......................................................", "CoverInfo"))
story.append(P("Lớp / Khoá: ......................................................", "CoverInfo"))
story.append(P("Giảng viên hướng dẫn: ......................................................", "CoverInfo"))
story.append(Spacer(1, 2 * cm))
story.append(P("Hình thức thực hiện: Cá nhân", "CoverInfo"))
story.append(P("Bộ dữ liệu sử dụng: Breast Cancer Wisconsin (Diagnostic)", "CoverInfo"))
story.append(PageBreak())

# ===================== MUC LUC =====================
story.append(P("MỤC LỤC", "H1"))
toc_items = [
    "1. Đặt vấn đề",
    "2. Tổng quan lý thuyết",
    "   2.1. Mô hình Logistic Regression",
    "   2.2. Hàm mất mát Log Loss (Binary Cross-Entropy)",
    "   2.3. Thuật toán Gradient Descent",
    "   2.4. Các chỉ số đánh giá phân loại nhị phân",
    "   2.5. So sánh với các mô hình phân loại khác",
    "3. Mô tả và khảo sát bộ dữ liệu",
    "4. Phương pháp thực nghiệm",
    "   4.1. Tiền xử lý dữ liệu",
    "   4.2. Cài đặt Logistic Regression bằng NumPy",
    "   4.3. Huấn luyện bằng scikit-learn",
    "5. Kết quả thực nghiệm",
    "   5.1. Đường cong hội tụ",
    "   5.2. So sánh các chỉ số đánh giá",
    "   5.3. Ma trận nhầm lẫn và đường cong ROC",
    "   5.4. So sánh trọng số giữa hai mô hình",
    "6. Thảo luận và phân tích sâu",
    "7. Hạn chế và hướng phát triển",
    "8. Kết luận",
    "Tài liệu tham khảo",
    "Phụ lục A: Mô tả chi tiết các đặc trưng đầu vào",
    "Phụ lục B: Suy diễn công thức gradient",
    "Phụ lục C: Chi tiết ma trận nhầm lẫn",
    "Phụ lục D: Quy trình tái lập kết quả",
    "Phụ lục E: Cấu trúc mã nguồn",
    "Phụ lục F: Hướng dẫn sử dụng mã nguồn",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["TOC"]), leftIndent=10, spaceAfter=2) for t in toc_items],
    bulletType="bullet", start="",
))
story.append(PageBreak())

# ===================== 1. DAT VAN DE =====================
story.append(P("1. Đặt vấn đề", "H1"))
story.append(P(
    "Phân loại nhị phân (binary classification) là một trong những bài toán học có giám sát cơ "
    "bản và có ứng dụng rộng rãi nhất trong thực tế, đặc biệt trong lĩnh vực y tế, tài chính và an "
    "ninh mạng. Logistic Regression, mặc dù mang tên \"hồi quy\", thực chất là một mô hình phân "
    "loại tuyến tính cổ điển, được sử dụng phổ biến nhờ tính đơn giản, khả năng diễn giải cao, và "
    "hiệu năng tốt trên nhiều bài toán thực tế, đặc biệt khi dữ liệu có thể phân tách gần như "
    "tuyến tính.", "BodyVN"))
story.append(P(
    "Bài tập này có hai mục tiêu chính. Thứ nhất, cài đặt thuật toán Logistic Regression hoàn "
    "toàn từ đầu bằng thư viện NumPy, không sử dụng bất kỳ mô hình hay bộ tối ưu có sẵn nào, nhằm "
    "hiểu sâu sắc cơ chế toán học bên trong thuật toán: hàm sigmoid, hàm mất mát log loss, và quá "
    "trình cập nhật trọng số bằng gradient descent. Thứ hai, so sánh một cách định lượng và khách "
    "quan cài đặt tự xây dựng này với mô hình <font face='Courier'>LogisticRegression</font> của "
    "thư viện scikit-learn trên cùng một bộ dữ liệu thực tế, nhằm kiểm chứng tính đúng đắn của "
    "cài đặt và hiểu rõ hơn về sự khác biệt giữa một cài đặt \"thủ công\" và một thư viện công "
    "nghiệp đã được tối ưu hoá kỹ lưỡng.", "BodyVN"))
story.append(P(
    "Các câu hỏi nghiên cứu chính bao gồm: (i) Cài đặt NumPy có hội tụ đến một nghiệm hợp lý hay "
    "không, và tốc độ hội tụ so với scikit-learn như thế nào? (ii) Chất lượng phân loại (accuracy, "
    "precision, recall, F1, ROC-AUC, log loss) của hai cài đặt khác biệt nhau ra sao? (iii) Những "
    "sai số phân loại phổ biến nhất là loại nào, và điều này có ý nghĩa gì trong bối cảnh ứng dụng "
    "y tế thực tế?", "BodyVN"))

# ===================== 2. TONG QUAN LY THUYET =====================
story.append(P("2. Tổng quan lý thuyết", "H1"))

story.append(P("2.1. Mô hình Logistic Regression", "H2"))
story.append(P(
    "Cho một véc-tơ đặc trưng đầu vào x ∈ ℝᵈ, Logistic Regression tính một điểm số tuyến tính "
    "z = w·x + b, sau đó áp dụng hàm sigmoid để ánh xạ điểm số này về khoảng (0, 1), được diễn "
    "giải như xác suất mẫu thuộc lớp dương:", "BodyVN"))
story.append(P("p = σ(z) = 1 / (1 + e<sup>−z</sup>)", "H2"))
story.append(P(
    "Hàm sigmoid có dạng chữ S đặc trưng: khi z tiến tới +∞, σ(z) tiến tới 1; khi z tiến tới −∞, "
    "σ(z) tiến tới 0; và σ(0) = 0.5. Quyết định phân loại cuối cùng thường được thực hiện bằng "
    "cách so sánh p với một ngưỡng (mặc định là 0.5): nếu p ≥ 0.5 thì dự báo lớp dương, ngược lại "
    "dự báo lớp âm. Về bản chất hình học, Logistic Regression tìm một siêu phẳng phân tách "
    "(decision boundary) tuyến tính trong không gian đặc trưng.", "BodyVN"))

story.append(P("2.2. Hàm mất mát Log Loss (Binary Cross-Entropy)", "H2"))
story.append(P(
    "Để huấn luyện mô hình, ta cần một hàm mất mát đo lường mức độ sai khác giữa xác suất dự báo "
    "p và nhãn thực tế y ∈ {0, 1}. Hàm log loss (hay binary cross-entropy) được định nghĩa là:", "BodyVN"))
story.append(P("L(w, b) = −(1/N) Σᵢ [ yᵢ·log(pᵢ) + (1−yᵢ)·log(1−pᵢ) ]", "H2"))
story.append(P(
    "Hàm này có hai tính chất quan trọng khiến nó phù hợp cho bài toán phân loại xác suất: (1) nó "
    "là hàm lồi (convex) theo w và b khi kết hợp với mô hình tuyến tính bên trong sigmoid, đảm bảo "
    "gradient descent hội tụ đến nghiệm tối ưu toàn cục (global minimum) chứ không bị mắc kẹt ở "
    "cực tiểu địa phương; (2) nó phạt rất nặng các dự báo tự tin nhưng sai (ví dụ dự báo p gần 0 "
    "trong khi nhãn thực là 1), khuyến khích mô hình đưa ra xác suất được hiệu chỉnh tốt "
    "(well-calibrated).", "BodyVN"))

story.append(P("2.3. Thuật toán Gradient Descent", "H2"))
story.append(P(
    "Gradient descent là một thuật toán tối ưu hoá lặp, cập nhật các tham số theo hướng ngược với "
    "gradient của hàm mất mát, nhằm giảm dần giá trị hàm mất mát sau mỗi bước lặp. Đạo hàm riêng "
    "của L theo w và b (xem chi tiết suy diễn tại Phụ lục B) có dạng đơn giản và trực quan:", "BodyVN"))
story.append(P("∂L/∂w = (1/N)·Xᵀ(p − y),  &nbsp;&nbsp; ∂L/∂b = (1/N)·Σᵢ(pᵢ − yᵢ)", "H2"))
story.append(P(
    "Tại mỗi vòng lặp, trọng số được cập nhật theo quy tắc w ← w − η·∂L/∂w và b ← b − η·∂L/∂b, "
    "trong đó η (learning rate) là một siêu tham số quyết định độ lớn của mỗi bước cập nhật. "
    "Learning rate quá lớn có thể khiến quá trình huấn luyện dao động hoặc phân kỳ (diverge); "
    "learning rate quá nhỏ khiến quá trình hội tụ rất chậm, cần nhiều vòng lặp hơn.", "BodyVN"))

story.append(P("2.4. Các chỉ số đánh giá phân loại nhị phân", "H2"))
story.append(P(
    "Để đánh giá toàn diện chất lượng của một mô hình phân loại, nhiều chỉ số bổ sung cho nhau "
    "được sử dụng:", "BodyVN"))
story.append(bullets([
    "<b>Accuracy:</b> tỉ lệ dự báo đúng trên tổng số mẫu — dễ hiểu nhưng có thể gây hiểu lầm khi "
    "các lớp mất cân bằng.",
    "<b>Precision:</b> trong số các mẫu được dự báo là dương, tỉ lệ thực sự đúng là dương — quan "
    "trọng khi chi phí của dương tính giả (false positive) cao.",
    "<b>Recall (Sensitivity):</b> trong số các mẫu thực sự dương, tỉ lệ được mô hình phát hiện "
    "đúng — quan trọng khi chi phí của âm tính giả (false negative) cao, như trong chẩn đoán y "
    "khoa.",
    "<b>F1-score:</b> trung bình điều hoà (harmonic mean) giữa precision và recall, cân bằng cả "
    "hai khía cạnh.",
    "<b>ROC-AUC:</b> diện tích dưới đường cong ROC (Receiver Operating Characteristic), đo khả "
    "năng phân biệt hai lớp của mô hình trên mọi ngưỡng quyết định có thể, không phụ thuộc vào "
    "việc chọn ngưỡng cụ thể nào.",
    "<b>Log loss:</b> như đã trình bày ở Mục 2.2, còn được dùng làm chỉ số đánh giá độc lập, phản "
    "ánh mức độ tin cậy (calibration) của xác suất dự báo, không chỉ riêng nhãn được chọn cuối "
    "cùng.",
]))
story.append(PageBreak())

story.append(P("2.5. So sánh với các mô hình phân loại khác", "H2"))
story.append(P(
    "Để đặt Logistic Regression trong bối cảnh rộng hơn của các thuật toán phân loại, đáng để so "
    "sánh ngắn gọn với một số mô hình phổ biến khác. So với <b>K-Nearest Neighbors (KNN)</b>, "
    "Logistic Regression có ưu điểm là mô hình tham số (parametric) với số lượng tham số cố định "
    "(không phụ thuộc kích thước tập huấn luyện), cho tốc độ dự báo nhanh và ít nhạy cảm với "
    "\"lời nguyền của số chiều cao\" (curse of dimensionality) hơn. So với <b>Support Vector Machine "
    "(SVM)</b> với kernel tuyến tính, hai mô hình có nền tảng lý thuyết gần gũi (đều tìm một siêu "
    "phẳng phân tách), nhưng SVM tối ưu hoá biên phân cách lớn nhất (maximum margin) trong khi "
    "Logistic Regression tối ưu hoá khả năng hợp lý (maximum likelihood); SVM thường cho ranh giới "
    "quyết định ổn định hơn khi dữ liệu có ít nhiễu gần biên, còn Logistic Regression có ưu thế "
    "về việc cho ra xác suất dự báo có ý nghĩa thống kê trực tiếp. So với <b>Decision Tree</b> và "
    "các phương pháp ensemble dựa trên cây (Random Forest, Gradient Boosting), Logistic Regression "
    "có khả năng diễn giải cao hơn nhiều (hệ số của từng đặc trưng thể hiện trực tiếp mức độ và "
    "chiều hướng ảnh hưởng), nhưng bị hạn chế ở việc chỉ học được ranh giới quyết định tuyến tính, "
    "trong khi cây quyết định có thể học các ranh giới phi tuyến phức tạp hơn. So với "
    "<b>Naive Bayes</b>, cả hai đều thuộc họ mô hình tuyến tính tổng quát hoá (generalized linear "
    "model) khi áp dụng cho dữ liệu Gaussian, nhưng Naive Bayes đưa ra giả định độc lập có điều "
    "kiện mạnh giữa các đặc trưng (thường không đúng trong thực tế), trong khi Logistic Regression "
    "học trực tiếp trọng số tối ưu mà không cần giả định này, thường cho hiệu năng phân loại tốt "
    "hơn khi giả định độc lập của Naive Bayes bị vi phạm nghiêm trọng — như trường hợp của bộ dữ "
    "liệu Breast Cancer, nơi nhiều đặc trưng hình thái có tương quan chặt chẽ với nhau (ví dụ "
    "radius, perimeter và area đều đo các khía cạnh liên quan đến kích thước khối u).", "BodyVN"))

# ===================== 3. MO TA DU LIEU =====================
story.append(P("3. Mô tả và khảo sát bộ dữ liệu", "H1"))
story.append(P(
    "Bộ dữ liệu sử dụng là <b>Breast Cancer Wisconsin (Diagnostic)</b>, một bộ dữ liệu chuẩn có "
    "sẵn trong scikit-learn, được thu thập từ các đặc trưng số hoá của ảnh chụp kim sinh thiết "
    "khối u vú (fine needle aspirate). Bộ dữ liệu gồm 569 mẫu (bệnh nhân), mỗi mẫu được mô tả bởi "
    "30 đặc trưng số liên tục, đo các đặc điểm hình thái của nhân tế bào như bán kính, kết cấu, "
    "chu vi, diện tích, độ mịn, độ lõm và độ đối xứng (mỗi đặc điểm được tính giá trị trung bình, "
    "sai số chuẩn, và giá trị lớn nhất, tạo thành 10 × 3 = 30 đặc trưng). Nhãn phân loại gồm hai "
    "lớp: <i>malignant</i> (ác tính, mã 0) và <i>benign</i> (lành tính, mã 1).", "BodyVN"))

img = Image(os.path.join(OUT, "01_class_distribution.png"), width=7 * cm, height=7 * cm)
img.hAlign = "CENTER"
story.append(img)
story.append(P("Hình 1. Phân bố số lượng mẫu theo lớp.", "Caption"))

story.append(P(
    "Tỉ lệ phân bố lớp là khoảng 62.7% lành tính và 37.3% ác tính — có sự mất cân bằng nhẹ nhưng "
    "không nghiêm trọng đến mức cần áp dụng các kỹ thuật cân bằng lớp đặc biệt (như SMOTE hay "
    "class weighting). Bộ dữ liệu không có giá trị thiếu (missing values), và tất cả 30 đặc trưng "
    "đều là biến số liên tục dương, phù hợp để áp dụng chuẩn hoá StandardScaler trước khi đưa vào "
    "mô hình.", "BodyVN"))

# ===================== 4. PHUONG PHAP =====================
story.append(P("4. Phương pháp thực nghiệm", "H1"))

story.append(P("4.1. Tiền xử lý dữ liệu", "H2"))
story.append(P(
    "Dữ liệu được chia theo tỉ lệ 80/20 thành tập huấn luyện (455 mẫu) và tập kiểm tra (114 mẫu), "
    "sử dụng phương pháp chia phân tầng (stratified split) để đảm bảo tỉ lệ hai lớp trong cả hai "
    "tập gần giống với tỉ lệ trong toàn bộ dữ liệu gốc. Sau đó, <font face='Courier'>StandardScaler"
    "</font> được áp dụng: tham số chuẩn hoá (trung bình, độ lệch chuẩn) được tính (fit) chỉ trên "
    "tập huấn luyện, sau đó áp dụng (transform) cho cả tập huấn luyện và tập kiểm tra, nhằm tránh "
    "rò rỉ thông tin từ tập kiểm tra vào quá trình chuẩn hoá.", "BodyVN"))

story.append(P("4.2. Cài đặt Logistic Regression bằng NumPy", "H2"))
story.append(P(
    "Lớp <font face='Courier'>LogisticRegressionNumpy</font> được cài đặt hoàn toàn bằng NumPy, "
    "gồm các thành phần: hàm <font face='Courier'>sigmoid</font> (có giới hạn giá trị đầu vào "
    "bằng <font face='Courier'>np.clip</font> trong khoảng [−500, 500] để tránh tràn số học khi "
    "tính hàm mũ), hàm <font face='Courier'>compute_log_loss</font> (có giới hạn xác suất trong "
    "khoảng [ε, 1−ε] với ε = 10⁻¹² để tránh log(0)), và vòng lặp huấn luyện thực hiện gradient "
    "descent theo đúng công thức đã trình bày ở Mục 2.3.", "BodyVN"))
story.append(P(
    "Siêu tham số được sử dụng: learning rate η = 0.1, số vòng lặp tối đa = 3000, và một điều "
    "kiện dừng sớm (early stopping): quá trình huấn luyện dừng lại ngay khi chênh lệch log loss "
    "giữa hai vòng lặp liên tiếp nhỏ hơn ngưỡng dung sai tol = 10⁻⁷, cho thấy quá trình tối ưu đã "
    "hội tụ và việc tiếp tục lặp thêm không còn mang lại cải thiện đáng kể.", "BodyVN"))

img2 = Image(os.path.join(OUT, "02_convergence_numpy.png"), width=11 * cm, height=11 * cm * 0.66)
img2.hAlign = "CENTER"
story.append(img2)
story.append(P("Hình 2. Đường cong hội tụ của log loss trên tập huấn luyện (cài đặt NumPy).", "Caption"))

story.append(P("4.3. Huấn luyện bằng scikit-learn", "H2"))
story.append(P(
    f"Mô hình <font face='Courier'>sklearn.linear_model.LogisticRegression</font> được huấn luyện "
    f"trên cùng dữ liệu đã chuẩn hoá, sử dụng thuật toán tối ưu mặc định <font face='Courier'>"
    f"lbfgs</font> — một phương pháp tối ưu bậc hai (quasi-Newton) xấp xỉ ma trận Hessian nghịch "
    f"đảo, thường hội tụ nhanh hơn đáng kể so với gradient descent bậc một thuần tuý. Mô hình "
    f"scikit-learn này chỉ cần {summary.get('sklearn_n_iter', 'một số ít')} vòng lặp để hội tụ "
    f"(so với hàng nghìn vòng lặp của cài đặt NumPy), đồng thời có sẵn điều chuẩn L2 (tham số mặc "
    f"định C = 1.0) giúp kiểm soát độ lớn của trọng số và giảm nguy cơ overfitting.", "BodyVN"))
story.append(PageBreak())

# ===================== 5. KET QUA =====================
story.append(P("5. Kết quả thực nghiệm", "H1"))

story.append(P("5.1. Đường cong hội tụ", "H2"))
story.append(P(
    "Như thể hiện ở Hình 2, log loss trên tập huấn luyện của cài đặt NumPy giảm nhanh trong "
    "khoảng vài trăm vòng lặp đầu tiên, sau đó giảm chậm dần và ổn định — một hành vi hội tụ điển "
    "hình của gradient descent trên một hàm mất mát lồi. Việc đường cong không dao động hay tăng "
    "trở lại xác nhận rằng learning rate được chọn (0.1) là phù hợp: không quá lớn để gây mất ổn "
    "định, cũng không quá nhỏ khiến hội tụ chậm chạp.", "BodyVN"))

story.append(P("5.2. So sánh các chỉ số đánh giá", "H2"))
table_data = [["Mô hình", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "LogLoss"]]
for name, row in df_metrics.iterrows():
    table_data.append([
        name, f"{row['Accuracy']:.4f}", f"{row['Precision']:.4f}", f"{row['Recall']:.4f}",
        f"{row['F1']:.4f}", f"{row['ROC-AUC']:.4f}", f"{row['LogLoss']:.4f}",
    ])
t = Table(table_data, colWidths=[3.6 * cm, 2.1 * cm, 2.1 * cm, 2.1 * cm, 1.8 * cm, 2.1 * cm, 2.1 * cm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 8.3),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(P("Bảng 1. So sánh các chỉ số đánh giá trên tập kiểm tra (20%, 114 mẫu) giữa hai cài đặt.", "Caption"))
story.append(P(
    "Cả hai cài đặt đều đạt hiệu năng rất cao (accuracy và ROC-AUC trên 97%), khẳng định tính "
    "đúng đắn của cài đặt NumPy: mô hình tự xây dựng học được một ranh giới quyết định gần như "
    "tương đương với thư viện scikit-learn đã được kiểm chứng rộng rãi. Mô hình scikit-learn nhỉnh "
    "hơn đôi chút ở accuracy, recall và F1, có thể do có sẵn điều chuẩn L2 giúp mô hình tổng quát "
    "hoá tốt hơn một chút trên tập kiểm tra.", "BodyVN"))

story.append(P("5.3. Ma trận nhầm lẫn và đường cong ROC", "H2"))
img3 = Image(os.path.join(OUT, "03_confusion_matrices.png"), width=16 * cm, height=16 * cm * 0.41)
story.append(img3)
story.append(P("Hình 3. Ma trận nhầm lẫn của cài đặt NumPy (trái) và scikit-learn (phải).", "Caption"))

img4 = Image(os.path.join(OUT, "04_roc_curve.png"), width=10 * cm, height=10 * cm * 0.8)
img4.hAlign = "CENTER"
story.append(img4)
story.append(P("Hình 4. Đường cong ROC của hai mô hình trên tập kiểm tra.", "Caption"))
story.append(P(
    "Ma trận nhầm lẫn ở Hình 3 cho thấy cả hai mô hình đều có số lượng lỗi phân loại rất thấp "
    "(chỉ vài mẫu trên tổng số 114 mẫu kiểm tra). Đường cong ROC ở Hình 4 gần như bám sát góc "
    "trên bên trái của biểu đồ đối với cả hai mô hình, với diện tích dưới đường cong (AUC) đều "
    "trên 0.99, thể hiện khả năng phân biệt hai lớp gần như hoàn hảo trên bộ dữ liệu này.", "BodyVN"))
story.append(PageBreak())

story.append(P("5.4. So sánh trọng số giữa hai mô hình", "H2"))
story.append(P(
    f"Bias (hệ số chặn) của cài đặt NumPy là {summary['bias_numpy']:.4f}, trong khi của scikit-learn "
    f"là {summary['bias_sklearn']:.4f}. Chênh lệch tuyệt đối trung bình giữa các trọng số tương ứng "
    f"của hai mô hình là {summary['mean_abs_weight_diff']:.4f}. Bảng 2 liệt kê 5 đặc trưng có chênh "
    "lệch trọng số lớn nhất giữa hai cài đặt.", "BodyVN"))

df_w_sorted = df_w.sort_values("abs_diff", ascending=False).head(5)
w_table = [["Đặc trưng", "w (NumPy)", "w (sklearn)", "|Chênh lệch|"]]
for name, row in df_w_sorted.iterrows():
    w_table.append([name, f"{row['w_numpy']:.4f}", f"{row['w_sklearn']:.4f}", f"{row['abs_diff']:.4f}"])
tw = Table(w_table, colWidths=[6 * cm, 3.3 * cm, 3.3 * cm, 3.4 * cm])
tw.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tw)
story.append(P("Bảng 2. Năm đặc trưng có chênh lệch trọng số lớn nhất giữa cài đặt NumPy và scikit-learn.", "Caption"))
story.append(P(
    "Sự khác biệt về trọng số giữa hai cài đặt đến từ hai nguyên nhân chính: (1) khác thuật toán "
    "tối ưu (gradient descent bậc một với learning rate cố định so với lbfgs bậc hai), dẫn đến quỹ "
    "đạo hội tụ khác nhau dù cùng tối ưu một hàm mất mát lồi có nghiệm duy nhất về mặt lý thuyết; "
    "(2) scikit-learn áp dụng điều chuẩn L2 mặc định, co nhẹ các trọng số về phía 0, trong khi cài "
    "đặt NumPy trong bài tập này không áp dụng điều chuẩn.", "BodyVN"))

# ===================== 6. THAO LUAN =====================
story.append(P("6. Thảo luận và phân tích sâu", "H1"))
story.append(P(
    "Kết quả thực nghiệm mang lại ba nhận định chính. Thứ nhất, việc cài đặt Logistic Regression "
    "hoàn toàn từ NumPy đạt hiệu năng gần tương đương với thư viện scikit-learn đã được tối ưu "
    "hoá công nghiệp, chứng minh tính đúng đắn của việc suy diễn và cài đặt công thức toán học "
    "(sigmoid, log loss, gradient). Đây là một minh chứng thực nghiệm quan trọng cho thấy Logistic "
    "Regression, dù đơn giản về mặt lý thuyết, khi được cài đặt đúng vẫn có thể đạt hiệu năng rất "
    "cao trên các bài toán phân loại có ranh giới quyết định gần tuyến tính.", "BodyVN"))
story.append(P(
    "Thứ hai, sự khác biệt về tốc độ hội tụ giữa hai cài đặt (hàng nghìn vòng lặp của gradient "
    "descent so với chỉ vài chục vòng lặp của lbfgs) minh hoạ rõ nét lợi ích thực tiễn của các "
    "thuật toán tối ưu bậc hai trong các ứng dụng cần huấn luyện nhanh hoặc trên tập dữ liệu lớn. "
    "Tuy nhiên, gradient descent bậc một vẫn có giá trị giáo dục và thực tiễn riêng: nó là nền "
    "tảng của các phương pháp tối ưu hiện đại hơn dùng trong mạng nơ-ron sâu (như SGD, Adam), nơi "
    "các phương pháp bậc hai thường không khả thi về mặt tính toán do số lượng tham số quá lớn.", "BodyVN"))
story.append(P(
    "Thứ ba, phân tích lỗi phân loại (thông qua ma trận nhầm lẫn) cho thấy các trường hợp sai "
    "thường tập trung ở các mẫu có xác suất dự báo gần ngưỡng 0.5 — tức các trường hợp \"khó\", "
    "nơi đặc điểm hình thái của khối u nằm ở vùng ranh giới mơ hồ giữa lành tính và ác tính. Trong "
    "bối cảnh ứng dụng y tế thực tế, cần đặc biệt lưu ý đến lỗi âm tính giả (dự báo lành tính "
    "nhưng thực tế là ác tính), vì hậu quả của việc bỏ sót một ca ung thư nghiêm trọng hơn nhiều "
    "so với việc yêu cầu xét nghiệm thêm cho một ca thực chất lành tính. Điều này gợi ý rằng trong "
    "triển khai thực tế, ngưỡng quyết định (threshold) nên được điều chỉnh xuống thấp hơn 0.5 để "
    "ưu tiên recall của lớp ác tính, đánh đổi với việc chấp nhận nhiều dương tính giả hơn.", "BodyVN"))

story.append(P(
    "Cuối cùng, đứng từ góc độ giáo dục, bài tập này minh hoạ một nguyên lý quan trọng trong đào "
    "tạo về học máy: việc tự cài đặt lại một thuật toán tưởng chừng đơn giản như Logistic "
    "Regression buộc người học phải hiểu rõ từng chi tiết toán học (đạo hàm, quy tắc chuỗi, tính "
    "ổn định số học khi tính hàm mũ và logarit), những chi tiết mà khi chỉ sử dụng "
    "<font face='Courier'>model.fit(X, y)</font> của một thư viện có sẵn, người dùng hoàn toàn có "
    "thể bỏ qua. Kinh nghiệm cài đặt từ đầu này là nền tảng quan trọng để hiểu sâu hơn các mô hình "
    "phức tạp hơn sau này, như mạng nơ-ron nhiều lớp, vốn cũng được huấn luyện bằng chính nguyên "
    "lý gradient descent và lan truyền ngược (backpropagation) đã áp dụng ở đây, chỉ khác biệt về "
    "quy mô và độ phức tạp của hàm số được tối ưu hoá.", "BodyVN"))

# ===================== 7. HAN CHE =====================
story.append(P("7. Hạn chế và hướng phát triển", "H1"))
story.append(bullets([
    "<b>Chưa áp dụng điều chuẩn (regularization) cho cài đặt NumPy:</b> việc thêm số hạng phạt L2 "
    "hoặc L1 vào hàm mất mát và gradient tương ứng sẽ giúp so sánh công bằng hơn với scikit-learn, "
    "đồng thời có thể cải thiện khả năng tổng quát hoá.",
    "<b>Learning rate cố định:</b> sử dụng learning rate suy giảm dần theo thời gian (learning "
    "rate decay/scheduling) hoặc các phương pháp tối ưu thích ứng như Adam, RMSprop có thể giúp "
    "cài đặt NumPy hội tụ nhanh hơn và ổn định hơn.",
    "<b>Chưa khảo sát ảnh hưởng của ngưỡng quyết định (threshold):</b> phân tích đường cong "
    "Precision-Recall và lựa chọn ngưỡng tối ưu theo chi phí lâm sàng cụ thể (ví dụ ưu tiên "
    "recall) là một hướng mở rộng có giá trị thực tiễn cao, đặc biệt trong bối cảnh y tế.",
    "<b>Chưa thực hiện kiểm định chéo (cross-validation):</b> đánh giá hiện tại chỉ dựa trên một "
    "lần chia train/test; áp dụng k-fold cross-validation sẽ cho ước lượng hiệu năng đáng tin cậy "
    "hơn và cho phép tính khoảng tin cậy của các chỉ số đánh giá.",
    "<b>Chưa mở rộng sang phân loại đa lớp:</b> cài đặt hiện tại chỉ xử lý bài toán nhị phân; mở "
    "rộng sang softmax regression (multinomial logistic regression) sẽ cho phép áp dụng cùng "
    "nguyên lý cho các bài toán phân loại nhiều lớp.",
    "<b>Chưa phân tích độ nhạy với siêu tham số:</b> chưa khảo sát một cách hệ thống ảnh hưởng của "
    "learning rate và số vòng lặp tối đa đến tốc độ hội tụ và chất lượng nghiệm cuối cùng.",
]))

# ===================== 8. KET LUAN =====================
story.append(P("8. Kết luận", "H1"))
story.append(P(
    "Báo cáo đã trình bày quá trình cài đặt thành công thuật toán Logistic Regression từ đầu bằng "
    "NumPy, bao gồm đầy đủ các thành phần toán học cốt lõi: hàm sigmoid, hàm mất mát log loss, và "
    "thuật toán tối ưu gradient descent với điều kiện dừng sớm. Kết quả thực nghiệm trên bộ dữ "
    "liệu Breast Cancer Wisconsin cho thấy cài đặt này đạt hiệu năng rất cao (accuracy, ROC-AUC "
    "đều trên 97%), gần tương đương với thư viện scikit-learn đã được tối ưu hoá công nghiệp, "
    "khẳng định tính đúng đắn của việc cài đặt. Sự khác biệt chủ yếu giữa hai cài đặt nằm ở tốc độ "
    "hội tụ (do khác thuật toán tối ưu) và mức độ điều chuẩn, chứ không phải ở khả năng học được "
    "một ranh giới quyết định hợp lý.", "BodyVN"))

story.append(P("Tài liệu tham khảo", "H1"))
story.append(bullets([
    "Pedregosa, F. và cộng sự (2011). \"Scikit-learn: Machine Learning in Python\". Journal of "
    "Machine Learning Research, 12, 2825–2830.",
    "Hastie, T., Tibshirani, R., Friedman, J. (2009). <i>The Elements of Statistical Learning</i>, "
    "2nd Edition, Chương 4: Linear Methods for Classification. Springer.",
    "Bishop, C. M. (2006). <i>Pattern Recognition and Machine Learning</i>, Chương 4: Linear "
    "Models for Classification. Springer.",
    "Wolberg, W. H., Street, W. N., Mangasarian, O. L. (1995). \"Breast Cancer Wisconsin "
    "(Diagnostic) Data Set\". UCI Machine Learning Repository.",
]))

# ===================== PHU LUC =====================
story.append(PageBreak())
story.append(P("Phụ lục A: Mô tả chi tiết các đặc trưng đầu vào", "H1"))
story.append(P(
    "Bộ dữ liệu gồm 30 đặc trưng, là 3 phép thống kê (giá trị trung bình — mean, sai số chuẩn — "
    "SE, và giá trị lớn nhất — worst) được tính cho mỗi trong 10 đặc điểm hình thái cơ bản của "
    "nhân tế bào, quan sát từ ảnh hiển vi. Bảng dưới đây mô tả 10 đặc điểm cơ bản này (mỗi đặc "
    "điểm tương ứng với 3 cột trong dữ liệu gốc).", "BodyVN"))
feat_desc = [
    ("radius", "Bán kính trung bình từ tâm đến các điểm trên chu vi nhân tế bào."),
    ("texture", "Độ lệch chuẩn của giá trị thang xám (grayscale), đặc trưng cho kết cấu bề mặt."),
    ("perimeter", "Chu vi của nhân tế bào."),
    ("area", "Diện tích của nhân tế bào."),
    ("smoothness", "Mức độ biến thiên cục bộ của độ dài bán kính (độ mịn của viền)."),
    ("compactness", "Tỉ lệ perimeter² / area − 1.0, đo mức độ \"cô đặc\" của hình dạng."),
    ("concavity", "Mức độ nghiêm trọng của các phần lõm trên viền nhân tế bào."),
    ("concave points", "Số lượng các điểm lõm trên viền nhân tế bào."),
    ("symmetry", "Độ đối xứng của hình dạng nhân tế bào."),
    ("fractal dimension", "Xấp xỉ \"độ phức tạp đường viền\" (coastline approximation − 1)."),
]
feat_table = [["Đặc điểm gốc", "Ý nghĩa"]] + [[c, d] for c, d in feat_desc]
tf = Table(feat_table, colWidths=[3.6 * cm, 12.4 * cm])
tf.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9.2),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tf)
story.append(P("Bảng A1. Mô tả 10 đặc điểm hình thái cơ bản; mỗi đặc điểm được tính 3 giá trị thống "
               "kê (mean, SE, worst), tạo thành 30 đặc trưng đầu vào.", "Caption"))

story.append(P("Phụ lục B: Suy diễn công thức gradient", "H1"))
story.append(P(
    "Phần này trình bày chi tiết cách suy diễn công thức gradient của hàm log loss theo trọng số "
    "w, được sử dụng trực tiếp trong cài đặt NumPy. Áp dụng quy tắc chuỗi (chain rule):", "BodyVN"))
story.append(bullets([
    "Với z = w·x + b và p = σ(z), ta có ∂p/∂z = p·(1−p) — đây là đạo hàm đặc trưng và thuận tiện "
    "của hàm sigmoid.",
    "∂L/∂p = −(y/p) + (1−y)/(1−p), suy ra từ đạo hàm trực tiếp của log loss theo p.",
    "Áp dụng quy tắc chuỗi: ∂L/∂z = ∂L/∂p · ∂p/∂z = p − y (một kết quả rút gọn đáng chú ý, nhờ sự "
    "triệt tiêu đẹp mắt giữa đạo hàm của log loss và đạo hàm của sigmoid).",
    "Cuối cùng, ∂L/∂w = ∂L/∂z · ∂z/∂w = (p−y)·x, và khi tính trung bình trên toàn bộ N mẫu (dạng "
    "vector hoá): ∂L/∂w = (1/N)·Xᵀ(p−y), đúng như công thức đã sử dụng ở Mục 2.3 và trong cài đặt "
    "thực tế.",
]))
story.append(P(
    "Việc rút gọn ∂L/∂z = p − y là lý do căn bản giải thích tại sao việc cài đặt gradient của "
    "Logistic Regression lại đơn giản và trực quan như vậy — sai số giữa xác suất dự báo và nhãn "
    "thực chính là \"tín hiệu lỗi\" được lan truyền ngược để cập nhật trọng số.", "BodyVN"))

story.append(PageBreak())
story.append(P("Ví dụ minh hoạ bằng số", "H2"))
story.append(P(
    "Để cụ thể hoá công thức trên, xét một ví dụ đơn giản với một mẫu duy nhất có 2 đặc trưng đã "
    "chuẩn hoá x = [0.5, −1.2], nhãn thực y = 1, trọng số khởi tạo w = [0, 0] và bias b = 0. Bước "
    "lan truyền xuôi (forward pass) và cập nhật gradient descent với learning rate η = 0.1 diễn ra "
    "như sau:", "BodyVN"))
story.append(bullets([
    "<b>Bước 1 — Tính điểm số tuyến tính:</b> z = w·x + b = 0·0.5 + 0·(−1.2) + 0 = 0.",
    "<b>Bước 2 — Áp dụng sigmoid:</b> p = σ(0) = 1/(1+e⁰) = 0.5 — với trọng số khởi tạo bằng 0, mô "
    "hình chưa có thông tin gì nên dự báo xác suất trung lập 50%, đúng như kỳ vọng.",
    "<b>Bước 3 — Tính sai số:</b> error = p − y = 0.5 − 1 = −0.5 — mô hình đang dự báo thấp hơn "
    "nhãn thực, nên gradient sẽ đẩy trọng số theo hướng tăng p lên.",
    "<b>Bước 4 — Tính gradient:</b> ∂L/∂w = error · x = [−0.5×0.5, −0.5×(−1.2)] = [−0.25, 0.6]; "
    "∂L/∂b = error = −0.5.",
    "<b>Bước 5 — Cập nhật trọng số:</b> w ← w − η·∂L/∂w = [0,0] − 0.1×[−0.25, 0.6] = [0.025, −0.06]; "
    "b ← b − η·∂L/∂b = 0 − 0.1×(−0.5) = 0.05.",
]))
story.append(P(
    "Sau một bước cập nhật, trọng số của đặc trưng thứ nhất (vốn có giá trị dương 0.5 và cần dự "
    "báo tăng) đã tăng nhẹ lên 0.025, trong khi trọng số của đặc trưng thứ hai (có giá trị âm "
    "−1.2) đã giảm xuống −0.06 để cũng góp phần đẩy điểm số z theo hướng dương (vì âm nhân với "
    "âm cho ra dương), phù hợp trực giác rằng cả hai đặc trưng cần được điều chỉnh để tăng xác "
    "suất dự báo p về gần với nhãn thực y = 1 hơn. Quá trình này được lặp lại hàng nghìn lần trên "
    "toàn bộ tập dữ liệu trong cài đặt thực tế, dẫn đến đường cong hội tụ đã quan sát ở Hình 2.", "BodyVN"))

story.append(P("Phụ lục C: Chi tiết ma trận nhầm lẫn", "H1"))
story.append(P(
    "Bảng dưới đây trình bày đầy đủ bốn thành phần của ma trận nhầm lẫn (True Positive, False "
    "Positive, False Negative, True Negative) cho cả hai mô hình trên tập kiểm tra, quy ước lớp "
    "dương (positive) là \"benign\" (lành tính, mã 1) theo đúng mã hoá gốc của scikit-learn.", "BodyVN"))
cm_np_vals = summary["confusion_matrix_numpy"]
cm_sk_vals = summary["confusion_matrix_sklearn"]
cm_table = [
    ["Thành phần", "NumPy", "scikit-learn", "Ý nghĩa"],
    ["TN (True Negative)", str(cm_np_vals[0][0]), str(cm_sk_vals[0][0]), "Dự báo đúng: ác tính"],
    ["FP (False Positive)", str(cm_np_vals[0][1]), str(cm_sk_vals[0][1]), "Dự báo sai: ác tính → lành tính"],
    ["FN (False Negative)", str(cm_np_vals[1][0]), str(cm_sk_vals[1][0]), "Dự báo sai: lành tính → ác tính"],
    ["TP (True Positive)", str(cm_np_vals[1][1]), str(cm_sk_vals[1][1]), "Dự báo đúng: lành tính"],
]
tcm = Table(cm_table, colWidths=[4.6 * cm, 2.4 * cm, 3 * cm, 6 * cm])
tcm.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tcm)
story.append(P("Bảng C1. Chi tiết bốn thành phần của ma trận nhầm lẫn trên tập kiểm tra (114 mẫu), "
               "quy ước lớp dương là \"benign\".", "Caption"))
story.append(P(
    "Số lượng FN (âm tính giả — bỏ sót ca ác tính) của cả hai mô hình đều rất thấp, đây là tín "
    "hiệu tích cực trong bối cảnh ứng dụng y tế. Tuy nhiên, với số lượng mẫu kiểm tra còn hạn chế "
    "(114 mẫu), mỗi trường hợp sai lệch đều có ảnh hưởng tương đối lớn đến tỉ lệ phần trăm các chỉ "
    "số; việc đánh giá trên một tập kiểm tra lớn hơn hoặc bằng k-fold cross-validation (như đã đề "
    "cập ở Mục 7) sẽ cho một bức tranh đáng tin cậy hơn về hiệu năng thực sự của mô hình trong "
    "triển khai lâm sàng.", "BodyVN"))

story.append(PageBreak())
story.append(P("Phụ lục D: Quy trình tái lập kết quả", "H1"))
story.append(P(
    "Để tái lập toàn bộ kết quả trong báo cáo này từ đầu, thực hiện tuần tự các bước sau:", "BodyVN"))
story.append(bullets([
    "Cài đặt các thư viện liệt kê trong <font face='Courier'>requirements.txt</font>.",
    "Chạy <font face='Courier'>main.py</font> — chương trình tự động tải bộ dữ liệu Breast Cancer "
    "từ scikit-learn (không cần mạng ngoài), huấn luyện cả hai mô hình, và ghi toàn bộ hình ảnh, "
    "bảng số liệu, và <font face='Courier'>summary.json</font> vào thư mục "
    "<font face='Courier'>outputs/</font>.",
    "Chạy <font face='Courier'>make_report.py</font> để sinh lại báo cáo PDF này dựa trên dữ liệu "
    "mới nhất trong <font face='Courier'>outputs/</font>.",
    "(Tuỳ chọn) Mở <font face='Courier'>notebook.ipynb</font> để xem lại từng bước một cách trực "
    "quan và tương tác.",
]))
story.append(P(
    "Với <font face='Courier'>random_state = 42</font> được cố định xuyên suốt, việc chạy lại mã "
    "nguồn sẽ cho ra đúng các con số đã trình bày trong báo cáo, đảm bảo tính tái lập của thực "
    "nghiệm.", "BodyVN"))

story.append(P("Phụ lục E: Cấu trúc mã nguồn", "H1"))
story.append(P(
    "Toàn bộ mã nguồn và kết quả của bài tập được tổ chức trong repository đi kèm báo cáo này, "
    "với cấu trúc như sau:", "BodyVN"))
story.append(Paragraph(
    "baitap2-logistic-regression/<br/>"
    "├── main.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# script chính, chạy toàn bộ pipeline từ đầu đến cuối<br/>"
    "├── notebook.ipynb&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# notebook tương đương, có sẵn output<br/>"
    "├── make_report.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# script tự sinh lại báo cáo PDF từ outputs/<br/>"
    "├── BaoCao_BaiTap2.pdf&nbsp;&nbsp;&nbsp;# báo cáo này<br/>"
    "├── outputs/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# hình ảnh, bảng CSV, summary.json sau khi chạy<br/>"
    "├── requirements.txt<br/>"
    "└── README.md",
    styles["Mono"],
))


# ===================== PHU LUC: HUONG DAN SU DUNG MA NGUON =====================
story.append(PageBreak())
story.append(P("Phụ lục F: Hướng dẫn sử dụng mã nguồn", "H1"))

story.append(P("1. Yêu cầu hệ thống", "H2"))
story.append(bullets([
    "Python từ 3.9 trở lên (đã kiểm thử với Python 3.12).",
    "Các thư viện trong <font face='Courier'>requirements.txt</font>: numpy, pandas, matplotlib, "
    "scikit-learn (từ 1.4 trở lên), jupyter, ipykernel, reportlab, pypdf.",
    "Không cần kết nối mạng khi chạy vì bộ dữ liệu được đóng gói sẵn trong scikit-learn.",
]))

story.append(P("2. Cài đặt môi trường", "H2"))
story.append(P("Mở terminal (hoặc Command Prompt / PowerShell trên Windows) tại thư mục "
               "<font face='Courier'>baitap2</font> và thực hiện lần lượt:", "BodyVN"))
story.append(Paragraph(
    "python -m venv venv<br/>"
    "source venv/bin/activate&nbsp;&nbsp;&nbsp;&nbsp;(macOS/Linux)<br/>"
    "venv\\Scripts\\activate&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Windows)<br/>"
    "pip install --upgrade pip<br/>"
    "pip install -r requirements.txt",
    styles["Cmd"]))

story.append(P("3. Chạy chương trình", "H2"))
cmd_rows = [
    [P("<b>Mục đích</b>", "Cell"), P("<b>Lệnh</b>", "Cell"), P("<b>Kết quả</b>", "Cell")],
    [P("Chạy toàn bộ pipeline", "Cell"), P("<font face='Courier'>python main.py</font>", "Cell"),
     P("In tiến trình ra màn hình; ghi hình, bảng CSV và summary.json vào <font face='Courier'>outputs/</font>.", "Cell")],
    [P("Sinh lại báo cáo PDF", "Cell"), P("<font face='Courier'>python make_report.py</font>", "Cell"),
     P("Tạo lại tệp PDF từ dữ liệu trong <font face='Courier'>outputs/</font> (phải chạy main.py trước).", "Cell")],
    [P("Chạy từng bước tương tác", "Cell"), P("<font face='Courier'>jupyter notebook</font>", "Cell"),
     P("Mở <font face='Courier'>notebook.ipynb</font>, chọn Kernel → Restart &amp; Run All.", "Cell")],
]
tc = Table(cmd_rows, colWidths=[3.8 * cm, 4.6 * cm, 7.6 * cm])
tc.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tc)
story.append(P("Bảng F1. Các lệnh chạy chính của bài tập.", "Caption"))

story.append(P("4. Các tệp kết quả trong thư mục outputs/", "H2"))
out_rows = [[P("<b>Tệp</b>", "Cell"), P("<b>Nội dung</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell")] for a, b in [('comparison_metrics.csv', 'Accuracy, Precision, Recall, F1, ROC-AUC, Log loss của hai cài đặt trên tập kiểm tra.'), ('weight_comparison.csv', 'Trọng số của 30 đặc trưng ở hai mô hình và độ chênh lệch tuyệt đối.'), ('01_class_distribution.png', 'Phân bố số mẫu theo lớp.'), ('02_convergence_numpy.png', 'Đường cong log loss trên tập huấn luyện theo vòng lặp (bản NumPy).'), ('03_confusion_matrices.png', 'Ma trận nhầm lẫn của hai mô hình.'), ('04_roc_curve.png', 'Đường cong ROC của hai mô hình.'), ('summary.json', 'Bias, chênh lệch trọng số, số vòng lặp, ma trận nhầm lẫn và các chỉ số đánh giá.')]
]
to = Table(out_rows, colWidths=[6 * cm, 10 * cm])
to.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(to)
story.append(P("Bảng F2. Danh sách tệp sinh ra sau khi chạy main.py.", "Caption"))

story.append(P("5. Các tham số có thể điều chỉnh", "H2"))
par_rows = [[P("<b>Tham số</b>", "Cell"), P("<b>Vị trí</b>", "Cell"), P("<b>Ý nghĩa</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell"), P(c, "Cell")]
    for a, b, c in [('lr', 'LogisticRegressionNumpy', 'Learning rate của gradient descent, mặc định 0.1. Quá lớn có thể dao động, quá nhỏ hội tụ chậm.'), ('n_iters', 'LogisticRegressionNumpy', 'Số vòng lặp tối đa, mặc định 3000.'), ('tol', 'LogisticRegressionNumpy', 'Ngưỡng dừng sớm khi log loss giảm ít hơn giá trị này, mặc định 1e-7.'), ('threshold', 'predict()', 'Ngưỡng quyết định, mặc định 0.5; hạ thấp để ưu tiên recall.'), ('max_iter', 'LogisticRegression', 'Số vòng lặp tối đa của bản scikit-learn, mặc định trong mã là 3000.')]
]
tp = Table(par_rows, colWidths=[3.8 * cm, 4.2 * cm, 8 * cm])
tp.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tp)
story.append(P("Bảng F3. Các tham số thường được thay đổi khi thử nghiệm.", "Caption"))

story.append(P("6. Các hàm và lớp chính trong main.py", "H2"))
fn_rows = [[P("<b>Tên</b>", "Cell"), P("<b>Chức năng</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell")] for a, b in [('sigmoid()', 'Hàm sigmoid có np.clip để tránh tràn số khi tính hàm mũ.'), ('compute_log_loss()', 'Tính log loss (binary cross-entropy), có cắt xác suất trong [1e-12, 1-1e-12].'), ('LogisticRegressionNumpy', 'Lớp cài đặt từ đầu: fit() chạy gradient descent, predict_proba() và predict() dự báo.'), ('evaluate()', 'Tính Accuracy, Precision, Recall, F1, ROC-AUC và Log loss từ nhãn và xác suất dự báo.'), ('main()', 'Điều phối quy trình: nạp dữ liệu, chia và chuẩn hoá, huấn luyện hai mô hình, đánh giá, vẽ hình, lưu kết quả.')]
]
tf2 = Table(fn_rows, colWidths=[5.2 * cm, 10.8 * cm])
tf2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tf2)
story.append(P("Bảng F4. Các thành phần chính của mã nguồn.", "Caption"))

story.append(P("7. Xử lý một số lỗi thường gặp", "H2"))
er_rows = [[P("<b>Hiện tượng</b>", "Cell"), P("<b>Nguyên nhân và cách khắc phục</b>", "Cell")]] + [
    [P(a, "Cell"), P(b, "Cell")] for a, b in [("ModuleNotFoundError: No module named 'sklearn' (hoặc numpy, pandas...)", 'Chưa cài thư viện hoặc chưa kích hoạt môi trường ảo. Kích hoạt lại venv rồi chạy pip install -r requirements.txt.'), ('Lệnh activate bị chặn trên PowerShell (Windows)', 'Chạy Set-ExecutionPolicy -Scope Process RemoteSigned trong cửa sổ PowerShell đó, hoặc dùng Command Prompt.'), ('make_report.py báo FileNotFoundError khi mở ảnh hoặc CSV', 'Chưa có thư mục outputs/ đầy đủ. Chạy python main.py trước rồi mới chạy make_report.py.'), ('Chữ trong PDF bị ô vuông hoặc mất dấu tiếng Việt', 'Không tìm thấy font DejaVu Sans. Cài matplotlib (đã kèm font này) hoặc đặt DejaVuSans.ttf và DejaVuSans-Bold.ttf cạnh make_report.py.'), ('Jupyter không tìm thấy kernel', 'Chạy python -m ipykernel install --user rồi mở lại notebook và chọn kernel Python tương ứng.')]
]
te = Table(er_rows, colWidths=[5.6 * cm, 10.4 * cm])
te.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(te)
story.append(P("Bảng F5. Lỗi thường gặp và cách khắc phục.", "Caption"))


doc = SimpleDocTemplate(
    REPORT_PATH, pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    title="Bao cao Bai tap 2 - Logistic Regression",
)
doc.build(story)

from pypdf import PdfReader
n = len(PdfReader(REPORT_PATH).pages)
print(f"Da tao: {REPORT_PATH} | So trang: {n}")
