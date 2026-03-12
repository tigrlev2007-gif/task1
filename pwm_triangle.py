import pwm_dac
import signal_generator as sg
import time

amplitude = 3.290
signal_frequency = 10
sampling_frequency = 1000

try:
    dac = pwm_dac.PWM_DAC(gpio_pin=12, pwm_frequency=500, dynamic_range=3.290, verbose=False)
    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        relative_amplitude = sg.get_triangle_wave_amplitude(signal_frequency, current_time)
        voltage = relative_amplitude * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()
