#include <stdio.h>

int main(void) {
    double local_organizational_capacity = 0.58;
    double mutual_aid_strength = 0.66;
    double communication_access = 0.54;
    double local_knowledge_integration = 0.50;
    double trust_level = 0.46;

    double response_capacity =
        (
            0.28 * local_organizational_capacity +
            0.25 * mutual_aid_strength +
            0.24 * communication_access +
            0.23 * local_knowledge_integration
        ) *
        (1.0 + 0.35 * trust_level);

    if (response_capacity > 1.5) {
        response_capacity = 1.5;
    }

    printf("trust_adjusted_response_capacity: %.3f\n", response_capacity);
    return 0;
}
