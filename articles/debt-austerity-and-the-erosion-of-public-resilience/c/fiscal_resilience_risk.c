#include <stdio.h>

int main(void) {
    double debt_service_pressure = 1.12;
    double austerity_intensity = 0.64;
    double social_vulnerability = 0.78;
    double hazard_exposure = 0.84;
    double inequality_pressure = 0.76;
    double public_resilience_capacity = 0.36;

    double fiscal_resilience_risk =
        (debt_service_pressure + austerity_intensity) *
        (1.0 + 0.35 * social_vulnerability) *
        (1.0 + 0.30 * hazard_exposure) *
        (1.0 + 0.25 * inequality_pressure) *
        (1.0 - 0.45 * public_resilience_capacity);

    printf("fiscal_resilience_risk: %.3f\n", fiscal_resilience_risk);
    return 0;
}
