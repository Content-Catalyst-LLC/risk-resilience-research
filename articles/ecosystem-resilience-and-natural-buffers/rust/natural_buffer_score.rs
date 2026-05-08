fn main() {
    let ecosystem_condition = 0.52;
    let ecological_connectivity = 0.46;
    let functional_biodiversity = 0.58;
    let maintenance_capacity = 0.48;
    let restoration_investment = 0.44;

    let natural_buffer_capacity =
        0.24 * ecosystem_condition +
        0.20 * ecological_connectivity +
        0.20 * functional_biodiversity +
        0.18 * maintenance_capacity +
        0.18 * restoration_investment;

    println!("natural_buffer_capacity: {:.3}", natural_buffer_capacity);
}
