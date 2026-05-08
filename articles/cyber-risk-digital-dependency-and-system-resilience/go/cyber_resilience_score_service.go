package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	DigitalCriticality             float64 `json:"digital_criticality"`
	ThreatPressure                float64 `json:"threat_pressure"`
	TechnicalVulnerabilityExposure float64 `json:"technical_vulnerability_exposure"`
	DependencyConcentration       float64 `json:"dependency_concentration"`
	IdentityAccessWeakness        float64 `json:"identity_access_weakness"`
	VendorSupplyChainExposure      float64 `json:"vendor_supply_chain_exposure"`
	OperationalTechnologyExposure  float64 `json:"operational_technology_exposure"`
	DataIntegrityRisk              float64 `json:"data_integrity_risk"`
	RecoveryCapacity              float64 `json:"recovery_capacity"`
	GovernanceCapacity            float64 `json:"governance_capacity"`
	BackupRedundancyCapacity      float64 `json:"backup_redundancy_capacity"`
	MonitoringMaturity            float64 `json:"monitoring_maturity"`
	LoggingMaturity               float64 `json:"logging_maturity"`
	IncidentExerciseMaturity      float64 `json:"incident_exercise_maturity"`
	UserVulnerability             float64 `json:"user_vulnerability"`
	CascadingDependencyExposure   float64 `json:"cascading_dependency_exposure"`
}

type Result struct {
	CyberDisruptionPressure  float64 `json:"cyber_disruption_pressure"`
	CyberResilienceCapacity  float64 `json:"cyber_resilience_capacity"`
	SystemicCyberRisk        float64 `json:"systemic_cyber_risk"`
	ServiceContinuityGap     float64 `json:"service_continuity_gap"`
	RecoveryPriorityScore    float64 `json:"recovery_priority_score"`
}

func score(p Profile) Result {
	disruptionPressure := p.DigitalCriticality *
		(0.18*p.ThreatPressure +
			0.16*p.TechnicalVulnerabilityExposure +
			0.15*p.DependencyConcentration +
			0.15*p.IdentityAccessWeakness +
			0.14*p.VendorSupplyChainExposure +
			0.12*p.OperationalTechnologyExposure +
			0.10*p.DataIntegrityRisk)

	resilienceCapacity := 0.20*p.RecoveryCapacity +
		0.18*p.GovernanceCapacity +
		0.17*p.BackupRedundancyCapacity +
		0.16*p.MonitoringMaturity +
		0.14*p.LoggingMaturity +
		0.15*p.IncidentExerciseMaturity

	systemicRisk := disruptionPressure *
		(1 + 0.35*p.DependencyConcentration) *
		(1 + 0.30*p.UserVulnerability) *
		(1 - 0.45*resilienceCapacity)

	serviceGap := math.Max(
		0,
		p.DigitalCriticality+systemicRisk+0.50*p.CascadingDependencyExposure-resilienceCapacity,
	)

	priority := serviceGap +
		0.30*p.DigitalCriticality +
		0.25*p.UserVulnerability +
		0.25*p.CascadingDependencyExposure

	return Result{
		CyberDisruptionPressure: disruptionPressure,
		CyberResilienceCapacity: resilienceCapacity,
		SystemicCyberRisk: systemicRisk,
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
