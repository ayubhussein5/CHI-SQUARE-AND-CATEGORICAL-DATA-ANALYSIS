# worked_example.py
# The small breakfast-and-CAT example from the report, done step by step,
# then checked against scipy so the hand calculation can be trusted.

import numpy as np
import scipy.stats as st

#                 Passed  Failed
obs = np.array([[18,      7],     # ate breakfast
                [10,     15]])    # skipped breakfast

row_tot = obs.sum(axis=1)
col_tot = obs.sum(axis=0)
n = obs.sum()

expected = np.outer(row_tot, col_tot) / n
contrib = (obs - expected) ** 2 / expected
chi2 = contrib.sum()
df = (obs.shape[0] - 1) * (obs.shape[1] - 1)
p = st.chi2.sf(chi2, df)

print("Row totals:", row_tot, " Column totals:", col_tot, " n =", n)
print("Expected counts:\n", expected)
print("Cell contributions (O-E)^2/E:\n", contrib.round(4))
print(f"Chi-square = {chi2:.4f}, df = {df}, p = {p:.4f}")
print(f"Critical value (alpha 0.05) = {st.chi2.ppf(0.95, df):.3f}")

# scipy check (correction=False so it matches the plain formula)
c, pv, d, e = st.chi2_contingency(obs, correction=False)
print(f"scipy: chi-square = {c:.4f}, p = {pv:.4f}")
print(f"Odds ratio = {(18 * 15) / (7 * 10):.3f}")
