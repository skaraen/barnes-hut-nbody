# N-Body simulation using Barnes-Hut
Simulation of an N-Body system using the Barnes-Hut algorithm on GPUs

## Running the code

### Manual run
Request a GPU allocation on Midway3 using the `srun` command. We used NVIDIA V100 for our simulations.
```bash
srun --nodes=1 --time=01:00:00 --account=<account_name> --partition=gpu --gres=gpu:1 --ntasks-per-node=1 --cpus-per-task=1 --constraint=<gpu_type> --pty zsh
```

Load the CUDA module to use `nvcc` to compile
```bash
module load cuda
```

**For the Brute force implementation**
```bash
nvcc -O3 nbody.cu -o nbody
./nbody <number of particles>
```

**For the Barnes-Hut implementation**
```bash
nvcc -O3 nbody_bh.cu -o nbody_bh
./nbody_bh <number of particles> <theta>
```

**To visualize the simulation**

Change the name of the binary file to be parsed, output file format and title as required
```bash
module load python
module load ffmpeg
python visualize.py
```

### SLURM run

## Performance Analysis

The increase in theta results in an increase in approximation and therefore results in higher speedup. We can also observe that the benefit of the the approximation is more evident when the number of particles drastically increase. However increasing theta also results in a compromise on accuracy.

| Method      | θ   | N (particles) | Avg Kernel Time / Step (ms) | Total Kernel Time (s) |
|-------------|----:|--------------:|----------------------------:|----------------------:|
| Brute force | —   |           100 | 0.024                       | 0.0479                |
| Brute force | —   |           500 | 0.085                       | 0.1705                |
| Brute force | —   |          3000 | 0.440                       | 0.8801                |
| Brute force | —   |         15000 | 2.242                       | 4.4831                |
| Brute force | —   |         75000 | 19.223                      | 38.4463               |
| Barnes–Hut  | 0.1 |           100 | 0.033                       | 0.0661                |
| Barnes–Hut  | 0.1 |           500 | 0.206                       | 0.4125                |
| Barnes–Hut  | 0.1 |          3000 | 1.859                       | 3.7187                |
| Barnes–Hut  | 0.1 |         15000 | 12.764                      | 25.5288               |
| Barnes–Hut  | 0.1 |         75000 | 117.468                     | 234.9364              |
| Barnes–Hut  | 0.4 |           100 | 0.040                       | 0.0808                |
| Barnes–Hut  | 0.4 |           500 | 0.229                       | 0.4575                |
| Barnes–Hut  | 0.4 |          3000 | 0.979                       | 1.9576                |
| Barnes–Hut  | 0.4 |         15000 | 2.367                       | 4.7338                |
| Barnes–Hut  | 0.4 |         75000 | 15.613                      | 31.2253               |
| Barnes–Hut  | 0.7 |           100 | 0.048                       | 0.0965                |
| Barnes–Hut  | 0.7 |           500 | 0.175                       | 0.3508                |
| Barnes–Hut  | 0.7 |          3000 | 0.588                       | 1.1757                |
| Barnes–Hut  | 0.7 |         15000 | 0.891                       | 1.7821                |
| Barnes–Hut  | 0.7 |         75000 | 4.801                       | 9.6027                |
| Barnes–Hut  | 1.0 |           100 | 0.041                       | 0.0825                |
| Barnes–Hut  | 1.0 |           500 | 0.131                       | 0.2625                |
| Barnes–Hut  | 1.0 |          3000 | 0.311                       | 0.6214                |
| Barnes–Hut  | 1.0 |         15000 | 0.568                       | 1.1362                |
| Barnes–Hut  | 1.0 |         75000 | 2.968                       | 5.9361                |

