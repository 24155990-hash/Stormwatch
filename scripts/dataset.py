import pandas as pd
csv_path="data/raw/ibtracs.NI.list.v04r01.csv"
columns=["SID","SEASON","NAME","ISO_TIME","NATURE","LAT","LON","WMO_WIND",
         "WMO_PRES","WMO_AGENCY","TRACK_TYPE","IFLAG"]
df=pd.read_csv(csv_path,usecols=columns,skiprows=[1],dtype=str,keep_default_na=False,)
print("Rows (observations):", len(df))
print("Distinct storms (SID):", df["SID"].nunique())
print("Season range:", df["SEASON"].min(), "to", df["SEASON"].max())
print()
print("TRACK_TYPE counts:")
print(df["TRACK_TYPE"].value_counts())

prov = df[df["TRACK_TYPE"].isin(["PROVISIONAL", "US-PROVISIONAL", "spur-merge"])]
main_sids = set(df.loc[df["TRACK_TYPE"] == "main", "SID"])

for track_type, group in prov.groupby("TRACK_TYPE"):
    sids = set(group["SID"])
    print(track_type)
    print("  rows:", len(group))
    print("  storms:", len(sids))
    print("  storms that ALSO have main rows:", len(sids & main_sids))
    print("  seasons:", sorted(group["SEASON"].unique()))
    print()

    spur = df[df["TRACK_TYPE"] == "spur-merge"]
spur_summary = spur.groupby("SID").agg(
    name=("NAME", "first"),
    season=("SEASON", "first"),
    start=("ISO_TIME", "min"),
    end=("ISO_TIME", "max"),
    rows=("SID", "size"),
)
print("spur-merge storms:")
print(spur_summary.to_string())

main_rows = df[df["TRACK_TYPE"] == "main"]
main_rows = main_rows.assign(decade=(main_rows["SEASON"].astype(int) // 10) * 10)
has_wind = main_rows["WMO_WIND"].str.strip() != ""

summary = pd.DataFrame({
    "storms": main_rows.groupby("decade")["SID"].nunique(),
    "rows": main_rows.groupby("decade").size(),
    "pct_with_wind": (has_wind.groupby(main_rows["decade"]).mean() * 100).round(1),
})
print()
print("Completeness by decade (main rows only):")
print(summary.to_string())