program food_resilience_gap
  implicit none

  real :: justice_weighted_food_risk
  real :: resilience_capacity
  real :: food_resilience_gap

  justice_weighted_food_risk = 1.92
  resilience_capacity = 0.52

  food_resilience_gap = justice_weighted_food_risk - resilience_capacity
  if (food_resilience_gap < 0.0) food_resilience_gap = 0.0

  print *, "food_resilience_gap:", food_resilience_gap
end program food_resilience_gap
