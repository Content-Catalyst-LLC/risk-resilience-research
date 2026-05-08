#include <iostream>
#include <algorithm>

int main() {
    double failure_pressure = 0.54;
    double interdependence_exposure = 1.32;
    double social_vulnerability = 0.64;
    double resilience_capacity = 0.46;
    double service_demand_under_stress = 0.88;
    double criticality = 0.94;

    double cascading_risk =
        (failure_pressure + interdependence_exposure) *
        (1.0 + 0.30 * social_vulnerability) *
        (1.0 - 0.45 * resilience_capacity);

    double service_gap =
        std::max(0.0, service_demand_under_stress - resilience_capacity);

    double recovery_priority =
        cascading_risk +
        0.35 * service_gap +
        0.25 * criticality +
        0.20 * social_vulnerability;

    std::cout << "cascading_infrastructure_risk: " << cascading_risk << std::endl;
    std::cout << "service_continuity_gap: " << service_gap << std::endl;
    std::cout << "recovery_priority_score: " << recovery_priority << std::endl;
    return 0;
}
