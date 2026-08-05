import pandas as pd


file_input = r"data\desil1_clean.csv"


print("="*60)
print("EXPLORATORY DATA ANALYSIS DESIL 1 AGAM")
print("="*60)


# LOAD DATA

df = pd.read_csv(file_input)



# ===============================
# AMBIL DATA KECAMATAN SAJA
# ===============================

df = df[
    df["LEVEL"] == "KECAMATAN"
].copy()



print("\nDATA KECAMATAN")
print(df.head())



print("\nUKURAN DATA")
print(df.shape)



print("\nINFORMASI DATA")
df.info()



print("\nNAMA KOLOM")
print(df.columns.tolist())



print("\nMISSING VALUE")
print(df.isnull().sum())



print("\nSTATISTIK DESKRIPTIF")

print(
    df[
        [
            "LAKI-LAKI",
            "PEREMPUAN",
            "TOTAL"
        ]
    ].describe()
)



print("\nJUMLAH KECAMATAN")

print(
    df["KECAMATAN"].nunique()
)



print("\nTOTAL KEPALA KELUARGA")

print(
    df["TOTAL"].sum()
)



print("\nTOTAL LAKI-LAKI")

print(
    df["LAKI-LAKI"].sum()
)



print("\nTOTAL PEREMPUAN")

print(
    df["PEREMPUAN"].sum()
)



print("\nTOP KECAMATAN KK DESIL 1 TERBANYAK")


ranking = (
    df[
        [
            "KECAMATAN",
            "TOTAL"
        ]
    ]
    .sort_values(
        by="TOTAL",
        ascending=False
    )
)


print(ranking)



ranking.to_csv(
    "data/ranking_kecamatan.csv",
    index=False
)



print("\nEDA SELESAI")