fn main() {
    let dependency_density = 0.88;
    let hidden_coupling = 0.74;
    let system_criticality = 0.92;
    let feedback_delay = 0.56;
    let signal_visibility = 0.42;
    let maintenance_deficit = 0.62;
    let adaptation_debt = 0.66;

    let coupling_pressure =
        0.48 * dependency_density +
        0.36 * hidden_coupling +
        0.16 * system_criticality;

    let deterioration_pressure =
        0.30 * feedback_delay +
        0.28 * (1.0 - signal_visibility) +
        0.22 * maintenance_deficit +
        0.20 * adaptation_debt;

    println!("coupling_pressure: {:.3}", coupling_pressure);
    println!("deterioration_pressure: {:.3}", deterioration_pressure);
}
