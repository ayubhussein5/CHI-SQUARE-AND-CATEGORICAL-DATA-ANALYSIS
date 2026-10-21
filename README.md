# Topic 17: Chi-square and Categorical Data Analysis

**BIT 4131 Statistical Computing and Reporting | Group work**

The question:- One of us said hostel students attend more classes because they're five minutes from the lecture halls. Another said it makes no difference, because the people who skip will skip wherever they live. Both variables are categories, not numbers, so the chi-square test was the natural way to settle it.

Along the way we answer two more questions with the same family of tests:

| | Question | Test |
|---|---|---|
| A | Is class attendance related to where a student lives? | Chi-square test of independence (3×3) |
| B | Are female and male students equally likely to use the library? | 2×2 chi-square, Yates' correction, Fisher's exact test, odds ratio |
| C | Does our sample match the housing office's 40 / 35 / 25 % split? | Chi-square goodness-of-fit |

## What's in this repository

```
topic17-chi-square/
├── data/
│   ├── generate_data.py         # rebuilds the dataset (fixed seed)
│   └── student_survey.csv       # 300 students, 6 columns
├── python/
│   ├── worked_example.py        # the breakfast example from the report, by hand
│   └── chi_square_analysis.py   # full analysis (scipy + statsmodels)
├── R/
│   └── chi_square_analysis.R    # same analysis in R (stats, vcd, MASS)
├── figures/
├── outputs/                     # console output saved as text
└── requirements.txt
```

## The data

We didn't have permission to use real student records, so we **simulated 300 survey responses**, building in patterns that felt believable to us. The seed is fixed, so you'll get the same file every time.

| Column | Values |
|---|---|
| `student_id` | S001 to S300 |
| `gender` | Female, Male |
| `year_of_study` | 1 to 4 |
| `residence` | Hostel, Off-campus, Home |
| `attendance` | High, Medium, Low |
| `uses_library` | Yes, No |

## How to run it

**Easiest: the notebook (results appear right inside VS Code)**

1. In VS Code, install the **Jupyter** extension (Extensions panel, search "Jupyter").
2. In the terminal: `python -m pip install -r requirements.txt`
3. Open `python/chi_square_analysis.ipynb` and click **Run All** at the top.
4. If VS Code asks you to pick a kernel, choose your Python 3 installation.

Every table and graph appears directly under the code that makes it. Graphs are also saved into `figures/` so you can put them in slides.

**Alternative: the plain script** (`python/chi_square_analysis.py`) prints all tables in the terminal, saves the graphs and opens a results page in your browser.

For R:

```r
install.packages(c("vcd", "MASS"))
# set working directory to the R/ folder, then source chi_square_analysis.R
```

## Main results

**A. Residence and attendance: related.**
χ² = 26.26, df = 4, p = 0.000028. Cramér's V = 0.21, which is a medium association by Cohen's guide.
Hostel students have far more "High" attendance than we'd expect by chance (adjusted residual +4.32). Students living at home have far more "Low" attendance (+3.16). Off-campus students sit almost exactly where independence predicts.

**B. Gender and library use: related.**
χ² = 10.93 (Yates: 10.17), Fisher's exact p = 0.0011. The odds of a female student using the library are 2.18 times the odds for a male student (95% CI 1.37 to 3.47).

**C. Goodness-of-fit: no evidence of a mismatch.**
χ² = 3.30, df = 2, p = 0.19. Our sample's split across residence types is consistent with the housing office figures, which makes us more comfortable treating the sample as representative.

## Group Members



| No. | Name | Registration Number |
|:---:|---|---|
| 1 | Ayub Hussein | BSCCS/2024/56898 |
| 2 | Samuel Njuguna | BSCCS/2024/54633 |
| 3 | Mike Momanyi | BSCCS/2024/57241 |
| 4 | Rickson Mwangi | BSCCS/2024/54222 |
| 5 | Annie Wangeci | BSCCS/2024/55251 |
| 6 | Linet Kamathi | BSCCS/2024/50325 |
| 7 | Steed Mbugua | BSCCS/2024/54025 |
| 8 | Joshua Muli | BSCCS/2024/73427 |
| 9 | Collins Matagi | BSCCS/2024/50482 |
| 10 | Kikuyu Brian | BSCCS/2024/74678 |
| 11 | Philip Philemon | BSS/2022/53061 |
| 12 | James Laat | BSS/2024/54875 |

