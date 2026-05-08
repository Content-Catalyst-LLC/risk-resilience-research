fn main() {
    let hazard_probability = 0.72;
    let expected_loss_index = 0.78;
    let probability_uncertainty = 0.26;
    let loss_uncertainty = 0.34;
    let dependency_density = 0.74;
    let feedback_strength = 0.58;
    let threshold_sensitivity = 0.63;
    let adaptive_behavior = 0.52;

    let expected_risk = hazard_probability * expected_loss_index;
    let combined_uncertainty = (probability_uncertainty + loss_uncertainty) / 2.0;
    let uncertainty_adjusted_risk = expected_risk * (1.0 + combined_uncertainty);

    let complexity_multiplier =
        1.0 +
        0.28 * dependency_density +
        0.24 * feedback_strength +
        0.24 * threshold_sensitivity +
        0.24 * adaptive_behavior;

    let systemic_risk = uncertainty_adjusted_risk * complexity_multiplier;

    println!("expected_risk: {:.3}", expected_risk);
    println!("uncertainty_adjusted_risk: {:.3}", uncertainty_adjusted_risk);
    println!("complexity_multiplier: {:.3}", complexity_multiplier);
    println!("systemic_risk: {:.3}", systemic_risk);
}
