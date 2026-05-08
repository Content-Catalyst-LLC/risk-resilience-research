#include <iostream>
#include <algorithm>

int main() {
    double cascade_potential = 0.86;
    double social_sensitivity_index = 0.74;
    double recovery_deficit = 0.72;
    double inequality_pressure = 0.80;
    double continuity_capacity = 0.42;

    double justice_weighted_social_risk =
        (0.38 * cascade_potential +
         0.30 * social_sensitivity_index +
         0.18 * recovery_deficit +
         0.14 * inequality_pressure) *
        (1.0 + 0.35 * inequality_pressure);

    double gap = std::max(0.0, justice_weighted_social_risk - continuity_capacity);

    std::cout << "justice_weighted_social_risk: " << justice_weighted_social_risk << std::endl;
    std::cout << "compound_resilience_gap: " << gap << std::endl;
    return 0;
}
