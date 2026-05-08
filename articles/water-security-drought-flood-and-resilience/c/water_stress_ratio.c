#include <stdio.h>

int main(void) {
    double water_demand_pressure = 0.84;
    double water_availability = 0.34;
    double stress = water_demand_pressure / (water_availability + 0.05);

    if (stress > 2.0) {
        stress = 2.0;
    }

    printf("water_stress_ratio: %.3f\n", stress);
    return 0;
}
