fn main() {
    let adaptive_capacity = 0.38;
    let mobility_resources = 0.36;
    let protection_access = 0.34;
    let migration_network_strength = 0.52;
    let destination_service_capacity = 0.42;
    let host_community_support = 0.46;
    let recovery_capacity = 0.38;

    let adaptive_mobility_capacity =
        0.16 * adaptive_capacity +
        0.15 * mobility_resources +
        0.16 * protection_access +
        0.14 * migration_network_strength +
        0.14 * destination_service_capacity +
        0.13 * host_community_support +
        0.12 * recovery_capacity;

    println!("adaptive_mobility_capacity: {:.3}", adaptive_mobility_capacity);
}
