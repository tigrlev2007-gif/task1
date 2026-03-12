import numpy as np
import time

def get_sin_wave_amplitude(freq, time_moment):
    sin_val = np.sin(2 * np.pi * freq * time_moment)
    return (sin_val + 1) / 2

def get_triangle_wave_amplitude(freq, time_moment):
    period = 1 / freq
    relative_time = time_moment % period
    if relative_time < period / 2:
        return (2 / period) * relative_time
    else:
        return 2 - (2 / period) * relative_time

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)
