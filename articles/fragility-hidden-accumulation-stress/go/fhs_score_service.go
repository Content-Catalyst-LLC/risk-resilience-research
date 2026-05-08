package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	VisiblePerformance       float64 `json:"visible_performance"`
	StressAccumulation      float64 `json:"stress_accumulation"`
	BufferErosion           float64 `json:"buffer_erosion"`
	DeferredMaintenance     float64 `json:"deferred_maintenance"`
	InstitutionalDrift      float64 `json:"institutional_drift"`
	SignalNormalization     float64 `json:"signal_normalization"`
	StandardErosion         float64 `json:"standard_erosion"`
	ThresholdProximity      float64 `json:"threshold_proximity"`
	AdaptationDebt          float64 `json:"adaptation_debt"`
	EcologicalSupportErosion float64 `json:"ecological_support_erosion"`
	SocialStrain            float64 `json:"social_strain"`
	TrustErosion            float64 `json:"trust_erosion"`
	MonitoringCapacity      float64 `json:"monitoring_capacity"`
	ResponseCapacity        float64 `json:"response_capacity"`
	JusticePressure         float64 `json:"justice_pressure"`
	SystemCriticality       float64 `json:"system_criticality"`
}

type Result struct {
	HiddenStressIndex        float64 `json:"hidden_stress_index"`
	DriftIndex              float64 `json:"drift_index"`
	LatentInstability       float64 `json:"latent_instability"`
	ResilienceMargin        float64 `json:"resilience_margin"`
	JusticeWeightedFragility float64 `json:"justice_weighted_fragility"`
	ResilienceGap           float64 `json:"resilience_gap"`
}

func score(p Profile) Result {
	hiddenStress := 0.20*p.StressAccumulation +
		0.16*p.BufferErosion +
		0.14*p.DeferredMaintenance +
		0.13*p.AdaptationDebt +
		0.12*p.EcologicalSupportErosion +
		0.13*p.SocialStrain +
		0.12*p.TrustErosion

	drift := 0.34*p.InstitutionalDrift +
		0.30*p.SignalNormalization +
		0.22*p.StandardErosion +
		0.14*(1-p.MonitoringCapacity)

	latentInstability := 0.38*p.ThresholdProximity +
		0.26*hiddenStress +
		0.20*drift +
		0.16*p.SystemCriticality

	resilienceMargin := 0.34*(1-p.BufferErosion) +
		0.24*p.MonitoringCapacity +
		0.24*p.ResponseCapacity +
		0.18*(1-p.ThresholdProximity)

	performanceMisalignment := math.Max(0, p.VisiblePerformance-(1-hiddenStress))

	fragility := (0.32*hiddenStress +
		0.24*drift +
		0.24*latentInstability +
		0.20*performanceMisalignment) *
		(1 + 0.25*p.SystemCriticality)

	justiceWeighted := fragility * (1 + 0.35*p.JusticePressure)
	gap := math.Max(0, justiceWeighted-resilienceMargin)

	return Result{
		HiddenStressIndex:         hiddenStress,
		DriftIndex:               drift,
		LatentInstability:        latentInstability,
		ResilienceMargin:         resilienceMargin,
		JusticeWeightedFragility: justiceWeighted,
		ResilienceGap:            gap,
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
