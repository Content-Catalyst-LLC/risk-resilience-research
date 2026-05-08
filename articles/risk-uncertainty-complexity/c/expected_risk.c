#include <stdio.h>

int main(void) {
    double hazard_probability = 0.72;
    double expected_loss_index = 0.78;
    double expected_risk = hazard_probability * expected_loss_index;

    printf("expected_risk: %.3f\n", expected_risk);
    return 0;
}
