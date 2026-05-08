#include <iostream>
#include <algorithm>

int main() {
    double prior_deferred_risk = 0.70;
    double austerity_intensity = 0.64;
    double public_investment = 0.34;
    double maintenance_capacity = 0.30;
    double adaptation_drr_spending = 0.28;
    double fiscal_resilience_risk = 1.45;
    double public_resilience_capacity = 0.36;

    double deferred_risk_burden =
        prior_deferred_risk +
        0.40 * austerity_intensity -
        0.20 * public_investment -
        0.20 * maintenance_capacity -
        0.20 * adaptation_drr_spending;

    deferred_risk_burden = std::max(0.0, std::min(1.5, deferred_risk_burden));

    double public_resilience_gap =
        std::max(
            0.0,
            fiscal_resilience_risk + deferred_risk_burden - public_resilience_capacity
        );

    std::cout << "deferred_risk_burden: " << deferred_risk_burden << std::endl;
    std::cout << "public_resilience_gap: " << public_resilience_gap << std::endl;
    return 0;
}
