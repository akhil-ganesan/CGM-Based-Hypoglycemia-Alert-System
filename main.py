import numpy as np
import math
from matplotlib import pyplot as plt
from scipy import stats

# Constants
data_length = 100
lowest_bs = 0 # Typically before fainting
highest_bs = 150 # Diabetics post eating
cutoff_bs = 54
augmented_SNR = 15
trials = 119
design_input_accuracy = data_length * (1 - 0.91)

np.random.seed(42)

simple_results = []
complex_results = []

def to_db(x):
    return 10*math.log10(x)

def from_db(x):
    return math.pow(10, x/10.0)

# Estimation Utilities
def estimate_error_count(estimate):
    return sum([1 if estimate[i] != hypoglycemia[i] else 0 for i in range(len(hypoglycemia))])

def filter_parameter_tuning(noisy_data) -> float:
    filter_params = []
    errors = []
    for f_a in range(1000):
        f_a /= 1000
        filter_params.append(f_a)
        errors.append(estimate_error_count(
            complex_estimate(noisy_data, f_a)
        ))

    # plt.plot(filter_params, errors, label="Filter Performance", color="red")
    # plt.title('Filter Tuning')
    # plt.ylabel('Errors (Counts)')
    # plt.xlabel('Filter Alpha')
    # plt.show()

    min_alpha = filter_params[np.argmin(errors)]

    # print("Min Filter Alpha", min_alpha)

    return min_alpha

def simple_estimate(noisy_data):
    return [1 if level < cutoff_bs else 0 for level in noisy_data]

def complex_estimate(noisy_data, smoothing_factor):
    return [1 if level < cutoff_bs else 0 for level in
                        [noisy_data[i] if i == 0 else
                         smoothing_factor * noisy_data[i] + (1 - smoothing_factor) * noisy_data[i - 1]
                         for i in range(len(noisy_data))]
                        ]

for trial in range(trials):
    # Augmented Data Generation
    # bs_levels = np.random.randint(low=lowest_bs, high=highest_bs, size=data_length)
    t = np.linspace(1, data_length, 1000)
    bs_levels = (highest_bs - lowest_bs) * (np.sin(t / (2*np.pi)) + 1) / 2 + lowest_bs
    hypoglycemia = [1 if level < cutoff_bs else 0 for level in bs_levels]

    # https://en.wikipedia.org/wiki/Signal-to-noise_ratio#Alternative_definition
    current_SNR = to_db(math.pow(np.mean(bs_levels) / np.std(bs_levels), 2))
    # print("Current SNR Estimate: ", current_SNR)
    # print("Target SNR: ", augmented_SNR)

    # https://stackoverflow.com/questions/14058340/adding-noise-to-a-signal-in-python
    # https://en.wikipedia.org/wiki/Additive_white_Gaussian_noise
    # https://en.wikipedia.org/wiki/Normal_distribution#Moments
    # https://www.mdpi.com/1424-8220/10/7/6751

    # Adding Additive White Gaussian Noise
    # Sqrt is for converting to sigma (based on 2nd moment of normal distribution)
    max_noise = np.sqrt(from_db(to_db(np.mean(bs_levels)) - augmented_SNR))
    noise = np.random.normal(-max_noise, max_noise, len(bs_levels))
    noisy_bs_levels = bs_levels + noise

    # Noisy Data Augmentation Visualization
    # plt.plot(t, noisy_bs_levels, label="Noisy BS Levels", color="green")
    # plt.plot(t, bs_levels, label="BS Levels", color="red")
    # plt.title('Blood Sugar Levels')
    # plt.ylabel('Levels (mg/dL)')
    # plt.xlabel('Reading')
    # plt.show()

    simple_estimation = simple_estimate(noisy_bs_levels)
    # print("Simple Estimate Errors: ", estimate_error_count(simple_estimate))

    filter_alpha = filter_parameter_tuning(noisy_bs_levels)

    complex_estimation = complex_estimate(noisy_bs_levels, filter_alpha)

    # print("Complex Estimate Errors: ", estimate_error_count(complex_estimate))


    # print(f"Performance Improvement: {100 * abs(estimate_error_count(simple_estimate) - estimate_error_count(complex_estimate)) / min(estimate_error_count(simple_estimate), estimate_error_count(complex_estimate)) }%")

    simple_error_count = estimate_error_count(simple_estimation)
    complex_error_count = estimate_error_count(complex_estimation)

    simple_results.append(simple_error_count)
    complex_results.append(complex_error_count)
    print(f"Trial {trial}: Simple ({simple_error_count}) & Complex ({complex_error_count}); Filter Alpha ({filter_alpha})")

print(sum(simple_results) * 1.0 / sum(complex_results))
print(simple_results)
print(complex_results)
print(np.average(simple_results))
print(np.average(complex_results))

# Perform Welch's t-test between groups
t_statistic_1, p_value_1 = stats.ttest_ind(simple_results, complex_results, equal_var=False)

print("Welch's t-statistic:", t_statistic_1)
print("Welch's p-value:", p_value_1)

# Perform Single-Sided t-test on design input
t_statistic_2, p_value_2 = stats.ttest_1samp(simple_results, design_input_accuracy)
t_statistic_3, p_value_3 = stats.ttest_1samp(complex_results, design_input_accuracy)

print("Simple t-statistic:", t_statistic_2)
print("Simple p-value:", p_value_2)

print("Complex t-statistic:", t_statistic_3)
print("Complex p-value:", p_value_3)

# Output

# C:\Users\Akhil\anaconda3\python.exe "C:\Users\Akhil\Documents\School (GT)\BMED 2310\Alert System POC\main.py"
# Trial 0: Simple (5) & Complex (4); Filter Alpha (0.386)
# Trial 1: Simple (9) & Complex (7); Filter Alpha (0.19)
# Trial 2: Simple (8) & Complex (7); Filter Alpha (0.089)
# Trial 3: Simple (7) & Complex (6); Filter Alpha (0.06)
# Trial 4: Simple (8) & Complex (7); Filter Alpha (0.466)
# Trial 5: Simple (5) & Complex (5); Filter Alpha (0.0)
# Trial 6: Simple (9) & Complex (6); Filter Alpha (0.346)
# Trial 7: Simple (6) & Complex (5); Filter Alpha (0.486)
# Trial 8: Simple (4) & Complex (4); Filter Alpha (0.99)
# Trial 9: Simple (7) & Complex (6); Filter Alpha (0.813)
# Trial 10: Simple (4) & Complex (4); Filter Alpha (0.0)
# Trial 11: Simple (6) & Complex (6); Filter Alpha (0.0)
# Trial 12: Simple (5) & Complex (2); Filter Alpha (0.489)
# Trial 13: Simple (5) & Complex (4); Filter Alpha (0.742)
# Trial 14: Simple (6) & Complex (6); Filter Alpha (0.598)
# Trial 15: Simple (7) & Complex (5); Filter Alpha (0.309)
# Trial 16: Simple (8) & Complex (6); Filter Alpha (0.42)
# Trial 17: Simple (7) & Complex (4); Filter Alpha (0.17)
# Trial 18: Simple (10) & Complex (7); Filter Alpha (0.256)
# Trial 19: Simple (9) & Complex (6); Filter Alpha (0.286)
# Trial 20: Simple (5) & Complex (3); Filter Alpha (0.606)
# Trial 21: Simple (7) & Complex (3); Filter Alpha (0.435)
# Trial 22: Simple (6) & Complex (5); Filter Alpha (0.572)
# Trial 23: Simple (6) & Complex (3); Filter Alpha (0.502)
# Trial 24: Simple (7) & Complex (4); Filter Alpha (0.211)
# Trial 25: Simple (6) & Complex (5); Filter Alpha (0.354)
# Trial 26: Simple (4) & Complex (4); Filter Alpha (0.0)
# Trial 27: Simple (5) & Complex (3); Filter Alpha (0.844)
# Trial 28: Simple (7) & Complex (5); Filter Alpha (0.701)
# Trial 29: Simple (10) & Complex (6); Filter Alpha (0.263)
# Trial 30: Simple (2) & Complex (2); Filter Alpha (0.694)
# Trial 31: Simple (9) & Complex (8); Filter Alpha (0.124)
# Trial 32: Simple (5) & Complex (3); Filter Alpha (0.127)
# Trial 33: Simple (9) & Complex (7); Filter Alpha (0.762)
# Trial 34: Simple (9) & Complex (8); Filter Alpha (0.071)
# Trial 35: Simple (9) & Complex (4); Filter Alpha (0.358)
# Trial 36: Simple (7) & Complex (5); Filter Alpha (0.616)
# Trial 37: Simple (10) & Complex (6); Filter Alpha (0.273)
# Trial 38: Simple (8) & Complex (6); Filter Alpha (0.675)
# Trial 39: Simple (6) & Complex (3); Filter Alpha (0.729)
# Trial 40: Simple (7) & Complex (7); Filter Alpha (0.0)
# Trial 41: Simple (11) & Complex (7); Filter Alpha (0.27)
# Trial 42: Simple (8) & Complex (6); Filter Alpha (0.193)
# Trial 43: Simple (5) & Complex (3); Filter Alpha (0.638)
# Trial 44: Simple (8) & Complex (6); Filter Alpha (0.558)
# Trial 45: Simple (5) & Complex (4); Filter Alpha (0.525)
# Trial 46: Simple (7) & Complex (7); Filter Alpha (0.913)
# Trial 47: Simple (8) & Complex (6); Filter Alpha (0.26)
# Trial 48: Simple (8) & Complex (7); Filter Alpha (0.383)
# Trial 49: Simple (5) & Complex (3); Filter Alpha (0.015)
# Trial 50: Simple (9) & Complex (7); Filter Alpha (0.622)
# Trial 51: Simple (7) & Complex (5); Filter Alpha (0.461)
# Trial 52: Simple (8) & Complex (4); Filter Alpha (0.23)
# Trial 53: Simple (10) & Complex (9); Filter Alpha (0.497)
# Trial 54: Simple (6) & Complex (4); Filter Alpha (0.464)
# Trial 55: Simple (6) & Complex (5); Filter Alpha (0.056)
# Trial 56: Simple (5) & Complex (3); Filter Alpha (0.494)
# Trial 57: Simple (9) & Complex (8); Filter Alpha (0.508)
# Trial 58: Simple (8) & Complex (6); Filter Alpha (0.0)
# Trial 59: Simple (10) & Complex (8); Filter Alpha (0.405)
# Trial 60: Simple (6) & Complex (5); Filter Alpha (0.616)
# Trial 61: Simple (7) & Complex (5); Filter Alpha (0.051)
# Trial 62: Simple (6) & Complex (6); Filter Alpha (0.0)
# Trial 63: Simple (8) & Complex (7); Filter Alpha (0.046)
# Trial 64: Simple (8) & Complex (6); Filter Alpha (0.261)
# Trial 65: Simple (11) & Complex (4); Filter Alpha (0.323)
# Trial 66: Simple (5) & Complex (5); Filter Alpha (0.0)
# Trial 67: Simple (8) & Complex (6); Filter Alpha (0.0)
# Trial 68: Simple (6) & Complex (5); Filter Alpha (0.029)
# Trial 69: Simple (8) & Complex (7); Filter Alpha (0.177)
# Trial 70: Simple (6) & Complex (4); Filter Alpha (0.0)
# Trial 71: Simple (12) & Complex (9); Filter Alpha (0.333)
# Trial 72: Simple (6) & Complex (4); Filter Alpha (0.524)
# Trial 73: Simple (5) & Complex (2); Filter Alpha (0.41)
# Trial 74: Simple (6) & Complex (3); Filter Alpha (0.518)
# Trial 75: Simple (8) & Complex (7); Filter Alpha (0.067)
# Trial 76: Simple (10) & Complex (7); Filter Alpha (0.389)
# Trial 77: Simple (6) & Complex (4); Filter Alpha (0.778)
# Trial 78: Simple (9) & Complex (5); Filter Alpha (0.442)
# Trial 79: Simple (5) & Complex (4); Filter Alpha (0.049)
# Trial 80: Simple (6) & Complex (4); Filter Alpha (0.301)
# Trial 81: Simple (6) & Complex (4); Filter Alpha (0.387)
# Trial 82: Simple (6) & Complex (6); Filter Alpha (0.985)
# Trial 83: Simple (7) & Complex (5); Filter Alpha (0.278)
# Trial 84: Simple (5) & Complex (5); Filter Alpha (0.0)
# Trial 85: Simple (5) & Complex (3); Filter Alpha (0.618)
# Trial 86: Simple (8) & Complex (5); Filter Alpha (0.42)
# Trial 87: Simple (8) & Complex (7); Filter Alpha (0.326)
# Trial 88: Simple (7) & Complex (6); Filter Alpha (0.466)
# Trial 89: Simple (6) & Complex (4); Filter Alpha (0.0)
# Trial 90: Simple (6) & Complex (4); Filter Alpha (0.674)
# Trial 91: Simple (8) & Complex (7); Filter Alpha (0.121)
# Trial 92: Simple (6) & Complex (6); Filter Alpha (0.0)
# Trial 93: Simple (6) & Complex (6); Filter Alpha (0.0)
# Trial 94: Simple (7) & Complex (5); Filter Alpha (0.42)
# Trial 95: Simple (8) & Complex (7); Filter Alpha (0.052)
# Trial 96: Simple (6) & Complex (6); Filter Alpha (0.0)
# Trial 97: Simple (9) & Complex (7); Filter Alpha (0.068)
# Trial 98: Simple (7) & Complex (6); Filter Alpha (0.084)
# Trial 99: Simple (7) & Complex (6); Filter Alpha (0.508)
# Trial 100: Simple (9) & Complex (6); Filter Alpha (0.07)
# Trial 101: Simple (7) & Complex (5); Filter Alpha (0.356)
# Trial 102: Simple (6) & Complex (6); Filter Alpha (0.699)
# Trial 103: Simple (8) & Complex (7); Filter Alpha (0.108)
# Trial 104: Simple (5) & Complex (5); Filter Alpha (0.0)
# Trial 105: Simple (8) & Complex (5); Filter Alpha (0.262)
# Trial 106: Simple (4) & Complex (4); Filter Alpha (0.428)
# Trial 107: Simple (9) & Complex (7); Filter Alpha (0.0)
# Trial 108: Simple (8) & Complex (6); Filter Alpha (0.708)
# Trial 109: Simple (7) & Complex (6); Filter Alpha (0.255)
# Trial 110: Simple (6) & Complex (5); Filter Alpha (0.755)
# Trial 111: Simple (8) & Complex (5); Filter Alpha (0.365)
# Trial 112: Simple (5) & Complex (3); Filter Alpha (0.75)
# Trial 113: Simple (5) & Complex (4); Filter Alpha (0.104)
# Trial 114: Simple (8) & Complex (6); Filter Alpha (0.235)
# Trial 115: Simple (6) & Complex (5); Filter Alpha (0.742)
# Trial 116: Simple (3) & Complex (3); Filter Alpha (0.597)
# Trial 117: Simple (8) & Complex (6); Filter Alpha (0.344)
# Trial 118: Simple (9) & Complex (8); Filter Alpha (0.065)
# 1.3169572107765453
# [5, 9, 8, 7, 8, 5, 9, 6, 4, 7, 4, 6, 5, 5, 6, 7, 8, 7, 10, 9, 5, 7, 6, 6, 7, 6, 4, 5, 7, 10, 2, 9, 5, 9, 9, 9, 7, 10, 8, 6, 7, 11, 8, 5, 8, 5, 7, 8, 8, 5, 9, 7, 8, 10, 6, 6, 5, 9, 8, 10, 6, 7, 6, 8, 8, 11, 5, 8, 6, 8, 6, 12, 6, 5, 6, 8, 10, 6, 9, 5, 6, 6, 6, 7, 5, 5, 8, 8, 7, 6, 6, 8, 6, 6, 7, 8, 6, 9, 7, 7, 9, 7, 6, 8, 5, 8, 4, 9, 8, 7, 6, 8, 5, 5, 8, 6, 3, 8, 9]
# [4, 7, 7, 6, 7, 5, 6, 5, 4, 6, 4, 6, 2, 4, 6, 5, 6, 4, 7, 6, 3, 3, 5, 3, 4, 5, 4, 3, 5, 6, 2, 8, 3, 7, 8, 4, 5, 6, 6, 3, 7, 7, 6, 3, 6, 4, 7, 6, 7, 3, 7, 5, 4, 9, 4, 5, 3, 8, 6, 8, 5, 5, 6, 7, 6, 4, 5, 6, 5, 7, 4, 9, 4, 2, 3, 7, 7, 4, 5, 4, 4, 4, 6, 5, 5, 3, 5, 7, 6, 4, 4, 7, 6, 6, 5, 7, 6, 7, 6, 6, 6, 5, 6, 7, 5, 5, 4, 7, 6, 6, 5, 5, 3, 4, 6, 5, 3, 6, 8]
# 6.983193277310924
# 5.302521008403361
# Welch's t-statistic: 7.817175581730814
# Welch's p-value: 1.9015378789176165e-13
# Simple t-statistic: -12.39158661189784
# Simple p-value: 4.2648640663610933e-23
# Complex t-statistic: -26.320533804567827
# Complex p-value: 3.270988245807373e-51
#
# Process finished with exit code 0
