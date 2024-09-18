#区间估计
import numpy as np
import scipy.stats as stats

def generate_binomial_sample_S(n_S, p_S, sample_size_S):
    samples_S = np.random.binomial(n_S, p_S, sample_size_S)
    return samples_S
def estimate_p_interval_S(samples_S, n_S, confidence_level_S=0.95):
    total_successes_S = np.sum(samples_S)
    sample_size_S = len(samples_S)
    p_hat_S = total_successes_S / (n_S * sample_size_S)  
    lower_bound_S, upper_bound_S = stats.binom.interval(confidence_level_S, n_S * sample_size_S, p_hat_S, loc=0)
    lower_bound_S = lower_bound_S / (n_S * sample_size_S)
    upper_bound_S = upper_bound_S / (n_S * sample_size_S)
    return p_hat_S, (lower_bound_S, upper_bound_S)

n_S = 10 
p_true_S = 0.05 
sample_size_S = 500 
samples_S = generate_binomial_sample_S(n_S, p_true_S, sample_size_S)
p_hat_S, confidence_interval_S = estimate_p_interval_S(samples_S, n_S)
print(f"估计的 p 值: {p_hat_S:.4f}")
print(f"{int(95)}% 置信区间: [{confidence_interval_S[0]:.4f}, {confidence_interval_S[1]:.4f}]")