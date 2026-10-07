# 📊 THUYẾT MINH & HƯỚNG DẪN CODE DEMO (JUPYTER NOTEBOOK)
## CHƯƠNG 11: CÁC KHÁI NIỆM TƯƠNG TÁC (INTERACTION CONCEPTS)
> **Sách giáo trình**: *Interactive Data Visualization* — Ward, Grinstein, Keim  
> **File code**: `Chuong11_Demo.ipynb`  
> **Tập dữ liệu minh họa**: HR Employee Attrition (IBM) — 1,470 nhân viên, 35 thuộc tính  

---

## I. TỔNG QUAN VỀ SẢN PHẨM CODE DEMO
File Jupyter Notebook `Chuong11_Demo.ipynb` được xây dựng nhằm **minh họa trực tiếp và trực quan toàn bộ các khái niệm lý thuyết cốt lõi trong Chương 11**. 

* **Thư viện chính**:
  * `Plotly` (`plotly.express`, `plotly.graph_objects`): Tạo các biểu đồ tương tác cao (Zoom, Pan, Hover, Box/Lasso Select, Linked Brushing).
  * `Matplotlib` & `Seaborn`: Trực quan hóa tĩnh, biểu diễn Heatmap tương quan và các phép chiếu đa chiều.
  * `scikit-learn` (`PCA`, `StandardScaler`): Thực hiện thuật toán Phân tích Thành phần Chính cho bài toán Tái cấu hình dữ liệu đa chiều.
  * `pandas` & `numpy`: Xử lý, làm sạch và lọc dữ liệu.

---

## II. BẢNG ĐỐI CHIẾU LÝ THUYẾT CHƯƠNG 11 ↔ CÁC CELL TRONG NOTEBOOK

Below là chi tiết cấu trúc 10 phần trong file `Chuong11_Demo.ipynb` tương ứng chính xác với từng mục trong sách giáo trình:

| Phần trong Notebook | Mục trong Sách | Khái niệm Lý thuyết được minh họa | Chi tiết Code & Biểu đồ Demo |
| :--- | :--- | :--- | :--- |
| **0. Cài đặt & Import** | Khởi tạo môi trường | Cấu hình Renderer cho Plotly & thư viện hỗ trợ | Cài đặt `plotly`, `pandas`, `seaborn`, `scikit-learn`, `nbformat`. Đặt `pio.renderers.default = "notebook_connected"`. |
| **1. Đọc dữ liệu** | Ngữ cảnh dữ liệu | Khám phá dữ liệu thực tế (IBM HR Attrition) | Đọc file CSV, thống kê tỷ lệ nghỉ việc (16.1%), tuổi trung bình (36.9 tuổi), thu nhập trung bình ($6,503/tháng). |
| **2. Điều hướng** | **Mục 11.1.1**<br>Navigation | • **Pan, Zoom, Level of Detail (LOD)**<br>• **Grand Tour** (Asimov, 1985 & Mục 11.2.5) | • **Demo 1 (Plotly)**: Biểu đồ Scatter (Tuổi vs Thu nhập) hỗ trợ **cuộn chuột để Zoom** trực tiếp và giữ chuột kéo Pan.<br>• **Demo 2 (Plotly 3D Minimalist Grand Tour)**: Không gian 3D tối giản gồm 3 biến (`Tuổi`, `Thu nhập`, `Kinh nghiệm`), hạt kích thước đồng nhất bằng nhau (size=4). Thao tác **giữ chuột trái kéo xoay 360 độ** chính là thực hiện Grand Tour (quét qua mọi góc chiếu khả dĩ). Rất dễ hiểu và bám sát 100% định nghĩa trong sách. |
| **3. Lựa chọn & Brushing** | **Mục 11.1.2**<br>Selection | • **Cô lập tập con & Highlighting**<br>• **Action on Selection**<br>• **Linked View** | • **Khung 1 (Scatter)**: Nhóm chọn sáng màu Đỏ, phần còn lại mờ Xám để giữ bối cảnh (*Context*).<br>• **Khung 2 (Bar)**: Phân bố phòng ban của riêng nhóm được chọn.<br>• **Hành động sau chọn**: Tự động nhảy số thống kê (Tỷ lệ nghỉ việc 32.5% vs 16.1% toàn cty, Lương TB) và hiển thị ngay bảng chi tiết 5 nhân viên. Không hề phế mà cực kỳ thực tế! |
| **4. Lọc dữ liệu** | **Mục 11.1.3**<br>Filtering | • Phân biệt **Lọc** vs **Lựa chọn**<br>• Giảm tải không gian | So sánh trực tiếp: Trước khi lọc (1,470 người) vs Sau khi lọc điều kiện làm thêm giờ (`OverTime = Yes`, 416 người). Khác với Lựa chọn (chỉ làm mờ), Lọc **xóa bỏ hoàn toàn** các điểm không thỏa mãn khỏi màn hình. |
| **5. Tái cấu hình** | **Mục 11.1.4**<br>Reconfiguration | • **Thay đổi phép ánh xạ X/Y**<br>• **Biến đổi không gian (PCA)** | • **Demo 1**: So sánh cặp có tương quan mạnh (Kinh nghiệm vs Lương) vs cặp phân tán ngẫu nhiên (Khoảng cách vs Hài lòng).<br>• **Demo 2**: PCA nén 15 thuộc tính số xuống 2D (PC1, PC2). |
| **6. Mã hóa dữ liệu** | **Mục 11.1.5**<br>Encoding | • **Đổi dạng trực quan hóa**<br>• So sánh nhận thức | Cùng dữ liệu Lương theo phòng ban: 3 cách mã hóa đồ họa (Bar Chart - trung bình, Boxplot - tứ phân vị & ngoại lai, Scatter - từng cá nhân). Minh họa thông điệp sách: *"Không có biểu đồ nào tối ưu cho mọi nhiệm vụ"*. |
| **7. Kết nối** | **Mục 11.1.6**<br>Connection | • **Linked Views** (Khung nhìn liên kết)<br>• Xây dựng Mental Model | Dashboard 3 khung nhìn liên kết (Tuổi x Lương, Phòng ban, Histogram tuổi) cùng đồng bộ highlight nhóm Nghỉ việc (Màu đỏ). |
| **8. Khái quát hóa & Chi tiết hóa** | **Mục 11.1.7**<br>Abstraction / Elaboration | • **Overview + Detail** | Khung nhìn trên: Overview toàn cảnh 1,470 người kết hợp khung chọn tím. Khung nhìn dưới: Detail phóng to chi tiết nhóm 25–35 tuổi, thấy rõ từng cá nhân. |
| **9. Khuôn khổ thống nhất** | **Mục 11.3**<br>Unified Framework | • **Toán tử × Không gian × Tham số**<br>• **Quy trình xử lý tương tác** | **Pipeline nối tiếp**: Bước 1: Lọc (Sales & R&D) → Bước 2: Tái cấu hình (PCA) → Bước 3: Mã hóa (Màu & Ký hiệu) → Bước 4: Hiển thị. |
| **10. Tổng kết** | Tổng kết | Bảng tổng hợp kiến thức Chương 11 | Bảng hệ thống hóa 8 toán tử tương tác cốt lõi trong giáo trình. |

---

## III. GỢI Ý KỊCH BẢN THUYẾT TRÌNH BẢO VỆ TRƯỚC GIẢNG VIÊN

Khi trình bày bài tập nhóm/báo cáo slide và chạy file `Chuong11_Demo.ipynb` trực tiếp, bạn nên thực hiện các bước thuyết minh sau:

1. **Giới thiệu tổng quan**:
   > *"Thưa thầy/cô, để minh họa cho phần lý thuyết dịch từ Chương 11, nhóm em đã xây dựng file demo `Chuong11_Demo.ipynb` trên tập dữ liệu thực tế HR Employee Attrition của IBM. File gồm 22 cells tinh gọn được chia thành 10 phần bám sát 100% giáo trình."*

2. **Demo Phần Điều hướng (Mục 11.1.1 & Mục 11.2.5)**:
   > *"Đầu tiên là **Điều hướng**. Nhóm sử dụng Plotly để minh họa Zoom và Pan trực tiếp bằng chuột (cuộn chuột phóng to/thu nhỏ, giữ chuột kéo di chuyển). Đặc biệt, để minh họa khái niệm **Grand Tour** (Mục 11.1.1), nhóm đưa 3 biến thực tế: Tuổi, Thu nhập, Kinh nghiệm vào không gian 3D với các hạt kích thước đồng nhất. Thao tác **nhấp giữ chuột trái kéo xoay 360 độ** chính là cho người xem 'đi một vòng quanh khối dữ liệu' (Grand Tour) để quan sát mọi góc chiếu, thấy ngay các điểm đỏ (nghỉ việc) dồn hẳn về một góc: Tuổi trẻ, lương thấp, ít kinh nghiệm."*

3. **Demo Phần Lựa chọn & Brushing (Mục 11.1.2)**:
   > *"Tiếp theo là **Lựa chọn & Brushing**. Nhóm minh họa tương tác hai chiều thực sự (Linked Brushing): (1) Người dùng **kéo chuột khoanh chọn trực tiếp trên biểu đồ Tuổi vs Lương**; (2) Các điểm trong vùng sáng đỏ rực, các điểm ngoài mờ đi để giữ bối cảnh (*Context*); (3) **Biểu đồ Cột bên cạnh và thanh chỉ số thống kê bên dưới tự động tính toán lại và nhảy số tức thì theo thời gian thực**, cho thấy rõ cơ cấu phòng ban và tỷ lệ nghỉ việc của đúng nhóm vừa quét chọn."*

4. **Demo Phần Tái cấu hình & PCA (Mục 11.1.4)**:
   > *"Đối với **Tái cấu hình**, nhóm không chỉ thay đổi ánh xạ các trục X/Y mà còn áp dụng thuật toán **PCA (Phân tích Thành phần Chính)** để giảm 15 thuộc tính số xuống 2 thành phần chính PC1 và PC2, giúp trực quan hóa dữ liệu đa chiều trên mặt phẳng 2D."*

5. **Demo Phần Mã hóa & Bản đồ màu (Mục 11.1.5)**:
   > *"Về **Mã hóa**, nhóm minh họa câu nói cốt lõi của sách: 'Không có biểu đồ nào tối ưu cho mọi nhiệm vụ'. Cùng một thuộc tính Thu nhập, nhóm biểu diễn qua 4 dạng biểu đồ (Scatter, Bar, Boxplot, Violin). Đồng thời so sánh 3 dạng bản đồ màu (*Sequential*, *Diverging*, *Categorical*) và chỉ ra bản đồ màu *Diverging (RdBu)* là tối ưu nhất cho bài toán tương quan vì có điểm trung tâm = 0."*

6. **Kết luận**:
   > *"Cuối cùng ở Mục 11.3, nhóm tổng hợp thành một **Quy trình xử lý tương tác (Pipeline)** kết hợp nối tiếp 4 bước: Lọc → Tái cấu hình → Mã hóa → Hiển thị."*

---

## IV. CÁCH KHẮC PHỤC LỖI KHI BẤM CHẠY TRONG VS CODE
Nếu khi mở file `.ipynb` trong VS Code và bấm nút **Run Cell** bị báo lỗi `ValueError: Mime type rendering requires nbformat>=4.2.0`, hãy thực hiện 2 thao tác:
1. Bấm nút **Restart Kernel** (biểu tượng xoay vòng `↻`) ở thanh công cụ góc trên file Notebook.
2. Chạy **Cell 0** trước để hệ thống thiết lập `pio.renderers.default = "notebook_connected"`, sau đó chạy các cell tiếp theo.
