package com.wearia.app.data.repositories

import com.wearia.app.data.local.SessionManager
import com.wearia.app.data.models.LoginRequest
import com.wearia.app.data.models.RegisterRequest
import com.wearia.app.data.models.TokenResponse
import com.wearia.app.data.remote.ApiService

class AuthRepository(
    private val apiService: ApiService,
    private val sessionManager: SessionManager
) {
    suspend fun login(email: String, motDePasse: String): Result<TokenResponse> {
        return try {
            val response = apiService.login(LoginRequest(email, motDePasse))
            if (response.isSuccessful && response.body() != null) {
                val tokenData = response.body()!!
                sessionManager.saveSession(
                    tokenData.access_token,
                    tokenData.user_id,
                    tokenData.nom,
                    tokenData.email
                )
                Result.success(tokenData)
            } else {
                Result.failure(Exception("Échec de connexion : identifiants invalides"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : impossible de joindre le serveur Wearia"))
        }
    }

    suspend fun register(nom: String, email: String, motDePasse: String, genre: String?, ville: String?): Result<TokenResponse> {
        return try {
            val response = apiService.register(RegisterRequest(nom, email, motDePasse, genre, ville))
            if (response.isSuccessful && response.body() != null) {
                val tokenData = response.body()!!
                sessionManager.saveSession(
                    tokenData.access_token,
                    tokenData.user_id,
                    tokenData.nom,
                    tokenData.email
                )
                Result.success(tokenData)
            } else {
                val errorMsg = response.errorBody()?.string() ?: "Erreur d'inscription"
                Result.failure(Exception(errorMsg))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau lors de l'inscription"))
        }
    }

    fun isLoggedIn(): Boolean = sessionManager.isLoggedIn()

    fun getUserName(): String = sessionManager.getUserName()

    fun logout() = sessionManager.clearSession()
}
