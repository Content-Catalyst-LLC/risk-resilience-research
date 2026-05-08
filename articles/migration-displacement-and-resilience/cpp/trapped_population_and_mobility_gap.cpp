#include <iostream>
#include <algorithm>

int main() {
    double mobility_pressure = 0.78;
    double mobility_resources = 0.24;
    double protection_access = 0.36;
    double migration_network_strength = 0.30;
    double forced_displacement_risk = 0.72;
    double destination_stress = 0.48;
    double adaptive_mobility_capacity = 0.34;

    double trapped_population_risk =
        std::max(
            0.0,
            mobility_pressure -
            mobility_resources -
            protection_access -
            migration_network_strength
        );

    double mobility_resilience_gap =
        std::max(
            0.0,
            forced_displacement_risk +
            trapped_population_risk +
            destination_stress -
            adaptive_mobility_capacity
        );

    std::cout << "trapped_population_risk: " << trapped_population_risk << std::endl;
    std::cout << "mobility_resilience_gap: " << mobility_resilience_gap << std::endl;
    return 0;
}
