package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	Connectedness             float64 `json:"connectedness"`
	Rigidity                  float64 `json:"rigidity"`
	ResilienceCapacity        float64 `json:"resilience_capacity"`
	ReleasePressure           float64 `json:"release_pressure"`
	ReorganizationCapacity    float64 `json:"reorganization_capacity"`
	NoveltyPotential          float64 `json:"novelty_potential"`
	MemoryCapacity            float64 `json:"memory_capacity"`
	RevoltPressure            float64 `json:"revolt_pressure"`
	CrossScaleDependency      float64 `json:"cross_scale_dependency"`
	InequalityPressure        float64 `json:"inequality_pressure"`
	InstitutionalLearning     float64 `json:"institutional_learning"`
	EcologicalBufferCondition float64 `json:"ecological_buffer_condition"`
	GovernanceFlexibility     float64 `json:"governance_flexibility"`
	SystemCriticality         float64 `json:"system_criticality"`
}

type Result struct {
	ConservationRigidity       float64 `json:"conservation_rigidity_index"`
	ReleaseRisk               float64 `json:"release_risk_index"`
	ReorganizationPotential    float64 `json:"reorganization_potential_index"`
	RememberCapacity           float64 `json:"remember_capacity"`
	RevoltCascadePressure      float64 `json:"revolt_cascade_pressure"`
	ResilienceTrapIndex        float64 `json:"resilience_trap_index"`
	TransformationReadiness    float64 `json:"transformation_readiness"`
	ReorganizationGap          float64 `json:"justice_weighted_reorganization_gap"`
}

func score(p Profile) Result {
	rigidity := 0.34*p.Connectedness + 0.34*p.Rigidity + 0.18*p.CrossScaleDependency + 0.14*(1-p.GovernanceFlexibility)
	release := 0.34*p.ReleasePressure + 0.24*rigidity + 0.18*p.RevoltPressure + 0.14*p.SystemCriticality + 0.10*p.InequalityPressure
	reorg := 0.28*p.ReorganizationCapacity + 0.22*p.NoveltyPotential + 0.18*p.MemoryCapacity + 0.16*p.InstitutionalLearning + 0.16*p.GovernanceFlexibility
	remember := 0.34*p.MemoryCapacity + 0.24*p.InstitutionalLearning + 0.22*p.EcologicalBufferCondition + 0.20*p.GovernanceFlexibility
	revolt := p.RevoltPressure * (1 + p.CrossScaleDependency) * (1 + 0.35*p.SystemCriticality) * (1 - 0.35*remember)
	trap := 0.32*rigidity + 0.24*(1-p.ReorganizationCapacity) + 0.18*(1-p.NoveltyPotential) + 0.16*p.InequalityPressure + 0.10*p.SystemCriticality
	transform := 0.28*reorg + 0.24*p.ResilienceCapacity + 0.18*p.InstitutionalLearning + 0.16*p.EcologicalBufferCondition + 0.14*p.GovernanceFlexibility
	gap := math.Max(0, (0.32*release+0.26*revolt+0.22*trap+0.20*p.InequalityPressure)*(1+0.30*p.InequalityPressure)-transform)

	return Result{
		ConservationRigidity:    rigidity,
		ReleaseRisk:             release,
		ReorganizationPotential: reorg,
		RememberCapacity:        remember,
		RevoltCascadePressure:   revolt,
		ResilienceTrapIndex:     trap,
		TransformationReadiness: transform,
		ReorganizationGap:       gap,
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
