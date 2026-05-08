#include <stdio.h>

int main(void) {
    double concurrent_hazard_intensity = 0.84;
    double sequential_hazard_pressure = 0.72;
    double exposure = 0.78;

    double compound_event_severity =
        0.42 * concurrent_hazard_intensity +
        0.34 * sequential_hazard_pressure +
        0.24 * exposure;

    printf("compound_event_severity: %.3f\n", compound_event_severity);
    return 0;
}
