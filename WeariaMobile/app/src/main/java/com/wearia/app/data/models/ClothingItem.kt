package com.wearia.app.data.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class ClothingItem(
    val id: Int,
    val user_id: Int,
    val nom: String,
    val photo_url: String,
    val type_vetement_id: Int,
    val categorie_id: Int,
    val couleur_id: Int,
    val style_id: Int?,
    val matiere: String?,
    val coupe: String?,
    val saison: String?,
    val est_thermique: Boolean,
    val est_impermeable: Boolean,
    var statut: String, // DISPONIBLE, SALE, EN_LAVAGE, INDISPONIBLE
    val categorie: CategorieItem? = null,
    val couleur: CouleurItem? = null,
    val type_vetement: TypeVetementItem? = null
) : Parcelable

data class ClothingCreateRequest(
    val nom: String,
    val photo_url: String,
    val type_vetement_id: Int,
    val categorie_id: Int,
    val couleur_id: Int,
    val style_id: Int? = null,
    val matiere: String? = "Coton",
    val coupe: String? = "REGULIERE",
    val saison: String? = "TOUTE_SAISON",
    val est_thermique: Boolean = false,
    val est_impermeable: Boolean = false,
    val statut: String = "DISPONIBLE"
)

data class ClothingUpdateRequest(
    val statut: String? = null,
    val nom: String? = null
)

data class ClassificationResponse(
    val category: String,
    val color: String,
    val confidence: Float,
    val image_url: String
)
