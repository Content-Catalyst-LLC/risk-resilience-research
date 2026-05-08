program continuity_gap
  implicit none

  real :: justice_weighted_social_risk
  real :: continuity_capacity
  real :: compound_resilience_gap

  justice_weighted_social_risk = 0.84
  continuity_capacity = 0.46

  compound_resilience_gap = justice_weighted_social_risk - continuity_capacity
  if (compound_resilience_gap < 0.0) compound_resilience_gap = 0.0

  print *, "compound_resilience_gap:", compound_resilience_gap
end program continuity_gap
