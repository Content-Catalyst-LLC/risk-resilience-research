#include <iostream>
#include <algorithm>

int main() {
    double participation_quality = 0.38;
    double institutional_support = 0.42;
    double exclusion_pressure = 0.64;
    double community_hazard_pressure = 1.02;
    double trust_adjusted_response_capacity = 0.66;

    double participation_legitimacy =
        participation_quality *
        (1.0 + 0.25 * institutional_support) *
        (1.0 - 0.35 * exclusion_pressure);

    participation_legitimacy = std::max(0.0, std::min(1.5, participation_legitimacy));

    double community_resilience_gap =
        std::max(
            0.0,
            community_hazard_pressure -
            trust_adjusted_response_capacity -
            participation_legitimacy
        );

    std::cout << "participation_legitimacy: " << participation_legitimacy << std::endl;
    std::cout << "community_resilience_gap: " << community_resilience_gap << std::endl;
    return 0;
}
