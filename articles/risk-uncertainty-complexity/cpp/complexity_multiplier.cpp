#include <iostream>

int main() {
    double dependency_density = 0.74;
    double feedback_strength = 0.58;
    double threshold_sensitivity = 0.63;
    double adaptive_behavior = 0.52;

    double multiplier =
        1.0 +
        0.28 * dependency_density +
        0.24 * feedback_strength +
        0.24 * threshold_sensitivity +
        0.24 * adaptive_behavior;

    std::cout << "complexity_multiplier: " << multiplier << std::endl;
    return 0;
}
