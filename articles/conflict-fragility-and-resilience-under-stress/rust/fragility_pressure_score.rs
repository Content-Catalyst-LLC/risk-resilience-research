fn main() {
    let conflict_intensity = 0.86;
    let social_vulnerability = 0.78;
    let displacement_pressure = 0.82;
    let livelihood_stress = 0.76;
    let hazard_exposure = 0.70;

    let fragility_pressure =
        0.24 * conflict_intensity +
        0.20 * social_vulnerability +
        0.18 * displacement_pressure +
        0.18 * livelihood_stress +
        0.20 * hazard_exposure;

    println!("fragility_pressure: {:.3}", fragility_pressure);
}
