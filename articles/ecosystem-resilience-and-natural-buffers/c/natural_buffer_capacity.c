#include <stdio.h>

int main(void) {
    double ecosystem_condition = 0.52;
    double ecological_connectivity = 0.46;
    double functional_biodiversity = 0.58;
    double maintenance_capacity = 0.48;
    double restoration_investment = 0.44;

    double natural_buffer_capacity =
        0.24 * ecosystem_condition +
        0.20 * ecological_connectivity +
        0.20 * functional_biodiversity +
        0.18 * maintenance_capacity +
        0.18 * restoration_investment;

    printf("natural_buffer_capacity: %.3f\n", natural_buffer_capacity);
    return 0;
}
