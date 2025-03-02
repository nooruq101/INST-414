import pandas as pd
import matplotlib.pyplot as plt
import re

# Load dataset
file_path = "161-topbooks.csv"  
df = pd.read_csv(file_path)

# Drop unnecessary index column
df = df.drop(columns=["Unnamed: 0"])

# Function to extract numeric values from 'Approximate sales'
def extract_sales(value):
    match = re.search(r"(\d+\.?\d*)", str(value))
    return float(match.group(1)) * 1_000_000 if match else None

# Clean 'Approximate sales' column
df["Approximate sales"] = df["Approximate sales"].apply(extract_sales)

# Convert 'First published' to numeric
df["First published"] = pd.to_numeric(df["First published"], errors="coerce")

# Standardize 'Genre' (lowercase, strip spaces)
df["Genre"] = df["Genre"].str.lower().str.strip()

# --- Sales Distribution ---
plt.figure(figsize=(10, 5))
plt.hist(df["Approximate sales"], bins=20, color="blue", alpha=0.7, edgecolor="black")
plt.xlabel("Approximate Sales (millions)")
plt.ylabel("Number of Books")
plt.title("Distribution of Bestseller Sales")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show(block=False)
plt.pause(3)  # Keep open for 3 seconds
plt.close()

# --- Top 10 Bestselling Books ---
top_books = df.nlargest(10, "Approximate sales")

plt.figure(figsize=(12, 6))
plt.barh(top_books["Book"], top_books["Approximate sales"], color="purple", alpha=0.7)
plt.xlabel("Approximate Sales (millions)")
plt.ylabel("Book Title")
plt.title("Top 10 Bestselling Books")
plt.gca().invert_yaxis()  # Invert to show highest at the top
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show(block=False)
plt.pause(3)
plt.close()

# Drop rows with missing genres
df_genre = df.dropna(subset=["Genre"])

# Extract the primary genre (taking the first genre if multiple are listed)
df_genre["Primary Genre"] = df_genre["Genre"].apply(lambda x: x.split(",")[0] if "," in x else x)

# Aggregate book counts by genre and decade
df_genre["Decade"] = (df_genre["First published"] // 10) * 10
genre_trends = df_genre.groupby(["Decade", "Primary Genre"]).size().unstack().fillna(0)

# --- Genre Trends Over Time ---
plt.figure(figsize=(12, 6))
for genre in genre_trends.columns:
    plt.plot(genre_trends.index, genre_trends[genre], marker="o", linestyle="-", label=genre)

plt.xlabel("Decade")
plt.ylabel("Number of Bestsellers")
plt.title("Genre Popularity Over Time")
plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show(block=False)
plt.pause(3)
plt.close()

