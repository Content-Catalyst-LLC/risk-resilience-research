program nbs_resilience_gap
  implicit none

  real :: justice_weighted_nbs_risk
  real :: buffer_effectiveness
  real :: resilience_gap

  justice_weighted_nbs_risk = 0.98
  buffer_effectiveness = 0.62

  resilience_gap = justice_weighted_nbs_risk - buffer_effectiveness
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "nbs_resilience_gap:", resilience_gap
end program nbs_resilience_gap
