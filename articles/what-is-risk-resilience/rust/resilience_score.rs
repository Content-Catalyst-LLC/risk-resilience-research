fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn main() {
    let hazard_pressure = 0.86;
    let exposure = 0.82;
    let vulnerability = 0.78;
    let protective_capacity = 0.42;

    let robustness = 0.40;
    let redundancy = 0.36;
    let adaptive_capacity = 0.46;
    let recovery_capacity = 0.38;
    let transformation_capacity = 0.44;
    let justice_legitimacy = 0.40;

    let risk_score = clamp01(
        hazard_pressure * exposure * vulnerability * (1.0 - protective_capacity),
    );

    let resilience_capacity = clamp01(
        0.22 * robustness
            + 0.20 * redundancy
            + 0.22 * adaptive_capacity
            + 0.18 * recovery_capacity
            + 0.18 * transformation_capacity,
    );

    let resilience_adjusted_risk = clamp01(risk_score / (1.0 + resilience_capacity));
    let justice_adjusted_risk = clamp01(resilience_adjusted_risk * (1.0 - justice_legitimacy));

    println!("risk_score: {:.3}", risk_score);
    println!("resilience_capacity: {:.3}", resilience_capacity);
    println!("resilience_adjusted_risk: {:.3}", resilience_adjusted_risk);
    println!("justice_adjusted_risk: {:.3}", justice_adjusted_risk);
}
