import pandas as pd
import re


# ======================================================
# SETTING FILE
# ======================================================

file_input = r"data\Data Desil 1 Berdasarkan KK.xlsx"
file_output = r"data\desil1_clean.csv"


print("=" * 60)
print("PREPROCESSING DATA DESIL 1 AGAM")
print("=" * 60)



# ======================================================
# LOAD DATA EXCEL
# ======================================================

df_raw = pd.read_excel(
    file_input,
    header=None
)


print("\nUKURAN DATA AWAL")
print(df_raw.shape)



# ======================================================
# CARI HEADER
# ======================================================

header_row = None


for i, row in df_raw.iterrows():

    text = " ".join(
        row.fillna("")
        .astype(str)
        .tolist()
    ).upper()


    if "KODE" in text and "KECAMATAN" in text:
        header_row = i
        break



if header_row is None:
    raise Exception(
        "Header tidak ditemukan"
    )


print(
    "Header ditemukan pada baris:",
    header_row
)



# ======================================================
# BACA DATA
# ======================================================

df = pd.read_excel(
    file_input,
    header=header_row
)



# ======================================================
# CLEANING AWAL
# ======================================================

df.dropna(
    axis=1,
    how="all",
    inplace=True
)


df.dropna(
    axis=0,
    how="all",
    inplace=True
)



df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)



print("\nKOLOM:")
print(df.columns)



# ======================================================
# BERSIHKAN TEKS
# ======================================================

for col in df.columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
    )



# ======================================================
# HAPUS HEADER ULANG
# ======================================================

df = df[
    df["KODE"].str.upper() != "KODE"
]



# ======================================================
# HAPUS JUDUL LAPORAN
# ======================================================

hapus = [
    "PROVINSI",
    "KABUPATEN",
    "DESIL",
    "KRITERIA"
]


for kata in hapus:

    df = df[
        ~df["KODE"]
        .str.upper()
        .str.contains(
            kata,
            na=False
        )
    ]



# ======================================================
# IDENTIFIKASI LEVEL WILAYAH
# ======================================================

df["LEVEL"] = df["KODE"].apply(
    lambda x:
    "KECAMATAN"
    if re.match(r"^\d{2}\.\d{2}\.\d{2}$", str(x))
    else "DESA"
)



# ======================================================
# ISI KECAMATAN KOSONG
# ======================================================

df["KECAMATAN"] = (
    df["KECAMATAN"]
    .replace(
        ["", "nan"],
        pd.NA
    )
    .ffill()
)



# ======================================================
# CLEAN ANGKA
# ======================================================

kolom_angka = [
    "LAKI-LAKI",
    "PEREMPUAN",
    "#NA/TIDAK DIKETAHUI",
    "TOTAL"
]


for kolom in kolom_angka:

    if kolom in df.columns:

        df[kolom] = (
            df[kolom]
            .astype(str)
            .str.replace(
                ",",
                "",
                regex=False
            )
        )


        df[kolom] = pd.to_numeric(
            df[kolom],
            errors="coerce"
        )



# isi kosong angka

df[kolom_angka] = (
    df[kolom_angka]
    .fillna(0)
)



# integer

for kolom in kolom_angka:

    df[kolom] = (
        df[kolom]
        .astype(int)
    )



# ======================================================
# HAPUS DUPLIKAT
# ======================================================

df.drop_duplicates(
    inplace=True
)


df.reset_index(
    drop=True,
    inplace=True
)



# ======================================================
# HASIL
# ======================================================

print("\nHASIL AKHIR")

print(df.info())


print("\nDATA KECAMATAN")

print(
    df[
        df["LEVEL"]=="KECAMATAN"
    ][
        [
            "KECAMATAN",
            "TOTAL"
        ]
    ]
)



print("\nUKURAN DATA")
print(df.shape)



print("\nMISSING")
print(df.isnull().sum())



# ======================================================
# SIMPAN
# ======================================================

df.to_csv(
    file_output,
    index=False,
    encoding="utf-8"
)



print("\n" + "="*60)
print("PREPROCESSING SELESAI")
print("="*60)

print(
    "OUTPUT:",
    file_output
)