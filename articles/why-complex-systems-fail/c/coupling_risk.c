#include <stdio.h>

int main(void) {
    double dependency_density = 0.88;
    double hidden_coupling = 0.74;
    double system_criticality = 0.92;

    double coupling_pressure =
        0.48 * dependency_density +
        0.36 * hidden_coupling +
        0.16 * system_criticality;

    printf("coupling_pressure: %.3f\n", coupling_pressure);
    return 0;
}
