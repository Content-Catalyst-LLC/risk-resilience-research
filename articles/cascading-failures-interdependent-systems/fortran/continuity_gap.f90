program continuity_gap
  implicit none

  real :: cascade_amplification
  real :: essential_function_continuity
  real :: gap

  cascade_amplification = 1.42
  essential_function_continuity = 0.44

  gap = cascade_amplification - essential_function_continuity
  if (gap < 0.0) gap = 0.0

  print *, "continuity_gap:", gap
end program continuity_gap
