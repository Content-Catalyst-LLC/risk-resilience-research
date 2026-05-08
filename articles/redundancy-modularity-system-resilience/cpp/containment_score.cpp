#include <iostream>

int main() {
    double modularity_capacity = 0.34;
    double containment_strength = 0.36;
    double coupling_intensity = 0.84;
    double dependency_concentration = 0.80;

    double modularity_index =
        0.42 * modularity_capacity +
        0.28 * containment_strength +
        0.18 * (1.0 - coupling_intensity) +
        0.12 * (1.0 - dependency_concentration);

    std::cout << "modularity_index: " << modularity_index << std::endl;
    return 0;
}
