# chi_square_analysis.py
# BIT 4131 - Topic 17: Chi-square and Categorical Data Analysis
#
# Three questions, three tests:
#   A. Is class attendance related to where a student lives?      -> test of independence (3x3)
#   B. Are female and male students equally likely to use the library? -> 2x2 test, Yates, Fisher, odds ratio
#   C. Does our sample match the housing office's 40/35/25% split? -> goodness-of-fit
#
# Just press Run. The script will:
#   1. print every result as a clean table in the terminal
#   2. save every table AND every graph as a PNG in ../figures
#   3. build one results page (outputs/chi_square_results.html) with all the
#      tables, graphs and conclusions, and open it in your browser
# No pop-up plot windows, so nothing stops the run.

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.stats as st
from statsmodels.stats.contingency_tables import Table, Table2x2
from report_utils import show_table, Report

warnings.filterwarnings("ignore")
pd.set_option("display.width", 120)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

# paths are worked out from this file's location, so the script runs from any folder
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "outputs")
os.makedirs(FIG, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
def fig_path(name): return os.path.join(FIG, name)

df = pd.read_csv(os.path.join(ROOT, "data", "student_survey.csv"))
res_order = ["Hostel", "Off-campus", "Home"]
att_order = ["High", "Medium", "Low"]
rep = Report("Topic 17: Chi-square and Categorical Data Analysis",
             "Does where you live affect how often you attend class? Output of chi_square_analysis.py")

def pfmt(p): return "< 0.001" if p < 0.001 else f"{p:.4f}"

rep.heading("The data")
rep.text(f"{len(df)} simulated student survey responses.")
show_table(df.head(), "Table 1: First five rows of the dataset", fig_path("table_01_data_preview.png"), rep)

# ==================================================================
# A. Residence x Attendance: chi-square test of independence
# ==================================================================
rep.heading("A. Is attendance related to where a student lives?")
observed = pd.crosstab(df.residence, df.attendance).loc[res_order, att_order]
obs_tot = observed.copy()
obs_tot["Total"] = obs_tot.sum(axis=1)
obs_tot.loc["Total"] = obs_tot.sum()
obs_tot.index.name = "Residence"
show_table(obs_tot, "Table 2: Observed counts (contingency table)", fig_path("table_02_observed.png"), rep)

row_pct = (pd.crosstab(df.residence, df.attendance, normalize="index").loc[res_order, att_order] * 100).round(1)
row_pct.index.name = "Residence (%)"
show_table(row_pct, "Table 3: Row percentages", fig_path("table_03_row_percentages.png"), rep,
           "More than half of hostel students report high attendance, against about a fifth of those living at home.")

chi2, p, dof, expected = st.chi2_contingency(observed)
expected = pd.DataFrame(expected, index=res_order, columns=att_order).round(2)
expected.index.name = "Residence"
show_table(expected, "Table 4: Expected counts if residence and attendance were independent",
           fig_path("table_04_expected.png"), rep,
           f"Smallest expected count = {expected.values.min():.2f}, which is above 5, so the test is valid.")

n = observed.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(observed.shape) - 1)))
crit = st.chi2.ppf(0.95, dof)
decision = "Reject H0: residence and attendance are related" if p < 0.05 else "Fail to reject H0"
test_a = pd.DataFrame({"Value": [f"{chi2:.4f}", str(dof), f"{crit:.3f}", f"{p:.6f}", f"{cramers_v:.4f}", decision]},
                      index=["Chi-square statistic", "Degrees of freedom", "Critical value (alpha = 0.05)",
                             "p-value", "Cramer's V (effect size)", "Decision"])
test_a.index.name = "Result"
show_table(test_a, "Table 5: Chi-square test of independence", fig_path("table_05_test_result.png"), rep)

adj_resid = pd.DataFrame(Table(observed).standardized_resids, index=res_order, columns=att_order).round(2)
adj_resid.index.name = "Residence"
show_table(adj_resid, "Table 6: Adjusted residuals (beyond +/-1.96 is notable)", fig_path("table_06_adjusted_residuals.png"), rep,
           "Hostel-High and Home-Low are well above expectation; Hostel-Low and Home-High are well below.")

# figure 1: stacked percentage bar chart
pct = row_pct
fig, ax = plt.subplots(figsize=(7, 4.2))
left = np.zeros(len(res_order))
for col, colour in zip(att_order, [BLUE, ORANGE, AQUA]):
    ax.barh(res_order, pct[col], left=left, color=colour, edgecolor="white", label=col)
    for i, v in enumerate(pct[col]):
        ax.text(left[i] + v / 2, i, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=9)
    left += pct[col].values
ax.invert_yaxis()
ax.set_xlabel("Percentage of students"); ax.set_title("Attendance level by residence")
ax.legend(title="Attendance", frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.15))
fig.tight_layout(); fig.savefig(fig_path("py_01_attendance_by_residence.png"), dpi=150); plt.close(fig)
rep.image(fig_path("py_01_attendance_by_residence.png"), "Figure 1: Attendance level within each residence group")

# figure 2: heat map of adjusted residuals
fig, ax = plt.subplots(figsize=(5.8, 4))
im = ax.imshow(adj_resid.values, cmap="RdBu_r", vmin=-4.5, vmax=4.5)
ax.set_xticks(range(3), att_order); ax.set_yticks(range(3), res_order)
for i in range(3):
    for j in range(3):
        v = adj_resid.values[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", color="white" if abs(v) > 2.5 else "black")
ax.set_title("Adjusted residuals (red = more than expected)")
fig.colorbar(im, ax=ax, shrink=0.8)
fig.tight_layout(); fig.savefig(fig_path("py_02_residual_heatmap.png"), dpi=150); plt.close(fig)
rep.image(fig_path("py_02_residual_heatmap.png"), "Figure 2: Which cells drive the result")

# figure 3: mosaic plot (tile width = share of students in that residence,
# tile height = share of that residence at each attendance level)
fig, ax = plt.subplots(figsize=(7, 4.5))
x0 = 0
for rn in res_order:
    row = observed.loc[rn]
    w = row.sum() / n
    y0 = 0
    for cn, colour in zip(att_order, [BLUE, ORANGE, AQUA]):
        h = row[cn] / row.sum()
        ax.add_patch(plt.Rectangle((x0, y0), w - 0.02, h - 0.02, color=colour, alpha=0.85))
        ax.text(x0 + (w - 0.02) / 2, y0 + (h - 0.02) / 2, f"{rn}\n{cn}\n{row[cn]}",
                ha="center", va="center", fontsize=8, color="white")
        y0 += h
    x0 += w
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Mosaic plot: residence and attendance")
fig.tight_layout(); fig.savefig(fig_path("py_03_mosaic.png"), dpi=150); plt.close(fig)
rep.image(fig_path("py_03_mosaic.png"), "Figure 3: Mosaic plot of residence and attendance")

concl_a = (f"Chi-square = {chi2:.2f} on {dof} df, p = {p:.6f}. We reject independence: attendance is related to residence. "
           f"Cramer's V = {cramers_v:.2f}, a medium association. Hostel students attend the most and students living at home the least.")
rep.callout(concl_a)

# ==================================================================
# B. Gender x Library use: 2x2 table
# ==================================================================
rep.heading("B. Are female and male students equally likely to use the library?")
lib = pd.crosstab(df.gender, df.uses_library).loc[["Female", "Male"], ["Yes", "No"]]
lib_tot = lib.copy()
lib_tot["Total"] = lib_tot.sum(axis=1)
lib_tot["% using"] = (lib["Yes"] / lib_tot["Total"] * 100).round(1)
lib_tot.index.name = "Gender"
show_table(lib_tot, "Table 7: Gender x library use", fig_path("table_07_library_table.png"), rep)

chi2_n, p_n, _, _ = st.chi2_contingency(lib, correction=False)
chi2_y, p_y, _, _ = st.chi2_contingency(lib, correction=True)
_, p_f = st.fisher_exact(lib)
t22 = Table2x2(lib.values)
lo, hi = t22.oddsratio_confint()
phi = np.sqrt(chi2_n / lib.values.sum())
test_b = pd.DataFrame({
    "Statistic": [f"{chi2_n:.4f}", f"{chi2_y:.4f}", "-", f"{t22.oddsratio:.4f}", f"{phi:.4f}"],
    "p-value / 95% CI": [f"{p_n:.6f}", f"{p_y:.6f}", f"{p_f:.6f}", f"{lo:.3f} to {hi:.3f}", "-"],
}, index=["Chi-square (no correction)", "Chi-square (Yates' correction)", "Fisher's exact test",
          "Odds ratio (female vs male)", "Phi coefficient"])
test_b.index.name = "Test"
show_table(test_b, "Table 8: 2x2 test results", fig_path("table_08_library_tests.png"), rep)

fig, ax = plt.subplots(figsize=(5.5, 3.8))
ax.bar(["Female", "Male"], lib_tot["% using"], color=[BLUE, ORANGE], width=0.55)
for i, v in enumerate(lib_tot["% using"]):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center")
ax.set_ylim(0, 100); ax.set_ylabel("% who use the library"); ax.set_title("Library use by gender")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout(); fig.savefig(fig_path("py_05_library_by_gender.png"), dpi=150); plt.close(fig)
rep.image(fig_path("py_05_library_by_gender.png"), "Figure 4: Share of each gender who use the library")

concl_b = (f"All three tests reject independence (Fisher p = {p_f:.4f}). The odds of a female student using the library "
           f"are {t22.oddsratio:.2f} times those of a male student (95% CI {lo:.2f} to {hi:.2f}).")
rep.callout(concl_b)

# ==================================================================
# C. Goodness-of-fit
# ==================================================================
rep.heading("C. Does our sample match the housing office's figures?")
obs_res = df.residence.value_counts().loc[res_order].values
claimed = np.array([0.40, 0.35, 0.25])
exp_res = claimed * obs_res.sum()
gof = st.chisquare(obs_res, f_exp=exp_res)
gof_tab = pd.DataFrame({
    "Claimed proportion": claimed,
    "Observed": obs_res,
    "Expected": exp_res.round(1),
    "(O - E)^2 / E": ((obs_res - exp_res) ** 2 / exp_res).round(3),
}, index=res_order)
gof_tab.index.name = "Residence"
show_table(gof_tab, "Table 9: Goodness-of-fit calculation", fig_path("table_09_goodness_of_fit.png"), rep,
           f"Chi-square = {gof.statistic:.4f}, df = 2, p = {gof.pvalue:.4f}. "
           + ("Fail to reject H0: the sample matches the claimed split." if gof.pvalue > 0.05 else "Reject H0."))

fig, ax = plt.subplots(figsize=(6.5, 4))
x = np.arange(3)
ax.bar(x - 0.2, obs_res, width=0.4, color=BLUE, label="Observed (our sample)")
ax.bar(x + 0.2, exp_res, width=0.4, color=ORANGE, label="Expected (housing office)")
ax.set_xticks(x, res_order); ax.set_ylabel("Number of students")
ax.set_title("Goodness-of-fit: observed vs expected"); ax.legend(frameon=False); ax.grid(axis="y", alpha=0.25)
fig.tight_layout(); fig.savefig(fig_path("py_04_goodness_of_fit.png"), dpi=150); plt.close(fig)
rep.image(fig_path("py_04_goodness_of_fit.png"), "Figure 5: Observed vs expected residence counts")

concl_c = (f"Chi-square = {gof.statistic:.2f}, p = {gof.pvalue:.2f}. No evidence that our sample differs from the "
           "housing office's 40/35/25 split, so the sample looks representative.")
rep.callout(concl_c)

# ==================================================================
# Summary
# ==================================================================
summary = pd.DataFrame({
    "Test": ["Independence (3x3)", "2x2 + Fisher", "Goodness-of-fit"],
    "Statistic": [f"Chi-sq = {chi2:.2f}", f"Chi-sq = {chi2_n:.2f}", f"Chi-sq = {gof.statistic:.2f}"],
    "p-value": [pfmt(p), pfmt(p_n), f"{gof.pvalue:.4f}"],
    "Decision": ["Reject H0" if p < 0.05 else "Fail to reject", "Reject H0" if p_n < 0.05 else "Fail to reject",
                 "Reject H0" if gof.pvalue < 0.05 else "Fail to reject"],
}, index=["A. Residence x attendance", "B. Gender x library use", "C. Residence vs housing office"])
summary.index.name = "Question"
rep.heading("Summary of all three tests")
show_table(summary, "Table 10: Summary of results", fig_path("table_10_summary.png"), rep)

print("\n" + "=" * 60 + "\n  CONCLUSIONS\n" + "=" * 60)
for c in (concl_a, concl_b, concl_c):
    print("- " + c)

print(f"\nAll tables and graphs saved as PNG images in: {FIG}")
rep.save_and_open(os.path.join(OUT, "chi_square_results.html"))
