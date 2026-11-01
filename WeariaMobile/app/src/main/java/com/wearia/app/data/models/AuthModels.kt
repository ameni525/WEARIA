package com.wearia.app.data.models

data class LoginRequest(
    val email: String,
    val mot_de_passe: String
)

data class RegisterRequest(
    val nom: String,
    val email: String,
    val mot_de_passe: String,
    val genre: String? = "FEMME",
    val ville: String? = "Tunis"
)

data class TokenResponse(
    val access_token: String,
    val token_type: String,
    val user_id: Int,
    val nom: String,
    val email: String
)

data class UserProfile(
    val id: Int,
    val nom: String,
    val email: String,
    val genre: String?,
    val ville: String?,
    val taille_vestimentaire: String?,
    val coupe_preferee: String?
)
