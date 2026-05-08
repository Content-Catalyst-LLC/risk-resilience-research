fn main() {
    let dependency_density = 0.86;
    let hidden_coupling = 0.74;
    let critical_node_exposure = 0.82;
    let system_criticality = 0.92;

    let dependency_pressure =
        0.34 * dependency_density +
        0.30 * hidden_coupling +
        0.22 * critical_node_exposure +
        0.14 * system_criticality;

    println!("dependency_pressure: {:.3}", dependency_pressure);
}
