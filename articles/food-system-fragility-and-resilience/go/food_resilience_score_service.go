package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	ProductionStress          float64 `json:"production_stress"`
	WaterStress               float64 `json:"water_stress"`
	EcologicalDegradation     float64 `json:"ecological_degradation"`
	LogisticsFragility        float64 `json:"logistics_fragility"`
	InputDependency           float64 `json:"input_dependency"`
	PriceVolatility           float64 `json:"price_volatility"`
	HouseholdVulnerability    float64 `json:"household_vulnerability"`
	InequalityPressure        float64 `json:"inequality_pressure"`
	SocialProtectionCapacity  float64 `json:"social_protection_capacity"`
	NutritionalAdequacy       float64 `json:"nutritional_adequacy"`
	FoodSystemDiversity       float64 `json:"food_system_diversity"`
	EcologicalBufferCondition float64 `json:"ecological_buffer_condition"`
	GovernanceCapacity        float64 `json:"governance_capacity"`
	MarketAccessReliability  float64 `json:"market_access_reliability"`
	StorageCapacity           float64 `json:"storage_capacity"`
	TradeDependency           float64 `json:"trade_dependency"`
	CrossSectorLinkage        float64 `json:"cross_sector_linkage"`
}

type Result struct {
	FoodSystemFragility      float64 `json:"food_system_fragility"`
	FoodAccessVulnerability float64 `json:"food_access_vulnerability"`
	ResilienceCapacity      float64 `json:"resilience_capacity"`
	CascadingFoodRisk       float64 `json:"cascading_food_risk"`
	JusticeWeightedFoodRisk float64 `json:"justice_weighted_food_risk"`
	FoodResilienceGap       float64 `json:"food_resilience_gap"`
}

func score(p Profile) Result {
	fragility := 0.20*p.ProductionStress +
		0.18*p.WaterStress +
		0.18*p.EcologicalDegradation +
		0.16*p.LogisticsFragility +
		0.14*p.InputDependency +
		0.14*p.PriceVolatility

	access := 0.24*p.HouseholdVulnerability +
		0.22*p.PriceVolatility +
		0.20*p.InequalityPressure +
		0.18*(1-p.SocialProtectionCapacity) +
		0.16*(1-p.NutritionalAdequacy)

	resilience := 0.20*p.FoodSystemDiversity +
		0.18*p.EcologicalBufferCondition +
		0.18*p.SocialProtectionCapacity +
		0.16*p.GovernanceCapacity +
		0.14*p.MarketAccessReliability +
		0.14*p.StorageCapacity

	cascade := (fragility + access) *
		(1 + 0.30*p.TradeDependency) *
		(1 + 0.30*p.CrossSectorLinkage)

	justice := cascade * (1 + 0.35*p.InequalityPressure)
	gap := math.Max(0, justice-resilience)

	return Result{
		FoodSystemFragility: fragility,
		FoodAccessVulnerability: access,
		ResilienceCapacity: resilience,
		CascadingFoodRisk: cascade,
		JusticeWeightedFoodRisk: justice,
		FoodResilienceGap: gap,
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
