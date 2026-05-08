#include <stdio.h>

int main(void) {
    double stress_load = 0.84;
    double resilience_margin = 0.34;
    double threshold_proximity = 0.76;

    double threshold_gap = threshold_proximity - resilience_margin;
    double crossing_pressure = stress_load * (1.0 + threshold_gap);

    printf("threshold_gap: %.3f\n", threshold_gap);
    printf("crossing_pressure: %.3f\n", crossing_pressure);

    return 0;
}
