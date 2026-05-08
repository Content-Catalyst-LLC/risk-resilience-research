#include <stdio.h>

int main(void) {
    double initiating_shock_severity = 0.78;
    double dependency_pressure = 0.82;
    double cascade_exposure = 0.84;
    double containment_capacity = 0.39;

    double propagation =
        initiating_shock_severity *
        (1.0 + dependency_pressure) *
        (1.0 + 0.35 * cascade_exposure) *
        (1.0 - 0.45 * containment_capacity);

    printf("propagation_likelihood: %.3f\n", propagation);
    return 0;
}
