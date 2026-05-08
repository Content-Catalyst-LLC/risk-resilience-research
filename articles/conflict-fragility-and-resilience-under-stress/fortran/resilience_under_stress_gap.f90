program resilience_under_stress_gap
  implicit none

  real :: conflict_amplified_systemic_risk
  real :: service_breakdown_gap
  real :: legitimacy_erosion
  real :: governance_resilience
  real :: resilience_gap

  conflict_amplified_systemic_risk = 0.86
  service_breakdown_gap = 0.58
  legitimacy_erosion = 0.62
  governance_resilience = 0.34

  resilience_gap = conflict_amplified_systemic_risk + service_breakdown_gap + legitimacy_erosion - governance_resilience
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "resilience_under_stress_gap:", resilience_gap
end program resilience_under_stress_gap
