#include <stdio.h>

int main(void) {
    double health_hazard_pressure = 0.84;
    double exposure = 0.78;
    double social_health_vulnerability = 0.72;
    double resilience_capacity = 0.50;
    double inequality_pressure = 0.74;
    double repeated_health_disruption_pressure = 0.70;

    double public_health_threat_pressure =
        health_hazard_pressure *
        exposure *
        (1.0 + 0.40 * social_health_vulnerability);

    double systemic_health_risk =
        public_health_threat_pressure *
        (1.0 - 0.45 * resilience_capacity) *
        (1.0 + 0.35 * inequality_pressure) *
        (1.0 + 0.15 * repeated_health_disruption_pressure);

    printf("public_health_threat_pressure: %.3f\n", public_health_threat_pressure);
    printf("systemic_health_risk: %.3f\n", systemic_health_risk);
    return 0;
}
