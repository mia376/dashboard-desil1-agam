import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import matplotlib.pyplot as plt


# ==========================
# KONFIGURASI
# ==========================

folder = "hasil_clean"

folder_output = "hasil_evaluasi"

os.makedirs(folder_output, exist_ok=True)


files = [
    "desil1_clean.csv",
    "desil2_clean.csv",
    "desil3_clean.csv",
    "desil4_clean.csv",
    "desil5_clean.csv",
    "sanitasi_clean.csv",
    "rtlh_clean.csv"
]


# menyimpan semua hasil
semua_hasil = []


# ==========================
# PROSES EVALUASI
# ==========================

for file in files:

    print("\n==============================")
    print("Evaluasi:", file)


    # membaca data
    df = pd.read_csv(
        os.path.join(folder, file)
    )


    # fitur clustering
    X = df[["TOTAL"]]


    # standardisasi
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    hasil = []


    # mencoba K = 2 sampai 5
    for k in range(2, 6):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )


        label = model.fit_predict(
            X_scaled
        )


        score = silhouette_score(
            X_scaled,
            label
        )


        hasil.append(
            [k, score]
        )


        semua_hasil.append(
            [
                file,
                k,
                score
            ]
        )


        print(
            "K =",
            k,
            "Silhouette =",
            round(score, 3)
        )


    # dataframe hasil
    hasil_df = pd.DataFrame(
        hasil,
        columns=[
            "K",
            "Silhouette"
        ]
    )


    # simpan grafik
    plt.figure(figsize=(6,4))

    plt.plot(
        hasil_df["K"],
        hasil_df["Silhouette"],
        marker="o"
    )


    plt.title(
        "Evaluasi " + file
    )


    plt.xlabel(
        "Jumlah Cluster (K)"
    )


    plt.ylabel(
        "Silhouette Score"
    )


    plt.grid()


    plt.savefig(
        f"{folder_output}/grafik_{file.replace('.csv','.png')}",
        bbox_inches="tight"
    )


    plt.close()



# ==========================
# SIMPAN HASIL AKHIR
# ==========================

df_hasil = pd.DataFrame(
    semua_hasil,
    columns=[
        "Dataset",
        "K",
        "Silhouette"
    ]
)


df_hasil.to_csv(
    f"{folder_output}/hasil_evaluasi_cluster.csv",
    index=False
)


print("\n==============================")
print("SEMUA EVALUASI SELESAI")

print("\nHasil tersimpan:")
print("hasil_evaluasi/hasil_evaluasi_cluster.csv")