import pandas as pd
import plotly.express as px
import os


folder = "hasil_cluster"


files = [
    "hasil_cluster_desil1.csv",
    "hasil_cluster_desil2.csv",
    "hasil_cluster_desil3.csv",
    "hasil_cluster_desil4.csv",
    "hasil_cluster_desil5.csv",
    "hasil_cluster_sanitasi.csv",
    "hasil_cluster_rtlh.csv"
]


for file in files:

    df = pd.read_csv(
        os.path.join(folder,file)
    )


    fig = px.bar(
        df,
        x="KECAMATAN",
        y="TOTAL",
        color="KATEGORI",
        title=file.replace(".csv","")
    )


    fig.update_layout(
        xaxis_tickangle=-45
    )


    fig.show()