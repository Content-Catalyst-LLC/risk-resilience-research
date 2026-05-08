package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	DisruptionSeverity           float64 `json:"disruption_severity"`
	RecoveryCapacity             float64 `json:"recovery_capacity"`
	RecoverySpeed                float64 `json:"recovery_speed"`
	EssentialFunctionRestoration float64 `json:"essential_function_restoration"`
	AdaptiveCapacity             float64 `json:"adaptive_capacity"`
	GovernanceCapacity           float64 `json:"governance_capacity"`
	LearningCapacity             float64 `json:"learning_capacity"`
	EcologicalBufferCapacity     float64 `json:"ecological_buffer_capacity"`
	SocialProtectionCapacity     float64 `json:"social_protection_capacity"`
	TransformationReadiness      float64 `json:"transformation_readiness"`
	StructuralUnsustainability   float64 `json:"structural_unsustainability"`
	JusticePressure              float64 `json:"justice_pressure"`
	MaladaptationRisk            float64 `json:"maladaptation_risk"`
	ResidualRisk                 float64 `json:"residual_risk"`
	PublicLegitimacy             float64 `json:"public_legitimacy"`
}

type Result struct {
	RecoveryScore                    float64 `json:"recovery_score"`
	AdaptationScore                  float64 `json:"adaptation_score"`
	TransformationNeed               float64 `json:"transformation_need"`
	TransformationScore              float64 `json:"transformation_score"`
	MaladaptationAdjustedPathwayGap   float64 `json:"maladaptation_adjusted_pathway_gap"`
	ClimateResilientDevelopmentScore float64 `json:"climate_resilient_development_score"`
}

func clamp01(x float64) float64 {
	return math.Max(0, math.Min(1, x))
}

func score(p Profile) Result {
	recovery := 0.38*p.RecoveryCapacity + 0.28*p.RecoverySpeed + 0.34*p.EssentialFunctionRestoration

	adaptation := 0.26*p.AdaptiveCapacity +
		0.22*p.GovernanceCapacity +
		0.18*p.LearningCapacity +
		0.18*p.EcologicalBufferCapacity +
		0.16*p.SocialProtectionCapacity

	transformationNeed := 0.36*p.StructuralUnsustainability +
		0.26*p.JusticePressure +
		0.22*p.ResidualRisk +
		0.16*p.MaladaptationRisk

	transformation := 0.34*p.TransformationReadiness +
		0.22*p.GovernanceCapacity +
		0.18*p.LearningCapacity +
		0.14*p.PublicLegitimacy +
		0.12*p.SocialProtectionCapacity

	responseCapacity := 0.28*recovery + 0.36*adaptation + 0.24*transformation + 0.12*p.PublicLegitimacy

	pathwayGap := math.Max(0, p.DisruptionSeverity+p.ResidualRisk-responseCapacity)
	maladaptationGap := pathwayGap * (1 + p.MaladaptationRisk)

	crdScore := clamp01(
		0.24*recovery +
			0.30*adaptation +
			0.26*transformation +
			0.12*p.PublicLegitimacy +
			0.08*(1-p.MaladaptationRisk),
	)

	return Result{
		RecoveryScore:                    recovery,
		AdaptationScore:                  adaptation,
		TransformationNeed:               transformationNeed,
		TransformationScore:              transformation,
		MaladaptationAdjustedPathwayGap:   maladaptationGap,
		ClimateResilientDevelopmentScore: crdScore,
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
