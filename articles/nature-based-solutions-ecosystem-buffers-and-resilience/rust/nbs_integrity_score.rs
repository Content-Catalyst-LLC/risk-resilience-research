fn main() {
    let ecosystem_condition = 0.58;
    let biodiversity_benefit = 0.62;
    let ecological_connectivity = 0.52;
    let intervention_quality = 0.60;
    let governance_capacity = 0.54;
    let maintenance_capacity = 0.48;

    let nbs_integrity =
        0.20 * ecosystem_condition +
        0.18 * biodiversity_benefit +
        0.16 * ecological_connectivity +
        0.16 * intervention_quality +
        0.15 * governance_capacity +
        0.15 * maintenance_capacity;

    println!("nbs_integrity: {:.3}", nbs_integrity);
}
