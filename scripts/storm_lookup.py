import pandas as pd

CSV_PATH = "data/raw/ibtracs.NI.list.v04r01.csv"
NAME = "FANI"
SEASON = "2019"

COLUMNS = [
    "SID", "SEASON", "NAME", "ISO_TIME", "LAT", "LON",
    "WMO_WIND", "WMO_PRES", "TRACK_TYPE", "IFLAG",
]

df = pd.read_csv(
    CSV_PATH,
    usecols=COLUMNS,
    skiprows=[1],
    dtype=str,
    keep_default_na=False,
)

storm = df[(df["NAME"] == NAME) & (df["SEASON"] == SEASON)]

print("Storm IDs found:", list(storm["SID"].unique()))
print("Observations:", len(storm))
print("First time:", storm["ISO_TIME"].min())
print("Last time:", storm["ISO_TIME"].max())

wind = pd.to_numeric(storm["WMO_WIND"], errors="coerce")
pres = pd.to_numeric(storm["WMO_PRES"], errors="coerce")
print("Max wind (kt):", wind.max())
print("Min pressure (mb):", pres.min())

print()
print(storm[["ISO_TIME", "LAT", "LON", "WMO_WIND", "WMO_PRES", "TRACK_TYPE", "IFLAG"]].head(5).to_string())
print("...")
print(storm[["ISO_TIME", "LAT", "LON", "WMO_WIND", "WMO_PRES", "TRACK_TYPE", "IFLAG"]].tail(5).to_string())

window = storm[storm["ISO_TIME"].between("2019-05-02 06:00:00", "2019-05-03 09:00:00")]
print()
print("Peak and landfall window:")
print(window[["ISO_TIME", "LAT", "LON", "WMO_WIND", "WMO_PRES", "IFLAG"]].to_string())