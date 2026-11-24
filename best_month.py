"""Find the best month to visit each National Park.
"Best" is defined as the QUIETEST USABLE month:
  - A month is "usable" if its average visits are at least 25% of the park's
    peak month. Months below that are treated as closed or inaccessible
    (e.g. snowed in), so they can't win just for being empty.
  - Among the usable months, the best one is the one with the fewest visitors.
"""
import pandas as pd

INPUT_FILE = "national_park_monthly.csv"
OUTPUT_FILE = "best_month_by_park.csv"

# A month needs at least this share of the peak month's visits to count as usable.
USABLE_THRESHOLD = 0.25

# Month number (1-12) -> month name. Index 0 is empty so month 1 is January.
MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def find_month(park_months, visits):
    # Return the month number that has exactly this many average visits.
    matching_rows = park_months[park_months["RecreationVisits"] == visits]
    return matching_rows["Month"].iloc[0]  # iloc[0] = the first row


def find_best_months():
    visits = pd.read_csv(INPUT_FILE)

    # Average each month across all years. This smooths out year-to-year noise.
    seasonal = visits.groupby(["UnitCode", "ParkName", "Month"])["RecreationVisits"].mean()
    seasonal = seasonal.reset_index()

    # Look at one park at a time.
    results = []
    for park_code in seasonal["UnitCode"].unique():
        park = seasonal[seasonal["UnitCode"] == park_code]
        park_name = park["ParkName"].iloc[0]

        # The peak month is the one with the highest average visits.
        peak_visits = park["RecreationVisits"].max()
        peak_month = find_month(park, peak_visits)

        # Keep only the usable months (at least 25% of the peak).
        usable = park[park["RecreationVisits"] >= USABLE_THRESHOLD * peak_visits]

        # The best month is the quietest of the usable months.
        best_visits = usable["RecreationVisits"].min()
        best_month = find_month(usable, best_visits)

        # How much quieter is the best month than the peak?
        percent_quieter = (peak_visits - best_visits) / peak_visits * 100

        results.append({
            "UnitCode": park_code,
            "ParkName": park_name,
            "PeakMonth": MONTH_NAMES[peak_month],
            "PeakAvgVisits": round(peak_visits),
            "BestMonth": MONTH_NAMES[best_month],
            "BestAvgVisits": round(best_visits),
            "PercentQuieterThanPeak": round(percent_quieter, 1),
            "UsableMonths": len(usable),
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    best_months = find_best_months()
    best_months.to_csv(OUTPUT_FILE, index=False)

    print("Saved", len(best_months), "parks to", OUTPUT_FILE)
    print("\nHow often each month is the best month:")
    print(best_months["BestMonth"].value_counts().to_string())
    print("\nParks with the fewest usable months (most seasonal):")
    most_seasonal = best_months.sort_values("UsableMonths").head(8)
    print(most_seasonal[["ParkName", "PeakMonth", "BestMonth", "UsableMonths"]].to_string(index=False))
