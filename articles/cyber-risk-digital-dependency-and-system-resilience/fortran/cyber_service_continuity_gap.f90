program cyber_service_continuity_gap
  implicit none

  real :: digital_criticality
  real :: systemic_cyber_risk
  real :: cascading_dependency_exposure
  real :: cyber_resilience_capacity
  real :: continuity_gap

  digital_criticality = 0.96
  systemic_cyber_risk = 0.72
  cascading_dependency_exposure = 0.54
  cyber_resilience_capacity = 0.38

  continuity_gap = digital_criticality + systemic_cyber_risk + 0.50 * cascading_dependency_exposure - cyber_resilience_capacity
  if (continuity_gap < 0.0) continuity_gap = 0.0

  print *, "service_continuity_gap:", continuity_gap
end program cyber_service_continuity_gap
