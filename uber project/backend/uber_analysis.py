"""
Uber Ride Data Analysis & EDA Project
====================================
End-to-end data analysis for the complete Uber dataset (1,155 rides).
Generates summary statistics and saves visualization plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "UberDataset (1).csv") if os.path.exists(os.path.join(BASE_DIR, "UberDataset (1).csv")) else "UberDataset (1).csv"

print("=" * 60)
print("1. LOADING THE COMPLETE DATASET")
print("=" * 60)
df = pd.read_csv(dataset_path)
print(f"Total raw rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Drop the summary row ("Totals") at the bottom of the dataset
df = df[df["START_DATE"] != "Totals"].copy()
print(f"Valid ride rows (excluding 'Totals'): {len(df)}")

print("\n" + "=" * 60)
print("2. DATA CLEANING & PREPROCESSING")
print("=" * 60)
# Handle missing PURPOSE values
df["PURPOSE"] = df["PURPOSE"].fillna("Not Specified")

# Parse mixed format datetime strings
df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="mixed", errors="coerce")
df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="mixed", errors="coerce")

# Drop any unparseable dates and drop duplicate rides
df = df.dropna(subset=["START_DATE", "END_DATE"]).drop_duplicates()
print(f"Total clean, unique ride records: {len(df)}")

print("\n" + "=" * 60)
print("3. FEATURE ENGINEERING")
print("=" * 60)
# Extract time features
df["HOUR"] = df["START_DATE"].dt.hour
df["DAY"] = df["START_DATE"].dt.day_name()
df["MONTH"] = df["START_DATE"].dt.month_name()
df["DURATION_MINS"] = (df["END_DATE"] - df["START_DATE"]).dt.total_seconds() / 60

# Categorize time of day
df["TIME_OF_DAY"] = pd.cut(
    df["HOUR"],
    bins=[-1, 10, 15, 19, 24],
    labels=["Morning", "Afternoon", "Evening", "Night"]
)

print("New columns created: HOUR, DAY, MONTH, DURATION_MINS, TIME_OF_DAY")

print("\n" + "=" * 60)
print("4. KEY METRICS & BREAKDOWNS")
print("=" * 60)
print("\n--- CATEGORY BREAKDOWN ---")
cat_counts = df["CATEGORY"].value_counts()
for cat, count in cat_counts.items():
    print(f"  {cat}: {count} ({count/len(df)*100:.1f}%)")

print("\n--- TOP PURPOSES ---")
purpose_counts = df["PURPOSE"].value_counts().head(7)
for purp, count in purpose_counts.items():
    print(f"  {purp}: {count}")

print("\n--- TIME OF DAY DISTRIBUTION ---")
time_counts = df["TIME_OF_DAY"].value_counts()
for period, count in time_counts.items():
    print(f"  {period}: {count} ({count/len(df)*100:.1f}%)")

print("\n--- TRIP DISTANCE (MILES) SUMMARY ---")
print(f"  Shortest trip: {df['MILES'].min()} miles")
print(f"  Average trip : {df['MILES'].mean():.2f} miles")
print(f"  Median trip  : {df['MILES'].median()} miles")
print(f"  Longest trip : {df['MILES'].max()} miles")

print("\n--- TRIP DURATION (MINUTES) SUMMARY ---")
print(f"  Average duration: {df['DURATION_MINS'].mean():.1f} minutes")
print(f"  Median duration : {df['DURATION_MINS'].median():.1f} minutes")

print("\n" + "=" * 60)
print("5. GENERATING VISUAL CHARTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Ride Category & Time of Day
sns.countplot(data=df, x="TIME_OF_DAY", hue="CATEGORY", palette="Set2", ax=axes[0, 0])
axes[0, 0].set_title("Rides by Time of Day & Category", fontsize=14, fontweight="bold")
axes[0, 0].set_xlabel("Time of Day")
axes[0, 0].set_ylabel("Total Rides")

# 2. Rides by Day of the Week
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sns.countplot(data=df, x="DAY", order=day_order, hue="DAY", legend=False, palette="Blues_d", ax=axes[0, 1])
axes[0, 1].set_title("Rides by Day of Week", fontsize=14, fontweight="bold")
axes[0, 1].set_xlabel("Day of Week")
axes[0, 1].set_ylabel("Total Rides")
axes[0, 1].tick_params(axis="x", rotation=30)

# 3. Purpose Distribution
sns.countplot(data=df, y="PURPOSE", order=df["PURPOSE"].value_counts().index, hue="PURPOSE", legend=False, palette="mako", ax=axes[1, 0])
axes[1, 0].set_title("Ride Purposes Breakdown", fontsize=14, fontweight="bold")
axes[1, 0].set_xlabel("Number of Rides")
axes[1, 0].set_ylabel("Purpose")

# 4. Trip Distance Distribution (trips < 40 miles)
sns.histplot(df[df["MILES"] < 40]["MILES"], bins=25, kde=True, color="teal", ax=axes[1, 1])
axes[1, 1].set_title("Distribution of Trip Miles (< 40 miles)", fontsize=14, fontweight="bold")
axes[1, 1].set_xlabel("Miles")
axes[1, 1].set_ylabel("Ride Count")

plt.tight_layout()
chart_path = os.path.join(BASE_DIR, "uber_analysis_charts.png")
plt.savefig(chart_path, dpi=200)
print(f"Saved complete EDA charts to: {chart_path}")
print("=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)
