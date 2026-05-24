#include <stdio.h>

double local_redundancy_ratio(double local_output_kg, double essential_demand_kg) {
    if (essential_demand_kg <= 0.0) {
        return 0.0;
    }
    return local_output_kg / essential_demand_kg;
}

double shock_supply(double external_supply_kg, double shock_fraction, double local_output_kg, double buffer_kg, double losses_kg) {
    return ((1.0 - shock_fraction) * external_supply_kg) + local_output_kg + buffer_kg - losses_kg;
}

int main(void) {
    double rho = local_redundancy_ratio(8200.0, 52000.0);
    double supply = shock_supply(43800.0, 0.25, 8200.0, 2000.0, 500.0);

    printf("Local redundancy ratio: %.3f\n", rho);
    printf("Shock scenario available supply: %.2f kg\n", supply);

    return 0;
}
