#include <iostream>
#include <algorithm>

int main() {
    double hazard_pressure = 0.78;
    double exposure = 0.72;
    double social_vulnerability = 0.60;
    double natural_buffer_capacity = 0.50;
    double governance_capacity = 0.52;

    double hazard_exposure_pressure =
        hazard_pressure * exposure * (1.0 + 0.35 * social_vulnerability);

    double buffer_adjusted_risk =
        hazard_exposure_pressure *
        (1.0 - 0.45 * natural_buffer_capacity) *
        (1.0 - 0.25 * governance_capacity);

    std::cout << "hazard_exposure_pressure: " << hazard_exposure_pressure << std::endl;
    std::cout << "buffer_adjusted_risk: " << buffer_adjusted_risk << std::endl;
    return 0;
}
