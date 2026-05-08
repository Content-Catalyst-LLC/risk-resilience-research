#include <stdio.h>

int main(void) {
    double stress_accumulation = 0.72;
    double buffer_erosion = 0.66;
    double deferred_maintenance = 0.74;

    double stress_index =
        0.20 * stress_accumulation +
        0.16 * buffer_erosion +
        0.14 * deferred_maintenance;

    printf("partial_hidden_stress_index: %.3f\n", stress_index);
    return 0;
}
