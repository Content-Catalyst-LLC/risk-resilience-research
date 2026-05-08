package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	StressLoad                float64 `json:"stress_load"`
	StressRate                float64 `json:"stress_rate"`
	ResilienceMargin          float64 `json:"resilience_margin"`
	BufferCapacity            float64 `json:"buffer_capacity"`
	MonitoringCapacity        float64 `json:"monitoring_capacity"`
	FeedbackDestabilization   float64 `json:"feedback_destabilization"`
	ThresholdProximity        float64 `json:"threshold_proximity"`
	InterdependencyDensity    float64 `json:"interdependency_density"`
	CascadeExposure           float64 `json:"cascade_exposure"`
	GovernanceReadiness       float64 `json:"governance_readiness"`
	RecoveryCapacity          float64 `json:"recovery_capacity"`
	SocialVulnerability       float64 `json:"social_vulnerability"`
	JusticePressure           float64 `json:"justice_pressure"`
	SystemCriticality         float64 `json:"system_criticality"`
	RegimeShiftReversibility  float64 `json:"regime_shift_reversibility"`
}

type Result struct {
	EffectiveMargin              float64 `json:"effective_margin"`
	ThresholdPressure            float64 `json:"threshold_pressure"`
	TippingPressure              float64 `json:"tipping_pressure"`
	RegimeShiftLikelihood        float64 `json:"regime_shift_likelihood"`
	CascadePotential             float64 `json:"cascade_potential"`
	JusticeWeightedBreakdownRisk float64 `json:"justice_weighted_breakdown_risk"`
	ResilienceGap                float64 `json:"resilience_gap"`
}

func clamp(x, low, high float64) float64 {
	return math.Max(low, math.Min(high, x))
}

func score(p Profile) Result {
	margin := 0.42*p.ResilienceMargin + 0.24*p.BufferCapacity + 0.18*p.MonitoringCapacity + 0.16*p.GovernanceReadiness

	thresholdPressure := 0.34*p.StressLoad + 0.22*p.StressRate + 0.26*p.ThresholdProximity + 0.18*p.FeedbackDestabilization

	tipping := thresholdPressure *
		(1 + 0.35*p.FeedbackDestabilization) *
		(1 + 0.25*p.StressRate) *
		(1 - 0.45*margin)

	regimeShift := clamp(
		0.34*tipping+
			0.26*p.ThresholdProximity+
			0.20*p.FeedbackDestabilization+
			0.20*(1-p.RegimeShiftReversibility),
		0,
		1.5,
	)

	cascade := regimeShift *
		(1 + p.InterdependencyDensity) *
		(1 + 0.5*p.CascadeExposure) *
		(1 + 0.35*p.SystemCriticality)

	recoveryDifficulty := clamp(
		0.32*regimeShift+
			0.24*(1-p.RecoveryCapacity)+
			0.22*(1-p.RegimeShiftReversibility)+
			0.22*p.SocialVulnerability,
		0,
		1.5,
	)

	breakdownRisk := 0.34*regimeShift + 0.28*clamp(cascade, 0, 1.5) + 0.20*recoveryDifficulty + 0.18*p.SocialVulnerability
	justiceWeighted := breakdownRisk * (1 + 0.35*p.JusticePressure)
	gap := math.Max(0, justiceWeighted-margin)

	return Result{
		EffectiveMargin:              margin,
		ThresholdPressure:            thresholdPressure,
		TippingPressure:              tipping,
		RegimeShiftLikelihood:        regimeShift,
		CascadePotential:             cascade,
		JusticeWeightedBreakdownRisk: justiceWeighted,
		ResilienceGap:                gap,
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
