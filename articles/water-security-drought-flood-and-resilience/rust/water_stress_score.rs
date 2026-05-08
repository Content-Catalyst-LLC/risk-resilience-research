fn main() {
    let water_demand_pressure = 0.84;
    let water_availability = 0.34;
    let water_stress_ratio = (water_demand_pressure / (water_availability + 0.05)).min(2.0);

    println!("water_stress_ratio: {:.3}", water_stress_ratio);
}
