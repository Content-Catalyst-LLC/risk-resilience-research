#include <stdio.h>

int main(void) {
    double cyber_disruption_pressure = 0.72;
    double dependency_concentration = 0.76;
    double user_vulnerability = 0.82;
    double cyber_resilience_capacity = 0.38;

    double systemic_cyber_risk =
        cyber_disruption_pressure *
        (1.0 + 0.35 * dependency_concentration) *
        (1.0 + 0.30 * user_vulnerability) *
        (1.0 - 0.45 * cyber_resilience_capacity);

    printf("systemic_cyber_risk: %.3f\n", systemic_cyber_risk);
    return 0;
}
