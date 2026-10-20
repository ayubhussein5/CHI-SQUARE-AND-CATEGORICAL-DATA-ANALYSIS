# generate_data.py
# Builds the synthetic student survey used for our chi-square analysis.
# The idea came from a question our group kept arguing about: do students who
# live in the hostels attend more classes than those who commute from home?
# We did not have permission to collect real student records, so we simulated
# 300 responses with patterns that felt realistic to us. Fixed seed = same file
# for everyone.

import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
n = 300

residence = rng.choice(["Hostel", "Off-campus", "Home"], size=n, p=[0.36, 0.38, 0.26])

# attendance probabilities depend on where the student lives
att_probs = {
    "Hostel":     [0.55, 0.32, 0.13],
    "Off-campus": [0.40, 0.38, 0.22],
    "Home":       [0.27, 0.38, 0.35],
}
attendance = np.array([rng.choice(["High", "Medium", "Low"], p=att_probs[r]) for r in residence])

gender = rng.choice(["Female", "Male"], size=n, p=[0.48, 0.52])
lib_probs = {"Female": 0.62, "Male": 0.46}
uses_library = np.array(["Yes" if rng.random() < lib_probs[g] else "No" for g in gender])

year = rng.choice([1, 2, 3, 4], size=n, p=[0.28, 0.26, 0.24, 0.22])

df = pd.DataFrame({
    "student_id": [f"S{i:03d}" for i in range(1, n + 1)],
    "gender": gender,
    "year_of_study": year,
    "residence": residence,
    "attendance": attendance,
    "uses_library": uses_library,
})

df.to_csv("student_survey.csv", index=False)
print(df.head())
print(f"\nSaved {len(df)} rows to student_survey.csv")
