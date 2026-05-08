fn main() {
    let stress_intensity = 0.84;
    let stress_variability = 0.42;
    let system_criticality = 0.88;
    let robustness_capacity = 0.78;
    let recovery_capacity = 0.48;
    let adaptive_capacity = 0.40;
    let redundancy_capacity = 0.52;
    let modularity_capacity = 0.38;
    let monitoring_capacity = 0.58;
    let failure_containment = 0.50;

    let stress_load =
        stress_intensity * (1.0 + 0.5 * stress_variability) * (1.0 + 0.4 * system_criticality);

    let resilience_score =
        0.23 * recovery_capacity +
        0.22 * adaptive_capacity +
        0.18 * redundancy_capacity +
        0.16 * modularity_capacity +
        0.11 * monitoring_capacity +
        0.10 * failure_containment;

    let response_gap = (stress_load - (0.45 * robustness_capacity + 0.55 * resilience_score)).max(0.0);

    println!("stress_load: {:.3}", stress_load);
    println!("robustness_score: {:.3}", robustness_capacity);
    println!("resilience_score: {:.3}", resilience_score);
    println!("response_gap: {:.3}", response_gap);
}
