#include <stdio.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

int main(void) {
    double hazard_pressure = 0.86;
    double exposure = 0.82;
    double vulnerability = 0.78;
    double protective_capacity = 0.42;

    double risk_score = clamp01(
        hazard_pressure * exposure * vulnerability * (1.0 - protective_capacity)
    );

    printf("risk_score: %.3f\n", risk_score);
    return 0;
}
