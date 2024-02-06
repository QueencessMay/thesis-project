from scipy import stats
import numpy as np

# Performance metrics without emojis and emoticons
metrics_without_emojis_emoticons = {
    'accuracy': 0.95398,
    'precision': 0.96224,
    'f1': 0.95357,
    'recall': 0.94505
}

# Performance metrics with emojis and emoticons
metrics_with_emojis_emoticons = {
    'accuracy': 0.97459,
    'precision': 0.97513,
    'f1': 0.97450,
    'recall': 0.97390
}

# Perform paired t-test
t_statistic, p_value = stats.ttest_rel(
    [metrics_with_emojis_emoticons[metric] for metric in metrics_with_emojis_emoticons],
    [metrics_without_emojis_emoticons[metric] for metric in metrics_without_emojis_emoticons]
)

# Calculate mean and standard deviation
mean_without_emojis_emoticons = np.mean([metrics_without_emojis_emoticons[metric] for metric in metrics_without_emojis_emoticons])
std_dev_without_emojis_emoticons = np.std([metrics_without_emojis_emoticons[metric] for metric in metrics_without_emojis_emoticons])

mean_with_emojis_emoticons = np.mean([metrics_with_emojis_emoticons[metric] for metric in metrics_with_emojis_emoticons])
std_dev_with_emojis_emoticons = np.std([metrics_with_emojis_emoticons[metric] for metric in metrics_with_emojis_emoticons])

# Display the results
print("Paired t-test results:")
print("T-statistic:", t_statistic)
print("P-value:", p_value)
print("\nMean and Standard Deviation:")
print("DistilBERT Without Emojis and Emoticons - Mean:", mean_without_emojis_emoticons, " | Standard Deviation:", std_dev_without_emojis_emoticons)
print("DistilBERT With Emojis and Emoticons - Mean:", mean_with_emojis_emoticons, " | Standard Deviation:", std_dev_with_emojis_emoticons)

# Interpret the results
alpha = 0.05  # significance level
if p_value < alpha:
    print("\nReject the null hypothesis. There is a significant difference.")
else:
    print("\nFail to reject the null hypothesis. There is no significant difference.")
