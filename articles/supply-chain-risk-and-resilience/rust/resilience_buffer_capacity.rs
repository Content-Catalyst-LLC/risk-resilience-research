fn main() {
    let inventory_buffer = 0.28;
    let substitutability = 0.24;
    let supplier_redundancy = 0.26;
    let modular_production_capacity = 0.30;
    let governance_capacity = 0.44;
    let logistics_flexibility = 0.34;

    let resilience_buffer_capacity =
        0.22 * inventory_buffer +
        0.20 * substitutability +
        0.20 * supplier_redundancy +
        0.16 * modular_production_capacity +
        0.12 * governance_capacity +
        0.10 * logistics_flexibility;

    println!("resilience_buffer_capacity: {:.3}", resilience_buffer_capacity);
}
