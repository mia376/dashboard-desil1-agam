import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(
    "data/desil1_clean.csv"
)


# ==========================
# AMBIL DATA KECAMATAN
# ==========================

df_kecamatan = df[
    df["LEVEL"] == "KECAMATAN"
].copy()


print("Jumlah Kecamatan:")
print(df_kecamatan.shape)



# ==========================
# FITUR CLUSTER
# ==========================

X = df_kecamatan[
    [
        "LAKI-LAKI",
        "PEREMPUAN",
        "TOTAL"
    ]
]



# ==========================
# NORMALISASI
# ==========================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)



# ==========================
# K-MEANS
# ==========================

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)


df_kecamatan["CLUSTER"] = (
    kmeans.fit_predict(X_scaled)
)



# ==========================
# EVALUASI
# ==========================

score = silhouette_score(
    X_scaled,
    df_kecamatan["CLUSTER"]
)


print(
    "\nSilhouette Score:",
    round(score,3)
)



# ==========================
# HASIL
# ==========================

print(
    "\nHASIL CLUSTER"
)

print(
    df_kecamatan[
        [
            "KECAMATAN",
            "TOTAL",
            "CLUSTER"
        ]
    ]
)



# simpan

df_kecamatan.to_csv(
    "data/hasil_cluster.csv",
    index=False
)


print(
    "\nFile tersimpan: data/hasil_cluster.csv"
)