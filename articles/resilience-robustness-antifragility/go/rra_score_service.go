package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	StressIntensity          float64 `json:"stress_intensity"`
	StressVariability        float64 `json:"stress_variability"`
	SystemCriticality         float64 `json:"system_criticality"`
	RobustnessCapacity       float64 `json:"robustness_capacity"`
	RecoveryCapacity         float64 `json:"recovery_capacity"`
	AdaptiveCapacity         float64 `json:"adaptive_capacity"`
	RedundancyCapacity       float64 `json:"redundancy_capacity"`
	ModularityCapacity       float64 `json:"modularity_capacity"`
	MonitoringCapacity       float64 `json:"monitoring_capacity"`
	LearningCapacity         float64 `json:"learning_capacity"`
	ExperimentationCapacity  float64 `json:"experimentation_capacity"`
	OptionalityCapacity      float64 `json:"optionality_capacity"`
	FailureContainment       float64 `json:"failure_containment"`
	HarmBoundingCapacity     float64 `json:"harm_bounding_capacity"`
	JusticeSafeguardCapacity float64 `json:"justice_safeguard_capacity"`
}

type Result struct {
	StressLoad                  float64 `json:"stress_load"`
	RobustnessScore             float64 `json:"robustness_score"`
	ResilienceScore             float64 `json:"resilience_score"`
	BoundedAntifragilityScore   float64 `json:"bounded_antifragility_score"`
	BrittlenessRisk             float64 `json:"brittleness_risk"`
	SustainableResilienceScore  float64 `json:"sustainable_resilience_score"`
	SystemResponseGap           float64 `json:"system_response_gap"`
}

func clamp01(x float64) float64 {
	return math.Max(0, math.Min(1, x))
}

func score(p Profile) Result {
	stressLoad := p.StressIntensity * (1 + 0.5*p.StressVariability) * (1 + 0.4*p.SystemCriticality)

	robustness := p.RobustnessCapacity

	resilience := 0.23*p.RecoveryCapacity +
		0.22*p.AdaptiveCapacity +
		0.18*p.RedundancyCapacity +
		0.16*p.ModularityCapacity +
		0.11*p.MonitoringCapacity +
		0.10*p.FailureContainment

	antifragilityPotential := 0.24*p.LearningCapacity +
		0.22*p.ExperimentationCapacity +
		0.20*p.OptionalityCapacity +
		0.16*p.ModularityCapacity +
		0.10*p.FailureContainment +
		0.08*p.MonitoringCapacity

	ethicalLimit := 0.42*p.HarmBoundingCapacity +
		0.36*p.JusticeSafeguardCapacity +
		0.22*p.FailureContainment

	boundedAntifragility := antifragilityPotential * ethicalLimit

	brittleness := math.Max(
		0,
		stressLoad-(0.42*robustness+0.38*resilience+0.20*ethicalLimit),
	)

	sustainableResilience := clamp01(
		0.30*robustness +
			0.42*resilience +
			0.18*boundedAntifragility +
			0.10*p.JusticeSafeguardCapacity,
	)

	gap := math.Max(0, stressLoad-sustainableResilience)

	return Result{
		StressLoad:                 stressLoad,
		RobustnessScore:            robustness,
		ResilienceScore:            resilience,
		BoundedAntifragilityScore:  boundedAntifragility,
		BrittlenessRisk:            brittleness,
		SustainableResilienceScore: sustainableResilience,
		SystemResponseGap:          gap,
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
