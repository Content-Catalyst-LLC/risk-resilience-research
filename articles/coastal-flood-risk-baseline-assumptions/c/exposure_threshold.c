#include <stdio.h>
#include <stdbool.h>

bool is_exposed(
    double modeled_baseline,
    double baseline_correction,
    double sea_level_rise,
    double tide_surge,
    double uncertainty_margin,
    double land_elevation,
    double protection_height
) {
    double water_height = modeled_baseline + baseline_correction + sea_level_rise + tide_surge + uncertainty_margin;
    double threshold = land_elevation + protection_height;
    return water_height >= threshold;
}

int main(void) {
    bool exposed = is_exposed(0.0, 0.30, 0.45, 0.55, 0.10, 1.25, 0.20);
    printf("Synthetic site exposed after baseline correction: %s\n", exposed ? "true" : "false");
    return 0;
}
