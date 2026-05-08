fn main() {
    let stress_accumulation = 0.72;
    let buffer_erosion = 0.66;
    let deferred_maintenance = 0.74;
    let adaptation_debt = 0.56;
    let ecological_support_erosion = 0.42;
    let social_strain = 0.50;
    let trust_erosion = 0.48;

    let hidden_stress_index =
        0.20 * stress_accumulation +
        0.16 * buffer_erosion +
        0.14 * deferred_maintenance +
        0.13 * adaptation_debt +
        0.12 * ecological_support_erosion +
        0.13 * social_strain +
        0.12 * trust_erosion;

    println!("hidden_stress_index: {:.3}", hidden_stress_index);
}
