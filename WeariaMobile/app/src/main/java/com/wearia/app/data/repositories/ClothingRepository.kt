package com.wearia.app.data.repositories

import com.wearia.app.data.models.*
import com.wearia.app.data.remote.ApiService
import okhttp3.MultipartBody

class ClothingRepository(private val apiService: ApiService) {

    suspend fun getClothes(
        categorieId: Int? = null,
        couleurId: Int? = null,
        saison: String? = null,
        statut: String? = null,
        search: String? = null
    ): Result<List<ClothingItem>> {
        return try {
            val response = apiService.getClothes(categorieId, couleurId, saison, statut, search)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Erreur de chargement du dressing"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun addClothing(request: ClothingCreateRequest): Result<ClothingItem> {
        return try {
            val response = apiService.addClothing(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                val err = response.errorBody()?.string() ?: "Erreur d'ajout"
                Result.failure(Exception(err))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun updateClothingStatus(clothingId: Int, newStatus: String): Result<ClothingItem> {
        return try {
            val response = apiService.updateClothing(clothingId, ClothingUpdateRequest(statut = newStatus))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Impossible de mettre à jour le statut"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun deleteClothing(clothingId: Int): Result<Unit> {
        return try {
            val response = apiService.deleteClothing(clothingId)
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Impossible de supprimer le vêtement"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur réseau : ${e.localizedMessage}"))
        }
    }

    suspend fun classifyImage(filePart: MultipartBody.Part): Result<ClassificationResponse> {
        return try {
            val response = apiService.classifyImage(filePart)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Échec de l'analyse IA de l'image"))
            }
        } catch (e: Exception) {
            Result.failure(Exception("Erreur lors de l'envoi de la photo à l'IA"))
        }
    }

    suspend fun getCategories(): Result<List<CategorieItem>> = try {
        val r = apiService.getCategories()
        if (r.isSuccessful && r.body() != null) Result.success(r.body()!!) else Result.failure(Exception("Erreur"))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getTypes(categorieId: Int? = null): Result<List<TypeVetementItem>> = try {
        val r = apiService.getTypes(categorieId)
        if (r.isSuccessful && r.body() != null) Result.success(r.body()!!) else Result.failure(Exception("Erreur"))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getColors(): Result<List<CouleurItem>> = try {
        val r = apiService.getColors()
        if (r.isSuccessful && r.body() != null) Result.success(r.body()!!) else Result.failure(Exception("Erreur"))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getStyles(): Result<List<StyleItem>> = try {
        val r = apiService.getStyles()
        if (r.isSuccessful && r.body() != null) Result.success(r.body()!!) else Result.failure(Exception("Erreur"))
    } catch (e: Exception) { Result.failure(e) }
}
