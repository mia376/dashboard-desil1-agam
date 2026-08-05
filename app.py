import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Dashboard Desil 1 Kabupaten Agam",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CUSTOM CSS - PERBAIKAN UKURAN FONT KPI
# =====================================================

st.markdown("""
<style>
    /* Background utama */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Style untuk title */
    h1 {
        color: #1a3c5e !important;
        font-weight: 700 !important;
        padding: 10px 0;
        border-bottom: 3px solid #2c6fbb;
        font-size: 28px !important;
    }
    
    /* Style untuk subheader */
    h2, h3 {
        color: #1a3c5e !important;
        font-weight: 600 !important;
        padding: 10px 0;
        border-bottom: 2px solid #e0e7f0;
        font-size: 20px !important;
    }
    
    /* ============================================= */
    /* PERBAIKAN KPI - FONT LEBIH KECIL */
    /* ============================================= */
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 8px 10px !important;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e7f0;
        transition: all 0.3s ease;
        border-left: 4px solid #2c6fbb;
        min-height: 60px;
        width: 100% !important;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 15px rgba(44, 111, 187, 0.15);
        transform: translateY(-2px);
        border-left-width: 6px;
    }
    
    /* LABEL KPI - JUDUL */
    div[data-testid="metric-container"] label {
        color: #4a6a8a !important;
        font-weight: 600 !important;
        font-size: 10px !important;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        display: block !important;
        margin-bottom: 2px !important;
    }
    
    /* VALUE KPI - ANGKA ATAU NAMA KECAMATAN (DIPERKECIL) */
    div[data-testid="metric-container"] div {
        color: #1a3c5e !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        line-height: 1.2 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    /* Delta KPI (jika ada) */
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 10px !important;
        color: #4a6a8a !important;
    }
    
    /* ============================================= */
    /* AKHIR PERBAIKAN KPI */
    /* ============================================= */
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3c5e 0%, #2c6fbb 100%);
        padding: 20px;
    }
    
    section[data-testid="stSidebar"] *:not(.stSelectbox):not(.stSelectbox *) {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 8px;
        padding: 2px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[role="listbox"] {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox div[role="listbox"] * {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox input {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox:hover {
        background: rgba(255,255,255,1) !important;
    }
    
    /* Detail card di sidebar */
    .detail-sidebar-card {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
    }
    
    .detail-sidebar-card h4 {
        color: white !important;
        margin: 0 0 10px 0;
        font-weight: 600;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 8px;
        font-size: 14px !important;
    }
    
    .detail-sidebar-card .detail-item {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .detail-sidebar-card .detail-label {
        opacity: 0.8;
        font-size: 12px;
        color: white !important;
    }
    
    .detail-sidebar-card .detail-value {
        font-weight: 600;
        font-size: 13px;
        color: white !important;
    }
    
    .detail-sidebar-card .cluster-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 5px;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
        margin: 12px 0;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 10px !important;
        border: 1px solid #e0e7f0 !important;
        overflow: hidden !important;
    }
    
    .stDataFrame thead {
        background: linear-gradient(90deg, #1a3c5e 0%, #2c6fbb 100%) !important;
        color: white !important;
    }
    
    .stDataFrame thead th {
        font-size: 12px !important;
        padding: 8px 10px !important;
    }
    
    .stDataFrame tbody td {
        font-size: 12px !important;
        padding: 6px 10px !important;
    }
    
    /* Plotly chart container */
    .plotly-graph-div {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e8ecf0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/hasil_cluster.csv")
    return df

df = load_data()

# =====================================================
# VALIDASI DATA
# =====================================================

required_col = [
    "KECAMATAN",
    "LAKI-LAKI",
    "PEREMPUAN",
    "TOTAL",
    "CLUSTER"
]

for col in required_col:
    if col not in df.columns:
        st.error(f"Kolom {col} tidak ditemukan pada dataset")
        st.stop()

# =====================================================
# TAMBAH KATEGORI CLUSTER
# =====================================================

nilai_cluster = sorted(df["CLUSTER"].unique())

nama_cluster = {}
for i, nilai in enumerate(nilai_cluster):
    if i == 0:
        nama_cluster[nilai] = "Rendah"
    elif i == 1:
        nama_cluster[nilai] = "Sedang"
    else:
        nama_cluster[nilai] = "Tinggi"

df["Kategori Cluster"] = df["CLUSTER"].map(nama_cluster)

# =====================================================
# FUNGSI UNTUK MEMPERSINGKAT NAMA KECAMATAN
# =====================================================

def shorten_name(name, max_length=10):
    """Memendekkan nama kecamatan jika terlalu panjang"""
    if len(name) > max_length:
        return name[:max_length] + "..."
    return name

# =====================================================
# HEADER
# =====================================================

st.title("📊 Dashboard Informasi Keluarga Desil 1 Kecamatan di Kabupaten Agam")
st.markdown("---")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🔎 Filter & Detail Kecamatan")
st.sidebar.markdown("---")

kecamatan_list = sorted(df["KECAMATAN"].unique())

selected_kecamatan = st.sidebar.selectbox(
    "Pilih Kecamatan",
    ["Semua Kecamatan"] + kecamatan_list,
    key="filter_kecamatan"
)

if selected_kecamatan == "Semua Kecamatan":
    data = df.copy()
else:
    data = df[df["KECAMATAN"] == selected_kecamatan]

st.sidebar.markdown("---")
st.sidebar.caption("ℹ️ Data desil 1 berdasarkan hasil clustering")

# =====================================================
# DETAIL KECAMATAN DI SIDEBAR
# =====================================================

if selected_kecamatan != "Semua Kecamatan":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Detail Kecamatan")
    
    info_detail = df[df["KECAMATAN"] == selected_kecamatan]
    
    if not info_detail.empty:
        cluster_name = info_detail['Kategori Cluster'].iloc[0]
        total_kk = int(info_detail['TOTAL'].iloc[0])
        laki = int(info_detail['LAKI-LAKI'].iloc[0])
        perempuan = int(info_detail['PEREMPUAN'].iloc[0])
        cluster_num = int(info_detail['CLUSTER'].iloc[0])
        
        badge_colors = {
            "Rendah": "#4A90D9",
            "Sedang": "#F5A623",
            "Tinggi": "#D0021B"
        }
        badge_color = badge_colors.get(cluster_name, "#2c6fbb")
        
        st.sidebar.markdown(f"""
        <div class="detail-sidebar-card">
            <h4>🏘️ {selected_kecamatan}</h4>
            <div class="detail-item">
                <span class="detail-label">Total KK</span>
                <span class="detail-value">{total_kk:,}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">KK Laki-laki</span>
                <span class="detail-value">{laki:,}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">KK Perempuan</span>
                <span class="detail-value">{perempuan:,}</span>
            </div>
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.2);">
                <span class="detail-label">Kategori: </span>
                <span class="cluster-badge" style="background-color: {badge_color};">
                    {cluster_name}
                </span>
                <span style="margin-left: 10px; font-size: 11px; opacity: 0.7; color: white !important;">
                    Cluster {cluster_num}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Pilih kecamatan spesifik untuk melihat detail")

# =====================================================
# KPI - MENGGUNAKAN HTML CUSTOM AGAR LEBIH RAPI
# =====================================================

total_kk = data["TOTAL"].sum()
jumlah_kecamatan = data["KECAMATAN"].nunique()
rata_kk = round(data["TOTAL"].mean())
max_daerah = data.loc[data["TOTAL"].idxmax(), "KECAMATAN"]
min_daerah = data.loc[data["TOTAL"].idxmin(), "KECAMATAN"]

# Buat 5 kolom
col1, col2, col3, col4, col5 = st.columns(5)

# Style CSS untuk KPI custom
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid #e0e7f0;
        border-left: 4px solid #2c6fbb;
        min-height: 55px;
        height: auto;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .kpi-label {
        color: #4a6a8a;
        font-weight: 600;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 1px;
    }
    .kpi-value {
        color: #1a3c5e;
        font-weight: 700;
        font-size: 14px;
        line-height: 1.2;
        word-break: break-word;
    }
    .kpi-small {
        font-size: 12px !important;
    }
    .kpi-sub {
        color: #6b8aaa;
        font-size: 9px;
        margin-top: 1px;
    }
</style>
""", unsafe_allow_html=True)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🏛️ Jumlah Kecamatan</div>
        <div class="kpi-value">{jumlah_kecamatan}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">👨‍👩‍👧‍👦 Total KK</div>
        <div class="kpi-value">{total_kk:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📊 Rata-rata KK</div>
        <div class="kpi-value">{rata_kk:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">⬆️ KK Tertinggi</div>
        <div class="kpi-value kpi-small">{max_daerah}</div>
        <div class="kpi-sub">Total: {data.loc[data['TOTAL'].idxmax(), 'TOTAL']:,} KK</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">⬇️ KK Terendah</div>
        <div class="kpi-value kpi-small">{min_daerah}</div>
        <div class="kpi-sub">Total: {data.loc[data['TOTAL'].idxmin(), 'TOTAL']:,} KK</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# DATA
# =====================================================

st.subheader("📋 Data Kecamatan Hasil Clustering")

st.dataframe(
    data,
    use_container_width=True,
    column_config={
        "KECAMATAN": "Kecamatan",
        "LAKI-LAKI": st.column_config.NumberColumn("Laki-laki", format="%d"),
        "PEREMPUAN": st.column_config.NumberColumn("Perempuan", format="%d"),
        "TOTAL": st.column_config.NumberColumn("Total", format="%d"),
        "CLUSTER": "Cluster",
        "Kategori Cluster": st.column_config.TextColumn("Kategori"),
    }
)

st.markdown("---")

# =====================================================
# GRAFIK TOTAL KK
# =====================================================

st.subheader("📈 Persebaran Jumlah Kepala Keluarga Desil 1")

color_map = {
    "Rendah": "#4A90D9",
    "Sedang": "#F5A623",
    "Tinggi": "#D0021B"
}

fig1 = px.bar(
    data.sort_values("TOTAL", ascending=False),
    x="KECAMATAN",
    y="TOTAL",
    color="Kategori Cluster",
    text="TOTAL",
    color_discrete_map=color_map,
    labels={"TOTAL": "Jumlah Kepala Keluarga"},
    template="plotly_white"
)

fig1.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    marker=dict(
        line=dict(width=2, color='rgba(255,255,255,0.9)'),
        opacity=0.9
    )
)

fig1.update_layout(
    height=500,
    xaxis_tickangle=-45,
    showlegend=True,
    legend_title_text="Kategori",
    plot_bgcolor='rgba(255,255,255,0.98)',
    paper_bgcolor='rgba(255,255,255,0.98)',
    font=dict(size=12, color="#2C3E50"),
    bargap=0.15,
    legend=dict(
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='rgba(0,0,0,0.08)',
        borderwidth=1
    ),
    margin=dict(l=40, r=40, t=40, b=80)
)

st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

# =====================================================
# RANKING SEMUA KECAMATAN
# =====================================================

st.subheader("🏆 Perbandingan Jumlah KK Desil 1 Antar Kecamatan")

all_kecamatan = data.sort_values("TOTAL", ascending=True)

fig2 = px.bar(
    all_kecamatan,
    x="TOTAL",
    y="KECAMATAN",
    orientation="h",
    text="TOTAL",
    color="TOTAL",
    color_continuous_scale="Blues",
    template="plotly_white"
)

fig2.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    marker=dict(
        line=dict(width=1.5, color='rgba(255,255,255,0.9)'),
        cornerradius=4,
        opacity=0.9
    )
)

fig2.update_layout(
    height=600,
    xaxis_title="Jumlah KK Desil 1",
    yaxis_title="",
    showlegend=False,
    plot_bgcolor='rgba(255,255,255,0.98)',
    paper_bgcolor='rgba(255,255,255,0.98)',
    font=dict(size=12, color="#2C3E50"),
    xaxis=dict(gridcolor='rgba(0,0,0,0.05)', gridwidth=0.5),
    yaxis=dict(
        categoryorder='total ascending',
        gridcolor='rgba(0,0,0,0.05)',
        gridwidth=0.5
    ),
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

# =====================================================
# GENDER
# =====================================================

st.subheader("👥 Komposisi Kepala Keluarga Berdasarkan Jenis Kelamin")

gender = data.melt(
    id_vars="KECAMATAN",
    value_vars=["LAKI-LAKI", "PEREMPUAN"],
    var_name="Jenis Kelamin",
    value_name="Jumlah"
)

fig3 = px.bar(
    gender,
    x="KECAMATAN",
    y="Jumlah",
    color="Jenis Kelamin",
    barmode="group",
    text="Jumlah",
    color_discrete_map={
        "LAKI-LAKI": "#2C6FBB",
        "PEREMPUAN": "#D4A5A5"
    },
    template="plotly_white"
)

fig3.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    marker=dict(
        line=dict(width=1.5, color='rgba(255,255,255,0.9)'),
        opacity=0.9
    )
)

fig3.update_layout(
    height=500,
    xaxis_tickangle=-45,
    legend_title_text="",
    plot_bgcolor='rgba(255,255,255,0.98)',
    paper_bgcolor='rgba(255,255,255,0.98)',
    font=dict(size=12, color="#2C3E50"),
    bargap=0.15,
    legend=dict(
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='rgba(0,0,0,0.08)',
        borderwidth=1
    ),
    margin=dict(l=40, r=40, t=40, b=80)
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")

# =====================================================
# CLUSTER SCATTER
# =====================================================

st.subheader("🔵 Pola Persebaran Cluster Kecamatan")

fig4 = px.scatter(
    data,
    x="LAKI-LAKI",
    y="PEREMPUAN",
    size="TOTAL",
    color="Kategori Cluster",
    hover_name="KECAMATAN",
    text="KECAMATAN",
    color_discrete_map=color_map,
    labels={
        "LAKI-LAKI": "KK Laki-laki",
        "PEREMPUAN": "KK Perempuan"
    },
    template="plotly_white",
    size_max=60
)

fig4.update_traces(
    marker=dict(
        line=dict(width=2, color='rgba(255,255,255,0.9)'),
        sizemode='area',
        opacity=0.85
    ),
    textposition='top center',
    textfont=dict(size=11)
)

fig4.update_layout(
    height=600,
    plot_bgcolor='rgba(255,255,255,0.98)',
    paper_bgcolor='rgba(255,255,255,0.98)',
    font=dict(size=12, color="#2C3E50"),
    legend_title_text="Kategori",
    legend=dict(
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='rgba(0,0,0,0.08)',
        borderwidth=1
    ),
    xaxis=dict(gridcolor='rgba(0,0,0,0.05)', gridwidth=0.5),
    yaxis=dict(gridcolor='rgba(0,0,0,0.05)', gridwidth=0.5),
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")

# =====================================================
# RINGKASAN CLUSTER
# =====================================================

st.subheader("📌 Profil Kelompok Kecamatan")

cluster = (
    data
    .groupby(["CLUSTER", "Kategori Cluster"])
    .agg(
        Jumlah_Kecamatan=("KECAMATAN", "count"),
        Total_KK=("TOTAL", "sum"),
        Rata_Rata_KK=("TOTAL", "mean")
    )
    .reset_index()
)

cluster["Rata_Rata_KK"] = cluster["Rata_Rata_KK"].round(0)
cluster["Total_KK"] = cluster["Total_KK"].apply(lambda x: f"{x:,}")

st.dataframe(
    cluster,
    use_container_width=True,
    column_config={
        "CLUSTER": "Cluster",
        "Kategori Cluster": "Kategori",
        "Jumlah_Kecamatan": "Jumlah Kecamatan",
        "Total_KK": "Total KK",
        "Rata_Rata_KK": "Rata-rata KK"
    }
)

st.markdown("---")

# =====================================================
# PIE
# =====================================================

fig5 = px.pie(
    cluster,
    names="Kategori Cluster",
    values="Jumlah_Kecamatan",
    hole=0.4,
    color="Kategori Cluster",
    color_discrete_map=color_map
)

fig5.update_traces(
    textinfo="label+percent",
    textposition='inside',
    marker=dict(line=dict(width=3, color='white')),
    pull=[0.05, 0, 0],
    textfont=dict(size=13, color='white')
)

fig5.update_layout(
    height=400,
    showlegend=True,
    plot_bgcolor='rgba(255,255,255,0.98)',
    paper_bgcolor='rgba(255,255,255,0.98)',
    font=dict(size=12, color="#2C3E50"),
    legend=dict(
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='rgba(0,0,0,0.08)',
        borderwidth=1
    )
)

st.plotly_chart(fig5, use_container_width=True)
st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div style="
    background: linear-gradient(90deg, #1a3c5e 0%, #2c6fbb 100%);
    padding: 15px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-top: 30px;
">
    <p style="margin: 0; font-size: 14px;">📊 Dashboard Informasi Keluarga Desil 1 Kabupaten Agam</p>
    
""", unsafe_allow_html=True)