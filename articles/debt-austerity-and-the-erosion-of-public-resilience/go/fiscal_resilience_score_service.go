package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	DebtServiceBurden        float64 `json:"debt_service_burden"`
	RevenueCapacity         float64 `json:"revenue_capacity"`
	EssentialServiceSpending float64 `json:"essential_service_spending"`
	PublicInvestment        float64 `json:"public_investment"`
	MaintenanceCapacity     float64 `json:"maintenance_capacity"`
	AdaptationDRRSpending   float64 `json:"adaptation_drr_spending"`
	SocialProtectionCapacity float64 `json:"social_protection_capacity"`
	GovernanceCapacity      float64 `json:"governance_capacity"`
	LocalGovernmentCapacity float64 `json:"local_government_capacity"`
	EssentialServiceCuts    float64 `json:"essential_service_cuts"`
	PublicInvestmentCuts    float64 `json:"public_investment_cuts"`
	MaintenanceDeferral     float64 `json:"maintenance_deferral"`
	AdaptationDeferral      float64 `json:"adaptation_deferral"`
	SocialProtectionCuts    float64 `json:"social_protection_cuts"`
	PublicWorkforceStress   float64 `json:"public_workforce_stress"`
	SocialVulnerability     float64 `json:"social_vulnerability"`
	HazardExposure          float64 `json:"hazard_exposure"`
	InequalityPressure      float64 `json:"inequality_pressure"`
	PriorDeferredRisk       float64 `json:"prior_deferred_risk"`
}

type Result struct {
	DebtServicePressure     float64 `json:"debt_service_pressure"`
	PublicResilienceCapacity float64 `json:"public_resilience_capacity"`
	AusterityIntensity     float64 `json:"austerity_intensity"`
	FiscalResilienceRisk   float64 `json:"fiscal_resilience_risk"`
	DeferredRiskBurden     float64 `json:"deferred_risk_burden"`
	PublicResilienceGap    float64 `json:"public_resilience_gap"`
}

func clamp(value float64, lower float64, upper float64) float64 {
	return math.Max(lower, math.Min(upper, value))
}

func score(p Profile) Result {
	debtPressure := clamp(p.DebtServiceBurden/(0.20+p.RevenueCapacity), 0, 1.5)

	publicCapacity := 0.18*p.EssentialServiceSpending +
		0.16*p.PublicInvestment +
		0.15*p.MaintenanceCapacity +
		0.16*p.AdaptationDRRSpending +
		0.15*p.SocialProtectionCapacity +
		0.12*p.GovernanceCapacity +
		0.08*p.LocalGovernmentCapacity

	austerity := 0.20*p.EssentialServiceCuts +
		0.20*p.PublicInvestmentCuts +
		0.18*p.MaintenanceDeferral +
		0.18*p.AdaptationDeferral +
		0.16*p.SocialProtectionCuts +
		0.08*p.PublicWorkforceStress

	fiscalRisk := (debtPressure + austerity) *
		(1 + 0.35*p.SocialVulnerability) *
		(1 + 0.30*p.HazardExposure) *
		(1 + 0.25*p.InequalityPressure) *
		(1 - 0.45*publicCapacity)

	deferred := p.PriorDeferredRisk +
		0.40*austerity -
		0.20*p.PublicInvestment -
		0.20*p.MaintenanceCapacity -
		0.20*p.AdaptationDRRSpending
	deferred = clamp(deferred, 0, 1.5)

	gap := math.Max(0, fiscalRisk+deferred-publicCapacity)

	return Result{
		DebtServicePressure: debtPressure,
		PublicResilienceCapacity: publicCapacity,
		AusterityIntensity: austerity,
		FiscalResilienceRisk: fiscalRisk,
		DeferredRiskBurden: deferred,
		PublicResilienceGap: gap,
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
