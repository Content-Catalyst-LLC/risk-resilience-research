fn main() {
    let baseline_capacity = 0.56;
    let redundancy = 0.38;
    let recovery_capacity = 0.42;
    let governance_capacity = 0.48;
    let monitoring_maturity = 0.46;

    let resilience_capacity =
        0.24 * baseline_capacity +
        0.20 * redundancy +
        0.20 * recovery_capacity +
        0.18 * governance_capacity +
        0.18 * monitoring_maturity;

    println!("resilience_capacity: {:.3}", resilience_capacity);
}
