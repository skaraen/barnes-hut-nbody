# N-Body simulation using Barnes-Hut
[Project report (PDF)](report.pdf)
[Class presentation (PDF)](Presentation.pdf)

Simulation of an N-body system on GPUs with both brute-force and Barnes–Hut kernels. Includes Midway3 cluster run instructions, local build/run steps, benchmark recordings, and a summarized report.

## Prerequisites
- NVIDIA GPU with CUDA support
- CUDA Toolkit installed (`nvcc` on `PATH`)
- Python 3 with `numpy`, `matplotlib`, and `ffmpeg` available for writing videos

## Build
Use the provided script or call `nvcc` directly:

```bash
# Build and run brute-force
# ./script.sh

# Manual compilation (brute-force)
nvcc nbody.cu -o nbody -O3

# Manual compilation (Barnes–Hut)
nvcc nbody_bh.cu -o nbody_bh -O3
```

## Running on Midway3 (GPU cluster)
Request a GPU allocation (example uses one GPU for 1 hour), then load CUDA:
```bash
srun --nodes=1 --time=01:00:00 --account=<account_name> --partition=gpu --gres=gpu:1 --ntasks-per-node=1 --cpus-per-task=1 --constraint=<gpu_type> --pty zsh
module load cuda
```

Build and run on the cluster:
```bash
# Brute force
nvcc -O3 nbody.cu -o nbody
./nbody <number of particles>

# Barnes–Hut
nvcc -O3 nbody_bh.cu -o nbody_bh
./nbody_bh <number of particles> <theta>
```

Visualization on the cluster:
```bash
module load python
module load ffmpeg
python visualize.py
```

## Run (local)
Execute the brute-force binary, optionally passing the number of particles (default `3000`). A 20-second simulation at `dt=0.01` is recorded to `nbody.bin` in the working directory.

```bash
# Default brute-force run
./nbody

# Larger brute-force run
./nbody 10000
```

Execute the Barnes–Hut binary with an optional opening angle `theta` (default `0.5`). Output is written to `nbody_barnes.bin`.

```bash
# Barnes–Hut with defaults (N=3000, theta=0.5)
./nbody_bh

# Barnes–Hut with custom N and theta
./nbody_bh 75000 0.7
```

## Output format
- First 32-bit int: number of particles `N`.
- Second 32-bit int: number of time steps `T`.
- Remaining data: `T` frames of `2 * N` 32-bit floats in row-major order: all `x` positions for the frame, then all `y` positions.

## Visualization
Convert a binary log into an animation with the bundled script:

```bash
python3 visualize.py        # reads nbody.bin and writes nbody.mp4 by default

# To generate a GIF instead
OUTPUT=nbody.gif python3 visualize.py
```

The script performs basic validation and saves either an MP4 (FFmpeg) or GIF (Pillow). Adjust `FILENAME` and `OUTPUT` at the top of the script to point to alternate runs such as `nbody_barnes.bin`.

## Prepared examples and recordings
- Sample `nbody.bin` and `nbody.mp4` (default brute-force configuration) live in the repo root.
- Additional recordings from benchmarking sweeps are under `old/` and `simulations/` (e.g., `simulations/nbody_bh*.mp4` for various `theta` values and `simulations/nbody_brute.mp4` for the brute-force run).

### Direct links to recordings (relative paths)
- Brute-force baseline: `simulations/nbody_brute.mp4`
- Barnes–Hut sweeps: `simulations/nbody_bh1.mp4`, `simulations/nbody_bh2.mp4`, `simulations/nbody_bh3.mp4`, `simulations/nbody_bh4.mp4`
- Legacy clips: `old/nbody.mp4`, `old/nbody_bh_th1.mp4`, `old/nbody_bh_th2.mp4`, `old/nbody_bh_th3.mp4`, `old/nbody_bh_th4.mp4`
- GitHub-hosted recordings: https://github.com/skaraen/barnes-hut-nbody/tree/main/simulations

## Performance summary
Karaen’s sweep shows how the Barnes–Hut opening angle (`theta`) trades accuracy for speed. Times below are average kernel time per step (ms) and total kernel time (s) for 20 simulated seconds at `dt=0.01`.

| Method      | theta | N (particles) | Avg ms/step | Total s |
|-------------|------:|--------------:|------------:|--------:|
| Brute force |   —   |           100 | 0.024 | 0.0479 |
| Brute force |   —   |           500 | 0.085 | 0.1705 |
| Brute force |   —   |          3000 | 0.440 | 0.8801 |
| Brute force |   —   |         15000 | 2.242 | 4.4831 |
| Brute force |   —   |         75000 | 19.223 | 38.4463 |
| Barnes–Hut  |  0.1  |           100 | 0.033 | 0.0661 |
| Barnes–Hut  |  0.1  |           500 | 0.206 | 0.4125 |
| Barnes–Hut  |  0.1  |          3000 | 1.859 | 3.7187 |
| Barnes–Hut  |  0.1  |         15000 | 12.764 | 25.5288 |
| Barnes–Hut  |  0.1  |         75000 | 117.468 | 234.9364 |
| Barnes–Hut  |  0.4  |           100 | 0.040 | 0.0808 |
| Barnes–Hut  |  0.4  |           500 | 0.229 | 0.4575 |
| Barnes–Hut  |  0.4  |          3000 | 0.979 | 1.9576 |
| Barnes–Hut  |  0.4  |         15000 | 2.367 | 4.7338 |
| Barnes–Hut  |  0.4  |         75000 | 15.613 | 31.2253 |
| Barnes–Hut  |  0.7  |           100 | 0.048 | 0.0965 |
| Barnes–Hut  |  0.7  |           500 | 0.175 | 0.3508 |
| Barnes–Hut  |  0.7  |          3000 | 0.588 | 1.1757 |
| Barnes–Hut  |  0.7  |         15000 | 0.891 | 1.7821 |
| Barnes–Hut  |  0.7  |         75000 | 4.801 | 9.6027 |
| Barnes–Hut  |  1.0  |           100 | 0.041 | 0.0825 |
| Barnes–Hut  |  1.0  |           500 | 0.131 | 0.2625 |
| Barnes–Hut  |  1.0  |          3000 | 0.311 | 0.6214 |
| Barnes–Hut  |  1.0  |         15000 | 0.568 | 1.1362 |
| Barnes–Hut  |  1.0  |         75000 | 2.968 | 5.9361 |

## Report summary (key contents)
- **Introduction:** The gravitational $N$-body problem grows as $O(N^2)$; efficient solvers matter for astrophysics, plasma, and interactive education. We target GPU acceleration and Barnes–Hut to scale larger $N$ while keeping physics plausible.
- **Background:** From Newton’s two-body solutions to Poincaré’s chaos in $N\ge3$, modern state-of-the-art uses hierarchical tree codes (Barnes–Hut) and fast multipole methods; GPUs now make these practical at scale.
- **Methodology:** CUDA C++ implementations of brute-force and Barnes–Hut kernels; SoA layout, velocity-Verlet integration ($dt=0.01$), softening $10^{-9}$, binary logging + Python visualization. Barnes–Hut uses a host-built quadtree with GPU traversal controlled by opening angle $\theta$.
- **Results:** Stable orbits for $N$ up to 75k. Barnes–Hut overtakes brute-force beyond a few thousand particles; speedups up to ~6× at $N=75$k for $\theta\approx1.0$ with mild precession, while $\theta\le0.7$ balances speed and fidelity. Figures in the PDF show runtime scaling and speedup curves.
- **Discussion:** Hierarchical methods unlock larger interactive simulations on modest GPUs. Next steps include GPU tree construction, Morton ordering for locality, adaptive timesteps, and 3D octrees. Compared to brute-force, Barnes–Hut offers a better cost/accuracy tradeoff at scale.

## Project structure
- `nbody.cu`: Brute-force CUDA implementation.
- `nbody_bh.cu`: Barnes–Hut CUDA implementation with configurable `theta`.
- `report.tex`, `report.pdf`: LaTeX source and compiled project report.
- `Presentation.pdf`: Slide deck for the class presentation.
- `visualize.py`: Python script to verify and visualize simulation output.
- `old/`, `simulations/`: Benchmark recordings.
- `README.md`: This file.
