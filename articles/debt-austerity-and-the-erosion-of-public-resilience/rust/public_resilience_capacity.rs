fn main() {
    let essential_service_spending = 0.42;
    let public_investment = 0.34;
    let maintenance_capacity = 0.30;
    let adaptation_drr_spending = 0.28;
    let social_protection_capacity = 0.36;
    let governance_capacity = 0.40;
    let local_government_capacity = 0.34;

    let public_resilience_capacity =
        0.18 * essential_service_spending +
        0.16 * public_investment +
        0.15 * maintenance_capacity +
        0.16 * adaptation_drr_spending +
        0.15 * social_protection_capacity +
        0.12 * governance_capacity +
        0.08 * local_government_capacity;

    println!("public_resilience_capacity: {:.3}", public_resilience_capacity);
}
