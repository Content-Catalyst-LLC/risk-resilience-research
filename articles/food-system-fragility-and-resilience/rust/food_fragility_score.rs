fn main() {
    let production_stress = 0.86;
    let water_stress = 0.84;
    let ecological_degradation = 0.72;
    let logistics_fragility = 0.58;
    let input_dependency = 0.70;
    let price_volatility = 0.76;

    let food_system_fragility =
        0.20 * production_stress +
        0.18 * water_stress +
        0.18 * ecological_degradation +
        0.16 * logistics_fragility +
        0.14 * input_dependency +
        0.14 * price_volatility;

    println!("food_system_fragility: {:.3}", food_system_fragility);
}
