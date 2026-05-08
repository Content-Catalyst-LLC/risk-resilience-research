#include <stdio.h>

int main(void) {
    double fragility_pressure = 0.78;
    double conflict_intensity = 0.86;
    double governance_resilience = 0.34;

    double conflict_amplified_systemic_risk =
        fragility_pressure *
        (1.0 + 0.45 * conflict_intensity) *
        (1.0 - 0.35 * governance_resilience);

    printf("conflict_amplified_systemic_risk: %.3f\n", conflict_amplified_systemic_risk);
    return 0;
}
