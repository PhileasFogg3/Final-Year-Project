import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("spawn_log.csv", names=["time", "phase"])

# Optional: convert to hours
df["time_hours"] = df["time"] / 3600

# Plot total spawns over time
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x="time_hours", bins=100, hue="phase", element="step", common_norm=False)
plt.title("Aircraft Spawns Over Time (By Phase)")
plt.xlabel("Time (hours)")
plt.ylabel("Spawns per bin")
plt.grid(True)
plt.tight_layout()
plt.show()
