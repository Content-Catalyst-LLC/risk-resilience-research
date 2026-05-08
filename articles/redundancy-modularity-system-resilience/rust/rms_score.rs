fn main() {
    let redundancy_capacity = 0.38;
    let backup_diversity = 0.36;
    let pathway_diversity = 0.40;
    let spare_capacity = 0.32;

    let redundancy_index =
        0.32 * redundancy_capacity +
        0.24 * backup_diversity +
        0.22 * pathway_diversity +
        0.22 * spare_capacity;

    println!("redundancy_index: {:.3}", redundancy_index);
}
