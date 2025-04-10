from scipy import stats
import numpy as np

design_input_accuracy = 9

simple_results = [5, 9, 8, 7, 8, 5, 9, 6, 4, 7, 4, 6, 5, 5, 6, 7, 8, 7, 10, 9, 5, 7, 6, 6, 7, 6, 4, 5, 7, 10, 2, 9, 5, 9, 9, 9, 7, 10, 8, 6, 7, 11, 8, 5, 8, 5, 7, 8, 8, 5, 9, 7, 8, 10, 6, 6, 5, 9, 8, 10, 6, 7, 6, 8, 8, 11, 5, 8, 6, 8, 6, 12, 6, 5, 6, 8, 10, 6, 9, 5, 6, 6, 6, 7, 5, 5, 8, 8, 7, 6, 6, 8, 6, 6, 7, 8, 6, 9, 7, 7, 9, 7, 6, 8, 5, 8, 4, 9, 8, 7, 6, 8, 5, 5, 8, 6, 3, 8, 9]
complex_results = [4, 7, 7, 6, 7, 5, 6, 5, 4, 6, 4, 6, 2, 4, 6, 5, 6, 4, 7, 6, 3, 3, 5, 3, 4, 5, 4, 3, 5, 6, 2, 8, 3, 7, 8, 4, 5, 6, 6, 3, 7, 7, 6, 3, 6, 4, 7, 6, 7, 3, 7, 5, 4, 9, 4, 5, 3, 8, 6, 8, 5, 5, 6, 7, 6, 4, 5, 6, 5, 7, 4, 9, 4, 2, 3, 7, 7, 4, 5, 4, 4, 4, 6, 5, 5, 3, 5, 7, 6, 4, 4, 7, 6, 6, 5, 7, 6, 7, 6, 6, 6, 5, 6, 7, 5, 5, 4, 7, 6, 6, 5, 5, 3, 4, 6, 5, 3, 6, 8]

print("Mean Simple Accuracy", 100 - np.average(simple_results))
print("Mean Complex Accuracy", 100 - np.average(complex_results))

# Perform Welch's t-test between groups
t_statistic_1, p_value_1 = stats.ttest_ind(simple_results, complex_results, equal_var=False)

print("Welch's t-statistic:", t_statistic_1)
print("Welch's p-value:", p_value_1)

# Perform Single-Sided t-test on design input
t_statistic_2, p_value_2 = stats.ttest_1samp(simple_results, design_input_accuracy, alternative='greater')
t_statistic_3, p_value_3 = stats.ttest_1samp(complex_results, design_input_accuracy, alternative='greater')

print("Simple t-statistic:", t_statistic_2)
print("Simple p-value:", p_value_2)

print("Complex t-statistic:", t_statistic_3)
print("Complex p-value:", p_value_3)

# Output

# 93.01680672268907
# 94.69747899159664
# Welch's t-statistic: 7.817175581730814
# Welch's p-value: 1.9015378789176165e-13
# Simple t-statistic: -12.39158661189786
# Simple p-value: 1.0
# Complex t-statistic: -26.32053380456785
# Complex p-value: 1.0

# The low Welch p-value indicates it's highly unlikely that the results are observed and the
# null hypothesis (the performance between simple/complex is the same) is true

# The high p-value for each t-statistic indicates the results are expected to be observed
# with ~100% confidence given the hypothesis that the algorithm performance is greater than
# The design input (~91% accurate)