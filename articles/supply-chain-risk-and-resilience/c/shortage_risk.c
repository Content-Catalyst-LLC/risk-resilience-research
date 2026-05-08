#include <stdio.h>

int main(void) {
    double disruption_pressure = 0.74;
    double recovery_time_pressure = 0.84;
    double resilience_buffer_capacity = 0.32;

    double shortage_risk =
        disruption_pressure *
        (1.0 + 0.40 * recovery_time_pressure) *
        (1.0 - 0.45 * resilience_buffer_capacity);

    printf("shortage_risk: %.3f\n", shortage_risk);
    return 0;
}
