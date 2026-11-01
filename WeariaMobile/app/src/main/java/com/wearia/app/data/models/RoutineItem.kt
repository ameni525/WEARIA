package com.wearia.app.data.models

data class RoutineItem(
    val id: Int,
    val user_id: Int,
    val jour_semaine: String,
    var occasion: String,
    var est_active: Boolean
)

data class RoutineCreateRequest(
    val jour_semaine: String,
    val occasion: String = "UNIVERSITE",
    val est_active: Boolean = true
)
