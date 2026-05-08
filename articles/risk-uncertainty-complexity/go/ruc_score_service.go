package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	HazardProbability           float64 `json:"hazard_probability"`
	ExpectedLossIndex          float64 `json:"expected_loss_index"`
	ProbabilityUncertainty     float64 `json:"probability_uncertainty"`
	LossUncertainty            float64 `json:"loss_uncertainty"`
	DependencyDensity          float64 `json:"dependency_density"`
	FeedbackStrength           float64 `json:"feedback_strength"`
	ThresholdSensitivity       float64 `json:"threshold_sensitivity"`
	AdaptiveBehavior           float64 `json:"adaptive_behavior"`
	MonitoringCapacity         float64 `json:"monitoring_capacity"`
	RedundancyCapacity         float64 `json:"redundancy_capacity"`
	FlexibilityCapacity        float64 `json:"flexibility_capacity"`
	InstitutionalLearning      float64 `json:"institutional_learning"`
	AdaptiveGovernanceCapacity float64 `json:"adaptive_governance_capacity"`
	SocialVulnerability        float64 `json:"social_vulnerability"`
	CriticalityIndex           float64 `json:"criticality_index"`
}

type Result struct {
	ExpectedRisk            float64 `json:"expected_risk"`
	UncertaintyAdjustedRisk float64 `json:"uncertainty_adjusted_risk"`
	ComplexityMultiplier    float64 `json:"complexity_multiplier"`
	SystemicRisk            float64 `json:"systemic_risk"`
	RobustResponseCapacity  float64 `json:"robust_response_capacity"`
	ResilienceGap           float64 `json:"resilience_gap"`
}

func clamp01(x float64) float64 {
	return math.Max(0, math.Min(1, x))
}

func score(p Profile) Result {
	expectedRisk := p.HazardProbability * p.ExpectedLossIndex
	combinedUncertainty := (p.ProbabilityUncertainty + p.LossUncertainty) / 2
	uncertaintyAdjusted := expectedRisk * (1 + combinedUncertainty)

	complexityMultiplier := 1 +
		0.28*p.DependencyDensity +
		0.24*p.FeedbackStrength +
		0.24*p.ThresholdSensitivity +
		0.24*p.AdaptiveBehavior

	systemicRisk := uncertaintyAdjusted * complexityMultiplier *
		(1 + 0.30*p.SocialVulnerability) *
		(1 + 0.20*p.CriticalityIndex)

	responseCapacity := clamp01(
		0.22*p.MonitoringCapacity +
			0.20*p.RedundancyCapacity +
			0.18*p.FlexibilityCapacity +
			0.20*p.InstitutionalLearning +
			0.20*p.AdaptiveGovernanceCapacity,
	)

	gap := math.Max(0, systemicRisk-responseCapacity)

	return Result{
		ExpectedRisk:            expectedRisk,
		UncertaintyAdjustedRisk: uncertaintyAdjusted,
		ComplexityMultiplier:    complexityMultiplier,
		SystemicRisk:            systemicRisk,
		RobustResponseCapacity:  responseCapacity,
		ResilienceGap:           gap,
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
