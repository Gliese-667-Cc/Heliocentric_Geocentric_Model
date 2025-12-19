import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Realistic orbital data
planet_data = [
    {"name": "Mercury", "color": "gray",   "radius_au": 0.39, "period_days": 35.2},
    {"name": "Venus",   "color": "orange", "radius_au": 0.72, "period_days": 90},
    {"name": "Earth",   "color": "tab:cyan",   "radius_au": 1.00, "period_days": 146},
    {"name": "Mars",    "color": "red",    "radius_au": 1.52, "period_days": 274.8},
]

# Scale factor to fit orbits nicely in plot
scale = 1.7  # max 1.52 AU * 1.7 ~ 2.6 units radius
for planet in planet_data:
    planet["radius"] = planet["radius_au"] * scale
    planet["omega"] = 2 * np.pi / planet["period_days"]  # rad/day
    # planet["nm"] = planet["name"]

# Animation config
fps = 24
duration_sec = 15
frames = fps * duration_sec
trail_length = 27 # trail history in frames

# Set up plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.axis("off")

background = plt.Rectangle((-4, -4), 8, 8, color='black', zorder=0)
ax.add_patch(background)
ax.add_patch(plt.Rectangle((-0.558/2, -2.7), 0.5882, 0.01, color='white', zorder=0))
plt.text(0.0, -2.85, "Scale: 1 unit = 0.5882 AU", color='white', fontsize=6, ha='center', va='center', fontweight='bold')
# Plot the Sun
sun = plt.Circle((0, 0), 0.1, color='yellow')
ax.add_patch(sun)

plt.text(0.0, 0.2, "Sun", color='yellow', fontsize=6, ha='center', va='center', fontweight='bold')
plt.text(0.0, 2.8, "Heliocentric Model", color='white', fontsize=12, ha='center', va='center', fontweight='bold')


# Initialize planet markers and trail lines
for planet in planet_data:
    planet["body"] = plt.Circle((0, 0), 0.05, color=planet["color"])
    planet["trail"], = ax.plot([], [], color=planet["color"], alpha=0.4, lw=1)
    planet["label"] = ax.text(0, 0, planet["name"], color=planet["color"], fontsize=6, ha='center', va='center')
    planet["history_x"] = []
    planet["history_y"] = []
    ax.add_patch(planet["body"])

# Update function
def update(frame):
    for planet in planet_data:
        angle = planet["omega"] * frame
        x = planet["radius"] * np.cos(angle)
        y = planet["radius"] * np.sin(angle)
        
        
        # Update history
        planet["history_x"].append(x)
        planet["history_y"].append(y)
        
        if len(planet["history_x"]) > trail_length:
            planet["history_x"].pop(0)
            planet["history_y"].pop(0)

        # Update plot objects
        planet["body"].set_center((x, y))
        planet["trail"].set_data(planet["history_x"], planet["history_y"])
        planet["label"].set_position((x, y + 0.2))
    return [p["body"] for p in planet_data] + [p["trail"] for p in planet_data] + [p["label"] for p in planet_data]

# Animate and save
ani = FuncAnimation(fig, update, frames=frames, blit=True)

ani.save("realistic_heliocentric_model.gif", writer=PillowWriter(fps=fps))


