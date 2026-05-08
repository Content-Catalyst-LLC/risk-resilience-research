#include <stdio.h>

int main(void) {
    double stress_load = 1.14;
    double robustness_capacity = 0.78;
    double robustness_margin = robustness_capacity - stress_load;

    printf("robustness_margin: %.3f\n", robustness_margin);
    return 0;
}
