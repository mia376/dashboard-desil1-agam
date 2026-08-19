import pandas as pd
import os


folder_input = "data"
folder_output = "hasil_clean"

os.makedirs(folder_output, exist_ok=True)


files = {
    "desil1": "Data Desil 1 Berdasarkan KK.xlsx",
    "desil2": "Data Desil 2 Berdasarkan KK.xlsx",
    "desil3": "Data Desil 3 Berdasarkan KK.xlsx",
    "desil4": "Data Desil 4 Berdasarkan KK.xlsx",
    "desil5": "Data Desil 5 Berdasarkan KK.xlsx",
    "sanitasi": "Data Desil 5 Rumah Sanitasi Tidak Layak.xlsx",
    "rtlh": "Data Desil 5 Rumah Tidak Layak Huni.xlsx"
}


for nama, file in files.items():

    print("\n============================")
    print("Memproses:", file)


    path = os.path.join(folder_input, file)


    # baca tanpa header
    raw = pd.read_excel(
        path,
        header=None
    )


    # ==============================
    # CARI BARIS HEADER OTOMATIS
    # ==============================

    header_index = None

    for i, row in raw.iterrows():

        isi = row.astype(str).tolist()

        if (
            "KODE" in isi and
            "KECAMATAN" in isi and
            "TOTAL" in isi
        ):
            header_index = i
            break


    if header_index is None:
        print("Header tidak ditemukan:", file)
        continue


    print("Header ditemukan pada baris:", header_index)


    # jadikan header
    raw.columns = raw.iloc[header_index]


    df = raw.iloc[header_index+1:]


    # ambil kolom
    df = df[
        [
            "KODE",
            "KECAMATAN",
            "TOTAL"
        ]
    ]


    # hapus kosong
    df = df.dropna(
        subset=["KECAMATAN"]
    )


    # bersihkan angka
    df["TOTAL"] = (
        df["TOTAL"]
        .astype(str)
        .str.replace(",", "")
    )


    df["TOTAL"] = pd.to_numeric(
        df["TOTAL"],
        errors="coerce"
    )


    # ambil level kecamatan
    df = df[
        df["KODE"]
        .astype(str)
        .str.match(r"13\.06\.\d{2}$")
    ]


    hasil = df[
        [
            "KECAMATAN",
            "TOTAL"
        ]
    ]


    output = (
        folder_output
        + "/"
        + nama
        + "_clean.csv"
    )


    hasil.to_csv(
        output,
        index=False
    )


    print("Berhasil:", output)
    print(hasil.head())


print("\nSEMUA SELESAI")