#include <stdio.h>

int main(void) {
    double hazard_intensity = 0.86;
    double exposure = 0.82;
    double social_vulnerability = 0.72;
    double interdependence_exposure = 0.66;
    double resilience_capacity = 0.48;

    double stress_load =
        hazard_intensity *
        exposure *
        (1.0 + 0.35 * social_vulnerability) *
        (1.0 + 0.30 * interdependence_exposure);

    double failure_pressure =
        stress_load *
        (1.0 - 0.45 * resilience_capacity);

    printf("stress_load: %.3f\n", stress_load);
    printf("failure_pressure: %.3f\n", failure_pressure);
    return 0;
}
