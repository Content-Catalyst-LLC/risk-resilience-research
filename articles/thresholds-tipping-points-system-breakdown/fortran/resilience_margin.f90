program resilience_margin
  implicit none

  real :: resilience_margin_score
  real :: buffer_capacity
  real :: monitoring_capacity
  real :: governance_readiness
  real :: effective_margin

  resilience_margin_score = 0.34
  buffer_capacity = 0.38
  monitoring_capacity = 0.42
  governance_readiness = 0.46

  effective_margin = 0.42 * resilience_margin_score + &
                     0.24 * buffer_capacity + &
                     0.18 * monitoring_capacity + &
                     0.16 * governance_readiness

  print *, "effective_margin:", effective_margin
end program resilience_margin
