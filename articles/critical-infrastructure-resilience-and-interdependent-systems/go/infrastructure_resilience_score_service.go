package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	Criticality              float64 `json:"criticality"`
	HazardExposure           float64 `json:"hazard_exposure"`
	AssetFragility           float64 `json:"asset_fragility"`
	CyberPhysicalRisk        float64 `json:"cyber_physical_risk"`
	InterdependenceExposure  float64 `json:"interdependence_exposure"`
	Redundancy               float64 `json:"redundancy"`
	MaintenanceCapacity      float64 `json:"maintenance_capacity"`
	GovernanceCapacity       float64 `json:"governance_capacity"`
	RecoveryCapacity         float64 `json:"recovery_capacity"`
	BackupCapacity           float64 `json:"backup_capacity"`
	WorkforceReadiness       float64 `json:"workforce_readiness"`
	ServiceDemandUnderStress float64 `json:"service_demand_under_stress"`
	SocialVulnerability      float64 `json:"social_vulnerability"`
}

type Result struct {
	FailurePressure             float64 `json:"failure_pressure"`
	ResilienceCapacity          float64 `json:"resilience_capacity"`
	CascadingInfrastructureRisk  float64 `json:"cascading_infrastructure_risk"`
	ServiceContinuityGap         float64 `json:"service_continuity_gap"`
	RecoveryPriorityScore       float64 `json:"recovery_priority_score"`
}

func score(p Profile) Result {
	failurePressure := p.Criticality *
		p.HazardExposure *
		p.AssetFragility *
		(1 + 0.35*p.CyberPhysicalRisk)

	resilienceCapacity := 0.22*p.Redundancy +
		0.20*p.MaintenanceCapacity +
		0.18*p.GovernanceCapacity +
		0.18*p.RecoveryCapacity +
		0.12*p.BackupCapacity +
		0.10*p.WorkforceReadiness

	cascadingRisk := (failurePressure + p.InterdependenceExposure) *
		(1 + 0.30*p.SocialVulnerability) *
		(1 - 0.45*resilienceCapacity)

	serviceGap := math.Max(0, p.ServiceDemandUnderStress-resilienceCapacity)

	priority := cascadingRisk +
		0.35*serviceGap +
		0.25*p.Criticality +
		0.20*p.SocialVulnerability

	return Result{
		FailurePressure: failurePressure,
		ResilienceCapacity: resilienceCapacity,
		CascadingInfrastructureRisk: cascadingRisk,
		ServiceContinuityGap: serviceGap,
		RecoveryPriorityScore: priority,
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
