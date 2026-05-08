#include <iostream>

int main() {
    double buffer_erosion = 0.66;
    double monitoring_capacity = 0.54;
    double response_capacity = 0.46;
    double threshold_proximity = 0.68;

    double resilience_margin =
        0.34 * (1.0 - buffer_erosion) +
        0.24 * monitoring_capacity +
        0.24 * response_capacity +
        0.18 * (1.0 - threshold_proximity);

    std::cout << "resilience_margin: " << resilience_margin << std::endl;
    return 0;
}
