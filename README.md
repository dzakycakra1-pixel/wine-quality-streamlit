# Wine Quality Lab — Praktikum Streamlit Bab 1–2

Proyek ini mempraktikkan materi pada buku **Implementasi Algoritma Machine Learning Berbasis Web dengan Framework Streamlit**, Bab 1 dan Bab 2, menggunakan dataset Wine Quality Red dan White serta notebook CRISP-DM yang diberikan.

## 1. Isi folder

```text
wine_quality_streamlit_bab1_2/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── data/
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── winequality-combined.csv
├── notebooks/
│   └── Wine_Quality_Master_Project_CRISP_DM_Lanjutan.ipynb
└── referensi/
    └── Modul_Streamlit_Bab_1_2.pdf
```

## 2. Pemetaan praktik terhadap modul

| Materi modul | Implementasi dalam aplikasi |
|---|---|
| Bab 1.1 Tentang Streamlit | Menu **Bab 1 - Pengenalan & Instalasi** |
| Bab 1.2 Instalasi Streamlit | Langkah virtual environment dan instalasi requirements |
| Bab 1.3 Aplikasi pertama | Contoh `st.write("Hello World!")` dan cara menjalankan aplikasi |
| Bab 2.1 Dasar Streamlit | `st.write()` untuk teks, angka, dan DataFrame |
| Bab 2.2 Elemen Text | `st.markdown`, `st.title`, `st.header`, `st.subheader`, `st.caption`, `st.code`, `st.text`, `st.latex`, `st.divider` |
| Bab 2.3 Menampilkan Data | `st.dataframe`, `st.table`, `st.metric`, `st.json` |
| Bab 2.4 Menampilkan Grafik | `st.line_chart`, `st.area_chart`, `st.bar_chart`, `st.pyplot`, `st.altair_chart`, `st.vega_lite_chart`, `st.plotly_chart`, `st.bokeh_chart`, `st.pydeck_chart`, `st.graphviz_chart`, `st.map` |
| Bab 2.5 Input Form | Button, data editor, download, checkbox, radio, selectbox, multiselect, slider, select slider, input teks/angka/area, tanggal, waktu, upload, kamera, color picker |
| Bab 2.6 Menampilkan Media | `st.image`, `st.audio`, `st.video` |
| Bab 2.7 Layout & Container | Sidebar, columns, tabs, expander, container, empty |
| Bab 2.8 Control Flow | `st.stop`, `st.form`, `st.form_submit_button`, `st.rerun` |

## 3. Cara menjalankan di Windows

1. Ekstrak ZIP proyek.
2. Buka folder `wine_quality_streamlit_bab1_2` melalui Visual Studio Code.
3. Buka Terminal di VS Code.
4. Jalankan perintah berikut satu per satu:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

5. Browser akan membuka aplikasi. Jika tidak terbuka otomatis, akses `http://localhost:8501`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## 4. Dataset yang digunakan

| File | Jumlah baris | Jumlah kolom asli |
|---|---:|---:|
| `winequality-red.csv` | 1,599 | 12 |
| `winequality-white.csv` | 4,898 | 12 |
| `winequality-combined.csv` | 6,497 | 13 |

- File red menggunakan delimiter titik koma (`;`).
- File white menggunakan delimiter koma (`,`).
- Aplikasi membaca delimiter secara otomatis, lalu menambahkan kolom `wine_type` untuk membedakan red dan white.
- Dataset gabungan berisi kolom `wine_type` selain kolom asli.

## 5. Catatan kompatibilitas Streamlit modern

Beberapa nama fungsi pada buku tahun 2023 telah berubah:
- `st.experimental_data_editor()` diganti dengan `st.data_editor()`.
- `st.experimental_rerun()` diganti dengan `st.rerun()`.

Aplikasi memakai API modern agar lebih sesuai dengan versi Streamlit yang baru.

## 6. Catatan visualisasi peta

Dataset Wine Quality tidak memiliki informasi lokasi geografis. Karena itu, menu `st.map()` dan `st.pydeck_chart()` memakai koordinat simulasi yang diberi label dengan jelas, hanya untuk mempraktikkan komponen peta—bukan data lokasi sampel wine.

### Catatan Graphviz

Untuk menjalankan visualisasi Graphviz pada beberapa sistem Windows, instal juga aplikasi Graphviz dari situs resminya dan pastikan folder `bin` Graphviz masuk ke PATH.

## 7. Notebook referensi

Notebook CRISP-DM disertakan di folder `notebooks/`. Lokasi pembacaan CSV pada salinan notebook disesuaikan menjadi `../data/` agar dapat dijalankan dari struktur folder proyek ini. Analisis notebook tetap menjadi referensi terpisah dari aplikasi Streamlit Bab 1–2.
