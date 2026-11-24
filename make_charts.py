# Create the three charts for the analysis and save them as PNG files.

import matplotlib.pyplot as plt
import pandas as pd

# The parks shown in the seasonal chart
SEASONAL_PARKS = {
    "YELL": "Yellowstone",
    "ROMO": "Rocky Mountain",
    "GRTE": "Grand Teton",
    "YOSE": "Yosemite",
    "DEVA": "Death Valley",
    "ARCH": "Arches",
}

# Month labels
MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# How many parks to show on percent chart
TOP_N = 10

# Make all the text readable.
plt.rcParams.update({"font.size": 12, "axes.titlesize": 14})


def make_seasonal_chart():
    visits = pd.read_csv("national_park_monthly.csv")

    plt.figure(figsize=(10, 6))

    # Draw one line for each park.
    for park_code in SEASONAL_PARKS:
        park = visits[visits["UnitCode"] == park_code]

        # Average each month
        monthly_average = park.groupby("Month")["RecreationVisits"].mean()

        # Divide by 1000 so the y-axis is in thousands of visits.
        plt.plot(monthly_average.index, monthly_average / 1000,
                 marker="o", linewidth=2, label=SEASONAL_PARKS[park_code])

    plt.xticks(range(1, 13), MONTH_LABELS)  # put month names under the numbers 1-12
    plt.xlabel("Month")
    plt.ylabel("Average recreation visits (thousands)")
    plt.title("Mountain parks surge in summer; Death Valley and Arches stay steady")
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig("seasonal_visits.png", dpi=150)
    plt.close()


def make_percent_change_chart():
    trends = pd.read_csv("park_trends.csv")

    # Sort from the biggest decline to the biggest growth.
    trends = trends.sort_values("PercentChange")

    # Take the parks with the biggest declines and the biggest growth
    biggest_declines = trends.head(TOP_N)
    biggest_growth = trends.tail(TOP_N)
    shown = pd.concat([biggest_declines, biggest_growth])

    # Pick a colors - red is decline and green is growth
    colors = []
    for change in shown["PercentChange"]:
        if change > 0:
            colors.append("green")
        else:
            colors.append("red")

    # Shorten the names so they fit
    names = []
    for name in shown["ParkName"]:
        names.append(name.replace(" National Park", ""))

    plt.figure(figsize=(10, 8))
    plt.barh(names, shown["PercentChange"], color=colors)  # horizontal bar
    plt.axvline(0, color="black", linewidth=1)  
    plt.xlabel("Change in yearly visits, first 3 years vs last 3 years (%)")
    plt.title("A few parks grew over 400%, while most others changed modestly")
    plt.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig("percent_change.png", dpi=150)
    plt.close()

if __name__ == "__main__":
    make_seasonal_chart()
    make_percent_change_chart()
    print("Saved seasonal_visits.png, percent_change.png, and annual_totals.png")
