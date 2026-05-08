#include <iostream>
#include <algorithm>

int main() {
    double stress_load = 1.05;
    double resilience_capacity = 0.48;
    double threshold_level = 0.62;
    double social_vulnerability = 0.72;
    double interdependence_exposure = 0.66;

    double threshold_proximity =
        stress_load / (0.20 + threshold_level + resilience_capacity);

    threshold_proximity = std::max(0.0, std::min(1.5, threshold_proximity));

    double service_continuity_gap =
        std::max(0.0, stress_load - resilience_capacity);

    double stress_test_priority_score =
        service_continuity_gap +
        0.35 * threshold_proximity +
        0.25 * social_vulnerability +
        0.25 * interdependence_exposure;

    std::cout << "threshold_proximity: " << threshold_proximity << std::endl;
    std::cout << "service_continuity_gap: " << service_continuity_gap << std::endl;
    std::cout << "stress_test_priority_score: " << stress_test_priority_score << std::endl;
    return 0;
}
