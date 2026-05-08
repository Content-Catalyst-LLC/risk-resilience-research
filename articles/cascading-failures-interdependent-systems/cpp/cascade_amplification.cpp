#include <iostream>

int main() {
    double propagation_likelihood = 1.18;
    double system_criticality = 0.92;
    double social_vulnerability = 0.58;
    double governance_response_capacity = 0.47;

    double cascade_amplification =
        propagation_likelihood *
        (1.0 + system_criticality) *
        (1.0 + social_vulnerability) *
        (1.0 - 0.35 * governance_response_capacity);

    std::cout << "cascade_amplification: " << cascade_amplification << std::endl;
    return 0;
}
