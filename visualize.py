#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

FILENAME = "nbody.bin"
OUTPUT   = "nbody.mp4"   # change to "nbody.gif" for GIF

def load_nbody(filename):
    with open(filename, "rb") as f:
        numParticles = np.fromfile(f, dtype=np.int32, count=1)[0]
        numSteps     = np.fromfile(f, dtype=np.int32, count=1)[0]
        data = np.fromfile(f, dtype=np.float32)

    expected = numSteps * 2 * numParticles
    if data.size != expected:
        raise ValueError(f"Expected {expected} floats, got {data.size}")

    frames = data.reshape(numSteps, 2, numParticles)
    x = frames[:, 0, :]
    y = frames[:, 1, :]
    return x, y, numParticles, numSteps

def main():
    x, y, numParticles, numSteps = load_nbody(FILENAME)
    print(f"Loaded {numParticles} particles, {numSteps} steps")

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    margin_x = 0.05 * (xmax - xmin + 1e-6)
    margin_y = 0.05 * (ymax - ymin + 1e-6)

    fig, ax = plt.subplots(figsize=(6, 6))
    scat = ax.scatter([], [], s=5)

    # ax.set_xlim(xmin - margin_x, xmax + margin_x)
    # ax.set_ylim(ymin - margin_y, ymax + margin_y)
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_aspect("equal", "box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    def update(frame):
        pts = np.column_stack((x[frame], y[frame]))
        scat.set_offsets(pts)
        ax.set_title(f"N-body simulation (step {frame+1}/{numSteps})")
        return scat,

    ani = FuncAnimation(
        fig,
        update,
        frames=numSteps,
        interval=30,
        blit=True
    )

    if OUTPUT.endswith(".mp4"):
        writer = FFMpegWriter(fps=30, bitrate=1800)
        ani.save(OUTPUT, writer=writer)
    elif OUTPUT.endswith(".gif"):
        writer = PillowWriter(fps=30)
        ani.save(OUTPUT, writer=writer)
    else:
        raise ValueError("OUTPUT must end in .mp4 or .gif")

    print(f"Saved animation to {OUTPUT}")

if __name__ == "__main__":
    main()
