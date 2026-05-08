fn main() {
    let surveillance_capacity = 0.58;
    let prevention_capacity = 0.54;
    let essential_service_continuity = 0.48;
    let workforce_capacity = 0.46;
    let supply_chain_reliability = 0.50;
    let public_trust = 0.44;
    let communication_capacity = 0.52;
    let recovery_capacity = 0.46;

    let resilience_capacity =
        0.16 * surveillance_capacity +
        0.14 * prevention_capacity +
        0.16 * essential_service_continuity +
        0.14 * workforce_capacity +
        0.12 * supply_chain_reliability +
        0.12 * public_trust +
        0.08 * communication_capacity +
        0.08 * recovery_capacity;

    println!("public_health_resilience_capacity: {:.3}", resilience_capacity);
}
