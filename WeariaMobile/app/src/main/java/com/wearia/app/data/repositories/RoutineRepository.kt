package com.wearia.app.data.repositories

import com.wearia.app.data.models.RoutineCreateRequest
import com.wearia.app.data.models.RoutineItem
import com.wearia.app.data.remote.ApiService

class RoutineRepository(private val apiService: ApiService) {

    suspend fun getRoutines(): Result<List<RoutineItem>> {
        return try {
            val response = apiService.getRoutines()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Erreur de récupération des routines"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun saveRoutine(jourSemaine: String, occasion: String): Result<RoutineItem> {
        return try {
            val response = apiService.saveRoutine(RoutineCreateRequest(jour_semaine = jourSemaine, occasion = occasion))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Erreur lors de l'enregistrement de la routine"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun deleteRoutine(id: Int): Result<Unit> {
        return try {
            val response = apiService.deleteRoutine(id)
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Erreur de suppression de la routine"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }
}
