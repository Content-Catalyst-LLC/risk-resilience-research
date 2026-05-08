program water_resilience_gap
  implicit none

  real :: justice_weighted_water_risk
  real :: water_security_capacity
  real :: resilience_gap

  justice_weighted_water_risk = 1.25
  water_security_capacity = 0.52

  resilience_gap = justice_weighted_water_risk - water_security_capacity
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "water_resilience_gap:", resilience_gap
end program water_resilience_gap
