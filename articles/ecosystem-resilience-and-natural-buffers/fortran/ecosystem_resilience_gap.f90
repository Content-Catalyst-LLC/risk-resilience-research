program ecosystem_resilience_gap
  implicit none

  real :: justice_weighted_ecosystem_risk
  real :: natural_buffer_capacity
  real :: ecosystem_resilience_gap

  justice_weighted_ecosystem_risk = 1.12
  natural_buffer_capacity = 0.48

  ecosystem_resilience_gap = justice_weighted_ecosystem_risk - natural_buffer_capacity
  if (ecosystem_resilience_gap < 0.0) ecosystem_resilience_gap = 0.0

  print *, "ecosystem_resilience_gap:", ecosystem_resilience_gap
end program ecosystem_resilience_gap
