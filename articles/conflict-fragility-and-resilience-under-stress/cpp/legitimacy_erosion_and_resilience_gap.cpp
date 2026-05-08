#include <iostream>
#include <algorithm>

int main() {
    double service_breakdown_gap = 0.58;
    double inequality_pressure = 0.80;
    double institutional_exclusion = 0.76;
    double repeated_disruption_pressure = 0.82;
    double public_trust = 0.30;
    double systemic_risk = 0.86;
    double governance_resilience = 0.34;

    double legitimacy_erosion =
        0.30 * service_breakdown_gap +
        0.26 * inequality_pressure +
        0.24 * institutional_exclusion +
        0.15 * repeated_disruption_pressure -
        0.20 * public_trust;

    legitimacy_erosion = std::max(0.0, std::min(1.5, legitimacy_erosion));

    double resilience_gap =
        std::max(
            0.0,
            systemic_risk + service_breakdown_gap + legitimacy_erosion - governance_resilience
        );

    std::cout << "legitimacy_erosion: " << legitimacy_erosion << std::endl;
    std::cout << "resilience_under_stress_gap: " << resilience_gap << std::endl;
    return 0;
}
