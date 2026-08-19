import pandas as pd

df = pd.read_csv("data/desil1_clean.csv")

print(
    df[
        df["KECAMATAN"].isin(
            [
                "LUBUK BASUNG",
                "TANJUNG RAYA",
                "IV KOTO",
                "PALEMBAYAN"
            ]
        )
    ]
)