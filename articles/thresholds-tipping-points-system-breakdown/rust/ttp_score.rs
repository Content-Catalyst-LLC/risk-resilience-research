fn main() {
    let stress_load = 0.84;
    let stress_rate = 0.62;
    let threshold_proximity = 0.76;
    let feedback_destabilization = 0.68;
    let resilience_margin = 0.34;
    let buffer_capacity = 0.38;
    let monitoring_capacity = 0.42;
    let governance_readiness = 0.46;

    let effective_margin =
        0.42 * resilience_margin +
        0.24 * buffer_capacity +
        0.18 * monitoring_capacity +
        0.16 * governance_readiness;

    let threshold_pressure =
        0.34 * stress_load +
        0.22 * stress_rate +
        0.26 * threshold_proximity +
        0.18 * feedback_destabilization;

    let tipping_pressure =
        threshold_pressure *
        (1.0 + 0.35 * feedback_destabilization) *
        (1.0 + 0.25 * stress_rate) *
        (1.0 - 0.45 * effective_margin);

    println!("effective_margin: {:.3}", effective_margin);
    println!("threshold_pressure: {:.3}", threshold_pressure);
    println!("tipping_pressure: {:.3}", tipping_pressure);
}
