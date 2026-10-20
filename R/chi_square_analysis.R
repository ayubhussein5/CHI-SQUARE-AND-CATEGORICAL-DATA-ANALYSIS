# chi_square_analysis.R
# BIT 4131 - Topic 17: Chi-square and Categorical Data Analysis (R version)
#
# Packages: stats (built in), vcd, MASS
# install.packages(c("vcd", "MASS"))   # run once
#
# Set the working directory to the R/ folder before running
# (RStudio: Session > Set Working Directory > To Source File Location).

library(vcd)
library(MASS)

dir.create("../figures", showWarnings = FALSE)
df <- read.csv("../data/student_survey.csv")

df$residence  <- factor(df$residence,  levels = c("Hostel", "Off-campus", "Home"))
df$attendance <- factor(df$attendance, levels = c("High", "Medium", "Low"))
df$gender     <- factor(df$gender,     levels = c("Female", "Male"))
df$uses_library <- factor(df$uses_library, levels = c("Yes", "No"))

# ==================================================================
# A. Residence x Attendance
# ==================================================================
tab <- table(df$residence, df$attendance)
names(dimnames(tab)) <- c("Residence", "Attendance")
addmargins(tab)
round(prop.table(tab, 1) * 100, 1)      # row percentages

test <- chisq.test(tab)
test                                     # X-squared, df, p-value
round(test$expected, 2)                  # expected counts
round(test$stdres, 2)                    # adjusted residuals
qchisq(0.95, df = test$parameter)        # critical value

assocstats(tab)                          # vcd: Cramer's V, phi, contingency coefficient

png("../figures/r_01_mosaic_shaded.png", width = 1200, height = 900, res = 150)
mosaic(tab, shade = TRUE, legend = TRUE,
       main = "Residence vs attendance (shaded by residual)")
dev.off()

png("../figures/r_02_attendance_barplot.png", width = 1200, height = 800, res = 150)
barplot(t(prop.table(tab, 1)) * 100, beside = TRUE,
        col = c("#2a78d6", "#eb6834", "#1baf7a"),
        legend.text = TRUE, args.legend = list(title = "Attendance", bty = "n"),
        ylab = "Percentage of students", main = "Attendance level by residence")
dev.off()

# MASS: a log-linear model gives the same conclusion from a different angle
loglm(~ Residence + Attendance, data = tab)   # independence model; small p = poor fit

# ==================================================================
# B. Gender x Library use (2x2)
# ==================================================================
lib <- table(df$gender, df$uses_library)
lib
chisq.test(lib, correct = FALSE)
chisq.test(lib)                     # with Yates' continuity correction (R's default for 2x2)
fisher.test(lib)                    # exact p-value + conditional odds ratio
oddsratio(lib, log = FALSE)         # vcd
confint(oddsratio(lib, log = FALSE))

# ==================================================================
# C. Goodness-of-fit against the housing office proportions
# ==================================================================
observed_res <- table(df$residence)
gof <- chisq.test(observed_res, p = c(0.40, 0.35, 0.25))
gof
gof$expected
