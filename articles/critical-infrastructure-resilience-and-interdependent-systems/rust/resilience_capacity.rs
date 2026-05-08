fn main() {
    let redundancy = 0.46;
    let maintenance_capacity = 0.42;
    let governance_capacity = 0.50;
    let recovery_capacity = 0.48;
    let backup_capacity = 0.44;
    let workforce_readiness = 0.52;

    let resilience_capacity =
        0.22 * redundancy +
        0.20 * maintenance_capacity +
        0.18 * governance_capacity +
        0.18 * recovery_capacity +
        0.12 * backup_capacity +
        0.10 * workforce_readiness;

    println!("resilience_capacity: {:.3}", resilience_capacity);
}
