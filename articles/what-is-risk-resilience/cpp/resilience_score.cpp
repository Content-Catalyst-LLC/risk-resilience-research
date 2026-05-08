#include <algorithm>
#include <iostream>

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

int main() {
    double robustness = 0.40;
    double redundancy = 0.36;
    double adaptive_capacity = 0.46;
    double recovery_capacity = 0.38;
    double transformation_capacity = 0.44;

    double resilience_capacity = clamp01(
        0.22 * robustness +
        0.20 * redundancy +
        0.22 * adaptive_capacity +
        0.18 * recovery_capacity +
        0.18 * transformation_capacity
    );

    std::cout << "resilience_capacity: " << resilience_capacity << std::endl;
    return 0;
}
