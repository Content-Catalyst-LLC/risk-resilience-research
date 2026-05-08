#include <iostream>
#include <algorithm>

int main() {
    double criticality = 0.96;
    double shortage_risk = 0.84;
    double resilience_buffer_capacity = 0.32;
    double vulnerable_population_exposure = 0.86;
    double essential_service_relevance = 0.96;

    double service_continuity_gap =
        std::max(0.0, criticality + shortage_risk - resilience_buffer_capacity);

    double public_priority_score =
        service_continuity_gap +
        0.30 * criticality +
        0.25 * vulnerable_population_exposure +
        0.25 * essential_service_relevance;

    std::cout << "service_continuity_gap: " << service_continuity_gap << std::endl;
    std::cout << "public_priority_score: " << public_priority_score << std::endl;
    return 0;
}
