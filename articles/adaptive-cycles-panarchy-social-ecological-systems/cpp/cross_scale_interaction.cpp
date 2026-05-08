#include <iostream>

int main() {
    double revolt_pressure = 0.70;
    double cross_scale_dependency = 0.72;
    double system_criticality = 0.74;
    double remember_capacity = 0.52;

    double revolt_cascade_pressure =
        revolt_pressure *
        (1.0 + cross_scale_dependency) *
        (1.0 + 0.35 * system_criticality) *
        (1.0 - 0.35 * remember_capacity);

    std::cout << "revolt_cascade_pressure: " << revolt_cascade_pressure << std::endl;
    return 0;
}
