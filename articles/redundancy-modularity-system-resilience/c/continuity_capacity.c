#include <stdio.h>

int main(void) {
    double redundancy_index = 0.36;
    double restoration_capacity = 0.42;
    double governance_coordination = 0.48;
    double monitoring_capacity = 0.54;
    double containment_strength = 0.36;

    double continuity_capacity =
        0.28 * redundancy_index +
        0.22 * restoration_capacity +
        0.20 * governance_coordination +
        0.16 * monitoring_capacity +
        0.14 * containment_strength;

    printf("continuity_capacity: %.3f\n", continuity_capacity);
    return 0;
}
