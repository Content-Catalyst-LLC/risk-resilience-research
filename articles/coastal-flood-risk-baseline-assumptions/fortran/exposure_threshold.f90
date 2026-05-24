program exposure_threshold
  implicit none

  real :: modeled_baseline, baseline_correction, sea_level_rise
  real :: tide_surge, uncertainty_margin, land_elevation, protection_height
  real :: water_height, threshold
  logical :: exposed

  modeled_baseline = 0.0
  baseline_correction = 0.30
  sea_level_rise = 0.45
  tide_surge = 0.55
  uncertainty_margin = 0.10
  land_elevation = 1.25
  protection_height = 0.20

  water_height = modeled_baseline + baseline_correction + sea_level_rise + tide_surge + uncertainty_margin
  threshold = land_elevation + protection_height
  exposed = water_height >= threshold

  print *, "Synthetic site exposed after baseline correction:", exposed
end program exposure_threshold
