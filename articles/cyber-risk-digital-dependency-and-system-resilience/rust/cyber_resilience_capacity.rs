fn main() {
    let recovery_capacity = 0.38;
    let governance_capacity = 0.42;
    let backup_redundancy_capacity = 0.34;
    let monitoring_maturity = 0.44;
    let logging_maturity = 0.40;
    let incident_exercise_maturity = 0.36;

    let cyber_resilience_capacity =
        0.20 * recovery_capacity +
        0.18 * governance_capacity +
        0.17 * backup_redundancy_capacity +
        0.16 * monitoring_maturity +
        0.14 * logging_maturity +
        0.15 * incident_exercise_maturity;

    println!("cyber_resilience_capacity: {:.3}", cyber_resilience_capacity);
}
