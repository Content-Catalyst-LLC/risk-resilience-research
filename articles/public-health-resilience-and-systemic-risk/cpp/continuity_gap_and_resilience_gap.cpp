#include <iostream>
#include <algorithm>

int main() {
    double systemic_health_risk = 0.86;
    double essential_service_demand = 0.82;
    double essential_service_continuity = 0.48;
    double trust_adjusted_response_capacity = 0.62;

    double continuity_gap =
        std::max(0.0, essential_service_demand - essential_service_continuity);

    double public_health_resilience_gap =
        std::max(
            0.0,
            systemic_health_risk + continuity_gap - trust_adjusted_response_capacity
        );

    std::cout << "continuity_gap: " << continuity_gap << std::endl;
    std::cout << "public_health_resilience_gap: " << public_health_resilience_gap << std::endl;
    return 0;
}
