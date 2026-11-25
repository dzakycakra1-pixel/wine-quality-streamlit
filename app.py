from __future__ import annotations

from pathlib import Path
from datetime import date, datetime
import json
import importlib.util

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# KONFIGURASI APLIKASI
# ============================================================
st.set_page_config(
    page_title="Wine Quality Lab | Praktikum Streamlit",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(_file_).resolve().parent

DATA_DIR = BASE_DIR / "data"

# Jika folder data tidak tersedia atau CSV tidak lengkap,
# baca CSV langsung dari folder utama repository.
if not all(
    (DATA_DIR / name).exists()
    for name in ("winequality-red.csv", "winequality-white.csv")
):
    DATA_DIR = BASE_DIR

st.markdown(
    """
    <style>
      .stApp { background: #f5f7fb; }
      .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px; }
      [data-testid="stSidebar"] { background: #edf3f6; }
      .hero {
        padding: 1.6rem 1.8rem; border-radius: 18px;
        background: linear-gradient(115deg, #0b3b46 0%, #116b70 58%, #3a9b91 100%);
        color: #ffffff; margin-bottom: 1.2rem;
      }
      .hero h1 { color: #ffffff; margin: 0 0 .35rem 0; font-size: 2.15rem; }
      .hero p { color: #e5f4f2; margin: 0; font-size: 1rem; }
      .section-note {
        padding: .8rem 1rem; border-left: 4px solid #16827d;
        background: #eaf3f4; border-radius: 8px; margin: .5rem 0 1rem 0;
      }
      div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e5eaf0;
        padding: 13px 15px; border-radius: 12px;
      }
      div[data-testid="stMetric"] label { color: #526575; }
      .small-muted { color: #607080; font-size: .88rem; }
      code { color: #0e5961; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PEMUATAN DATA
# ============================================================
@st.cache_data(show_spinner=False)
def load_default_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    red_file = DATA_DIR / "winequality-red.csv"
    white_file = DATA_DIR / "winequality-white.csv"

    if not red_file.exists() or not white_file.exists():
        raise FileNotFoundError(
            "CSV default tidak ditemukan. Pastikan folder data berisi "
            "winequality-red.csv dan winequality-white.csv."
        )

    # sep=None + engine='python' mendeteksi pemisah CSV secara otomatis.
    red = pd.read_csv(red_file, sep=None, engine="python")
    white = pd.read_csv(white_file, sep=None, engine="python")

    red["wine_type"] = "red"
    white["wine_type"] = "white"
    combined = pd.concat([red, white], ignore_index=True)
    return red, white, combined


def read_uploaded_csv(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file, sep=None, engine="python")


try:
    red_data, white_data, all_wines = load_default_data()
except Exception as exc:
    st.error(f"Gagal memuat dataset: {exc}")
    st.stop()


# ============================================================
# SIDEBAR / NAVIGASI (BAB 2.7: SIDEBAR)
# ============================================================
PAGES = [
    "Beranda",
    "Bab 1 - Pengenalan & Instalasi",
    "2.1 Dasar Streamlit",
    "2.2 Elemen Text",
    "2.3 Menampilkan Data",
    "2.4 Menampilkan Grafik",
    "2.5 Input Form",
    "2.6 Menampilkan Media",
    "2.7 Layout & Container",
    "2.8 Control Flow",
    "Eksplorasi Dataset",
]

st.sidebar.markdown("## WINE QUALITY LAB")
st.sidebar.caption("Praktikum Streamlit • Modul Bab 1–2")
selected_page = st.sidebar.radio("Navigasi", PAGES, index=0)
st.sidebar.divider()
dataset_choice = st.sidebar.selectbox(
    "Dataset aktif",
    ["Gabungan Red + White", "Red Wine", "White Wine"],
)
if dataset_choice == "Red Wine":
    current_df = red_data.copy()
elif dataset_choice == "White Wine":
    current_df = white_data.copy()
else:
    current_df = all_wines.copy()

st.sidebar.caption(f"{len(current_df):,} baris aktif")
st.sidebar.caption("Sumber: CSV Wine Quality yang disertakan dalam proyek.")


# ============================================================
# FUNGSI BANTU
# ============================================================
def section_intro(title: str, description: str) -> None:
    st.title(title)
    st.markdown(f'<div class="section-note">{description}</div>', unsafe_allow_html=True)


def csv_bytes(frame: pd.DataFrame) -> bytes:
    return frame.to_csv(index=False).encode("utf-8")


def make_demo_map(n: int = 35) -> pd.DataFrame:
    """Koordinat simulasi untuk demonstrasi API peta; bukan lokasi sampel wine."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "lat": -6.20 + rng.normal(0, 0.035, n),
            "lon": 106.82 + rng.normal(0, 0.035, n),
            "quality": rng.choice([4, 5, 6, 7, 8], n),
        }
    )


# ============================================================
# BERANDA
# ============================================================
if selected_page == "Beranda":
    st.markdown(
        """
        <div class="hero">
          <h1>Wine Quality Lab</h1>
          <p>Praktikum implementasi Streamlit berdasarkan seluruh materi Bab 1 dan Bab 2,
          menggunakan dataset Wine Quality Red & White.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Ringkasan dataset aktif")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah sampel", f"{len(current_df):,}")
    c2.metric("Jumlah fitur/kolom", f"{current_df.shape[1]}")
    c3.metric("Rata-rata quality", f"{current_df['quality'].mean():.2f}")
    c4.metric("Missing value", f"{int(current_df.isna().sum().sum()):,}")

    st.divider()
    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Tujuan praktikum")
        st.write(
            "Aplikasi ini menggabungkan contoh dasar Streamlit dengan eksplorasi "
            "dataset Wine Quality. Setiap menu di sidebar mewakili tahapan pada "
            "modul, sehingga fungsi-fungsi dapat dicoba langsung melalui browser."
        )
        st.markdown(
            """
            - Memahami instalasi dan menjalankan aplikasi Streamlit.
            - Mencoba komponen teks, data, grafik, input, media, dan layout.
            - Mempraktikkan form, tombol, kondisi, stop, dan rerun.
            - Mengeksplorasi data red wine, white wine, dan data gabungan.
            """
        )
    with right:
        st.subheader("Komposisi dataset")
        summary = pd.DataFrame(
            {"Jenis Wine": ["Red", "White"], "Jumlah": [len(red_data), len(white_data)]}
        ).set_index("Jenis Wine")
        st.bar_chart(summary, y="Jumlah", color="#16827d")
        st.caption("Jumlah sampel berdasarkan dua file CSV yang disediakan.")

    st.divider()
    st.subheader("Peta materi")
    roadmap = pd.DataFrame(
        {
            "Bab": ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"],
            "Materi": [
                "Tentang Streamlit", "Instalasi", "Aplikasi pertama", "Dasar Streamlit",
                "Elemen Text", "Menampilkan Data", "Menampilkan Grafik", "Input Form",
                "Media", "Layout & Container", "Control Flow",
            ],
            "Status": ["Diimplementasikan"] * 11,
        }
    )
    st.dataframe(roadmap, hide_index=True, use_container_width=True)
    st.caption("Pilih materi pada navigasi di sebelah kiri untuk melihat demonstrasi.")


# ============================================================
# BAB 1: PENGENALAN, INSTALASI, APLIKASI PERTAMA
# ============================================================
elif selected_page == "Bab 1 - Pengenalan & Instalasi":
    section_intro(
        "Bab 1 — Pengenalan Framework Web Streamlit",
        "Bagian ini merangkum pengenalan Streamlit, persiapan lingkungan kerja, instalasi pustaka, dan aplikasi pertama.",
    )
    st.header("1.1 Tentang Streamlit")
    st.write(
        "Streamlit adalah framework Python open-source untuk membangun aplikasi web "
        "interaktif, terutama untuk kebutuhan data science, visualisasi data, dan "
        "machine learning. Antarmuka dapat dibuat langsung dengan Python tanpa harus "
        "membangun frontend web dari awal."
    )
    st.markdown(
        """
        **Komponen utama pada praktikum ini**
        - Python sebagai bahasa pemrograman.
        - Visual Studio Code sebagai editor.
        - Streamlit sebagai framework web.
        - Browser seperti Chrome atau Edge untuk melihat aplikasi.
        - Pandas, NumPy, dan Matplotlib untuk pengolahan serta visualisasi data.
        """
    )

    st.divider()
    st.header("1.2 Instalasi Streamlit")
    st.subheader("A. Persiapan perangkat")
    st.markdown(
        """
        1. Instal Python 3.10 atau versi lebih baru.
        2. Instal Visual Studio Code.
        3. Siapkan browser.
        4. Buka folder proyek ini melalui VS Code.
        """
    )
    st.subheader("B. Membuat virtual environment")
    st.code(
        r"""# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate""",
        language="bash",
    )
    st.subheader("C. Instalasi seluruh library")
    st.code(
        """python -m pip install --upgrade pip
pip install -r requirements.txt""",
        language="bash",
    )
    st.caption(
        "requirements.txt sudah mencakup Streamlit, Pandas, NumPy, Matplotlib, "
        "serta library visualisasi yang digunakan pada contoh Bab 2."
    )

    st.divider()
    st.header("1.3 Aplikasi Pertama Streamlit")
    st.write("Contoh paling sederhana sesuai modul:")
    hello_code = """import streamlit as st

st.write("Hello World!")"""
    st.code(hello_code, language="python")
    st.subheader("Output")
    st.success("Hello World!")
    st.markdown("Untuk menjalankan aplikasi proyek ini, buka terminal pada folder proyek:")
    st.code("streamlit run app.py", language="bash")
    st.info("Setelah perintah dijalankan, buka alamat lokal yang ditampilkan di terminal (umumnya http://localhost:8501).")


# ============================================================
# BAB 2.1: DASAR STREAMLIT
# ============================================================
elif selected_page == "2.1 Dasar Streamlit":
    section_intro(
        "2.1 — Dasar Streamlit",
        "Modul memperkenalkan st.write() untuk menampilkan teks maupun objek data di halaman web.",
    )
    st.write("Hello World!")
    st.write("Ini adalah contoh teks menggunakan st.write().")
    st.write("Bilangan:", 1234)
    st.write("Rata-rata quality:", round(current_df["quality"].mean(), 3))
    st.write("Contoh DataFrame:", current_df.head(5))
    st.divider()
    st.subheader("Kode yang digunakan")
    st.code(
        """import streamlit as st
import pandas as pd

st.write("Hello World!")
st.write(1234)
st.write(pd.DataFrame({"kolom": [1, 2, 3]}))""",
        language="python",
    )


# ============================================================
# BAB 2.2: ELEMEN TEXT
# ============================================================
elif selected_page == "2.2 Elemen Text":
    section_intro(
        "2.2 — Elemen Text",
        "Demonstrasi markdown, title, header, subheader, caption, code, text, LaTeX, dan divider.",
    )
    st.markdown("### A. st.markdown()")
    st.markdown("Teks **tebal**, *miring*, dan :green[teks berwarna hijau].")
    st.markdown("- Red wine\n- White wine\n- Dataset gabungan")

    st.divider()
    st.title("B. st.title()")
    st.header("C. st.header()")
    st.subheader("D. st.subheader()")
    st.caption("E. st.caption() — teks keterangan berukuran kecil.")
    st.text("G. st.text() — menampilkan teks biasa tanpa format Markdown.")
    st.code('st.title("Judul Aplikasi")\nst.header("Bagian Utama")', language="python")

    st.divider()
    st.markdown("### H. st.latex()")
    st.latex(r"z = \frac{x - \mu}{\sigma}")
    st.caption("Persamaan standardisasi fitur yang juga digunakan pada notebook referensi.")
    st.markdown("### I. st.divider()")
    st.write("Divider di atas memisahkan kelompok materi.")


# ============================================================
# BAB 2.3: MENAMPILKAN DATA
# ============================================================
elif selected_page == "2.3 Menampilkan Data":
    section_intro(
        "2.3 — Menampilkan Data",
        "Contoh st.dataframe(), st.table(), st.metric(), dan st.json() menggunakan data Wine Quality.",
    )
    st.subheader("A. st.dataframe() — tabel interaktif")
    st.dataframe(current_df.head(20), use_container_width=True)

    st.subheader("B. st.table() — tabel statis")
    st.table(current_df[["wine_type", "alcohol", "density", "pH", "quality"]].head(6))

    st.subheader("C. st.metric() — ringkasan angka")
    a, b, c = st.columns(3)
    a.metric("Jumlah data", f"{len(current_df):,}")
    b.metric("Quality rata-rata", f"{current_df['quality'].mean():.2f}")
    c.metric("Alkohol rata-rata", f"{current_df['alcohol'].mean():.2f}%")

    st.subheader("D. st.json() — metadata dataset")
    metadata = {
        "dataset_aktif": dataset_choice,
        "jumlah_baris": int(current_df.shape[0]),
        "jumlah_kolom": int(current_df.shape[1]),
        "kolom": current_df.columns.tolist(),
        "missing_values": int(current_df.isna().sum().sum()),
        "rentang_quality": [
            int(current_df["quality"].min()),
            int(current_df["quality"].max()),
        ],
    }
    st.json(metadata)

    st.divider()
    st.subheader("Unggah CSV untuk diperiksa")
    uploaded_csv = st.file_uploader("Pilih file CSV", type=["csv"], key="data_csv_upload")
    if uploaded_csv is not None:
        try:
            user_df = read_uploaded_csv(uploaded_csv)
            st.success(f"CSV berhasil dibaca: {user_df.shape[0]:,} baris × {user_df.shape[1]} kolom.")
            st.dataframe(user_df.head(30), use_container_width=True)
            st.download_button(
                "Unduh kembali CSV yang dibaca",
                data=csv_bytes(user_df),
                file_name="csv_hasil_pemeriksaan.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"CSV tidak dapat dibaca: {exc}")


# ============================================================
# BAB 2.4: MENAMPILKAN GRAFIK
# ============================================================
elif selected_page == "2.4 Menampilkan Grafik":
    section_intro(
        "2.4 — Menampilkan Grafik",
        "Grafik garis, area, batang, Matplotlib, Altair, Vega-Lite, Plotly, Bokeh, PyDeck, Graphviz, dan peta.",
    )
    st.caption(
        "Visualisasi utama menggunakan data asli Wine Quality. Contoh peta memakai "
        "koordinat simulasi karena dataset wine tidak memiliki kolom latitude/longitude."
    )

    chart_options = [
        "Line chart",
        "Area chart",
        "Bar chart",
        "Matplotlib (pyplot)",
        "Altair",
        "Vega-Lite",
        "Plotly",
        "Bokeh",
        "PyDeck",
        "Graphviz",
        "Map",
    ]
    chart_choice = st.selectbox("Pilih jenis grafik", chart_options)
    chart_df = (
        current_df.groupby(["quality", "wine_type"], as_index=False)
        .agg(
            alcohol=("alcohol", "mean"),
            volatile_acidity=("volatile acidity", "mean"),
            sample_count=("quality", "size"),
        )
    )

    if chart_choice == "Line chart":
        line_data = current_df.groupby("quality")[["alcohol", "volatile acidity"]].mean()
        st.line_chart(line_data)
        st.caption("st.line_chart(): menampilkan tren rata-rata fitur berdasarkan skor quality.")
    elif chart_choice == "Area chart":
        area_data = current_df.groupby("quality")[["alcohol", "volatile acidity"]].mean()
        st.area_chart(area_data)
        st.caption("st.area_chart(): menampilkan area nilai rata-rata fitur.")
    elif chart_choice == "Bar chart":
        bar_data = current_df.groupby("quality").size().rename("jumlah sampel").to_frame()
        st.bar_chart(bar_data)
        st.caption("st.bar_chart(): membandingkan jumlah sampel pada setiap skor quality.")
    elif chart_choice == "Matplotlib (pyplot)":
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for wine_type, group in current_df.groupby("wine_type"):
            ax.hist(group["alcohol"], bins=25, alpha=0.55, label=wine_type)
        ax.set_title("Distribusi Alcohol berdasarkan Jenis Wine")
        ax.set_xlabel("Alcohol")
        ax.set_ylabel("Frekuensi")
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    elif chart_choice == "Altair":
        try:
            import altair as alt
            sample = current_df.sample(min(700, len(current_df)), random_state=42)
            chart = (
                alt.Chart(sample)
                .mark_circle(size=55, opacity=0.55)
                .encode(
                    x=alt.X("alcohol:Q", title="Alcohol"),
                    y=alt.Y("volatile acidity:Q", title="Volatile Acidity"),
                    color=alt.Color("wine_type:N", title="Jenis wine"),
                    tooltip=["wine_type", "alcohol", "volatile acidity", "quality"],
                )
                .properties(height=430, title="Alcohol vs Volatile Acidity")
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)
        except ImportError:
            st.warning("Altair belum terpasang. Jalankan pip install -r requirements.txt.")
    elif chart_choice == "Vega-Lite":
        try:
            values = (
                current_df.groupby("quality", as_index=False)
                .size()
                .rename(columns={"size": "jumlah"})
                .to_dict("records")
            )
            spec = {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4},
                "encoding": {
                    "x": {"field": "quality", "type": "ordinal", "title": "Quality"},
                    "y": {"field": "jumlah", "type": "quantitative", "title": "Jumlah sampel"},
                    "tooltip": [
                        {"field": "quality", "type": "ordinal"},
                        {"field": "jumlah", "type": "quantitative"},
                    ],
                },
                "height": 380,
            }
            st.vega_lite_chart(data=pd.DataFrame(values), spec=spec, use_container_width=True)
        except Exception as exc:
            st.error(f"Vega-Lite tidak dapat ditampilkan: {exc}")
    elif chart_choice == "Plotly":
        try:
            import plotly.express as px
            sample = current_df.sample(min(1200, len(current_df)), random_state=42)
            fig = px.scatter(
                sample,
                x="alcohol",
                y="volatile acidity",
                color="wine_type",
                size="quality",
                hover_data=["quality", "density", "pH"],
                title="Hubungan Alcohol dan Volatile Acidity",
                opacity=0.65,
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.warning("Plotly belum terpasang. Jalankan pip install -r requirements.txt.")
    elif chart_choice == "Bokeh":
        try:
            from bokeh.plotting import figure
            sample = current_df.sample(min(500, len(current_df)), random_state=42)
            fig = figure(
                title="Bokeh: Alcohol vs Quality",
                x_axis_label="Alcohol",
                y_axis_label="Quality",
                height=420,
                sizing_mode="stretch_width",
                tools="pan,wheel_zoom,box_zoom,reset,save",
            )
            fig.circle(
                sample["alcohol"],
                sample["quality"],
                size=7,
                alpha=0.45,
                color="#16827d",
            )
            st.bokeh_chart(fig, use_container_width=True)
        except ImportError:
            st.warning("Bokeh belum terpasang. Jalankan pip install -r requirements.txt.")
    elif chart_choice == "PyDeck":
        try:
            import pydeck as pdk
            map_demo = make_demo_map()
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_demo,
                get_position="[lon, lat]",
                get_fill_color="[22, 130, 125, 170]",
                get_radius=3500,
                pickable=True,
            )
            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=pdk.ViewState(
                    latitude=float(map_demo["lat"].mean()),
                    longitude=float(map_demo["lon"].mean()),
                    zoom=9,
                    pitch=0,
                ),
                tooltip={"text": "Quality simulasi: {quality}"},
            )
            st.pydeck_chart(deck, use_container_width=True)
            st.caption("Titik dan skor pada peta ini sepenuhnya simulasi untuk demonstrasi PyDeck.")
        except ImportError:
            st.warning("PyDeck belum terpasang. Jalankan pip install -r requirements.txt.")
    elif chart_choice == "Graphviz":
        graph = """
        digraph WineQuality {
          rankdir=LR;
          graph [bgcolor="transparent"];
          node [shape=box, style="rounded,filled", fillcolor="#e8f2f2", color="#16827d"];
          alcohol [label="Alcohol"];
          acidity [label="Volatile Acidity"];
          density [label="Density"];
          quality [label="Quality"];
          alcohol -> quality;
          acidity -> quality;
          density -> quality;
        }
        """
        st.graphviz_chart(graph, use_container_width=True)
        st.caption("Diagram konseptual hubungan fitur dengan target; bukan hasil kausalitas.")
    elif chart_choice == "Map":
        map_demo = make_demo_map()
        st.map(map_demo[["lat", "lon"]])
        st.dataframe(map_demo.head(10), use_container_width=True)
        st.caption("Koordinat simulasi hanya untuk mencoba st.map(); dataset Wine Quality tidak menyimpan lokasi geografis.")


# ============================================================
# BAB 2.5: INPUT FORM
# ============================================================
elif selected_page == "2.5 Input Form":
    section_intro(
        "2.5 — Menampilkan Input Form",
        "Praktik button, data editor, download button, checkbox, radio, selectbox, multiselect, slider, text, angka, tanggal, waktu, upload, camera, dan color picker.",
    )

    st.subheader("A. Button")
    if st.button("Klik untuk menjalankan aksi", key="demo_button"):
        st.success("Tombol berhasil ditekan.")

    st.divider()
    st.subheader("B. Data editor")
    st.caption("Padanan modern dari st.experimental_data_editor() pada modul adalah st.data_editor().")
    editable = current_df.head(12).copy()
    edited_df = st.data_editor(
        editable,
        num_rows="dynamic",
        use_container_width=True,
        key="wine_data_editor",
    )
    st.download_button(
        "C. Download hasil data editor",
        data=csv_bytes(edited_df),
        file_name="wine_quality_edit.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader("D–H. Contoh widget pilihan dan input")
    c1, c2 = st.columns(2)
    with c1:
        checkbox_value = st.checkbox("Tampilkan keterangan tambahan", value=True)
        radio_value = st.radio("Pilih jenis wine", ["Red", "White", "Gabungan"], horizontal=True)
        select_value = st.selectbox("Pilih skor quality", sorted(current_df["quality"].unique()))
        multi_value = st.multiselect(
            "Pilih fitur",
            ["alcohol", "density", "pH", "volatile acidity", "citric acid"],
            default=["alcohol", "pH"],
        )
        slider_value = st.slider("Rentang alcohol", 8.0, 15.0, (9.0, 13.0), 0.1)
        select_slider_value = st.select_slider(
            "Tingkat kualitas",
            options=["Rendah", "Sedang", "Tinggi"],
            value="Sedang",
        )
    with c2:
        text_value = st.text_input("Nama praktikan", placeholder="Masukkan nama")
        number_value = st.number_input("Jumlah sampel untuk ditampilkan", min_value=1, max_value=100, value=10)
        area_value = st.text_area("Catatan praktikum", placeholder="Tulis catatan di sini...")
        date_value = st.date_input("Tanggal praktikum", value=date.today())
        time_value = st.time_input("Waktu praktikum", value=datetime.now().time().replace(second=0, microsecond=0))
        color_value = st.color_picker("Pilih warna aksen", "#16827d")

    if checkbox_value:
        st.info(
            f"Pilihan: wine={radio_value}, quality={select_value}, fitur={multi_value}, "
            f"alcohol={slider_value}, kategori={select_slider_value}."
        )
    st.markdown(
        f'<div style="padding:12px;border-radius:10px;background:{color_value};color:white">'
        f'Warna pilihan: {color_value}</div>',
        unsafe_allow_html=True,
    )
    st.write(
        {
            "nama": text_value,
            "jumlah_sampel": int(number_value),
            "tanggal": str(date_value),
            "waktu": str(time_value),
            "catatan": area_value,
        }
    )

    st.divider()
    st.subheader("I–K. File uploader dan camera input")
    csv_upload = st.file_uploader("Unggah CSV untuk dibaca", type=["csv"], key="input_csv")
    if csv_upload is not None:
        try:
            uploaded_df = read_uploaded_csv(csv_upload)
            st.success(f"File CSV terbaca: {uploaded_df.shape}")
            st.dataframe(uploaded_df.head(10), use_container_width=True)
        except Exception as exc:
            st.error(f"Gagal membaca CSV: {exc}")

    camera_photo = st.camera_input("Ambil foto melalui kamera perangkat")
    if camera_photo is not None:
        st.image(camera_photo, caption="Foto dari camera_input", use_container_width=True)


# ============================================================
# BAB 2.6: MEDIA
# ============================================================
elif selected_page == "2.6 Menampilkan Media":
    section_intro(
        "2.6 — Menampilkan Media",
        "Modul membahas st.image(), st.audio(), dan st.video(). Unggah media sendiri untuk mencoba masing-masing komponen.",
    )
    st.subheader("A. st.image()")
    image_file = st.file_uploader(
        "Unggah gambar (PNG/JPG/JPEG)",
        type=["png", "jpg", "jpeg"],
        key="media_image",
    )
    if image_file is not None:
        st.image(image_file, caption="Gambar yang diunggah", use_container_width=True)
    else:
        st.info("Belum ada gambar yang diunggah. Contoh visualisasi dataset ditampilkan di bawah.")
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.hist(current_df["quality"], bins=np.arange(2.5, 10.5, 1), color="#16827d", edgecolor="white")
        ax.set_title("Distribusi Skor Quality")
        ax.set_xlabel("Quality")
        ax.set_ylabel("Jumlah sampel")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.divider()
    st.subheader("B. st.audio()")
    audio_file = st.file_uploader(
        "Unggah audio (MP3/WAV/OGG)",
        type=["mp3", "wav", "ogg"],
        key="media_audio",
    )
    if audio_file is not None:
        st.audio(audio_file)
    else:
        st.caption("Unggah file audio untuk mengaktifkan pemutar audio.")

    st.divider()
    st.subheader("C. st.video()")
    video_file = st.file_uploader(
        "Unggah video (MP4/MOV)",
        type=["mp4", "mov"],
        key="media_video",
    )
    if video_file is not None:
        st.video(video_file)
    else:
        st.caption("Unggah file video untuk mengaktifkan pemutar video.")


# ============================================================
# BAB 2.7: LAYOUT DAN CONTAINER
# ============================================================
elif selected_page == "2.7 Layout & Container":
    section_intro(
        "2.7 — Layout dan Container",
        "Praktik sidebar, columns, tabs, expander, container, dan empty untuk menyusun halaman aplikasi.",
    )
    st.subheader("A. Sidebar")
    st.write(
        "Sidebar berada di sebelah kiri aplikasi. Navigasi dan pilihan dataset pada proyek ini "
        "dibuat menggunakan st.sidebar.radio() dan st.sidebar.selectbox()."
    )

    st.divider()
    st.subheader("B. Columns")
    col1, col2, col3 = st.columns(3)
    col1.metric("Red wine", f"{len(red_data):,}")
    col2.metric("White wine", f"{len(white_data):,}")
    col3.metric("Gabungan", f"{len(all_wines):,}")

    st.divider()
    st.subheader("C. Tabs")
    tab1, tab2, tab3 = st.tabs(["Ringkasan", "Data", "Grafik"])
    with tab1:
        st.write("Tab digunakan untuk mengelompokkan konten yang saling berkaitan.")
        st.write("Rata-rata quality:", round(current_df["quality"].mean(), 2))
    with tab2:
        st.dataframe(current_df.head(8), use_container_width=True)
    with tab3:
        st.bar_chart(current_df["quality"].value_counts().sort_index())

    st.divider()
    st.subheader("D. Expander")
    with st.expander("Klik untuk melihat penjelasan"):
        st.write(
            "Expander menyimpan beberapa komponen di dalam wadah yang dapat dibuka "
            "dan ditutup oleh pengguna."
        )
        st.code('with st.expander("Penjelasan"):\n    st.write("Isi penjelasan")', language="python")

    st.subheader("E. Container")
    with st.container(border=True):
        st.markdown("**Contoh konten di dalam container**")
        st.write("Container mengelompokkan beberapa elemen antarmuka.")
        st.metric("Rata-rata alcohol", f"{current_df['alcohol'].mean():.2f}")

    st.subheader("F. Empty")
    placeholder = st.empty()
    placeholder.info("Ini adalah elemen placeholder dari st.empty().")
    if st.button("Ganti isi placeholder"):
        placeholder.success("Isi placeholder berhasil diganti.")


# ============================================================
# BAB 2.8: CONTROL FLOW
# ============================================================
elif selected_page == "2.8 Control Flow":
    section_intro(
        "2.8 — Control Flow",
        "Praktik st.stop(), st.form(), st.form_submit_button(), dan rerun. Fungsi rerun modern adalah st.rerun().",
    )

    st.subheader("A. st.stop()")
    st.write("Tekan tombol berikut untuk menghentikan eksekusi halaman ini.")
    if st.button("Stop Aplikasi (Demo)", type="secondary"):
        st.warning("Aplikasi dihentikan menggunakan st.stop(). Muat ulang halaman untuk melanjutkan.")
        st.stop()
    st.caption("Kalimat ini hanya tampil jika tombol Stop belum ditekan.")

    st.divider()
    st.subheader("B–C. st.form() dan st.form_submit_button()")
    with st.form("form_praktikan"):
        name_col, age_col = st.columns(2)
        with name_col:
            student_name = st.text_input("Nama praktikan")
            student_age = st.number_input("Umur", min_value=0, max_value=100, value=20)
            address = st.text_area("Alamat")
        with age_col:
            major = st.selectbox("Jurusan", ["Informatika", "Sistem Informasi", "Teknik Elektro"])
            hobbies = st.multiselect("Hobi", ["Olahraga", "Membaca", "Menulis", "Coding"])
            uts = st.number_input("Nilai UTS", min_value=0, max_value=100, value=80)
            uas = st.number_input("Nilai UAS", min_value=0, max_value=100, value=80)
            assignment = st.number_input("Nilai Tugas", min_value=0, max_value=100, value=80)
        submit = st.form_submit_button("Submit Form", type="primary")

    if submit:
        final_score = (uts + uas + assignment) / 3
        st.success("Form berhasil dikirim.")
        st.write(
            {
                "nama": student_name,
                "umur": int(student_age),
                "alamat": address,
                "jurusan": major,
                "hobi": hobbies,
                "nilai_akhir": round(final_score, 2),
            }
        )

    st.divider()
    st.subheader("D. Rerun aplikasi")
    if "rerun_count" not in st.session_state:
        st.session_state.rerun_count = 0
    st.write(f"Jumlah rerun manual: **{st.session_state.rerun_count}**")
    if st.button("Jalankan st.rerun()"):
        st.session_state.rerun_count += 1
        st.rerun()
    st.caption(
        "Modul memakai st.experimental_rerun(). Pada Streamlit modern, gunakan st.rerun() "
        "sebagai penggantinya."
    )


# ============================================================
# EKSPLORASI DATASET
# ============================================================
elif selected_page == "Eksplorasi Dataset":
    section_intro(
        "Eksplorasi Dataset Wine Quality",
        "Gunakan filter untuk mengeksplorasi jenis wine, skor quality, dan fitur fisikokimia.",
    )

    with st.form("filter_dataset"):
        c1, c2, c3 = st.columns(3)
        with c1:
            type_filter = st.multiselect(
                "Jenis wine",
                ["red", "white"],
                default=sorted(current_df["wine_type"].unique().tolist()),
            )
        with c2:
            qmin, qmax = st.slider(
                "Rentang quality",
                int(all_wines["quality"].min()),
                int(all_wines["quality"].max()),
                (
                    int(current_df["quality"].min()),
                    int(current_df["quality"].max()),
                ),
            )
        with c3:
            feature_filter = st.multiselect(
                "Kolom yang ditampilkan",
                current_df.columns.tolist(),
                default=["wine_type", "alcohol", "volatile acidity", "density", "quality"],
            )
        search_text = st.text_input("Cari nama kolom (opsional)", placeholder="Contoh: alcohol")
        apply_filter = st.form_submit_button("Terapkan Filter", type="primary")

    filtered = current_df.copy()
    if apply_filter:
        if type_filter:
            filtered = filtered[filtered["wine_type"].isin(type_filter)]
        else:
            filtered = filtered.iloc[0:0]
        filtered = filtered[filtered["quality"].between(qmin, qmax)]

    display_cols = feature_filter or filtered.columns.tolist()
    if search_text.strip():
        display_cols = [c for c in display_cols if search_text.lower() in c.lower()]

    m1, m2, m3 = st.columns(3)
    m1.metric("Data setelah filter", f"{len(filtered):,}")
    m2.metric("Rata-rata quality", f"{filtered['quality'].mean():.2f}" if len(filtered) else "-")
    m3.metric("Missing value", f"{int(filtered.isna().sum().sum()):,}" if len(filtered) else "0")

    if not display_cols:
        st.warning("Tidak ada nama kolom yang cocok dengan pencarian. Ubah kata kunci atau pilihan kolom.")
    elif len(filtered):
        filtered_view = filtered[display_cols]
        st.dataframe(filtered_view.head(500), use_container_width=True)
        st.download_button(
            "Unduh hasil filter CSV",
            data=csv_bytes(filtered_view),
            file_name="wine_quality_filtered.csv",
            mime="text/csv",
        )
    else:
        st.warning("Tidak ada baris yang sesuai dengan filter.")

    st.subheader("Ringkasan statistik")
    if len(filtered):
        st.dataframe(filtered.select_dtypes(include="number").describe().T, use_container_width=True)
        st.bar_chart(filtered["quality"].value_counts().sort_index())


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption(
    "Wine Quality Lab • Praktikum Streamlit Bab 1–2 • "
    "Notebook CRISP-DM dan file CSV disertakan di dalam folder proyek."
)
