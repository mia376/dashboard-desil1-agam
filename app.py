# app.py — Dashboard Data Agam (Versi Rapi & Warna Profesional)
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================================================================
# 1. KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="Dashboard Data Agam",
    page_icon="📊",
    layout="wide"
)

# =====================================================================
# 2. PALET WARNA (satu sumber warna untuk semua grafik & elemen)
#    Silakan ganti nilai hex di sini kalau ingin ubah nuansa dashboard.
# =====================================================================
COLOR_KATEGORI = {
    "Rendah": "#4FA8ED",   # biru — tetap jadi yang paling terang di grup, tapi jauh lebih jenuh dari sebelumnya
    "Sedang": "#0B63C7",   # biru medium pekat — kontras jelas dari Rendah maupun Tinggi
    "Tinggi": "#061B3D",   # navy nyaris hitam — nilai tinggi, warna paling gelap & pekat
}

COLOR_PRIMARY = "#0A2A5C"      # navy sangat pekat — warna utama header & judul
COLOR_SECONDARY = "#0B5FE0"    # biru royal jenuh — warna kedua gradasi header, kontras kuat dgn primary
COLOR_ACCENT = "#0B5FE0"       # biru royal jenuh — aksen tombol / highlight
COLOR_BG_CARD = "#FFFFFF"      # putih — latar kartu
COLOR_BG_PAGE = "#F4F6F9"      # abu-putih netral — latar halaman (flat, tidak mencolok)
COLOR_SIDEBAR_BG = "#071A38"   # navy nyaris hitam solid — latar sidebar, lebih pekat dari sebelumnya
COLOR_TEXT_MUTED = "#3B4A63"   # abu kebiruan pekat — teks sekunder, tetap kontras jelas (bukan pudar)
COLOR_LIVE = "#12C765"         # hijau pekat & segar — aksen indikator "data aktif" yang berdenyut
COLOR_GLOW = "#F2A400"         # kuning keemasan pekat — aksen hangat untuk sorotan kecil (dipakai sangat terbatas)

EMOJI_KATEGORI = {"Tinggi": "⚫", "Sedang": "🔵", "Rendah": "⚪"}

# Warna garis aksen untuk 4 kartu KPI — dipakai sebagai border kiri, bukan latar penuh
COLOR_KPI = ["#0A2A5C", "#0B5FE0", "#0B63C7", "#071A38"]

# Warna orb dekoratif di header — dipakai sangat samar (opacity rendah) sebagai lapisan kedalaman
COLOR_HEADER_ORB_1 = "#2E7CFF"
COLOR_HEADER_ORB_2 = "#F2A400"


def dgn_alpha(hex_color, alpha):
    """Mengubah kode warna hex menjadi rgba dengan transparansi tertentu, untuk bayangan & badge lembut."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

# Template & pengaturan grafik Plotly agar tampak lebih tajam ("HD") dan konsisten
PLOTLY_TEMPLATE = "plotly_white"
PLOTLY_CONFIG = {
    "displaylogo": False,
    "toImageButtonOptions": {"format": "png", "scale": 4},  # unduhan gambar resolusi tinggi
    "responsive": True,
}

# Ukuran font grafik — dibuat kecil & proporsional agar tidak mendominasi grafik
FONT_FAMILY = "'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif"
FONT_BASE = 8        # teks umum (sumbu, hover)
FONT_TITLE = 10       # judul grafik
FONT_TICK = 7         # angka pada sumbu
FONT_LEGEND = 7       # keterangan warna
FONT_DATALABEL = 7    # angka di atas/pada batang, pie, dll.


def perhalus_grafik(fig):
    """Menerapkan gaya seragam ke semua grafik: font tegas & tajam, gridline halus, latar bersih."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        font=dict(family=FONT_FAMILY, size=FONT_BASE, color="#0F172A"),
        title_font=dict(family=FONT_FAMILY, size=FONT_TITLE, color=COLOR_PRIMARY),
        legend=dict(font=dict(size=FONT_LEGEND, color="#0F172A")),
        hoverlabel=dict(
            font=dict(family=FONT_FAMILY, size=FONT_TICK, color="#FFFFFF"),
            bgcolor=COLOR_PRIMARY,
        ),
        uniformtext=dict(minsize=8, mode="hide"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, l=10, r=10, b=10),
    )
    fig.update_xaxes(
        gridcolor="#E5EAF2", zerolinecolor="#E5EAF2", linecolor="#94A3B8",
        tickfont=dict(size=FONT_TICK, color="#0F172A"),
        title_font=dict(size=FONT_BASE, color="#0F172A"),
    )
    fig.update_yaxes(
        gridcolor="#E5EAF2", zerolinecolor="#E5EAF2", linecolor="#94A3B8",
        tickfont=dict(size=FONT_TICK, color="#0F172A"),
        title_font=dict(size=FONT_BASE, color="#0F172A"),
    )
    # Label angka di atas/pada batang & pie dipekatkan (hitam pekat, tebal) agar tidak pudar
    fig.update_traces(
        textfont=dict(color="#0F172A"),
        selector=dict(type="bar"),
    )
    # Sudut batang dibulatkan halus & garis tepi tipis putih agar tampak lebih modern
    try:
        fig.update_traces(marker=dict(cornerradius=6), selector=dict(type="bar"))
    except ValueError:
        pass  # versi Plotly lama tanpa dukungan cornerradius — abaikan agar tidak error
    return fig


# =====================================================================
# 3. CUSTOM CSS
#    - Membuat tampilan multiselect bisa di-scroll
#    - Memberi nuansa dashboard profesional (header, kartu, jarak antar elemen)
# =====================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {{
        --font-display: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        --font-mono: 'JetBrains Mono', 'Segoe UI', monospace;
    }}

    /* Font lebih tajam & halus di semua elemen, pakai tipografi khas dashboard modern */
    html, body, [class*="css"] {{
        font-family: var(--font-display);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
        scroll-behavior: smooth;
    }}

    /* Latar halaman dengan tekstur titik halus — memberi kedalaman tanpa ramai */
    .stApp {{
        background:
            radial-gradient(circle, rgba(18,60,122,0.06) 1px, transparent 1px) 0 0/22px 22px,
            {COLOR_BG_PAGE};
    }}

    /* Animasi dasar yang dipakai berulang di seluruh dashboard */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 200% 50%; }}
    }}
    @keyframes pulseDot {{
        0% {{ box-shadow: 0 0 0 0 rgba(34,197,94,0.55); }}
        70% {{ box-shadow: 0 0 0 8px rgba(34,197,94,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(34,197,94,0); }}
    }}
    @keyframes growWidth {{
        from {{ width: 0%; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}

    /* Sidebar warna solid navy, tidak bergradasi agar terkesan lebih formal */
    section[data-testid="stSidebar"] {{
        background: {COLOR_SIDEBAR_BG};
        border-right: 1px solid rgba(255,255,255,0.08);
    }}
    section[data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.35);
        color: #FFFFFF !important;
        border-radius: 6px;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: rgba(255,255,255,0.20);
        border-color: #FFFFFF;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background: rgba(255,255,255,0.10);
        border-radius: 6px;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="tag"] {{
        background: rgba(255,255,255,0.25) !important;
    }}

    /* Dropdown multiselect bisa di-scroll rapi */
    div[data-baseweb="select"] div[data-baseweb="menu"],
    div[data-baseweb="select"] ul {{
        max-height: 300px !important;
        overflow-y: auto !important;
    }}
    div[data-baseweb="select"] div[data-baseweb="menu"]::-webkit-scrollbar {{
        width: 8px;
    }}
    div[data-baseweb="select"] div[data-baseweb="menu"]::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 10px;
    }}
    div[data-baseweb="select"] div[data-baseweb="menu"]::-webkit-scrollbar-thumb {{
        background: {COLOR_ACCENT};
        border-radius: 10px;
    }}

    @keyframes floatOrb {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        50% {{ transform: translate(-12px, 10px) scale(1.08); }}
    }}
    @keyframes floatOrbSlow {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        50% {{ transform: translate(14px, -8px) scale(0.95); }}
    }}

    /* Header judul dengan gradasi navy bergerak halus — formal tapi terasa hidup */
    .dashboard-header {{
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, {COLOR_PRIMARY}, {COLOR_SECONDARY}, {COLOR_PRIMARY});
        background-size: 200% 200%;
        animation: shimmer 10s ease-in-out infinite;
        padding: 1.4rem 2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
        border-left: 6px solid {COLOR_SECONDARY};
        box-shadow: 0 14px 30px {dgn_alpha(COLOR_PRIMARY, 0.28)};
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.6rem;
    }}
    /* Dua "orb" cahaya lembut yang melayang perlahan di belakang teks header — kedalaman tanpa ramai */
    .dashboard-header::before, .dashboard-header::after {{
        content: "";
        position: absolute;
        border-radius: 50%;
        filter: blur(30px);
        pointer-events: none;
        z-index: 0;
    }}
    .dashboard-header::before {{
        width: 180px; height: 180px;
        background: {dgn_alpha(COLOR_HEADER_ORB_1, 0.35)};
        top: -70px; right: 8%;
        animation: floatOrb 9s ease-in-out infinite;
    }}
    .dashboard-header::after {{
        width: 130px; height: 130px;
        background: {dgn_alpha(COLOR_HEADER_ORB_2, 0.22)};
        bottom: -60px; left: 18%;
        animation: floatOrbSlow 11s ease-in-out infinite;
    }}
    .dashboard-header > div, .dashboard-header > span {{
        position: relative;
        z-index: 1;
    }}
    .dashboard-header h1 {{
        margin: 0;
        font-size: 2rem !important;
        font-weight: 800;
        letter-spacing: 0.2px;
        text-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }}
    .dashboard-header p {{
        margin: 0.3rem 0 0 0;
        opacity: 0.88;
        font-size: 1.05rem !important;
    }}
    .live-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(255,255,255,0.14);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 999px;
        padding: 0.35rem 0.8rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: #FFFFFF;
        white-space: nowrap;
        transition: background 0.2s ease, transform 0.2s ease;
    }}
    .live-badge:hover {{
        background: rgba(255,255,255,0.22);
        transform: translateY(-1px);
    }}
    .live-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {COLOR_LIVE};
        animation: pulseDot 1.8s infinite;
    }}

    /* Kartu ringkasan kategori — putih bersih, muncul lembut, terangkat saat disorot kursor */
    .info-card {{
        background: {COLOR_BG_CARD};
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E5E9F0;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
        margin-bottom: 0.6rem;
        animation: fadeInUp 0.5s cubic-bezier(.22,.9,.32,1) both;
        transition: transform 0.25s cubic-bezier(.22,.9,.32,1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .info-card:hover {{
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 14px 26px rgba(16, 24, 40, 0.12);
        border-color: #D6DEEA;
    }}

    /* Bar persentase kecil di dalam kartu ringkasan kategori — dengan kilau bergerak halus */
    .mini-bar-track {{
        width: 100%;
        height: 7px;
        background: #EEF2F7;
        border-radius: 999px;
        margin-top: 0.55rem;
        overflow: hidden;
    }}
    .mini-bar-fill {{
        height: 100%;
        border-radius: 999px;
        position: relative;
        overflow: hidden;
        animation: growWidth 1.1s cubic-bezier(.22,.9,.32,1) both;
    }}
    .mini-bar-fill::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent);
        background-size: 200% 100%;
        animation: shimmer 2.4s ease-in-out infinite;
    }}

    /* Kartu KPI: putih bersih dengan garis aksen kiri, muncul bertahap & terangkat saat disorot */
    .kpi-card {{
        background: {COLOR_BG_CARD};
        border: 1px solid #E5E9F0;
        border-left: 4px solid #123C7A;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        color: #1F2937;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
        margin-bottom: 0.5rem;
        animation: fadeInUp 0.5s cubic-bezier(.22,.9,.32,1) both;
        transition: transform 0.25s cubic-bezier(.22,.9,.32,1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 16px 28px rgba(16, 24, 40, 0.14);
        border-color: #D6DEEA;
    }}
    .kpi-card-row {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    .kpi-card .kpi-icon-circle {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        flex-shrink: 0;
        transition: transform 0.25s ease;
    }}
    .kpi-card:hover .kpi-icon-circle {{
        transform: scale(1.08) rotate(-4deg);
    }}
    .kpi-card .kpi-icon {{
        font-size: 1.2rem;
        line-height: 1;
        flex-shrink: 0;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    .kpi-card .kpi-value {{
        font-family: var(--font-mono);
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLOR_PRIMARY};
    }}

    /* Judul subheader diberi aksen garis tipis di kiri, ukuran diperkecil agar tidak dominan */
    h3 {{
        border-left: 3px solid {COLOR_PRIMARY};
        padding-left: 0.6rem;
        color: #1F2937;
        font-size: 1.05rem !important;
    }}
    h1 {{ font-size: 1.5rem !important; }}
    h2 {{ font-size: 1.15rem !important; }}

    /* Perkecil teks umum di seluruh dashboard (label, sidebar, tab, tombol, tag) */
    p, span, label, div {{
        font-size: 0.92rem;
    }}
    .stMarkdown p {{ font-size: 0.9rem; }}
    section[data-testid="stSidebar"] h2 {{ font-size: 1rem !important; }}
    section[data-testid="stSidebar"] h4 {{ font-size: 0.88rem !important; }}
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] p {{
        font-size: 0.78rem !important;
    }}
    div[data-baseweb="select"] {{ font-size: 0.82rem !important; }}
    div[data-baseweb="tag"] {{
        font-size: 0.72rem !important;
        padding: 0.1rem 0.3rem !important;
    }}
    div[data-baseweb="tag"] span {{ font-size: 0.72rem !important; }}
    .stRadio label, .stSelectbox label, .stMultiSelect label {{
        font-size: 0.85rem !important;
    }}
    .stButton button, .stDownloadButton button {{
        font-size: 0.82rem !important;
    }}
    .kpi-card .kpi-label {{ font-size: 0.72rem !important; }}
    .kpi-card .kpi-value {{ font-size: 1.25rem !important; }}
    .info-card span {{ font-size: 0.95rem !important; }}

    /* Tombol & elemen interaktif Streamlit terasa lebih responsif */
    .stButton button, .stDownloadButton button {{
        transition: transform 0.18s cubic-bezier(.22,.9,.32,1), box-shadow 0.18s ease, border-color 0.18s ease;
        border-radius: 8px !important;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(16, 24, 40, 0.10);
    }}
    .stDownloadButton button {{
        background: linear-gradient(120deg, {COLOR_PRIMARY}, {COLOR_SECONDARY}) !important;
        border: none !important;
        color: #FFFFFF !important;
    }}
    div[data-testid="stPlotlyChart"] {{
        animation: fadeInUp 0.6s ease both;
        border-radius: 12px;
        transition: box-shadow 0.25s ease;
    }}
    div[data-testid="stPlotlyChart"]:hover {{
        box-shadow: 0 10px 26px rgba(16, 24, 40, 0.08);
    }}

    /* Pembatas antar-bagian diganti garis gradasi tipis, lebih elegan dari garis abu polos */
    hr {{
        border: none !important;
        height: 2px !important;
        margin: 1.6rem 0 !important;
        background: linear-gradient(90deg, transparent, {dgn_alpha(COLOR_PRIMARY, 0.25)}, transparent) !important;
    }}

    /* Tab (jika dipakai) & expander diberi sentuhan hover lembut yang konsisten dengan kartu lain */
    .streamlit-expanderHeader {{
        border-radius: 8px;
        transition: background 0.2s ease;
    }}

    /* ============================================================
       PEMEKATAN TEKS — Streamlit secara default merender caption,
       teks di dalam kotak info/warning/success, dan beberapa label
       dengan warna abu-abu pudar & opacity rendah. Blok ini menimpa
       semua itu supaya teksnya tegas dan mudah dibaca.
    ============================================================ */
    .stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p,
    .stMarkdown small, small {{
        color: #334155 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }}
    /* Kotak st.info / st.warning / st.success — teksnya dipekatkan, bukan abu-abu pudar */
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] div {{
        color: #0F172A !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }}
    /* Teks umum & label form dipastikan pekat, tidak abu-abu transparan */
    .stMarkdown p, .stMarkdown li, label, p, span {{
        color: #1F2937;
        opacity: 1 !important;
    }}
    /* Placeholder & teks bantu di dalam dropdown/multiselect dipekatkan */
    div[data-baseweb="select"] * {{
        opacity: 1 !important;
    }}
    /* Nilai di dalam tabel data dipastikan pekat, bukan abu-abu */
    div[data-testid="stDataFrame"] * {{
        color: #0F172A !important;
    }}
    /* Teks di dalam header tetap putih solid, tidak pudar oleh opacity */
    .dashboard-header p {{
        opacity: 1 !important;
        color: rgba(255,255,255,0.96) !important;
        font-weight: 500;
    }}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# 4. HEADER UTAMA
# =====================================================================
st.markdown(f"""
<div class="dashboard-header">
    <div>
        <h1>📊 DASHBOARD VISUALISASI DATA DESIL 1–5 KABUPATEN AGAM</h1>
        <p>Visualisasi dan Pemetaan Data Berdasarkan Kecamatan di Kabupaten Agam</p>
    </div>
    <span class="live-badge"><span class="live-dot"></span> Data Aktif</span>
</div>
""", unsafe_allow_html=True)


# =====================================================================
# 5. FUNGSI BANTUAN — MEMUAT DATA
#    Dipisah jadi fungsi supaya mudah dibaca dan dipahami alurnya.
# =====================================================================
@st.cache_data
def load_data():
    """Membaca semua file CSV hasil clustering dari folder hasil_cluster."""
    folder = "hasil_cluster"
    files = {
        "Desil 1": "hasil_cluster_desil1.csv",
        "Desil 2": "hasil_cluster_desil2.csv",
        "Desil 3": "hasil_cluster_desil3.csv",
        "Desil 4": "hasil_cluster_desil4.csv",
        "Desil 5": "hasil_cluster_desil5.csv",
        "Sanitasi Tidak Layak": "hasil_cluster_sanitasi.csv",
        "Rumah Tidak Layak Huni": "hasil_cluster_rtlh.csv",
    }

    data = {}
    for nama, file in files.items():
        path = os.path.join(folder, file)
        if os.path.exists(path):
            data[nama] = pd.read_csv(path)
    return data


@st.cache_data
def convert_df_to_csv(df):
    """Mengubah dataframe menjadi CSV siap diunduh."""
    return df.to_csv(index=False).encode("utf-8")


def buat_grafik_batang(df, x, y, judul, orientasi="v", tinggi=450, urutkan=None):
    """Grafik batang dengan warna kategori yang konsisten di seluruh dashboard."""
    fig = px.bar(
        df,
        x=x if orientasi == "v" else y,
        y=y if orientasi == "v" else x,
        color="KATEGORI",
        color_discrete_map=COLOR_KATEGORI,
        title=judul,
        text=y,  # selalu label dengan kolom nilai (numerik), bukan tertukar saat horizontal
        orientation=orientasi,
        height=tinggi,
    )
    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        textfont=dict(size=FONT_DATALABEL, family=FONT_FAMILY),
    )
    fig.update_layout(showlegend=True)
    return perhalus_grafik(fig)


# =====================================================================
# 6. SIDEBAR — FILTER DATA
# =====================================================================
st.sidebar.header("⚙️ Filter Data")

all_data = load_data()

if not all_data:
    st.error("⚠️ Data tidak ditemukan. Pastikan folder 'hasil_cluster' berisi file CSV.")
    st.stop()

# --- Pilih dataset ---
selected_dataset = st.sidebar.selectbox("Pilih Jenis Data", options=list(all_data.keys()))
df = all_data[selected_dataset]

# --- Pilih kecamatan (dibuat sesederhana mungkin untuk pengguna awam) ---
st.sidebar.markdown("#### 🏙️ Pilih Kecamatan")
st.sidebar.caption("Klik kotak di bawah lalu pilih kecamatan, atau gunakan tombol cepat.")

kecamatan_list = sorted(df["KECAMATAN"].unique())

# Kalau dataset berganti, otomatis pilih ulang semua kecamatan dari dataset baru
if st.session_state.get("dataset_aktif") != selected_dataset:
    st.session_state["kecamatan_multiselect"] = kecamatan_list
    st.session_state["dataset_aktif"] = selected_dataset

# Dua tombol cepat: pilih semua / kosongkan — lebih mudah daripada klik satu-satu
tombol_semua, tombol_kosong = st.sidebar.columns(2)
if tombol_semua.button("✅ Pilih Semua", use_container_width=True):
    st.session_state["kecamatan_multiselect"] = kecamatan_list
if tombol_kosong.button("❌ Kosongkan", use_container_width=True):
    st.session_state["kecamatan_multiselect"] = []

selected_kecamatan = st.sidebar.multiselect(
    "Kecamatan yang ditampilkan",
    options=kecamatan_list,
    key="kecamatan_multiselect",
    placeholder="Ketik atau pilih nama kecamatan...",
)

if selected_kecamatan:
    st.sidebar.success(f"✅ {len(selected_kecamatan)} dari {len(kecamatan_list)} kecamatan ditampilkan")
else:
    st.sidebar.warning("⚠️ Belum ada kecamatan dipilih — klik 'Pilih Semua' di atas")

# --- Terapkan filter ---
df_filtered = df[df["KECAMATAN"].isin(selected_kecamatan)]

# --- Tombol unduh ---
st.sidebar.markdown("---")
st.sidebar.header("📥 Unduh Data")
st.sidebar.download_button(
    label="Download Data (CSV)",
    data=convert_df_to_csv(df_filtered),
    file_name=f"{selected_dataset}.csv",
    mime="text/csv",
    use_container_width=True,
)

if df_filtered.empty:
    st.info("👈 Silakan pilih minimal satu kecamatan di sidebar untuk menampilkan dashboard.")
    st.stop()


# =====================================================================
# 7. RINGKASAN ANGKA UTAMA (KPI)
# =====================================================================
kpi_items = [
    ("🏙️", "Jumlah Kecamatan", f"{len(df_filtered['KECAMATAN'].unique())}"),
    ("📊", "Jumlah Data", f"{len(df_filtered)}"),
    ("🧮", "Total Nilai", f"{df_filtered['TOTAL'].sum():,.0f}"),
    ("📈", "Rata-rata Nilai", f"{df_filtered['TOTAL'].mean():,.0f}"),
]

cols_kpi = st.columns(4)
for i, (col, (ikon, label, value), warna) in enumerate(zip(cols_kpi, kpi_items, COLOR_KPI)):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {warna}; animation-delay: {i * 0.08:.2f}s;">
            <div class="kpi-card-row">
                <div class="kpi-icon-circle" style="background: {dgn_alpha(warna, 0.16)};">
                    <span class="kpi-icon">{ikon}</span>
                </div>
                <div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="color: {warna};">{value}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# =====================================================================
# 8. GRAFIK PERBANDINGAN PER KECAMATAN
# =====================================================================
st.subheader("📊 Perbandingan Data Kesejahteraan Antar Kecamatan")

fig1 = buat_grafik_batang(df_filtered, "KECAMATAN", "TOTAL", f"Data {selected_dataset}")
fig1.update_layout(xaxis_tickangle=-45, xaxis_title="Kecamatan", yaxis_title="Total Nilai")
st.plotly_chart(fig1, use_container_width=True, config=PLOTLY_CONFIG)
st.caption("💡 Semakin tinggi batang, semakin besar nilai di kecamatan tersebut")

st.markdown("---")


# =====================================================================
# 9. PERSENTASE KATEGORI & RINGKASAN
# =====================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Persentase Kategori")
    kategori_counts = df_filtered["KATEGORI"].value_counts().reset_index()
    kategori_counts.columns = ["KATEGORI", "JUMLAH"]

    fig2 = px.pie(
        kategori_counts,
        values="JUMLAH",
        names="KATEGORI",
        color="KATEGORI",
        color_discrete_map=COLOR_KATEGORI,
        hole=0.35,
        title="",
    )
    fig2.update_traces(
        textposition="inside", textinfo="percent+label",
        textfont=dict(size=FONT_DATALABEL, family=FONT_FAMILY, color="#FFFFFF"),
        insidetextfont=dict(size=FONT_DATALABEL, family=FONT_FAMILY, color="#FFFFFF"),
        marker=dict(line=dict(color="#FFFFFF", width=2)),
    )
    fig2.update_layout(height=400)
    fig2 = perhalus_grafik(fig2)
    # Anotasi jumlah kecamatan di tengah lubang donat — aksen kecil yang membuat chart terasa lebih "hidup"
    fig2.add_annotation(
        text=f"<b style='font-size:20px;color:{COLOR_PRIMARY}'>{kategori_counts['JUMLAH'].sum()}</b><br><span style='font-size:9px;color:{COLOR_TEXT_MUTED}'>Kecamatan</span>",
        showarrow=False, x=0.5, y=0.5, font=dict(family=FONT_FAMILY),
    )
    st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("💡 Potongan terbesar menunjukkan kategori yang paling banyak jumlah kecamatannya")

with col2:
    st.subheader("📝 Ringkasan Kategori")
    for i, kat in enumerate(["Tinggi", "Sedang", "Rendah"]):
        jumlah = len(df_filtered[df_filtered["KATEGORI"] == kat])
        total = len(df_filtered)
        persen = (jumlah / total * 100) if total > 0 else 0
        warna = COLOR_KATEGORI[kat]

        st.markdown(f"""
        <div class="info-card" style="border-left: 5px solid {warna}; animation-delay: {i * 0.1:.2f}s;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1.05rem;">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 1.8rem; height: 1.8rem; border-radius: 50%; background: {dgn_alpha(warna, 0.16)};">{EMOJI_KATEGORI[kat]}</span>
                    {kat}
                </span>
                <span style="font-weight: 700; color: {warna}; font-family: var(--font-mono);">{jumlah} ({persen:.1f}%)</span>
            </div>
            <div class="mini-bar-track">
                <div class="mini-bar-fill" style="width: {persen:.1f}%; background: {warna}; animation-delay: {0.2 + i * 0.1:.2f}s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# =====================================================================
# 10. PERINGKAT KECAMATAN
# =====================================================================
st.subheader("📶 Peringkat Kecamatan Berdasarkan Nilai")

df_ranking = df_filtered.copy()
df_ranking["Peringkat"] = df_ranking["TOTAL"].rank(ascending=False, method="min").astype(int)

rank_option = st.radio(
    "Pilih Tampilan:",
    ["📊 Semua Kecamatan", "🔼 10 Nilai Tertinggi", "🔽 10 Nilai Terendah"],
    horizontal=True,
)

if rank_option == "🔼 10 Nilai Tertinggi":
    df_rank_display = df_ranking.nlargest(10, "TOTAL")
    judul_rank = "10 Kecamatan dengan Nilai Tertinggi"
elif rank_option == "🔽 10 Nilai Terendah":
    df_rank_display = df_ranking.nsmallest(10, "TOTAL")
    judul_rank = "10 Kecamatan dengan Nilai Terendah"
else:
    df_rank_display = df_ranking.sort_values("TOTAL", ascending=False)
    judul_rank = f"Peringkat Semua Kecamatan ({len(df_ranking)} kecamatan)"

tinggi_grafik = 500 if len(df_rank_display) > 10 else 400
fig_rank = buat_grafik_batang(
    df_rank_display, "KECAMATAN", "TOTAL", judul_rank,
    orientasi="h", tinggi=tinggi_grafik,
)
fig_rank.update_layout(
    xaxis_title="Total Nilai",
    yaxis_title="Kecamatan",
    yaxis=dict(autorange="reversed"),
)
st.plotly_chart(fig_rank, use_container_width=True, config=PLOTLY_CONFIG)

col1, col2, col3 = st.columns(3)
if len(df_ranking) > 0:
    tertinggi = df_ranking.nlargest(1, "TOTAL").iloc[0]
    terendah = df_ranking.nsmallest(1, "TOTAL").iloc[0]
    col1.info(f"📈 **Nilai Tertinggi:** {tertinggi['KECAMATAN']} ({tertinggi['TOTAL']:,.0f})")
    col2.info(f"📉 **Nilai Terendah:** {terendah['KECAMATAN']} ({terendah['TOTAL']:,.0f})")
col3.info(f"📊 **Rata-rata Nilai:** {df_ranking['TOTAL'].mean():,.0f}")

st.markdown("---")


# =====================================================================
# 11. RINGKASAN PER KATEGORI
#     (Bersifat informatif untuk bahan tinjauan — keputusan tetap berada
#     pada pihak Bappeda selaku pengguna data)
# =====================================================================
st.subheader("📌 Ringkasan per Kategori")
st.caption("Menampilkan jumlah dan rata-rata nilai kecamatan pada tiap kategori, sebagai bahan tinjauan lebih lanjut.")

KETERANGAN_KATEGORI = {
    "Rendah": "Kelompok dengan nilai paling rendah dibanding kategori lain",
    "Sedang": "Kelompok dengan nilai menengah",
    "Tinggi": "Kelompok dengan nilai paling tinggi dibanding kategori lain",
}

kategori_stats = df_filtered.groupby("KATEGORI").agg(
    DAFTAR_KECAMATAN=("KECAMATAN", list),
    JUMLAH=("TOTAL", "count"),
    RATA_RATA=("TOTAL", "mean"),
).reset_index()

ringkasan_data = []
for _, row in kategori_stats.iterrows():
    ringkasan_data.append({
        "KATEGORI": row["KATEGORI"],
        "JUMLAH": row["JUMLAH"],
        "RATA_RATA": row["RATA_RATA"],
        "KETERANGAN": KETERANGAN_KATEGORI.get(row["KATEGORI"], ""),
        "WARNA": COLOR_KATEGORI.get(row["KATEGORI"], COLOR_ACCENT),
        "DAFTAR_KECAMATAN": row["DAFTAR_KECAMATAN"],
    })

# Ditampilkan sebagai kartu ringkas (bukan grafik) agar sekali lihat langsung paham
cols = st.columns(3)
for i, (col, row) in enumerate(zip(cols, ringkasan_data)):
    with col:
        daftar = ", ".join(row["DAFTAR_KECAMATAN"][:5])
        lebih_banyak = f" (+{len(row['DAFTAR_KECAMATAN']) - 5} lainnya)" if len(row["DAFTAR_KECAMATAN"]) > 5 else ""
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {row['WARNA']}; height: 100%; animation-delay: {i * 0.1:.2f}s;">
            <div class="kpi-label">{EMOJI_KATEGORI[row['KATEGORI']]} KATEGORI {row['KATEGORI'].upper()}</div>
            <div class="kpi-value" style="color: {row['WARNA']};">{row['JUMLAH']} Kecamatan</div>
            <div style="font-size: 0.85rem; color: {COLOR_TEXT_MUTED}; margin: 0.4rem 0;">
                Rata-rata nilai: <strong>{row['RATA_RATA']:,.0f}</strong>
            </div>
            <div style="font-size: 0.85rem; color: #1F2937;">{row['KETERANGAN']}</div>
            <div style="margin-top: 0.6rem; font-size: 0.78rem; color: #263449; font-weight: 500; border-top: 1px solid #E5E9F0; padding-top: 0.5rem;">
                <strong>Kecamatan:</strong> {daftar}{lebih_banyak}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# =====================================================================
# 12. ANALISIS DISTRIBUSI DATA (HISTOGRAM & PERBANDINGAN NILAI)
# =====================================================================
st.subheader("📈 Sebaran Data")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        df_filtered, x="TOTAL", color="KATEGORI",
        color_discrete_map=COLOR_KATEGORI,
        title="Sebaran Nilai", nbins=20,
    )
    fig_hist.update_layout(height=350, xaxis_title="Nilai", yaxis_title="Jumlah Kecamatan")
    fig_hist = perhalus_grafik(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("💡 Grafik ini menunjukkan sebaran nilai di semua kecamatan")

with col2:
    # Diganti dari box plot (sulit dipahami orang awam) menjadi grafik batang
    # sederhana: Minimum, Rata-rata, Maksimum per kategori.
    ringkasan_kategori = df_filtered.groupby("KATEGORI").agg(
        Minimum=("TOTAL", "min"),
        **{"Rata-rata": ("TOTAL", "mean")},
        Maksimum=("TOTAL", "max"),
    ).reindex(["Rendah", "Sedang", "Tinggi"]).dropna().reset_index()

    ringkasan_long = ringkasan_kategori.melt(
        id_vars="KATEGORI", value_vars=["Minimum", "Rata-rata", "Maksimum"],
        var_name="Ukuran", value_name="Nilai",
    )

    fig_box = px.bar(
        ringkasan_long,
        x="KATEGORI", y="Nilai", color="Ukuran",
        barmode="group",
        color_discrete_map={"Minimum": "#A9D3F5", "Rata-rata": "#2E9BE6", "Maksimum": "#0B2D5C"},
        title="Nilai Terendah, Rata-rata, dan Tertinggi per Kategori",
        text="Nilai",
    )
    fig_box.update_traces(
        texttemplate="%{text:,.0f}", textposition="outside",
        textfont=dict(size=FONT_DATALABEL, family=FONT_FAMILY),
    )
    fig_box.update_layout(height=350, xaxis_title="Kategori", yaxis_title="Nilai", legend_title="")
    fig_box = perhalus_grafik(fig_box)
    st.plotly_chart(fig_box, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("💡 Untuk tiap kategori: nilai terendah, rata-rata, dan tertinggi")

st.markdown("---")


# =====================================================================
# 13. HUBUNGAN KELOMPOK (CLUSTER) DAN NILAI
# =====================================================================
st.subheader("🎯 Hubungan Kelompok Data dan Nilai")

fig_scatter = px.scatter(
    df_filtered, x="CLUSTER", y="TOTAL", color="KATEGORI", size="TOTAL",
    hover_data=["KECAMATAN"],
    color_discrete_map=COLOR_KATEGORI,
    title="Sebaran Nilai berdasarkan Kelompok (Cluster)",
)
fig_scatter.update_layout(height=400, xaxis_title="Kelompok (Cluster)", yaxis_title="Total Nilai")
fig_scatter = perhalus_grafik(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True, config=PLOTLY_CONFIG)
st.caption("💡 Titik yang lebih besar menunjukkan nilai yang lebih tinggi")

st.markdown("---")


# =====================================================================
# 14. TABEL DATA LENGKAP
# =====================================================================
st.subheader("📋 Tabel Data Lengkap")

df_display = df_filtered.copy()
df_display["Peringkat"] = df_display["TOTAL"].rank(ascending=False, method="min").astype(int)

LABEL_KOLOM = {
    "TOTAL": "Total Nilai",
    "KECAMATAN": "Nama Kecamatan",
    "KATEGORI": "Kategori",
    "CLUSTER": "Kelompok (Cluster)",
}

col1, col2 = st.columns(2)
with col1:
    sort_by = st.selectbox(
        "Urutkan Berdasarkan",
        options=["TOTAL", "KECAMATAN", "KATEGORI", "CLUSTER"],
        format_func=lambda x: LABEL_KOLOM.get(x, x),
    )
with col2:
    ascending = st.radio(
        "Urutan", options=["Terbesar ke Terkecil", "Terkecil ke Terbesar"],
        horizontal=True, index=0,
    )

df_display = df_display.sort_values(sort_by, ascending=(ascending == "Terkecil ke Terbesar"))

st.dataframe(
    df_display[["Peringkat", "KECAMATAN", "TOTAL", "KATEGORI", "CLUSTER"]],
    use_container_width=True,
    height=400,
    column_config={
        "Peringkat": "🔢 Peringkat",
        "KECAMATAN": "Kecamatan",
        "TOTAL": "Total Nilai",
        "KATEGORI": "Kategori",
        "CLUSTER": "Kelompok",
    },
)


# =====================================================================
# 15. STATISTIK LENGKAP (opsional, dilipat/expander)
# =====================================================================
with st.expander("📊 Statistik Lengkap", expanded=False):
    st.subheader("Statistik per Kategori")

    stats = df_filtered.groupby("KATEGORI").agg(
        Jumlah=("TOTAL", "count"),
        **{"Rata-rata": ("TOTAL", "mean")},
        Minimum=("TOTAL", "min"),
        Maksimum=("TOTAL", "max"),
        Total=("TOTAL", "sum"),
    ).reset_index()

    st.dataframe(
        stats.style.format({
            "Rata-rata": "{:,.0f}",
            "Minimum": "{:,.0f}",
            "Maksimum": "{:,.0f}",
            "Total": "{:,.0f}",
        }),
        use_container_width=True,
        height=200,
    )


# =====================================================================
# 16. FOOTER
# =====================================================================
st.markdown("---")
st.caption(
    "📊 Dashboard Data Agam | Dibuat dengan Streamlit | Data terakhir diperbarui: "
    + pd.Timestamp.now().strftime("%d %B %Y %H:%M")
)
