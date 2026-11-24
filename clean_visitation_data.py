# Clean the raw NPS data down to monthly National Park visits.

import pandas as pd

DATA_FILE = "Main_Data.csv"
PARKS_FILE = "national_parks.csv"
OUTPUT_FILE = "national_park_monthly.csv"


def clean_visitation_data():
    # Load files.
    data = pd.read_csv(DATA_FILE)
    parks = pd.read_csv(PARKS_FILE)

    # Keep only recreation visits (TRV)
    visits = data[data["Statistic"] == "TRV"]
    visits = visits[["UnitCode", "Year", "Month", "Value"]]
    visits = visits.rename(columns={"Value": "RecreationVisits"})

    # A visit count can't be negative, so we'll treat those as missing (NaN).
    visits["RecreationVisits"] = visits["RecreationVisits"].where(
        visits["RecreationVisits"] >= 0
    )

    # Keep only National Parks and attach their names. --get rid of state and memorial parks
    visits = visits.merge(
        parks[["UnitCode", "ParkName", "States", "ParkCode"]],
        on="UnitCode",
        how="inner",
    )

    # Sort so the output is readable.
    visits = visits.sort_values(["ParkName", "Year", "Month"])

    # Make sure each park-year-month appears only once.
    if visits.duplicated(subset=["UnitCode", "Year", "Month"]).any():
        raise ValueError("Found duplicate UnitCode/Year/Month rows")

    return visits


if __name__ == "__main__":
    cleaned = clean_visitation_data()
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(cleaned):,} rows for {cleaned['UnitCode'].nunique()} parks to {OUTPUT_FILE}")
