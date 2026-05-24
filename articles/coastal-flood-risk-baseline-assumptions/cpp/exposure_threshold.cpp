#include <iostream>

bool is_exposed(
    double modeled_baseline,
    double baseline_correction,
    double sea_level_rise,
    double tide_surge,
    double uncertainty_margin,
    double land_elevation,
    double protection_height
) {
    const double water_height = modeled_baseline + baseline_correction + sea_level_rise + tide_surge + uncertainty_margin;
    const double threshold = land_elevation + protection_height;
    return water_height >= threshold;
}

int main() {
    const bool exposed = is_exposed(0.0, 0.30, 0.45, 0.55, 0.10, 1.25, 0.20);
    std::cout << "Synthetic site exposed after baseline correction: "
              << (exposed ? "true" : "false") << "\n";
    return 0;
}
