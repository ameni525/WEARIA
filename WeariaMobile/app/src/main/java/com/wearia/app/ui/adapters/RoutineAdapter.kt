package com.wearia.app.ui.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.wearia.app.data.models.RoutineItem
import com.wearia.app.databinding.ItemRoutineBinding

class RoutineAdapter(
    private var items: MutableList<RoutineItem> = mutableListOf(),
    private val onDeleteClicked: (RoutineItem) -> Unit = {}
) : RecyclerView.Adapter<RoutineAdapter.RoutineViewHolder>() {

    inner class RoutineViewHolder(private val binding: ItemRoutineBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: RoutineItem) {
            binding.tvJourSemaine.text = item.jour_semaine
            binding.tvOccasion.text = "Occasion : ${item.occasion}"

            binding.btnDeleteRoutine.setOnClickListener {
                onDeleteClicked(item)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RoutineViewHolder {
        val binding = ItemRoutineBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return RoutineViewHolder(binding)
    }

    override fun onBindViewHolder(holder: RoutineViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount(): Int = items.size

    fun updateList(newList: List<RoutineItem>) {
        this.items = newList.toMutableList()
        notifyDataSetChanged()
    }
}
