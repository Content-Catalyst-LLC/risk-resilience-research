#include <iostream>

int main() {
    double adaptive = 0.44;
    double governance = 0.40;
    double learning = 0.46;
    double ecological_buffer = 0.36;
    double social_protection = 0.32;

    double adaptation =
        0.26 * adaptive +
        0.22 * governance +
        0.18 * learning +
        0.18 * ecological_buffer +
        0.16 * social_protection;

    std::cout << "adaptation_capacity: " << adaptation << std::endl;
    return 0;
}
