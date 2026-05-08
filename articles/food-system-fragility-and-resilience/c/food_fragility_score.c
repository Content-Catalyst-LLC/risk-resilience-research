#include <stdio.h>

int main(void) {
    double production_stress = 0.86;
    double water_stress = 0.84;
    double ecological_degradation = 0.72;
    double logistics_fragility = 0.58;
    double input_dependency = 0.70;
    double price_volatility = 0.76;

    double food_system_fragility =
        0.20 * production_stress +
        0.18 * water_stress +
        0.18 * ecological_degradation +
        0.16 * logistics_fragility +
        0.14 * input_dependency +
        0.14 * price_volatility;

    printf("food_system_fragility: %.3f\n", food_system_fragility);
    return 0;
}
