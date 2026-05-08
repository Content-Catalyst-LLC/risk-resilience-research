program recovery_loss
  implicit none

  real :: baseline_function
  real :: minimum_function_after_shock
  real :: recovery_days
  real :: functional_loss_area

  baseline_function = 1.0
  minimum_function_after_shock = 0.38
  recovery_days = 90.0

  ! Linear recovery approximation:
  ! area = 0.5 * depth of disruption * recovery duration
  functional_loss_area = 0.5 * (baseline_function - minimum_function_after_shock) * recovery_days

  print *, "functional_loss_area:", functional_loss_area
end program recovery_loss
