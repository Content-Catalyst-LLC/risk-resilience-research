fn main() {
    let recovery_capacity = 0.38;
    let recovery_speed = 0.34;
    let essential_function_restoration = 0.42;
    let adaptive_capacity = 0.44;
    let governance_capacity = 0.40;
    let learning_capacity = 0.46;
    let ecological_buffer_capacity = 0.36;
    let social_protection_capacity = 0.32;
    let transformation_readiness = 0.58;
    let public_legitimacy = 0.44;

    let recovery_score =
        0.38 * recovery_capacity + 0.28 * recovery_speed + 0.34 * essential_function_restoration;

    let adaptation_score =
        0.26 * adaptive_capacity +
        0.22 * governance_capacity +
        0.18 * learning_capacity +
        0.18 * ecological_buffer_capacity +
        0.16 * social_protection_capacity;

    let transformation_score =
        0.34 * transformation_readiness +
        0.22 * governance_capacity +
        0.18 * learning_capacity +
        0.14 * public_legitimacy +
        0.12 * social_protection_capacity;

    println!("recovery_score: {:.3}", recovery_score);
    println!("adaptation_score: {:.3}", adaptation_score);
    println!("transformation_score: {:.3}", transformation_score);
}
