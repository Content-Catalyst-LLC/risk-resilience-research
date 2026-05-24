package main

import "fmt"

func IsExposed(
	modeledBaseline float64,
	baselineCorrection float64,
	seaLevelRise float64,
	tideSurge float64,
	uncertaintyMargin float64,
	landElevation float64,
	protectionHeight float64,
) bool {
	waterHeight := modeledBaseline + baselineCorrection + seaLevelRise + tideSurge + uncertaintyMargin
	threshold := landElevation + protectionHeight
	return waterHeight >= threshold
}

func main() {
	exposed := IsExposed(0.0, 0.30, 0.45, 0.55, 0.10, 1.25, 0.20)
	fmt.Printf("Synthetic site exposed after baseline correction: %t\n", exposed)
}
