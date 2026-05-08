#include <iostream>

int main() {
    double regime_shift_likelihood = 0.72;
    double interdependency_density = 0.84;
    double cascade_exposure = 0.82;
    double system_criticality = 0.92;

    double cascade_potential =
        regime_shift_likelihood *
        (1.0 + interdependency_density) *
        (1.0 + 0.5 * cascade_exposure) *
        (1.0 + 0.35 * system_criticality);

    std::cout << "cascade_potential: " << cascade_potential << std::endl;
    return 0;
}
