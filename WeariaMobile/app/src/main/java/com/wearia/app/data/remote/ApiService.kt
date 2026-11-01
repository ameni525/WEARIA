package com.wearia.app.data.remote

import com.wearia.app.data.models.*
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // --- AUTHENTIFICATION ---
    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<TokenResponse>

    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<TokenResponse>

    @GET("users/me")
    suspend fun getProfile(): Response<UserProfile>

    // --- RÉFÉRENTIELS ---
    @GET("referentials/categories")
    suspend fun getCategories(): Response<List<CategorieItem>>

    @GET("referentials/types")
    suspend fun getTypes(@Query("categorie_id") categorieId: Int? = null): Response<List<TypeVetementItem>>

    @GET("referentials/colors")
    suspend fun getColors(): Response<List<CouleurItem>>

    @GET("referentials/styles")
    suspend fun getStyles(): Response<List<StyleItem>>

    // --- CLOTHES (CRUD DRESSING) ---
    @GET("clothes")
    suspend fun getClothes(
        @Query("categorie_id") categorieId: Int? = null,
        @Query("couleur_id") couleurId: Int? = null,
        @Query("saison") saison: String? = null,
        @Query("statut") statut: String? = null,
        @Query("search") search: String? = null
    ): Response<List<ClothingItem>>

    @POST("clothes")
    suspend fun addClothing(@Body request: ClothingCreateRequest): Response<ClothingItem>

    @GET("clothes/{id}")
    suspend fun getClothingDetail(@Path("id") id: Int): Response<ClothingItem>

    @PUT("clothes/{id}")
    suspend fun updateClothing(
        @Path("id") id: Int,
        @Body request: ClothingUpdateRequest
    ): Response<ClothingItem>

    @DELETE("clothes/{id}")
    suspend fun deleteClothing(@Path("id") id: Int): Response<Unit>

    // --- IA & CLASSIFICATION ---
    @Multipart
    @POST("ai/classify")
    suspend fun classifyImage(@Part file: MultipartBody.Part): Response<ClassificationResponse>

    // --- ROUTINES HEBDOMADAIRES (BR09) ---
    @GET("routines")
    suspend fun getRoutines(): Response<List<RoutineItem>>

    @POST("routines")
    suspend fun saveRoutine(@Body request: RoutineCreateRequest): Response<RoutineItem>

    @DELETE("routines/{id}")
    suspend fun deleteRoutine(@Path("id") id: Int): Response<Unit>

    // --- RECOMMANDATIONS DE TENUES (BR01, BR02, BR03, BR08, BR09) ---
    @POST("recommendations")
    suspend fun getRecommendation(@Body request: OutfitRecommendationRequest): Response<OutfitRecommendationResponse>

    @POST("outfits/{id}/feedback")
    suspend fun submitFeedback(
        @Path("id") id: Int,
        @Body request: FeedbackRequest
    ): Response<Unit>
}
