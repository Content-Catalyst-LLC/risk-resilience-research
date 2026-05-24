#include <stdio.h>
#include <stdbool.h>

bool meets_priority_demand(
    double desalination_output,
    double outage_fraction,
    double alternative_supply,
    double emergency_transfer,
    double losses,
    double priority_demand
) {
    double outage_supply = ((1.0 - outage_fraction) * desalination_output)
                         + alternative_supply
                         + emergency_transfer
                         - losses;
    return outage_supply >= priority_demand;
}

int main(void) {
    bool stable = meets_priority_demand(420.0, 0.25, 85.0, 40.0, 28.0, 360.0);
    printf("Synthetic system meets priority demand under outage: %s\n", stable ? "true" : "false");
    return 0;
}
