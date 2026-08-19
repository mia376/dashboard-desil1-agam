import pandas as pd
import os


# lokasi folder data
folder_data = "data"


# daftar file excel
files = [
    "Data Desil 1 Berdasarkan KK.xlsx",
    "Data Desil 2 Berdasarkan KK.xlsx",
    "Data Desil 3 Berdasarkan KK.xlsx",
    "Data Desil 4 Berdasarkan KK.xlsx",
    "Data Desil 5 Berdasarkan KK.xlsx",
    "Data Desil 5 Rumah Sanitasi Tidak Layak.xlsx",
    "Data Desil 5 Rumah Tidak Layak Huni.xlsx"
]


for file in files:

    path = os.path.join(folder_data, file)

    print("\n===================================")
    print("FILE :", file)

    df = pd.read_excel(path)

    print("Ukuran data :", df.shape)

    print("\nNama kolom:")
    print(df.columns.tolist())

    print("\nContoh data:")
    print(df.head())