program public_health_resilience_gap
  implicit none

  real :: systemic_health_risk
  real :: continuity_gap
  real :: trust_adjusted_response_capacity
  real :: resilience_gap

  systemic_health_risk = 0.86
  continuity_gap = 0.34
  trust_adjusted_response_capacity = 0.62

  resilience_gap = systemic_health_risk + continuity_gap - trust_adjusted_response_capacity
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "public_health_resilience_gap:", resilience_gap
end program public_health_resilience_gap
