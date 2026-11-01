package com.wearia.app.ui.adapters

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.wearia.app.data.models.ClothingItem
import com.wearia.app.databinding.ItemClothingBinding
import com.wearia.app.utils.Constants

class ClothingAdapter(
    private var items: MutableList<ClothingItem> = mutableListOf(),
    private val onItemClicked: (ClothingItem) -> Unit = {},
    private val onItemLongClicked: (ClothingItem) -> Boolean = { false }
) : RecyclerView.Adapter<ClothingAdapter.ClothingViewHolder>() {

    inner class ClothingViewHolder(private val binding: ItemClothingBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: ClothingItem) {
            binding.tvClothingName.text = item.nom
            binding.tvClothingCategory.text = item.categorie?.nom ?: "Catégorie"
            binding.tvClothingColor.text = item.couleur?.nom ?: "Couleur"

            binding.tvClothingStatus.text = item.statut
            if (item.statut == "DISPONIBLE") {
                binding.tvClothingStatus.setTextColor(Color.parseColor("#16A34A"))
            } else {
                binding.tvClothingStatus.setTextColor(Color.parseColor("#DC2626"))
            }

            // Chargement de la photo avec Coil
            val fullUrl = Constants.getFullImageUrl(item.photo_url)
            binding.ivClothingPhoto.load(fullUrl) {
                crossfade(true)
                placeholder(android.R.drawable.ic_menu_gallery)
                error(android.R.drawable.ic_menu_report_image)
            }

            // Gestion des clics comme étudiée en cours (Chapitre 4 / TP4)
            binding.root.setOnClickListener { onItemClicked(item) }
            binding.root.setOnLongClickListener { onItemLongClicked(item) }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ClothingViewHolder {
        val binding = ItemClothingBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ClothingViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ClothingViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount(): Int = items.size

    fun updateList(newList: List<ClothingItem>) {
        this.items = newList.toMutableList()
        notifyDataSetChanged()
    }
}
