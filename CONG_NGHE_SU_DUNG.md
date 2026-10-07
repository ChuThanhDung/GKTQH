# 🚀 BÁO CÁO CÔNG NGHỆ & KỸ THUẬT SỬ DỤNG TRONG ĐỒ ÁN

> **Tên đề tài:** Trực quan hóa dữ liệu tương tác (Interactive Data Visualization)  
> **Nội dung:** Minh họa các khái niệm & toán tử tương tác theo **Chương 11 (Ward, Grinstein, Keim)**  
> **Ứng dụng Demo:** Web App Trực Quan Hóa Nhân Sự (IBM HR Attrition)

---

## 📌 1. BẢNG TỔNG QUAN CÔNG NGHỆ (TECH STACK)

| Phân loại | Công nghệ / Thư viện | Vai trò & Mục đích sử dụng |
| :--- | :--- | :--- |
| **Language** | **Python 3.x** | Ngôn ngữ xử lý dữ liệu, thuật toán và logic ứng dụng chính. |
| **Web Framework** | **Streamlit** | Xây dựng giao diện Web tương tác trực tiếp bằng Python mà không cần HTML/JS phức tạp. |
| **Data Viz** | **Plotly (Express & Graph Objects)** | Tạo các biểu đồ 2D & 3D tương tác cao (Pan, Zoom, Hover, Box/Lasso Select, 3D Rotate). |
| **Data Processing** | **Pandas & NumPy** | Nạp dữ liệu CSV, làm sạch, lọc, nhóm, phân tích thống kê và biến đổi dữ liệu. |
| **Machine Learning** | **Scikit-learn (Sklearn)** | • `StandardScaler`: Chuẩn hóa dữ liệu.<br>• `PCA`: Giảm chiều dữ liệu cho toán tử Reconfiguring (11.1.4). |
| **UI Styling** | **Custom CSS & HTML Injection** | Thiết kế giao diện Dark Mode hiện đại, các thẻ Metric Card, Theory Box chuyên nghiệp. |
| **Dataset** | **IBM HR Employee Attrition** | 1,470 nhân viên với 35 thuộc tính số & phân loại. |

---

## 💡 2. CÁCH TRẢ LỜI GIẢNG VIÊN KHI ĐƯỢC HỎI

Khi Giảng viên hỏi: *"Em/Nhóm em dùng công nghệ gì để phát triển bài tập/đồ án này?"*, bạn có thể trả lời theo cấu trúc 3 phần ngắn gọn, rõ ràng như sau:

### 🎤 Mẫu trả lời tham khảo (Khoảng 1 - 2 phút):

> *"Thưa thầy/cô, nhóm em phát triển ứng dụng Web này hoàn toàn bằng **Python** kết hợp với các thư viện chuyên dụng cho trực quan hóa dữ liệu và học máy:*
>
> 1. **Về Giao diện & Web App:** Nhóm em sử dụng **Streamlit** để dựng giao diện Web tương tác nhanh, kết hợp tùy chỉnh **Custom CSS** để tạo theme Dark Mode hiện đại.
> 2. **Về Trực quan hóa dữ liệu (Visualization):** Nhóm em dùng **Plotly (Plotly Express & Graph Objects)**. Thư viện này hỗ trợ mạnh mẽ các tương tác chuẩn như *Zoom, Pan, Hover tooltip, Box Select, Lasso Select, và xoay biểu đồ 3D (Grand Tour)*.
> 3. **Về Xử lý & Thuật toán:** 
>    - Dùng **Pandas & NumPy** để nạp và xử lý tập dữ liệu nhân sự IBM HR (1,470 bản ghi x 35 thuộc tính).
>    - Dùng **Scikit-learn** thực hiện kỹ thuật **PCA (Principal Component Analysis)** giúp giảm chiều dữ liệu từ đa chiều về 2D/3D nhằm minh họa cho toán tử *Tái cấu hình dữ liệu (Reconfiguring)*.
> 
> *Tất cả các chức năng trên Web App đều bám sát theo đúng **8 toán tử tương tác trong Chương 11** của cuốn sách Interactive Data Visualization."*

---

## 🛠️ 3. CHI TIẾT VAI TRÒ CỦA TỪNG CÔNG NGHỆ

### 🌐 1. Streamlit (Web Framework)
- **Tại sao chọn:** Đơn giản, tích hợp trực tiếp với môi trường Python, phản hồi nhanh theo thời gian thực khi người dùng tương tác với thanh trượt (slider), dropdown, radio button.
- **Tính năng áp dụng:**
  - `st.sidebar`: Thanh điều hướng chọn các toán tử tương tác 11.1.1 - 11.1.7.
  - `st.cache_data`: Optimize tốc độ nạp dữ liệu CSV.
  - `st.columns`, `st.tabs`, `st.metric`: Bố trí bố cục Dashboard khoa học.

### 📊 2. Plotly (Interactive Chart Library)
- **Tại sao chọn:** So với Matplotlib hay Seaborn (chỉ tạo hình ảnh tĩnh), Plotly tạo ra các biểu đồ HTML/JS tương tác gốc (Native Interactive Charts).
- **Tính năng áp dụng:**
  - **Pan / Zoom:** Di chuyển và thu phóng không gian góc nhìn.
  - **Grand Tour 3D:** Biểu đồ `px.scatter_3d` cho phép xoay 360° quan sát cấu trúc dữ liệu không gian 3 chiều.
  - **Selected / Unselected Points:** Phục vụ toán tử **Brushing & Selection** (làm mờ điểm không chọn).
  - **Parallel Coordinates (`go.Parcoords`):** Trực quan hóa dữ liệu đa chiều cùng lúc.

### 🤖 3. Scikit-learn (PCA & Normalization)
- **Tại sao chọn:** Thư viện học máy tiêu chuẩn trong Python.
- **Tính năng áp dụng:**
  - **PCA (Principal Component Analysis):** Giảm từ 35 thuộc tính (Tuổi, Lương, Thâm niên, Tỷ lệ theo giờ...) xuống 2 hoặc 3 trục tọa độ chính ($PC_1, PC_2, PC_3$), giúp giữ lại phần lớn biến thiên dữ liệu (Explained Variance Ratio).
  - **StandardScaler:** Vi chuẩn hóa dữ liệu về trung bình bằng 0, độ lệch chuẩn bằng 1 trước khi chạy PCA.

---

## 📚 4. KHUÔN KHỔ LÝ THUYẾT ĐƯỢC ÁP DỤNG (CHƯƠNG 11)

Ứng dụng hiện thực hóa đầy đủ các khái niệm trong sách của **Ward, Grinstein, Keim**:

1. **Navigation (11.1.1):** Pan, Zoom, Grand Tour 3D.
2. **Selection & Brushing (11.1.2):** Lựa chọn điểm dữ liệu, quét vùng (Lasso/Box select).
3. **Filtering (11.1.3):** Lọc theo khoảng giá trị (Range filter) và thuộc tính phân loại.
4. **Reconfiguring (11.1.4):** Sắp xếp lại dữ liệu, chiếu không gian bằng PCA.
5. **Encoding (11.1.5):** Thay đổi mã hóa màu sắc, kích thước hạt dữ liệu theo thuộc tính.
6. **Connection / Linked Views (11.1.6):** Kết nối các biểu đồ (Chọn biểu đồ A -> highlight biểu đồ B).
7. **Overview + Detail (11.1.7):** Xem toàn cảnh công ty và soi chi tiết từng phòng ban/nhân viên.
8. **Unified Pipeline (11.3):** Mô hình đường ống toán tử tương tác.
