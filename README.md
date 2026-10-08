# Trực quan hóa dữ liệu tương tác — Chương 11 (Nhóm 18)

Ứng dụng web minh họa các toán tử tương tác trong **Chương 11: Các khái niệm tương tác** của sách
*Interactive Data Visualization* (Ward, Grinstein, Keim), xây dựng bằng **Streamlit + Plotly**
trên tập dữ liệu **IBM HR Employee Attrition** (1.470 nhân viên, 35 thuộc tính).

## Nội dung ứng dụng

| Mục | Toán tử | Minh họa |
| :--- | :--- | :--- |
| 11.1.1 | Điều hướng (Navigation) | Grand Tour tự động (quỹ đạo chiếu 2D chạy liên tục, chỉnh kích thước bước); Pan, Zoom 2D; xoay 3D bằng tay ở phiên bản cũ |
| 11.1.2 | Lựa chọn & Brushing | Box/Lasso Select trực tiếp trên biểu đồ, chọn mới thay thế hoặc cộng thêm vào lựa chọn cũ, thống kê và biểu đồ cột cập nhật theo vùng chọn |
| 11.1.3 | Lọc dữ liệu (Filtering) | Loại bỏ hẳn các bản ghi không thỏa điều kiện |
| 11.1.4 | Tái cấu hình & PCA | Đổi ánh xạ trục, giảm chiều bằng PCA |
| 11.1.5 | Mã hóa đồ họa (Encoding) | Trước/Sau khi mã hóa màu và kích thước, so sánh dạng biểu đồ, so sánh bản đồ màu |
| 11.1.6 | Khung nhìn kết nối | Chọn một nhóm, nhiều biểu đồ cùng được làm nổi bật; có thể tách liên kết từng khung để làm mốc so sánh |
| 11.1.7 | Khái quát & Chi tiết | Biến dạng Fisheye (tiêu điểm, phạm vi, mức phóng đại, 2 tiêu điểm); Overview + Detail ở phiên bản cũ |
| 11.3 | Pipeline thống nhất | Lọc, PCA, Mã hóa, Hiển thị; bật/tắt từng bước |

## Yêu cầu

- Python 3.9 trở lên
- Các thư viện trong [requirements.txt](requirements.txt) (Streamlit phải từ 1.35 trở lên để dùng tính năng chọn vùng trên biểu đồ)

## Cài đặt

```bash
git clone https://github.com/ChuThanhDung/GKTQH.git
cd GKTQH

# (khuyến nghị) tạo môi trường ảo
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Chạy ứng dụng

Chạy lệnh sau **trong thư mục chứa `app.py`** (ứng dụng đọc file CSV theo đường dẫn tương đối):

```bash
streamlit run app.py
```

Trình duyệt sẽ tự mở tại http://localhost:8501. Nếu không tự mở, hãy dán địa chỉ này vào trình duyệt.
Muốn đổi cổng: `streamlit run app.py --server.port 8502`. Dừng ứng dụng bằng `Ctrl + C` trong terminal.

## Cấu trúc thư mục

```
app.py                                  # Ứng dụng Streamlit
WA_Fn-UseC_-HR-Employee-Attrition.csv   # Dữ liệu IBM HR Attrition
requirements.txt                        # Thư viện cần cài
.streamlit/config.toml                  # Theme trắng - cam
code_nhom18_gk.ipynb                    # Notebook demo
Slide_nhom18_GK_moi.pptx                # Slide thuyết trình
CONG_NGHE_SU_DUNG.md                    # Công nghệ sử dụng
HUONG_DAN_CODE_DEMO_IPYNB.md            # Hướng dẫn notebook demo
```

## Lỗi thường gặp

- **`streamlit` không được nhận diện:** thử `python -m streamlit run app.py`.
- **Không đọc được file CSV:** chưa chạy lệnh trong thư mục chứa `app.py` và file CSV.
- **Chọn vùng trên biểu đồ (11.1.2) không phản hồi:** kiểm tra `pip show streamlit`, cần bản 1.35 trở lên.
