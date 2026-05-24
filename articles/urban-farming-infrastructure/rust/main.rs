fn local_redundancy_ratio(local_output_kg: f64, essential_demand_kg: f64) -> f64 {
    if essential_demand_kg <= 0.0 {
        0.0
    } else {
        local_output_kg / essential_demand_kg
    }
}

fn shock_supply(
    external_supply_kg: f64,
    shock_fraction: f64,
    local_output_kg: f64,
    buffer_kg: f64,
    losses_kg: f64,
) -> f64 {
    ((1.0 - shock_fraction) * external_supply_kg) + local_output_kg + buffer_kg - losses_kg
}

fn main() {
    let rho = local_redundancy_ratio(8200.0, 52000.0);
    let supply = shock_supply(43800.0, 0.25, 8200.0, 2000.0, 500.0);

    println!("Local redundancy ratio: {:.3}", rho);
    println!("Shock scenario available supply: {:.2} kg", supply);
}
