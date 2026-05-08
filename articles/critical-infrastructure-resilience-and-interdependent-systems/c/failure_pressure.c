#include <stdio.h>

int main(void) {
    double criticality = 0.94;
    double hazard_exposure = 0.78;
    double asset_fragility = 0.58;
    double cyber_physical_risk = 0.72;

    double failure_pressure =
        criticality *
        hazard_exposure *
        asset_fragility *
        (1.0 + 0.35 * cyber_physical_risk);

    printf("failure_pressure: %.3f\n", failure_pressure);
    return 0;
}
