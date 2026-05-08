program public_resilience_gap
  implicit none

  real :: fiscal_resilience_risk
  real :: deferred_risk_burden
  real :: public_resilience_capacity
  real :: resilience_gap

  fiscal_resilience_risk = 1.45
  deferred_risk_burden = 0.77
  public_resilience_capacity = 0.36

  resilience_gap = fiscal_resilience_risk + deferred_risk_burden - public_resilience_capacity
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "public_resilience_gap:", resilience_gap
end program public_resilience_gap
