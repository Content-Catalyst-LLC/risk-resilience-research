# Lightweight resilience indicator summary utility.
# Run from the repository root with:
# Rscript r/resilience_indicator_summary.R

indicators <- read.csv("data/indicators.csv", stringsAsFactors = FALSE)

summary_table <- as.data.frame(table(indicators$indicator_family))
names(summary_table) <- c("indicator_family", "count")

dir.create("outputs", showWarnings = FALSE)
write.csv(summary_table, "outputs/resilience-indicator-summary.csv", row.names = FALSE)

cat("Wrote outputs/resilience-indicator-summary.csv\n")
