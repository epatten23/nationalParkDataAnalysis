# Find which National Parks have grown or declined in popularity.
#   1. Add up each park's visits for every year.
#   2. Average each park's FIRST three years and its LAST three years.
#   3. Measure the absolute and relative change
# Only complete years (all 12 months have data) are used.


import pandas as pd

INPUT_FILE = "national_park_monthly.csv"
TRENDS_FILE = "park_trends.csv"
TOTALS_FILE = "annual_totals.csv"

# How many years go into the "start" and "end" averages.
WINDOW_YEARS = 3


def years_to_text(years):
    # Turn a list of years like into the text"
    text = ""
    for year in years:
        if text != "":
            text = text + ", "
        text = text + str(year)
    return text


def get_yearly_visits():
    #  Return the total visits for each park in each year (complete years only)."""
    visits = pd.read_csv(INPUT_FILE)

    # Mark each row as True if it has a visit count, False if it is missing.
    visits["MonthsWithData"] = visits["RecreationVisits"].notna()

    # Add up the visits and count the months for each park and year.
    yearly = visits.groupby(["UnitCode", "ParkName", "Year"])[["RecreationVisits", "MonthsWithData"]].sum()
    yearly = yearly.reset_index()
    yearly = yearly.rename(columns={"RecreationVisits": "TotalVisits"})

    # Keep only the years where all 12 months have data.
    yearly = yearly[yearly["MonthsWithData"] == 12]
    return yearly


def measure_park_trends(yearly):
    # Compare each park's first three years with its last three years.
    results = []

    for park_code in yearly["UnitCode"].unique():
        # Get just this park's years, in order from oldest to newest.
        park = yearly[yearly["UnitCode"] == park_code]
        park = park.sort_values("Year")
        park_name = park["ParkName"].iloc[0]

        # Each park uses its OWN first and last year, so set those
        first_years = park.head(WINDOW_YEARS)  # first 3 rows
        last_years = park.tail(WINDOW_YEARS)   # last 3 rows

        # Average yearly visits
        start_average = first_years["TotalVisits"].mean()
        end_average = last_years["TotalVisits"].mean()

        # Absolute change = how many visits per year were gained or lost.
        absolute_change = end_average - start_average

        # Relative change = that same change as a percent of where the park started.
        percent_change = absolute_change / start_average * 100

        results.append({
            "UnitCode": park_code,
            "ParkName": park_name,
            "StartYears": years_to_text(first_years["Year"]),
            "EndYears": years_to_text(last_years["Year"]),
            "StartAvgVisits": round(start_average),
            "EndAvgVisits": round(end_average),
            "AbsoluteChange": round(absolute_change),
            "PercentChange": round(percent_change, 1),
        })

    return pd.DataFrame(results)


def print_top_five(trends, column, title, smallest_first):
    # Print the top 5 parks for both biggest gains and biggest losses
    print("\n" + title)
    sorted_trends = trends.sort_values(column, ascending=smallest_first)
    top_five = sorted_trends.head(5)
    print(top_five[["ParkName", "StartAvgVisits", "EndAvgVisits", column]].to_string(index=False))


if __name__ == "__main__":
    yearly = get_yearly_visits()

    # Trend for each park.
    trends = measure_park_trends(yearly)
    trends.to_csv(TRENDS_FILE, index=False)

    # Total across all parks for each year (this shows the 2020 drop).
    totals = yearly.groupby("Year")["TotalVisits"].sum()
    totals = totals.reset_index()
    totals.to_csv(TOTALS_FILE, index=False)

    print("Saved", len(trends), "parks to", TRENDS_FILE, "and", len(totals), "years to", TOTALS_FILE)

    growing = len(trends[trends["AbsoluteChange"] > 0])
    declining = len(trends[trends["AbsoluteChange"] < 0])
    print("Parks growing:", growing, " Parks declining:", declining)

    # Biggest gains and losses in visits per year.
    print_top_five(trends, "AbsoluteChange", "Biggest absolute GAINS (visits per year):", smallest_first=False)
    print_top_five(trends, "AbsoluteChange", "Biggest absolute LOSSES (visits per year):", smallest_first=True)

    # Fastest growth and decline in percent.
    print_top_five(trends, "PercentChange", "Fastest relative GROWTH (%):", smallest_first=False)
    print_top_five(trends, "PercentChange", "Fastest relative DECLINE (%):", smallest_first=True)
