#include <iostream>
#include <algorithm>

int main() {
    double hydrological_risk_pressure = 0.74;
    double systemic_water_vulnerability = 0.80;
    double inequality_pressure = 0.82;
    double water_security_capacity = 0.42;

    double justice_weighted_water_risk =
        (hydrological_risk_pressure + systemic_water_vulnerability) *
        (1.0 + 0.30 * inequality_pressure);

    double gap = std::max(0.0, justice_weighted_water_risk - water_security_capacity);

    std::cout << "justice_weighted_water_risk: " << justice_weighted_water_risk << std::endl;
    std::cout << "water_resilience_gap: " << gap << std::endl;
    return 0;
}
