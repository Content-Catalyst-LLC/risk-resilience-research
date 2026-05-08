package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	HazardPressure         float64 `json:"hazard_pressure"`
	Exposure               float64 `json:"exposure"`
	Vulnerability           float64 `json:"vulnerability"`
	ProtectiveCapacity     float64 `json:"protective_capacity"`
	Robustness              float64 `json:"robustness"`
	Redundancy              float64 `json:"redundancy"`
	AdaptiveCapacity        float64 `json:"adaptive_capacity"`
	RecoveryCapacity        float64 `json:"recovery_capacity"`
	TransformationCapacity  float64 `json:"transformation_capacity"`
	JusticeLegitimacy       float64 `json:"justice_legitimacy"`
}

type Result struct {
	RiskScore              float64 `json:"risk_score"`
	ResilienceCapacity    float64 `json:"resilience_capacity"`
	ResilienceAdjustedRisk float64 `json:"resilience_adjusted_risk"`
	JusticeAdjustedRisk   float64 `json:"justice_adjusted_risk"`
}

func clamp01(x float64) float64 {
	return math.Max(0, math.Min(1, x))
}

func score(p Profile) Result {
	risk := clamp01(p.HazardPressure * p.Exposure * p.Vulnerability * (1 - p.ProtectiveCapacity))

	resilience := clamp01(
		0.22*p.Robustness +
			0.20*p.Redundancy +
			0.22*p.AdaptiveCapacity +
			0.18*p.RecoveryCapacity +
			0.18*p.TransformationCapacity,
	)

	resilienceAdjusted := clamp01(risk / (1 + resilience))
	justiceAdjusted := clamp01(resilienceAdjusted * (1 - p.JusticeLegitimacy))

	return Result{
		RiskScore: risk,
		ResilienceCapacity: resilience,
		ResilienceAdjustedRisk: resilienceAdjusted,
		JusticeAdjustedRisk: justiceAdjusted,
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
