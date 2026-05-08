fn main() {
    let concurrent_hazard_intensity = 0.84;
    let sequential_hazard_pressure = 0.72;
    let exposure = 0.78;

    let compound_event_severity =
        0.42 * concurrent_hazard_intensity +
        0.34 * sequential_hazard_pressure +
        0.24 * exposure;

    println!("compound_event_severity: {:.3}", compound_event_severity);
}
