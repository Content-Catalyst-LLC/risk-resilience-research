#include <iostream>
#include <algorithm>

int main() {
    double ecosystem_condition = 0.50;
    double biodiversity_benefit = 0.60;
    double social_legitimacy = 0.48;
    double maintenance_capacity = 0.42;
    double displacement_pressure = 0.66;
    double nature_adjusted_risk = 0.52;
    double social_vulnerability = 0.70;
    double buffer_effectiveness = 0.62;

    double credibility_risk =
        0.22 * (1.0 - ecosystem_condition) +
        0.20 * (1.0 - biodiversity_benefit) +
        0.18 * (1.0 - social_legitimacy) +
        0.18 * (1.0 - maintenance_capacity) +
        0.22 * displacement_pressure;

    double justice_weighted_nbs_risk =
        (nature_adjusted_risk + credibility_risk) *
        (1.0 + 0.30 * social_vulnerability);

    double nbs_resilience_gap =
        std::max(0.0, justice_weighted_nbs_risk - buffer_effectiveness);

    std::cout << "credibility_risk: " << credibility_risk << std::endl;
    std::cout << "justice_weighted_nbs_risk: " << justice_weighted_nbs_risk << std::endl;
    std::cout << "nbs_resilience_gap: " << nbs_resilience_gap << std::endl;
    return 0;
}
