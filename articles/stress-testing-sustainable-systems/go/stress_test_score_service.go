package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	BaselineCapacity        float64 `json:"baseline_capacity"`
	HazardIntensity         float64 `json:"hazard_intensity"`
	Exposure                float64 `json:"exposure"`
	SocialVulnerability     float64 `json:"social_vulnerability"`
	InterdependenceExposure float64 `json:"interdependence_exposure"`
	Redundancy              float64 `json:"redundancy"`
	RecoveryCapacity        float64 `json:"recovery_capacity"`
	GovernanceCapacity      float64 `json:"governance_capacity"`
	MonitoringMaturity      float64 `json:"monitoring_maturity"`
	ThresholdLevel          float64 `json:"threshold_level"`
}

type Result struct {
	StressLoad              float64 `json:"stress_load"`
	ResilienceCapacity      float64 `json:"resilience_capacity"`
	FailurePressure         float64 `json:"failure_pressure"`
	ThresholdProximity      float64 `json:"threshold_proximity"`
	ServiceContinuityGap    float64 `json:"service_continuity_gap"`
	StressTestPriorityScore float64 `json:"stress_test_priority_score"`
}

func clamp(value float64, lower float64, upper float64) float64 {
	return math.Max(lower, math.Min(upper, value))
}

func score(p Profile) Result {
	stressLoad := p.HazardIntensity *
		p.Exposure *
		(1 + 0.35*p.SocialVulnerability) *
		(1 + 0.30*p.InterdependenceExposure)

	resilienceCapacity := 0.24*p.BaselineCapacity +
		0.20*p.Redundancy +
		0.20*p.RecoveryCapacity +
		0.18*p.GovernanceCapacity +
		0.18*p.MonitoringMaturity

	failurePressure := stressLoad * (1 - 0.45*resilienceCapacity)

	thresholdProximity := stressLoad / (0.20 + p.ThresholdLevel + resilienceCapacity)
	thresholdProximity = clamp(thresholdProximity, 0, 1.5)

	serviceGap := math.Max(0, stressLoad-resilienceCapacity)

	priority := serviceGap +
		0.35*thresholdProximity +
		0.25*p.SocialVulnerability +
		0.25*p.InterdependenceExposure

	return Result{
		StressLoad: stressLoad,
		ResilienceCapacity: resilienceCapacity,
		FailurePressure: failurePressure,
		ThresholdProximity: thresholdProximity,
		ServiceContinuityGap: serviceGap,
		StressTestPriorityScore: priority,
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	var profile Profile
	if err := json.NewDecoder(r.Body).Decode(&profile); err != nil {
		http.Error(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(score(profile))
}

func main() {
	http.HandleFunc("/score", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
