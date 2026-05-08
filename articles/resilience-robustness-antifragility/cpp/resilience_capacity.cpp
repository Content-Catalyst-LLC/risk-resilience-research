#include <iostream>

int main() {
    double recovery = 0.48;
    double adaptive = 0.40;
    double redundancy = 0.52;
    double modularity = 0.38;
    double monitoring = 0.58;
    double containment = 0.50;

    double resilience =
        0.23 * recovery +
        0.22 * adaptive +
        0.18 * redundancy +
        0.16 * modularity +
        0.11 * monitoring +
        0.10 * containment;

    std::cout << "resilience_capacity: " << resilience << std::endl;
    return 0;
}
