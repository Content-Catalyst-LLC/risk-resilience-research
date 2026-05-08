#include <iostream>

int main() {
    double coupling_pressure = 0.836;
    double external_stress = 0.74;
    double system_criticality = 0.92;
    double modularity_capacity = 0.36;

    double cascade_potential =
        coupling_pressure *
        (1.0 + external_stress) *
        (1.0 + 0.5 * system_criticality) *
        (1.0 - 0.35 * modularity_capacity);

    std::cout << "cascade_potential: " << cascade_potential << std::endl;
    return 0;
}
