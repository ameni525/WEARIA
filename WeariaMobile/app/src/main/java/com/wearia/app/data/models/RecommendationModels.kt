package com.wearia.app.data.models

data class OutfitItem(
    val id: Int,
    val name: String,
    val category: String,
    val color: String,
    val photo_url: String
)

data class OutfitRecommendationRequest(
    val occasion: String? = null,
    val temperature_celsius: Float = 19.0f,
    val precipitations: Boolean = false,
    val description_meteo: String = "Ensoleillé"
)

data class OutfitRecommendationResponse(
    val outfit_id: Int?,
    val occasion: String,
    val temperature: Float,
    val weather: String,
    val items: List<OutfitItem>,
    val score: Int,
    val explanation: String
)

data class FeedbackRequest(
    val appreciation: String, // AIME, MOYEN, PAS_POUR_MOI
    val motif_rejet: String? = null
)
