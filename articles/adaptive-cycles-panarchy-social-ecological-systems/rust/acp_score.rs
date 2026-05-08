fn main() {
    let connectedness = 0.82;
    let rigidity = 0.78;
    let cross_scale_dependency = 0.72;
    let governance_flexibility = 0.40;

    let conservation_rigidity_index =
        0.34 * connectedness +
        0.34 * rigidity +
        0.18 * cross_scale_dependency +
        0.14 * (1.0 - governance_flexibility);

    println!("conservation_rigidity_index: {:.3}", conservation_rigidity_index);
}
