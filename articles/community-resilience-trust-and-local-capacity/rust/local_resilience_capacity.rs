fn main() {
    let trust_level = 0.46;
    let local_organizational_capacity = 0.58;
    let mutual_aid_strength = 0.66;
    let communication_access = 0.54;
    let local_knowledge_integration = 0.50;
    let institutional_support = 0.42;
    let participation_quality = 0.38;
    let recovery_capacity = 0.44;

    let local_resilience_capacity =
        0.16 * trust_level +
        0.15 * local_organizational_capacity +
        0.14 * mutual_aid_strength +
        0.13 * communication_access +
        0.14 * local_knowledge_integration +
        0.12 * institutional_support +
        0.08 * participation_quality +
        0.08 * recovery_capacity;

    println!("local_resilience_capacity: {:.3}", local_resilience_capacity);
}
