fn meets_priority_demand(
    desalination_output: f64,
    outage_fraction: f64,
    alternative_supply: f64,
    emergency_transfer: f64,
    losses: f64,
    priority_demand: f64,
) -> bool {
    let outage_supply = ((1.0 - outage_fraction) * desalination_output)
        + alternative_supply
        + emergency_transfer
        - losses;
    outage_supply >= priority_demand
}

fn main() {
    let stable = meets_priority_demand(420.0, 0.25, 85.0, 40.0, 28.0, 360.0);
    println!("Synthetic system meets priority demand under outage: {}", stable);
}
