package com.wearia.app.data.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class CategorieItem(
    val id: Int,
    val nom: String
) : Parcelable {
    override fun toString(): String = nom
}

@Parcelize
data class TypeVetementItem(
    val id: Int,
    val nom: String,
    val categorie_id: Int,
    val genre_cible: String,
    val est_couche_superieure: Boolean
) : Parcelable {
    override fun toString(): String = nom
}

@Parcelize
data class CouleurItem(
    val id: Int,
    val nom: String,
    val code_hex: String
) : Parcelable {
    override fun toString(): String = nom
}

@Parcelize
data class StyleItem(
    val id: Int,
    val libelle: String
) : Parcelable {
    override fun toString(): String = libelle
}
