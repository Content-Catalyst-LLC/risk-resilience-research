#include <stdio.h>

int main(void) {
    double mobility_pressure = 0.78;
    double social_vulnerability = 0.82;
    double adaptive_mobility_capacity = 0.34;

    double forced_displacement_risk =
        mobility_pressure *
        (1.0 + 0.35 * social_vulnerability) *
        (1.0 - 0.45 * adaptive_mobility_capacity);

    printf("forced_displacement_risk: %.3f\n", forced_displacement_risk);
    return 0;
}
