import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# ==========================
# KONFIGURASI
# ==========================

folder_input = "hasil_clean"
folder_output = "hasil_cluster"

os.makedirs(folder_output, exist_ok=True)


# K terbaik dari hasil evaluasi

dataset_cluster = {

    "desil1_clean.csv": 3,

    "desil2_clean.csv": 2,

    "desil3_clean.csv": 2,

    "desil4_clean.csv": 2,

    "desil5_clean.csv": 2,

    "sanitasi_clean.csv": 2,

    "rtlh_clean.csv": 2
}



# ==========================
# PROSES CLUSTERING
# ==========================

for file, k in dataset_cluster.items():

    print("\n==============================")
    print("Clustering:", file)
    print("Jumlah cluster:", k)


    # membaca data

    df = pd.read_csv(
        os.path.join(folder_input, file)
    )


    # fitur

    X = df[["TOTAL"]]


    # standardisasi

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # K-Means

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )


    df["CLUSTER"] = model.fit_predict(
        X_scaled
    )


    # ==========================
    # URUTKAN CLUSTER BERDASARKAN NILAI TOTAL
    # ==========================

    rata_cluster = (
        df.groupby("CLUSTER")["TOTAL"]
        .mean()
        .sort_values()
    )


    label_cluster = {}

    for nomor, cluster in enumerate(rata_cluster.index):

        if nomor == 0:
            label_cluster[cluster] = "Rendah"

        elif nomor == len(rata_cluster)-1:
            label_cluster[cluster] = "Tinggi"

        else:
            label_cluster[cluster] = "Sedang"



    df["KATEGORI"] = (
        df["CLUSTER"]
        .map(label_cluster)
    )


    # simpan hasil

    nama_output = (
        file
        .replace("_clean.csv","")
    )


    output = (
        folder_output
        + "/hasil_cluster_"
        + nama_output
        + ".csv"
    )


    df.to_csv(
        output,
        index=False
    )


    print("Berhasil:", output)

    print(df.head())


print("\nSEMUA CLUSTER SELESAI")