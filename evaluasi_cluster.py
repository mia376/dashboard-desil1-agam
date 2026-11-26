import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

# 1. BACA SEMUA FILE, LALU GABUNGKAN JADI SATU (bukan diproses terpisah)
files = {
    'Desil1': 'desil1_clean.csv',
    'Desil2': 'desil2_clean.csv',
    'Desil3': 'desil3_clean.csv',
    'Desil4': 'desil4_clean.csv',
    'Desil5': 'desil5_clean.csv',
    'RTLH': 'rtlh_clean.csv',
    'Sanitasi': 'sanitasi_clean.csv',
}

merged = None
for var_name, filename in files.items():
    df = pd.read_csv(filename)
    # asumsi tiap csv punya kolom 'kode_nagari' dan 'total'
    # sesuaikan nama kolom dengan csv kamu
    df = df.rename(columns={'total': var_name})
    df = df[['kode_nagari', var_name]]
    if merged is None:
        merged = df
    else:
        merged = merged.merge(df, on='kode_nagari', how='outer')

print("Jumlah baris setelah digabung:", merged.shape[0])  # harus 92
print("Jumlah kolom:", merged.shape[1])  # harus 8 (1 kode + 7 variabel)

# 2. STANDARISASI SEMUA VARIABEL SEKALIGUS
features = ['Desil1','Desil2','Desil3','Desil4','Desil5','RTLH','Sanitasi']
X = merged[features].values
X_scaled = StandardScaler().fit_transform(X)

# 3. JALANKAN K-MEANS SATU KALI PER NILAI K (bukan per file)
print(f"\n{'K':<4}{'DBI':<10}{'Silhouette':<12}{'Min Cluster Size'}")
for k in range(2, 6):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    dbi = davies_bouldin_score(X_scaled, labels)
    sil = silhouette_score(X_scaled, labels)
    min_size = pd.Series(labels).value_counts().min()
    print(f"{k:<4}{dbi:<10.4f}{sil:<12.4f}{min_size}")