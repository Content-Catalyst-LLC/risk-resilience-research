package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	ConflictIntensity          float64 `json:"conflict_intensity"`
	GovernanceCapacity         float64 `json:"governance_capacity"`
	ServiceContinuity          float64 `json:"service_continuity"`
	InstitutionalLegitimacy    float64 `json:"institutional_legitimacy"`
	AdministrativeReach        float64 `json:"administrative_reach"`
	RecoveryCapacity           float64 `json:"recovery_capacity"`
	SocialVulnerability         float64 `json:"social_vulnerability"`
	DisplacementPressure       float64 `json:"displacement_pressure"`
	LivelihoodStress           float64 `json:"livelihood_stress"`
	HazardExposure             float64 `json:"hazard_exposure"`
	EssentialServiceDemand     float64 `json:"essential_service_demand"`
	InequalityPressure         float64 `json:"inequality_pressure"`
	InstitutionalExclusion     float64 `json:"institutional_exclusion"`
	PublicTrust                float64 `json:"public_trust"`
	RepeatedDisruptionPressure float64 `json:"repeated_disruption_pressure"`
}

type Result struct {
	FragilityPressure              float64 `json:"fragility_pressure"`
	GovernanceResilience           float64 `json:"governance_resilience"`
	ConflictAmplifiedSystemicRisk  float64 `json:"conflict_amplified_systemic_risk"`
	ServiceBreakdownGap            float64 `json:"service_breakdown_gap"`
	LegitimacyErosion              float64 `json:"legitimacy_erosion"`
	ResilienceUnderStressGap       float64 `json:"resilience_under_stress_gap"`
}

func score(p Profile) Result {
	fragility := 0.24*p.ConflictIntensity +
		0.20*p.SocialVulnerability +
		0.18*p.DisplacementPressure +
		0.18*p.LivelihoodStress +
		0.20*p.HazardExposure

	governance := 0.24*p.GovernanceCapacity +
		0.22*p.ServiceContinuity +
		0.20*p.InstitutionalLegitimacy +
		0.18*p.AdministrativeReach +
		0.16*p.RecoveryCapacity

	systemicRisk := fragility *
		(1 + 0.45*p.ConflictIntensity) *
		(1 - 0.35*governance)

	serviceGap := math.Max(0, p.EssentialServiceDemand-p.ServiceContinuity)

	legitimacy := 0.30*serviceGap +
		0.26*p.InequalityPressure +
		0.24*p.InstitutionalExclusion +
		0.15*p.RepeatedDisruptionPressure -
		0.20*p.PublicTrust
	legitimacy = math.Max(0, math.Min(1.5, legitimacy))

	resilienceGap := math.Max(0, systemicRisk+serviceGap+legitimacy-governance)

	return Result{
		FragilityPressure: fragility,
		GovernanceResilience: governance,
		ConflictAmplifiedSystemicRisk: systemicRisk,
		ServiceBreakdownGap: serviceGap,
		LegitimacyErosion: legitimacy,
		ResilienceUnderStressGap: resilienceGap,
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
