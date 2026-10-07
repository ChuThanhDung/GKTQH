import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Chương 11 — Các Khái Niệm Tương Tác",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- WHITE + ORANGE THEME ---
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #fff7ed;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        border: 1px solid #fdba74;
        border-radius: 10px;
        padding: 12px 18px;
        box-shadow: 0 2px 8px rgba(249, 115, 22, 0.12);
    }
    div[data-testid="stMetric"] label {
        color: #9a3412 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ea580c !important;
        font-size: 1.8rem !important;
        font-weight: 700;
    }
    .theory-box {
        background: linear-gradient(135deg, #fff7ed 0%, #fffbf5 100%);
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 20px;
        color: #292524;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .theory-box strong { color: #c2410c; }
    .theory-box code {
        color: #ea580c;
        background: #fff7ed;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #fed7aa;
    }
    .theory-box .uses { margin-top: 10px; padding-top: 8px; border-top: 1px dashed #fdba74; color: #44403c; }
    .highlight-red { color: #ef4444; font-weight: bold; }
    .highlight-green { color: #22c55e; font-weight: bold; }
    h1, h2, h3 { color: #9a3412; }

    .side-title { font-size: 1.25rem; font-weight: 700; color: #9a3412; line-height: 1.3; margin-top: 4px; }
    .side-sub { font-size: 0.82rem; color: #78716c; margin: 6px 0 18px 0; line-height: 1.5; }
    .side-section { font-size: 0.72rem; font-weight: 700; letter-spacing: 1.2px; color: #a8a29e;
        border-top: 1px solid #fed7aa; padding-top: 14px; margin-bottom: 6px; }
    .side-data { font-size: 0.8rem; color: #57534e; line-height: 1.6; background: #ffedd5;
        border-left: 3px solid #f97316; border-radius: 6px; padding: 10px 12px; margin-top: 18px; }
    [data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        width: 100%; margin: 0; padding: 9px 12px; border-radius: 8px;
        border-left: 3px solid transparent; cursor: pointer; transition: background 0.15s;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label p { font-size: 0.95rem; color: #44403c; margin: 0; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: #ffedd5; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: #ffedd5; border-left-color: #f97316;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p { color: #9a3412; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = 'plotly_white'
COLOR_YES = '#ef4444'
COLOR_NO = '#22c55e'
COLOR_MAP_ATTRITION = {'No': COLOR_NO, 'Yes': COLOR_YES}
COLOR_DEPT = {'Sales': '#f97316', 'Research & Development': '#0ea5e9', 'Human Resources': '#f59e0b'}

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

try:
    df = load_data()
except Exception as e:
    st.error(f"Không thể đọc file CSV. Lỗi: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown("<div class='side-title'>Trực quan hóa dữ liệu</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div class='side-sub'>Chương 11: Các khái niệm tương tác<br>Ward, Grinstein, Keim</div>",
    unsafe_allow_html=True)
st.sidebar.markdown("<div class='side-section'>NỘI DUNG</div>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Nội dung minh họa",
    [
        "Tổng quan dữ liệu",
        "11.1.1  Điều hướng",
        "11.1.2  Lựa chọn & Brushing",
        "11.1.3  Lọc dữ liệu",
        "11.1.4  Tái cấu hình & PCA",
        "11.1.5  Mã hóa đồ họa",
        "11.1.6  Khung nhìn kết nối",
        "11.1.7  Khái quát & Chi tiết",
        "11.3  Pipeline thống nhất",
        "Bảng tổng kết",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown(
    "<div class='side-data'><b>Dữ liệu</b><br>IBM HR Attrition<br>1.470 nhân viên · 35 thuộc tính</div>",
    unsafe_allow_html=True)

# ==========================================
# 0. TỔNG QUAN
# ==========================================
if menu == "Tổng quan dữ liệu":
    st.title("Tập Dữ Liệu IBM HR Attrition")
    st.markdown("""
    <div class="theory-box">
        <strong>Ngữ cảnh:</strong> Dữ liệu nhân sự gồm 1,470 nhân viên với 35 thuộc tính.
        Toàn bộ toán tử tương tác Chương 11 được minh họa trên tập dữ liệu này.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    total_emp = len(df)
    quit_emp = (df['Attrition'] == 'Yes').sum()
    rate = quit_emp / total_emp * 100

    c1.metric("Tổng nhân viên", f"{total_emp:,}")
    c2.metric("Nghỉ việc", f"{quit_emp}", f"{rate:.1f}%", delta_color="inverse")
    c3.metric("Tuổi trung bình", f"{df['Age'].mean():.1f}")
    c4.metric("Lương TB", f"${df['MonthlyIncome'].mean():,.0f}/th")

    st.subheader("Xem trước dữ liệu")
    cols_show = ['Age', 'MonthlyIncome', 'Department', 'JobRole', 'TotalWorkingYears', 'OverTime', 'Attrition']
    st.dataframe(df[cols_show].head(15), use_container_width=True)

# ==========================================
# 1. ĐIỀU HƯỚNG
# ==========================================
elif menu == "11.1.1  Điều hướng":
    st.title("11.1.1 Điều Hướng (Navigation)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        • <strong>Pan & Zoom:</strong> Thay đổi vị trí camera / mức chi tiết (LOD) mà không biến đổi dữ liệu.<br>
        • <strong>Grand Tour (Asimov 1985):</strong> Chiếu liên tục dữ liệu đa chiều lên không gian con. Xoay 3D 360° = Grand Tour.
        <div class="uses"><strong>Thường dùng để:</strong> Tìm kiếm và khám phá dữ liệu: phóng to xem chi tiết một vùng, thu nhỏ để xem toàn cảnh, kéo (pan) để đổi vùng quan sát, xoay để nhìn dữ liệu đa chiều từ nhiều góc. Hữu ích khi dữ liệu quá lớn hoặc quá dày để đọc trong một khung nhìn.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 Pan & Zoom 2D", "🌐 Grand Tour 3D"])

    with tab1:
        st.subheader("Tuổi vs Thu nhập")
        st.caption("⬅️➡️ Giữ chuột kéo = Pan · 🔍 Cuộn chuột = Zoom")
        fig2d = px.scatter(
            df, x='Age', y='MonthlyIncome', color='Attrition',
            color_discrete_map=COLOR_MAP_ATTRITION,
            labels={'Age': 'Tuổi', 'MonthlyIncome': 'Lương/tháng ($)', 'Attrition': 'Nghỉ việc'},
            opacity=0.7, template=PLOTLY_TEMPLATE
        )
        fig2d.update_layout(height=500, dragmode='pan')
        st.plotly_chart(fig2d, use_container_width=True, config={'scrollZoom': True})

    with tab2:
        st.subheader("Xoay 360° khám phá phân bố đa chiều")
        st.caption("🖱️ Giữ chuột trái kéo xoay theo mọi hướng")
        c_x, c_y, c_z = st.columns(3)
        num_opts = ['Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'DistanceFromHome', 'PercentSalaryHike']
        x_ax = c_x.selectbox("Trục X:", num_opts, index=0)
        y_ax = c_y.selectbox("Trục Y:", num_opts, index=1)
        z_ax = c_z.selectbox("Trục Z:", num_opts, index=2)

        fig3d = px.scatter_3d(
            df, x=x_ax, y=y_ax, z=z_ax, color='Attrition',
            color_discrete_map=COLOR_MAP_ATTRITION,
            labels={'Attrition': 'Nghỉ việc'}, opacity=0.7, template=PLOTLY_TEMPLATE
        )
        fig3d.update_traces(marker=dict(size=4))
        fig3d.update_layout(height=600, margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig3d, use_container_width=True)
        st.success("🎯 Khi xoay 3D, các điểm đỏ (nghỉ việc) tập trung ở góc: **Tuổi trẻ, Lương thấp, Ít kinh nghiệm**.")

# ==========================================
# 2. LỰA CHỌN & BRUSHING (MỚI)
# ==========================================
elif menu == "11.1.2  Lựa chọn & Brushing":
    st.title("11.1.2 Lựa Chọn & Linked Brushing")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        • <strong>Selection:</strong> Cô lập một tập con, điểm không chọn vẫn hiển thị mờ để giữ bối cảnh (Context).<br>
        • <strong>Linked Brushing:</strong> Chọn ở biểu đồ này → phản hồi đồng bộ ở biểu đồ khác & thống kê real-time.
        <div class="uses"><strong>Thường dùng để:</strong> Cô lập các đối tượng quan tâm để làm nổi bật, xem chi tiết hoặc làm đầu vào cho hành động tiếp theo (tính thống kê, lọc, so sánh). Trả lời câu hỏi kiểu "nhóm này có đặc điểm gì?" mà không mất bối cảnh xung quanh.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Brushing trực tiếp trên biểu đồ")
    st.caption("🖱️ Chọn công cụ **Box Select** (⬜) hoặc **Lasso Select** (〰️) trên thanh công cụ biểu đồ, rồi kéo chuột khoanh vùng dữ liệu.")

    fig_brush = go.Figure()
    fig_brush.add_trace(go.Scatter(
        x=df['Age'].values,
        y=df['MonthlyIncome'].values,
        mode='markers',
        marker=dict(
            color=[COLOR_YES if a == 'Yes' else COLOR_NO for a in df['Attrition']],
            size=6, opacity=0.7
        ),
        selected=dict(marker=dict(opacity=1, size=10)),
        unselected=dict(marker=dict(opacity=0.12, size=4)),
        hovertemplate='Tuổi: %{x}<br>Lương: $%{y:,.0f}<extra></extra>'
    ))
    fig_brush.update_layout(
        template=PLOTLY_TEMPLATE, height=500, dragmode='select',
        xaxis_title='Tuổi', yaxis_title='Lương/tháng ($)',
        title='Kéo chuột khoanh vùng để Brush (Box/Lasso Select)'
    )

    selected_indices = []
    try:
        event = st.plotly_chart(
            fig_brush, on_select="rerun", key="brush_main", use_container_width=True
        )
        if event.selection and event.selection.point_indices:
            selected_indices = event.selection.point_indices
    except (TypeError, AttributeError):
        st.plotly_chart(fig_brush, use_container_width=True)
        st.warning("⚠️ Cần Streamlit ≥ 1.35 để dùng Linked Brushing. Cập nhật: `pip install -U streamlit`")

    if selected_indices:
        sel_df = df.iloc[selected_indices]
        sel_quit = (sel_df['Attrition'] == 'Yes').sum()
        sel_rate = sel_quit / len(sel_df) * 100

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Đã chọn", f"{len(sel_df)} / {len(df)}")
        m2.metric("Nghỉ việc trong vùng chọn", f"{sel_quit}", f"{sel_rate:.1f}%", delta_color="inverse")
        m3.metric("So với toàn công ty", "16.1%", f"{sel_rate - 16.1:+.1f}%", delta_color="inverse")
        m4.metric("Lương TB vùng chọn", f"${sel_df['MonthlyIncome'].mean():,.0f}")

        c_linked1, c_linked2 = st.columns(2)
        with c_linked1:
            dept_counts = sel_df['Department'].value_counts()
            fig_bar = go.Figure(go.Bar(
                x=dept_counts.index, y=dept_counts.values,
                marker_color=[COLOR_DEPT.get(d, '#f97316') for d in dept_counts.index],
                text=dept_counts.values, textposition='outside'
            ))
            fig_bar.update_layout(
                template=PLOTLY_TEMPLATE, height=350,
                title="Linked: Phòng ban nhóm đã chọn"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c_linked2:
            role_counts = sel_df['JobRole'].value_counts().head(5)
            fig_role = go.Figure(go.Bar(
                x=role_counts.values, y=role_counts.index, orientation='h',
                marker_color='#f97316',
                text=role_counts.values, textposition='outside'
            ))
            fig_role.update_layout(
                template=PLOTLY_TEMPLATE, height=350,
                title="Linked: Top 5 vị trí trong vùng chọn"
            )
            st.plotly_chart(fig_role, use_container_width=True)

        with st.expander("📋 Xem danh sách nhân viên trong vùng chọn"):
            st.dataframe(
                sel_df[['Age', 'MonthlyIncome', 'Department', 'JobRole', 'TotalWorkingYears', 'Attrition']].head(15),
                use_container_width=True
            )
    else:
        st.info("👆 Dùng **Box Select** hoặc **Lasso Select** trên biểu đồ để chọn một nhóm điểm. Các chỉ số và biểu đồ liên kết sẽ tự động cập nhật.")

    with st.expander("📂 Xem phiên bản Brushing bằng Slider (cũ)"):
        col_f1, col_f2 = st.columns(2)
        age_range = col_f1.slider("Vùng quét Tuổi:", int(df['Age'].min()), int(df['Age'].max()), (22, 35), key="old_age")
        inc_range = col_f2.slider("Vùng quét Lương:", int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max()), (1000, 6000), key="old_inc")
        mask = (
            (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
            (df['MonthlyIncome'] >= inc_range[0]) & (df['MonthlyIncome'] <= inc_range[1])
        )
        selected_old = df[mask]
        unselected_old = df[~mask]

        fig_old = go.Figure()
        fig_old.add_trace(go.Scatter(
            x=unselected_old['Age'], y=unselected_old['MonthlyIncome'],
            mode='markers', marker=dict(color='#d1d5db', size=4, opacity=0.3), name='Ngoài vùng chọn'
        ))
        fig_old.add_trace(go.Scatter(
            x=selected_old['Age'], y=selected_old['MonthlyIncome'],
            mode='markers', marker=dict(
                color=selected_old['Attrition'].map({'Yes': COLOR_YES, 'No': COLOR_NO}),
                size=6, opacity=0.9
            ), name='Trong vùng chọn'
        ))
        fig_old.update_layout(template=PLOTLY_TEMPLATE, height=400, showlegend=False)
        st.plotly_chart(fig_old, use_container_width=True)

# ==========================================
# 3. LỌC DỮ LIỆU
# ==========================================
elif menu == "11.1.3  Lọc dữ liệu":
    st.title("11.1.3 Lọc Dữ Liệu (Filtering)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        Khác với Lựa chọn (giữ bối cảnh, chỉ làm mờ), <strong>Lọc</strong> sẽ <strong>xóa bỏ hoàn toàn</strong>
        các bản ghi không thỏa mãn khỏi màn hình để giảm tải nhận thức.
        <div class="uses"><strong>Thường dùng để:</strong> Thu hẹp phạm vi dữ liệu theo điều kiện để giảm quá tải thị giác và tập trung vào nhóm cần phân tích; loại bỏ nhiễu và giảm hiện tượng các điểm chồng lên nhau (overplotting).</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    filter_attr = col1.selectbox("Thuộc tính lọc:", ['OverTime', 'Department', 'MaritalStatus', 'Gender', 'JobRole'])
    unique_vals = df[filter_attr].unique().tolist()
    filter_val = col2.selectbox("Giá trị:", unique_vals)

    filtered_df = df[df[filter_attr] == filter_val]

    m1, m2, m3 = st.columns(3)
    m1.metric("Dữ liệu ban đầu", f"{len(df)} người")
    m2.metric(f"Sau lọc ({filter_val})", f"{len(filtered_df)} người", f"-{len(df) - len(filtered_df)} loại bỏ")
    f_rate = (filtered_df['Attrition'] == 'Yes').mean() * 100
    m3.metric("Tỷ lệ nghỉ việc nhóm lọc", f"{f_rate:.1f}%", f"{f_rate - 16.1:+.1f}% so với toàn cty", delta_color="inverse")

    c_f1, c_f2 = st.columns(2)
    with c_f1:
        fig_before = px.scatter(
            df, x='Age', y='MonthlyIncome', color='Attrition',
            color_discrete_map=COLOR_MAP_ATTRITION,
            title=f"TRƯỚC LỌC (1,470 người)", template=PLOTLY_TEMPLATE, opacity=0.35
        )
        fig_before.update_layout(height=450)
        st.plotly_chart(fig_before, use_container_width=True)

    with c_f2:
        fig_after = px.scatter(
            filtered_df, x='Age', y='MonthlyIncome', color='Attrition',
            color_discrete_map=COLOR_MAP_ATTRITION,
            title=f"SAU LỌC: {filter_val} ({len(filtered_df)} người)", template=PLOTLY_TEMPLATE, opacity=0.85
        )
        fig_after.update_layout(height=450)
        st.plotly_chart(fig_after, use_container_width=True)

# ==========================================
# 4. TÁI CẤU HÌNH & PCA
# ==========================================
elif menu == "11.1.4  Tái cấu hình & PCA":
    st.title("11.1.4 Tái Cấu Hình (Reconfiguration)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        • <strong>Đổi ánh xạ trục:</strong> Thay thuộc tính X/Y để tìm tương quan ẩn.<br>
        • <strong>PCA (Biến đổi không gian):</strong> Nén nhiều chiều về 2D/3D giữ tối đa phương sai.
        <div class="uses"><strong>Thường dùng để:</strong> Nhìn cùng một dữ liệu từ góc độ khác: đổi trục, sắp xếp lại, giảm chiều. Giúp phát hiện tương quan, cụm và ngoại lệ mà cách bố trí ban đầu đã che khuất.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📈 Đổi ánh xạ trục", "🧮 PCA giảm chiều"])

    with tab1:
        st.subheader("Cặp tương quan mạnh vs Cặp phân tán ngẫu nhiên")
        c1, c2 = st.columns(2)
        with c1:
            fig_c1 = px.scatter(
                df, x='TotalWorkingYears', y='MonthlyIncome', color='Attrition',
                color_discrete_map=COLOR_MAP_ATTRITION,
                title="Kinh nghiệm vs Lương (tương quan mạnh)", template=PLOTLY_TEMPLATE, opacity=0.6
            )
            fig_c1.update_layout(height=420)
            st.plotly_chart(fig_c1, use_container_width=True)
        with c2:
            fig_c2 = px.scatter(
                df, x='DistanceFromHome', y='JobSatisfaction', color='Attrition',
                color_discrete_map=COLOR_MAP_ATTRITION,
                title="Khoảng cách vs Hài lòng (phân tán)", template=PLOTLY_TEMPLATE, opacity=0.6
            )
            fig_c2.update_layout(height=420)
            st.plotly_chart(fig_c2, use_container_width=True)

    with tab2:
        st.subheader("PCA: Nén 15 thuộc tính → 2 thành phần chính")
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        num_cols = [c for c in num_cols if c not in ['EmployeeCount', 'StandardHours', 'EmployeeNumber']]

        X_scaled = StandardScaler().fit_transform(df[num_cols])
        pca = PCA(n_components=2)
        coords = pca.fit_transform(X_scaled)

        df_pca = pd.DataFrame({
            'PC1': coords[:, 0], 'PC2': coords[:, 1],
            'Attrition': df['Attrition'], 'Department': df['Department']
        })

        var_explained = pca.explained_variance_ratio_.sum() * 100
        st.info(f"💡 PC1 + PC2 giải thích **{var_explained:.1f}%** phương sai của {len(num_cols)} chiều gốc.")

        color_by = st.selectbox("Biến phân tách màu:", ['Attrition', 'Department'])
        cmap = COLOR_MAP_ATTRITION if color_by == 'Attrition' else COLOR_DEPT

        fig_pca = px.scatter(
            df_pca, x='PC1', y='PC2', color=color_by,
            color_discrete_map=cmap,
            title=f"Không gian 2D sau PCA (từ {len(num_cols)} chiều)", template=PLOTLY_TEMPLATE, opacity=0.7
        )
        fig_pca.update_layout(height=520)
        st.plotly_chart(fig_pca, use_container_width=True)

# ==========================================
# 5. MÃ HÓA ĐỒ HỌA (MỚI + CŨ)
# ==========================================
elif menu == "11.1.5  Mã hóa đồ họa":
    st.title("11.1.5 Mã Hóa Đồ Họa (Encoding)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        <em>'Không có dạng biểu diễn nào tối ưu cho mọi nhiệm vụ'</em> (Ward, Grinstein, Keim).<br>
        Thay đổi hình thức đồ họa (Bar, Boxplot, Scatter, Violin) và bản đồ màu (Colormap) phục vụ các mục tiêu nhận thức khác nhau.
        <div class="uses"><strong>Thường dùng để:</strong> Chọn cách biểu diễn phù hợp với nhiệm vụ: so sánh giá trị, xem phân phối, thấy mật độ, hoặc biểu thị thêm thuộc tính bằng màu sắc, kích thước, hình dạng. Đổi mã hóa giúp nhấn mạnh những đặc trưng khác nhau của cùng một dữ liệu.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_enc0, tab_enc1, tab_enc2 = st.tabs([
        "✨ Trước / Sau: mã hóa thuộc tính", "📊 So sánh dạng biểu đồ", "🎨 So sánh bản đồ màu (Colormap)"
    ])

    with tab_enc0:
        st.subheader("Cùng một Scatter — thêm Màu sắc & Kích thước để lộ thêm thông tin")
        st.caption("Trái: chỉ vị trí (X, Y). Phải: mã hóa thêm 2 thuộc tính bằng màu và kích thước hạt.")

        enc_attrs = {
            'Số năm tại công ty': 'YearsAtCompany',
            'Tổng số năm làm việc': 'TotalWorkingYears',
            'Khoảng cách từ nhà (km)': 'DistanceFromHome',
            'Mức hài lòng công việc': 'JobSatisfaction',
            'Tuổi': 'Age',
        }
        ec1, ec2 = st.columns(2)
        color_label = ec1.selectbox("Mã hóa bằng MÀU SẮC theo:", list(enc_attrs.keys()), index=0, key="enc_color")
        size_label = ec2.selectbox("Mã hóa bằng KÍCH THƯỚC theo:", list(enc_attrs.keys()), index=2, key="enc_size")
        color_col, size_col = enc_attrs[color_label], enc_attrs[size_label]

        color_vals = df[color_col]
        size_vals = df[size_col]
        marker_sizes = 4 + 16 * (size_vals - size_vals.min()) / max(size_vals.max() - size_vals.min(), 1)

        fig_ba = make_subplots(rows=1, cols=2, subplot_titles=["Trước: chưa mã hóa", "Sau: mã hóa màu + kích thước"],
                               horizontal_spacing=0.08, shared_yaxes=True)
        fig_ba.add_trace(go.Scatter(
            x=df['Age'], y=df['MonthlyIncome'], mode='markers',
            marker=dict(color='#bdbdbd', size=7, opacity=0.7), showlegend=False,
            hovertemplate='Tuổi: %{x}<br>Thu nhập: $%{y:,}<extra></extra>'
        ), row=1, col=1)
        fig_ba.add_trace(go.Scatter(
            x=df['Age'], y=df['MonthlyIncome'], mode='markers',
            marker=dict(color=color_vals, colorscale='Oranges', size=marker_sizes, opacity=0.8,
                        showscale=True, colorbar=dict(title=color_label, len=0.8, x=1.02)),
            showlegend=False, customdata=np.column_stack([color_vals, size_vals]),
            hovertemplate='Tuổi: %{x}<br>Thu nhập: $%{y:,}<br>' + color_label + ': %{customdata[0]}<br>' + size_label + ': %{customdata[1]}<extra></extra>'
        ), row=1, col=2)
        fig_ba.update_xaxes(title_text="Tuổi")
        fig_ba.update_yaxes(title_text="Thu nhập hàng tháng ($)", row=1, col=1)
        fig_ba.update_layout(template=PLOTLY_TEMPLATE, height=520, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_ba, use_container_width=True)
        st.info("💡 Màu đậm = giá trị lớn, hạt to = giá trị lớn. Cùng dữ liệu, nhưng mã hóa thêm thuộc tính giúp thấy ngay các cụm nhân viên khác nhau.")

    with tab_enc1:
        st.subheader("Cùng dữ liệu Lương theo Phòng ban — 4 cách mã hóa")

        fig_enc = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                "1. Bar Chart: Giá trị trung bình",
                "2. Boxplot: Tứ phân vị & ngoại lai",
                "3. Scatter: Mật độ từng cá nhân",
                "4. Violin: Phân phối mật độ liên tục"
            ],
            vertical_spacing=0.12
        )

        dept_mean = df.groupby('Department')['MonthlyIncome'].mean().reset_index()
        fig_enc.add_trace(go.Bar(
            x=dept_mean['Department'], y=dept_mean['MonthlyIncome'],
            marker_color='#f97316', name='Lương TB', showlegend=False
        ), row=1, col=1)

        for dept_name, col in COLOR_DEPT.items():
            sub = df[df['Department'] == dept_name]['MonthlyIncome']
            fig_enc.add_trace(go.Box(y=sub, name=dept_name, marker_color=col, showlegend=False), row=1, col=2)

        fig_enc.add_trace(go.Scatter(
            x=df['Department'], y=df['MonthlyIncome'],
            mode='markers', marker=dict(color='#f97316', size=3, opacity=0.3), showlegend=False
        ), row=2, col=1)

        for dept_name, col in COLOR_DEPT.items():
            sub = df[df['Department'] == dept_name]['MonthlyIncome']
            fig_enc.add_trace(go.Violin(y=sub, name=dept_name, fillcolor=col, opacity=0.6, line_color=col, showlegend=False), row=2, col=2)

        fig_enc.update_layout(template=PLOTLY_TEMPLATE, height=700)
        st.plotly_chart(fig_enc, use_container_width=True)

        st.markdown("""
        | Dạng biểu đồ | Mục đích tối ưu | Điểm yếu |
        | :--- | :--- | :--- |
        | **Bar** | So sánh nhanh giá trị đại diện (Mean) | Giấu độ lệch chuẩn và ngoại lai |
        | **Boxplot** | Phân bố thống kê (Min, Q1, Median, Q3, Max) | Không thấy số lượng mẫu |
        | **Scatter** | Phát hiện mật độ cụm & cá nhân ngoại lệ | Overplotting khi dữ liệu lớn |
        | **Violin** | Hình dạng phân phối liên tục | Khó đọc giá trị cụ thể |
        """)

    with tab_enc2:
        st.subheader("So sánh 3 loại bản đồ màu (Colormap)")
        st.caption("Cùng dữ liệu tương quan giữa các thuộc tính số — khác colormap → khác nhận thức.")

        num_cols_corr = ['Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'DistanceFromHome', 'JobSatisfaction']
        corr_matrix = df[num_cols_corr].corr()

        c_cm1, c_cm2, c_cm3 = st.columns(3)

        with c_cm1:
            fig_seq = px.imshow(
                corr_matrix, text_auto='.2f', color_continuous_scale='Oranges',
                title='Sequential (Oranges)', template=PLOTLY_TEMPLATE,
                labels=dict(color="Tương quan")
            )
            fig_seq.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_seq, use_container_width=True)
            st.caption("✅ Tốt cho giá trị **một chiều** (0 → max)")

        with c_cm2:
            fig_div = px.imshow(
                corr_matrix, text_auto='.2f', color_continuous_scale='RdBu_r',
                title='Diverging (RdBu)', template=PLOTLY_TEMPLATE, zmin=-1, zmax=1,
                labels=dict(color="Tương quan")
            )
            fig_div.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_div, use_container_width=True)
            st.caption("✅ **Tối ưu nhất** cho tương quan: trung tâm = 0, hai cực rõ ràng")

        with c_cm3:
            fig_cat = px.imshow(
                corr_matrix, text_auto='.2f', color_continuous_scale='Rainbow',
                title='Qualitative / Rainbow', template=PLOTLY_TEMPLATE,
                labels=dict(color="Tương quan")
            )
            fig_cat.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_cat, use_container_width=True)
            st.caption("❌ **Sai mục đích**: Rainbow gây hiểu nhầm thứ tự dữ liệu liên tục")

    with st.expander("📂 Xem phiên bản cũ (3 biểu đồ ngang)"):
        fig_old_enc = make_subplots(
            rows=1, cols=3,
            subplot_titles=["Bar Chart", "Boxplot", "Scatter Plot"]
        )
        fig_old_enc.add_trace(go.Bar(
            x=dept_mean['Department'], y=dept_mean['MonthlyIncome'],
            marker_color='#f97316', showlegend=False
        ), row=1, col=1)
        for dept_name, col in COLOR_DEPT.items():
            fig_old_enc.add_trace(go.Box(
                y=df[df['Department'] == dept_name]['MonthlyIncome'],
                name=dept_name, marker_color=col, showlegend=False
            ), row=1, col=2)
        fig_old_enc.add_trace(go.Scatter(
            x=df['Department'], y=df['MonthlyIncome'],
            mode='markers', marker=dict(color='#d1d5db', size=3, opacity=0.4), showlegend=False
        ), row=1, col=3)
        fig_old_enc.update_layout(template=PLOTLY_TEMPLATE, height=400)
        st.plotly_chart(fig_old_enc, use_container_width=True)

# ==========================================
# 6. KHUNG NHÌN KẾT NỐI (MỚI)
# ==========================================
elif menu == "11.1.6  Khung nhìn kết nối":
    st.title("11.1.6 Khung Nhìn Kết Nối (Connected Views)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        • Ghép nối nhiều khung nhìn độc lập cùng chia sẻ chung quy ước mã hóa & bộ lọc tương tác.<br>
        • Khi thay đổi tham số ở một nơi, <strong>tất cả các khung nhìn đồng bộ cập nhật</strong> → giúp xây dựng Mental Model tổng thể.
        <div class="uses"><strong>Thường dùng để:</strong> Kết hợp ưu điểm của nhiều khung nhìn: mỗi biểu đồ cho thấy một khía cạnh, chọn ở một nơi thì thấy phần tương ứng ở các nơi khác. Giúp kiểm tra mối liên hệ giữa nhiều thuộc tính cùng lúc và diễn đạt các ràng buộc phức tạp.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Bộ điều khiển đồng bộ")
    ctrl1, ctrl2 = st.columns(2)
    highlight_group = ctrl1.selectbox(
        "Nhóm highlight trên tất cả khung nhìn:",
        ["Nghỉ việc (Yes)", "Sales", "Research & Development", "Human Resources", "Tuổi < 30", "Lương < $5,000"]
    )
    show_context = ctrl2.checkbox("Hiện điểm nền (Context)", value=True)

    if highlight_group == "Nghỉ việc (Yes)":
        mask_hl = df['Attrition'] == 'Yes'
        hl_color = COLOR_YES
    elif highlight_group in ["Sales", "Research & Development", "Human Resources"]:
        mask_hl = df['Department'] == highlight_group
        hl_color = COLOR_DEPT[highlight_group]
    elif highlight_group == "Tuổi < 30":
        mask_hl = df['Age'] < 30
        hl_color = '#f97316'
    else:
        mask_hl = df['MonthlyIncome'] < 5000
        hl_color = '#f97316'

    hl_df = df[mask_hl]
    bg_df = df[~mask_hl]

    st.markdown(f"**Nhóm highlight:** {len(hl_df)} người · **Nền:** {len(bg_df)} người")

    c_v1, c_v2, c_v3 = st.columns(3)

    with c_v1:
        fig_v1 = go.Figure()
        if show_context:
            fig_v1.add_trace(go.Scatter(
                x=bg_df['Age'], y=bg_df['MonthlyIncome'], mode='markers',
                marker=dict(color='#e5e7eb', size=3, opacity=0.3), name='Nền', showlegend=False
            ))
        fig_v1.add_trace(go.Scatter(
            x=hl_df['Age'], y=hl_df['MonthlyIncome'], mode='markers',
            marker=dict(color=hl_color, size=5, opacity=0.8), name='Highlight', showlegend=False
        ))
        fig_v1.update_layout(template=PLOTLY_TEMPLATE, height=380, title="Khung 1: Tuổi × Lương",
                             xaxis_title="Tuổi", yaxis_title="Lương ($)")
        st.plotly_chart(fig_v1, use_container_width=True)

    with c_v2:
        dept_all = df['Department'].value_counts()
        dept_hl = hl_df['Department'].value_counts().reindex(dept_all.index, fill_value=0)
        fig_v2 = go.Figure()
        fig_v2.add_trace(go.Bar(
            x=dept_all.index, y=dept_all.values,
            marker_color='#e5e7eb', name='Tổng', showlegend=True
        ))
        fig_v2.add_trace(go.Bar(
            x=dept_hl.index, y=dept_hl.values,
            marker_color=hl_color, name='Highlight', showlegend=True
        ))
        fig_v2.update_layout(template=PLOTLY_TEMPLATE, height=380, title="Khung 2: Phòng ban",
                             barmode='overlay', yaxis_title="Số người")
        st.plotly_chart(fig_v2, use_container_width=True)

    with c_v3:
        fig_v3 = go.Figure()
        if show_context:
            fig_v3.add_trace(go.Histogram(
                x=bg_df['Age'], marker_color='#e5e7eb', nbinsx=20, name='Nền', showlegend=False
            ))
        fig_v3.add_trace(go.Histogram(
            x=hl_df['Age'], marker_color=hl_color, nbinsx=20, name='Highlight', opacity=0.8, showlegend=False
        ))
        fig_v3.update_layout(template=PLOTLY_TEMPLATE, height=380, title="Khung 3: Phân bố tuổi",
                             barmode='overlay', xaxis_title="Tuổi", yaxis_title="Số người")
        st.plotly_chart(fig_v3, use_container_width=True)

    st.success(f"🎯 **Thông điệp kết nối:** Thay đổi nhóm highlight ở bộ điều khiển → cả 3 khung nhìn đồng bộ cập nhật, giúp bạn nhanh chóng so sánh đặc điểm của bất kỳ nhóm nào từ nhiều góc độ.")

    with st.expander("📂 Xem phiên bản cũ (3 subplot tĩnh)"):
        yes_df = df[df['Attrition'] == 'Yes']
        no_df = df[df['Attrition'] == 'No']
        fig_old_conn = make_subplots(rows=1, cols=3, subplot_titles=["Tuổi × Lương", "% Nghỉ việc/PB", "Tháp tuổi"])
        fig_old_conn.add_trace(go.Scatter(
            x=no_df['Age'], y=no_df['MonthlyIncome'], mode='markers',
            marker=dict(color=COLOR_NO, size=3, opacity=0.3), name='Ở lại'
        ), row=1, col=1)
        fig_old_conn.add_trace(go.Scatter(
            x=yes_df['Age'], y=yes_df['MonthlyIncome'], mode='markers',
            marker=dict(color=COLOR_YES, size=5, opacity=0.8), name='Nghỉ việc'
        ), row=1, col=1)
        attr_rate = df.groupby('Department')['Attrition'].apply(lambda x: (x == 'Yes').mean() * 100).round(1)
        fig_old_conn.add_trace(go.Bar(
            x=attr_rate.index, y=attr_rate.values, marker_color=COLOR_YES,
            text=[f"{v}%" for v in attr_rate.values], textposition='outside', showlegend=False
        ), row=1, col=2)
        fig_old_conn.add_trace(go.Histogram(
            x=yes_df['Age'], marker_color=COLOR_YES, nbinsx=15, showlegend=False
        ), row=1, col=3)
        fig_old_conn.update_layout(template=PLOTLY_TEMPLATE, height=400)
        st.plotly_chart(fig_old_conn, use_container_width=True)

# ==========================================
# 7. OVERVIEW + DETAIL
# ==========================================
elif menu == "11.1.7  Khái quát & Chi tiết":
    st.title("11.1.7 Overview + Detail")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết:</strong><br>
        Shneiderman (1996): <em>'Overview first, zoom and filter, then details-on-demand'</em>.<br>
        Khung trên = <strong>Overview</strong> (toàn cảnh), khung dưới = <strong>Detail</strong> (phóng to chi tiết).
        <div class="uses"><strong>Thường dùng để:</strong> Đi từ tổng quan đến chi tiết theo yêu cầu: xem bức tranh chung trước, sau đó đào sâu từng vùng mà vẫn giữ ngữ cảnh. Cân bằng giữa cái nhìn toàn cục và chi tiết cục bộ.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Chọn vùng tuổi tiêu điểm:")
    focus_age = st.slider("Cửa sổ tiêu điểm:", 18, 60, (25, 35))
    focus_df = df[(df['Age'] >= focus_age[0]) & (df['Age'] <= focus_age[1])]

    fig_od = make_subplots(
        rows=2, cols=1, row_heights=[0.35, 0.65],
        subplot_titles=[
            f"OVERVIEW: Toàn cảnh 1,470 người (vùng cam: {focus_age[0]}–{focus_age[1]} tuổi)",
            f"DETAIL: Phóng to {focus_age[0]}–{focus_age[1]} tuổi ({len(focus_df)} người)"
        ]
    )

    fig_od.add_trace(go.Scatter(
        x=df['Age'], y=df['MonthlyIncome'], mode='markers',
        marker=dict(color='#d1d5db', size=3, opacity=0.3), showlegend=False
    ), row=1, col=1)
    fig_od.add_vrect(
        x0=focus_age[0], x1=focus_age[1],
        fillcolor='#f97316', opacity=0.2, line_width=1.5, line_color='#f97316',
        row=1, col=1
    )

    fig_od.add_trace(go.Scatter(
        x=focus_df['Age'], y=focus_df['MonthlyIncome'], mode='markers',
        marker=dict(
            color=focus_df['Attrition'].map({'Yes': COLOR_YES, 'No': COLOR_NO}),
            size=6, opacity=0.85
        ), showlegend=False
    ), row=2, col=1)

    fig_od.update_layout(template=PLOTLY_TEMPLATE, height=600)
    st.plotly_chart(fig_od, use_container_width=True)

# ==========================================
# 8. PIPELINE
# ==========================================
elif menu == "11.3  Pipeline thống nhất":
    st.title("11.3 Khuôn Khổ Thống Nhất (Pipeline)")
    st.markdown("""
    <div class="theory-box">
        <strong>Lý thuyết (Mục 11.3):</strong> Các toán tử không dùng riêng lẻ mà <strong>nối tiếp thành một chuỗi xử lý</strong>:
        đầu ra của bước trước là đầu vào của bước sau. Người dùng có thể can thiệp vào <strong>bất kỳ bước nào</strong>,
        và mọi bước đều <strong>tùy chọn — có thể bật/tắt</strong>.<br>
        <code>Dữ liệu gốc ➔ Lọc ➔ Tái cấu hình (PCA) ➔ Mã hóa ➔ Hiển thị</code>
        <div class="uses"><strong>Thường dùng để:</strong> Ghép nhiều toán tử thành một quy trình phân tích hoàn chỉnh: thu hẹp dữ liệu, đổi cách nhìn, mã hóa rồi hiển thị; người dùng tinh chỉnh từng bước để tự khám phá.</div>
    </div>
    """, unsafe_allow_html=True)

    PCA_CANDIDATES = {
        'Tuổi': 'Age', 'Thu nhập hàng tháng': 'MonthlyIncome', 'Tổng năm làm việc': 'TotalWorkingYears',
        'Số năm tại công ty': 'YearsAtCompany', 'Khoảng cách từ nhà': 'DistanceFromHome',
        'Số năm ở vai trò hiện tại': 'YearsInCurrentRole', 'Mức hài lòng công việc': 'JobSatisfaction',
        'Số năm từ lần thăng chức cuối': 'YearsSinceLastPromotion',
    }
    COLOR_OPTIONS = {'Phòng ban': 'Department', 'Nghỉ việc (Attrition)': 'Attrition', 'Làm thêm giờ (OverTime)': 'OverTime',
                     'Giới tính': 'Gender', 'Tình trạng hôn nhân': 'MaritalStatus', 'Chức danh': 'JobRole'}
    SYMBOL_OPTIONS = {'Không dùng': None, 'Nghỉ việc (Attrition)': 'Attrition', 'Làm thêm giờ (OverTime)': 'OverTime',
                      'Giới tính': 'Gender'}
    SIZE_OPTIONS = {'Không dùng': None, 'Thu nhập hàng tháng': 'MonthlyIncome', 'Số năm tại công ty': 'YearsAtCompany',
                    'Tổng năm làm việc': 'TotalWorkingYears'}

    # ---- Điều khiển 3 bước ----
    st.markdown("### 🎛️ Điều khiển Pipeline")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**① Lọc (Filtering)**")
        use_filter = st.checkbox("Bật bước Lọc", value=True, key="pp_use_filter")
        selected_depts = st.multiselect("Phòng ban:", df['Department'].unique().tolist(),
                                        default=['Sales', 'Research & Development'], disabled=not use_filter, key="pp_depts")
        age_range = st.slider("Khoảng tuổi:", int(df['Age'].min()), int(df['Age'].max()),
                              (int(df['Age'].min()), int(df['Age'].max())), disabled=not use_filter, key="pp_age")
        overtime_opt = st.radio("Làm thêm giờ:", ['Tất cả', 'Yes', 'No'], horizontal=True,
                                disabled=not use_filter, key="pp_ot")

    with c2:
        st.markdown("**② Tái cấu hình (PCA)**")
        use_pca = st.checkbox("Bật bước PCA (nén chiều)", value=True, key="pp_use_pca")
        if use_pca:
            pca_labels = st.multiselect("Thuộc tính đưa vào PCA:", list(PCA_CANDIDATES.keys()),
                                        default=['Tuổi', 'Thu nhập hàng tháng', 'Tổng năm làm việc', 'Số năm tại công ty'],
                                        key="pp_feats")
            pca_features = [PCA_CANDIDATES[k] for k in pca_labels]
            st.caption("Nén các thuộc tính này xuống 2 trục PC1, PC2.")
        else:
            pca_features = []
            axis_labels = list(PCA_CANDIDATES.keys())
            x_label = st.selectbox("Trục X (không PCA):", axis_labels, index=0, key="pp_x")
            y_label = st.selectbox("Trục Y (không PCA):", axis_labels, index=1, key="pp_y")

    with c3:
        st.markdown("**③ Mã hóa (Encoding)**")
        use_enc = st.checkbox("Bật bước Mã hóa", value=True, key="pp_use_enc")
        color_label = st.selectbox("Màu sắc theo:", list(COLOR_OPTIONS.keys()), index=0, disabled=not use_enc, key="pp_color")
        symbol_label = st.selectbox("Ký hiệu theo:", list(SYMBOL_OPTIONS.keys()), index=1, disabled=not use_enc, key="pp_symbol")
        size_label = st.selectbox("Kích thước theo:", list(SIZE_OPTIONS.keys()), index=0, disabled=not use_enc, key="pp_size")

    # ---- Chạy pipeline ----
    n_raw = len(df)
    work = df.copy()
    if use_filter:
        work = work[work['Department'].isin(selected_depts)]
        work = work[(work['Age'] >= age_range[0]) & (work['Age'] <= age_range[1])]
        if overtime_opt != 'Tất cả':
            work = work[work['OverTime'] == overtime_opt]
    n_filtered = len(work)

    pca_ready = (not use_pca) or len(pca_features) >= 2
    explained = None
    loadings = None
    if n_filtered < 3:
        st.warning("Sau bước Lọc còn quá ít nhân viên (< 3). Hãy nới điều kiện lọc ở bước ①.")
        st.stop()
    if not pca_ready:
        st.warning("Hãy chọn ít nhất 2 thuộc tính cho bước PCA.")
        st.stop()

    work = work.copy()
    if use_pca:
        scaled = StandardScaler().fit_transform(work[pca_features])
        pca = PCA(n_components=2)
        coords = pca.fit_transform(scaled)
        work['PC1'], work['PC2'] = coords[:, 0], coords[:, 1]
        explained = pca.explained_variance_ratio_
        loadings = pd.DataFrame(pca.components_.T, index=pca_labels, columns=['PC1', 'PC2'])
        x_col, y_col = 'PC1', 'PC2'
        x_title = f"PC1 ({explained[0] * 100:.1f}% phương sai)"
        y_title = f"PC2 ({explained[1] * 100:.1f}% phương sai)"
    else:
        x_col, y_col = PCA_CANDIDATES[x_label], PCA_CANDIDATES[y_label]
        x_title, y_title = x_label, y_label

    # ---- Thanh tiến trình pipeline ----
    def step_card(num, name, detail, active):
        bg = '#fff7ed' if active else '#f5f5f4'
        border = '#f97316' if active else '#d6d3d1'
        color = '#9a3412' if active else '#a8a29e'
        return (f"<div style='flex:1;min-width:150px;background:{bg};border:2px solid {border};border-radius:10px;"
                f"padding:10px 12px;text-align:center;'>"
                f"<div style='font-size:0.75rem;color:{color};font-weight:700;'>BƯỚC {num}</div>"
                f"<div style='font-size:1rem;font-weight:700;color:{color};'>{name}</div>"
                f"<div style='font-size:0.82rem;color:#57534e;margin-top:4px;'>{detail}</div></div>")

    arrow_html = "<div style='align-self:center;font-size:1.6rem;color:#f97316;font-weight:700;'>➔</div>"
    cards = [
        step_card(0, "Dữ liệu gốc", f"{n_raw:,} nhân viên", True),
        step_card(1, "Lọc", f"còn {n_filtered:,} người" if use_filter else "Bỏ qua (bước đã tắt)", use_filter),
        step_card(2, "Tái cấu hình",
                  f"{len(pca_features)} biến ➔ 2 chiều<br>giữ {sum(explained) * 100:.1f}% thông tin" if use_pca
                  else f"Chỉ đổi trục:<br>{x_label} / {y_label}", True),
        step_card(3, "Mã hóa",
                  f"Màu: {color_label}<br>Ký hiệu: {symbol_label} · Cỡ: {size_label}" if use_enc else "Bỏ qua: mọi điểm cùng màu", use_enc),
        step_card(4, "Hiển thị", "Scatter tương tác", True),
    ]
    st.markdown("### 🔗 Luồng dữ liệu qua từng bước")
    st.markdown("<div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;'>"
                + arrow_html.join(cards) + "</div>", unsafe_allow_html=True)

    # ---- Hiển thị ----
    tab_res, tab_pca, tab_data = st.tabs(["📊 Kết quả cuối (Hiển thị)", "🧮 PCA giải thích điều gì?", "📋 Dữ liệu sau pipeline"])

    with tab_res:
        plot_kwargs = dict(x=x_col, y=y_col, template=PLOTLY_TEMPLATE, opacity=0.75)
        hover_cols = ['Department', 'Age', 'MonthlyIncome', 'Attrition']
        if use_enc:
            color_col = COLOR_OPTIONS[color_label]
            plot_kwargs['color'] = color_col
            if color_col == 'Department':
                plot_kwargs['color_discrete_map'] = COLOR_DEPT
            elif color_col == 'Attrition':
                plot_kwargs['color_discrete_map'] = COLOR_MAP_ATTRITION
            else:
                plot_kwargs['color_discrete_sequence'] = px.colors.qualitative.Set2
            if SYMBOL_OPTIONS[symbol_label]:
                plot_kwargs['symbol'] = SYMBOL_OPTIONS[symbol_label]
            if SIZE_OPTIONS[size_label]:
                sc = SIZE_OPTIONS[size_label]
                work['_size'] = 4 + 14 * (work[sc] - work[sc].min()) / max(work[sc].max() - work[sc].min(), 1)
                plot_kwargs['size'] = '_size'
                plot_kwargs['size_max'] = 18
        plot_kwargs['hover_data'] = {c: True for c in hover_cols if c not in (x_col, y_col)}
        fig_pipe = px.scatter(work, **plot_kwargs)
        if not use_enc:
            fig_pipe.update_traces(marker=dict(color='#9ca3af', size=7))
        elif not SIZE_OPTIONS[size_label]:
            fig_pipe.update_traces(marker=dict(size=8))
        fig_pipe.update_layout(
            height=560, xaxis_title=x_title, yaxis_title=y_title,
            title=f"Lọc ({n_filtered:,} người) ➔ {'PCA' if use_pca else 'Đổi trục'} ➔ "
                  f"{'Mã hóa' if use_enc else 'Không mã hóa'} ➔ Hiển thị")
        st.plotly_chart(fig_pipe, use_container_width=True)
        st.info("💡 Thử bật/tắt từng bước và đổi tham số: cả chuỗi chạy lại ngay. Đây chính là ý của mục 11.3 — "
                "toán tử nối tiếp, người dùng can thiệp được ở mọi bước, mọi bước đều tùy chọn.")

    with tab_pca:
        if use_pca:
            st.markdown(f"PCA nén **{len(pca_features)} thuộc tính** xuống **2 trục mới**. Hai trục giữ lại "
                        f"**{sum(explained) * 100:.1f}%** thông tin (phương sai) của dữ liệu đã lọc.")
            pc_a, pc_b = st.columns(2)
            with pc_a:
                fig_var = go.Figure(go.Bar(x=['PC1', 'PC2'], y=explained * 100, marker_color='#f97316',
                                           text=[f"{v * 100:.1f}%" for v in explained], textposition='outside'))
                fig_var.update_layout(template=PLOTLY_TEMPLATE, title="Phương sai mỗi trục giữ lại (%)",
                                      height=380, yaxis_range=[0, max(explained) * 100 * 1.25])
                st.plotly_chart(fig_var, use_container_width=True)
            with pc_b:
                fig_load = px.imshow(loadings, text_auto='.2f', color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                                     template=PLOTLY_TEMPLATE, title="Mỗi trục được tạo từ thuộc tính nào?", aspect='auto')
                fig_load.update_layout(height=380)
                st.plotly_chart(fig_load, use_container_width=True)
            st.caption("Ô càng đỏ/xanh đậm = thuộc tính đó đóng góp càng nhiều vào trục. "
                       "Các thuộc tính cùng dấu và cùng đậm thường tương quan mạnh với nhau.")
        else:
            st.info("Bước PCA đang tắt — biểu đồ dùng trực tiếp hai thuộc tính gốc làm trục. Bật lại bước ② để xem phân tích PCA.")

    with tab_data:
        show_cols = ['Department', 'Age', 'MonthlyIncome', 'OverTime', 'Attrition']
        if use_pca:
            show_cols += ['PC1', 'PC2']
        st.caption(f"Dữ liệu thực sự đi vào biểu đồ sau khi qua các bước ({n_filtered:,} dòng).")
        st.dataframe(work[show_cols].round(2), use_container_width=True, height=400)

# ==========================================
# 9. TỔNG KẾT
# ==========================================
elif menu == "Bảng tổng kết":
    st.title("Tổng Kết Các Toán Tử Tương Tác")
    st.markdown("""
    <div class="theory-box">
        Hệ thống hóa toàn bộ toán tử tương tác cốt lõi trong
        <em>Interactive Data Visualization</em> (Ward, Grinstein, Keim) — Chương 11.
    </div>
    """, unsafe_allow_html=True)

    summary_data = [
        {"Mục": "11.1.1", "Toán tử": "Navigation", "Mục đích": "Thay đổi góc nhìn, LOD", "Demo": "Pan, Zoom, Grand Tour 3D"},
        {"Mục": "11.1.2", "Toán tử": "Selection", "Mục đích": "Cô lập tập con, giữ bối cảnh", "Demo": "Box/Lasso Select → Linked KPI"},
        {"Mục": "11.1.3", "Toán tử": "Filtering", "Mục đích": "Xóa bỏ hoàn toàn điểm không thỏa mãn", "Demo": "Lọc theo OverTime, Phòng ban"},
        {"Mục": "11.1.4", "Toán tử": "Reconfiguration", "Mục đích": "Đổi trục tọa độ / nén chiều", "Demo": "Đổi cặp trục, PCA 15D → 2D"},
        {"Mục": "11.1.5", "Toán tử": "Encoding", "Mục đích": "Đổi biểu diễn đồ thị", "Demo": "Bar/Box/Scatter/Violin + Colormap"},
        {"Mục": "11.1.6", "Toán tử": "Connection", "Mục đích": "Đồng bộ nhiều khung nhìn", "Demo": "3 khung nhìn linked highlight"},
        {"Mục": "11.1.7", "Toán tử": "Abstraction", "Mục đích": "Khái quát ↔ Chi tiết", "Demo": "Overview + Detail (Shneiderman)"},
        {"Mục": "11.3", "Toán tử": "Pipeline", "Mục đích": "Chuỗi toán tử nối tiếp", "Demo": "Lọc → PCA → Mã hóa → Hiển thị"},
    ]
    st.table(pd.DataFrame(summary_data))
