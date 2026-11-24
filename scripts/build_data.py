import json
from pathlib import Path

import pandas as pd

CSV_PATH = "data/raw/ibtracs.NI.list.v04r01.csv"
OUTPUT_DIR = Path("public/data")

COLUMNS = [
    "SID", "SEASON", "NAME", "ISO_TIME", "LAT", "LON",
    "WMO_WIND", "WMO_PRES", "TRACK_TYPE", "IFLAG",
]


def to_number(text):
    """Turn text from the CSV into a number, or None if it is blank."""
    text = text.strip()
    if text == "":
        return None
    return float(text)


def is_recorded(iflag):
    """True if at least one agency reported this row as an original ('O')."""
    return "O" in iflag


def make_point(row):
    """Build one track point (a dictionary) from one CSV row."""
    return {
        "time": row["ISO_TIME"],
        "lat": to_number(row["LAT"]),
        "lon": to_number(row["LON"]),
        "windKt": to_number(row["WMO_WIND"]),
        "pressureMb": to_number(row["WMO_PRES"]),
        "recorded": is_recorded(row["IFLAG"]),
    }


def build_storm(rows):
    """Turn all rows of ONE storm into (index entry, list of track points)."""
    rows = rows.sort_values("ISO_TIME")
    points = [make_point(row) for _, row in rows.iterrows()]

    winds = [p["windKt"] for p in points if p["windKt"] is not None]
    pressures = [p["pressureMb"] for p in points if p["pressureMb"] is not None]
    first = rows.iloc[0]

    entry = {
        "id": first["SID"],
        "name": first["NAME"],
        "season": int(first["SEASON"]),
        "startTime": points[0]["time"],
        "endTime": points[-1]["time"],
        "startLat": points[0]["lat"],
        "startLon": points[0]["lon"],
        "maxWindKt": max(winds) if winds else None,
        "minPressureMb": min(pressures) if pressures else None,
        "trackType": first["TRACK_TYPE"],
    }
    return entry, points


def write_json(path, data):
    """Save data as a JSON file, creating folders if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_rows():
    """Read the raw CSV. Everything is kept as text for now."""
    return pd.read_csv(
        CSV_PATH,
        usecols=COLUMNS,
        skiprows=[1],
        dtype=str,
        keep_default_na=False,
    )


if __name__ == "__main__":
    df = load_rows()
    fani_rows = df[(df["NAME"] == "FANI") & (df["SEASON"] == "2019")]

    entry, points = build_storm(fani_rows)

    write_json(OUTPUT_DIR / "tracks" / (entry["id"] + ".json"), points)
    write_json(OUTPUT_DIR / "cyclones.json", [entry])

    print("Index entry:")
    print(entry)
    print("Track points written:", len(points))