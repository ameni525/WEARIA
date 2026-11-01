package com.wearia.app.data.repositories

import com.wearia.app.data.models.FeedbackRequest
import com.wearia.app.data.models.OutfitRecommendationRequest
import com.wearia.app.data.models.OutfitRecommendationResponse
import com.wearia.app.data.remote.ApiService

class RecommendationRepository(private val apiService: ApiService) {

    suspend fun getDailyRecommendation(
        occasion: String? = null,
        tempCelsius: Float = 19.0f,
        isRaining: Boolean = false,
        weatherDesc: String = "Ensoleillé"
    ): Result<OutfitRecommendationResponse> {
        return try {
            val req = OutfitRecommendationRequest(
                occasion = occasion,
                temperature_celsius = tempCelsius,
                precipitations = isRaining,
                description_meteo = weatherDesc
            )
            val response = apiService.getRecommendation(req)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Impossible de générer une recommandation"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun sendFeedback(outfitId: Int, appreciation: String): Result<Unit> {
        return try {
            val response = apiService.submitFeedback(outfitId, FeedbackRequest(appreciation))
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Échec de l'envoi du feedback"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau"))
        }
    }
}
