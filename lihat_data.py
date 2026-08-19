import pandas as pd


file = r"data/Data Desil 1 Berdasarkan KK.xlsx"


df = pd.read_excel(
    file,
    header=None
)


pd.set_option(
    "display.max_rows",
    None
)

pd.set_option(
    "display.max_columns",
    None
)


print(df.head(30))