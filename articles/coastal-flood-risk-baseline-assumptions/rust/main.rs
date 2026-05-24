fn is_exposed(
    modeled_baseline: f64,
    baseline_correction: f64,
    sea_level_rise: f64,
    tide_surge: f64,
    uncertainty_margin: f64,
    land_elevation: f64,
    protection_height: f64,
) -> bool {
    let water_height = modeled_baseline
        + baseline_correction
        + sea_level_rise
        + tide_surge
        + uncertainty_margin;
    let threshold = land_elevation + protection_height;
    water_height >= threshold
}

fn main() {
    let exposed = is_exposed(0.0, 0.30, 0.45, 0.55, 0.10, 1.25, 0.20);
    println!("Synthetic site exposed after baseline correction: {}", exposed);
}
