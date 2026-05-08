#include <iostream>
#include <algorithm>

int main() {
    double digital_criticality = 0.96;
    double systemic_cyber_risk = 0.72;
    double cascading_dependency_exposure = 0.54;
    double cyber_resilience_capacity = 0.38;
    double user_vulnerability = 0.82;

    double service_continuity_gap =
        std::max(
            0.0,
            digital_criticality +
            systemic_cyber_risk +
            0.50 * cascading_dependency_exposure -
            cyber_resilience_capacity
        );

    double recovery_priority_score =
        service_continuity_gap +
        0.30 * digital_criticality +
        0.25 * user_vulnerability +
        0.25 * cascading_dependency_exposure;

    std::cout << "service_continuity_gap: " << service_continuity_gap << std::endl;
    std::cout << "recovery_priority_score: " << recovery_priority_score << std::endl;
    return 0;
}
