#include <stdio.h>

int main(void) {
    double release_pressure = 0.74;
    double conservation_rigidity = 0.72;
    double revolt_pressure = 0.70;
    double system_criticality = 0.74;
    double inequality_pressure = 0.76;

    double release_risk =
        0.34 * release_pressure +
        0.24 * conservation_rigidity +
        0.18 * revolt_pressure +
        0.14 * system_criticality +
        0.10 * inequality_pressure;

    printf("release_risk_index: %.3f\n", release_risk);
    return 0;
}
