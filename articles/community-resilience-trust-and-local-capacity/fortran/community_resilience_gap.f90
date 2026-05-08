program community_resilience_gap
  implicit none

  real :: community_hazard_pressure
  real :: trust_adjusted_response_capacity
  real :: participation_legitimacy
  real :: resilience_gap

  community_hazard_pressure = 1.02
  trust_adjusted_response_capacity = 0.66
  participation_legitimacy = 0.32

  resilience_gap = community_hazard_pressure - trust_adjusted_response_capacity - participation_legitimacy
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "community_resilience_gap:", resilience_gap
end program community_resilience_gap
