import pandas as pd
from kd_tree import build_kdtree, nearest_neighbor, range_search

df = pd.read_csv("ahmedabad_facilities.csv")

points = list(zip(df["lat"], df["lon"], df["name"], df["category"]))

tree = build_kdtree(points)

print("KD Tree built successfully!")