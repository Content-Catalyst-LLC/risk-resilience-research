# Risk, vulnerability, and resilience dashboard
#
# Synthetic-data workflow for the article:
# "What Are Risk and Resilience in Sustainable Systems?"

library(readr)
library(dplyr)
library(tidyr)

input_file <- "articles/risk-resilience/data/risk_resilience_profiles.csv"
output_dir <- "articles/risk-resilience/outputs"

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

profiles <- read_csv(input_file, show_col_types = FALSE)

required_cols <- c(
  "system_name",
  "system_type",
  "hazard_pressure",
  "exposure",
  "vulnerability",
  "protective_capacity",
  "robustness",
  "redundancy",
  "adaptive_capacity",
  "recovery_capacity",
  "transformation_capacity",
  "justice_legitimacy",
  "baseline_function",
  "minimum_function_after_shock",
  "recovery_days"
)

missing_cols <- setdiff(required_cols, names(profiles))
if (length(missing_cols) > 0) {
  stop(paste("Missing required columns:", paste(missing_cols, collapse = ", ")))
}

estimate_functional_loss <- function(
  baseline_function,
  minimum_function_after_shock,
  recovery_days
) {
  0.5 * (baseline_function - minimum_function_after_shock) * recovery_days
}

scores <- profiles %>%
  mutate(
    risk_score = pmin(
      pmax(
        hazard_pressure * exposure * vulnerability * (1 - protective_capacity),
        0
      ),
      1
    ),
    resilience_capacity = pmin(
      pmax(
        0.22 * robustness +
          0.20 * redundancy +
          0.22 * adaptive_capacity +
          0.18 * recovery_capacity +
          0.18 * transformation_capacity,
        0
      ),
      1
    ),
    resilience_adjusted_risk = pmin(
      pmax(risk_score / (1 + resilience_capacity), 0),
      1
    ),
    justice_adjusted_risk = pmin(
      pmax(resilience_adjusted_risk * (1 - justice_legitimacy), 0),
      1
    ),
    functional_loss_area = estimate_functional_loss(
      baseline_function,
      minimum_function_after_shock,
      recovery_days
    ),
    priority_score = pmin(
      pmax(
        0.35 * resilience_adjusted_risk +
          0.30 * justice_adjusted_risk +
          0.20 * percent_rank(functional_loss_area) +
          0.15 * (1 - protective_capacity),
        0
      ),
      1
    )
  ) %>%
  arrange(desc(priority_score), desc(justice_adjusted_risk))

summary <- scores %>%
  group_by(system_type) %>%
  summarise(
    systems = n(),
    mean_risk_score = mean(risk_score),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_resilience_adjusted_risk = mean(resilience_adjusted_risk),
    mean_justice_adjusted_risk = mean(justice_adjusted_risk),
    mean_functional_loss_area = mean(functional_loss_area),
    mean_priority_score = mean(priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_priority_score))

dashboard_long <- scores %>%
  select(
    system_name,
    system_type,
    hazard_pressure,
    exposure,
    vulnerability,
    protective_capacity,
    risk_score,
    resilience_capacity,
    resilience_adjusted_risk,
    justice_adjusted_risk,
    functional_loss_area,
    priority_score
  ) %>%
  pivot_longer(
    cols = -c(system_name, system_type),
    names_to = "indicator",
    values_to = "value"
  )

write_csv(scores, file.path(output_dir, "risk_resilience_scores_from_r.csv"))
write_csv(summary, file.path(output_dir, "risk_resilience_summary_from_r.csv"))
write_csv(dashboard_long, file.path(output_dir, "risk_resilience_dashboard_long.csv"))

print(scores)
print(summary)
