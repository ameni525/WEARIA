package com.wearia.app.ui

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import coil.load
import com.wearia.app.R
import com.wearia.app.data.local.SessionManager
import com.wearia.app.databinding.ActivityMainBinding
import com.wearia.app.ui.auth.LoginActivity
import com.wearia.app.ui.dressing.AddClothingActivity
import com.wearia.app.ui.dressing.WardrobeActivity
import com.wearia.app.ui.routine.RoutineActivity
import com.wearia.app.utils.Constants
import com.wearia.app.viewmodel.MainViewModel
import com.wearia.app.viewmodel.ViewModelFactory

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels { ViewModelFactory(this) }
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        sessionManager = SessionManager(this)

        setupUI()
        setupListeners()
        observeViewModel()

        viewModel.generateDailyOutfit()
    }

    private fun setupUI() {
        binding.tvGreeting.text = "Bonjour, ${sessionManager.getUserName()} 👋"
    }

    private fun setupListeners() {
        binding.btnLogout.setOnClickListener {
            AlertDialog.Builder(this)
                .setTitle("Déconnexion")
                .setMessage("Voulez-vous vraiment vous déconnecter de Wearia ?")
                .setIcon(android.R.drawable.ic_dialog_alert)
                .setPositiveButton("Oui") { _, _ ->
                    sessionManager.clearSession()
                    val intent = Intent(this, LoginActivity::class.java)
                    startActivity(intent)
                    finish()
                }
                .setNegativeButton("Annuler", null)
                .show()
        }

        binding.btnGenerateAnother.setOnClickListener {
            viewModel.generateDailyOutfit()
        }

        binding.btnLikeOutfit.setOnClickListener {
            val outfit = viewModel.outfit.value
            if (outfit != null && outfit.outfit_id != null) {
                viewModel.submitFeedback(outfit.outfit_id, "AIME")
            } else {
                Toast.makeText(this, "Tenue ajoutée à vos favoris !", Toast.LENGTH_SHORT).show()
            }
        }

        binding.cardWardrobe.setOnClickListener {
            startActivity(Intent(this, WardrobeActivity::class.java))
        }

        binding.cardAddClothing.setOnClickListener {
            startActivity(Intent(this, AddClothingActivity::class.java))
        }

        binding.cardRoutines.setOnClickListener {
            startActivity(Intent(this, RoutineActivity::class.java))
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { loading ->
            binding.pbOutfit.visibility = if (loading) View.VISIBLE else View.GONE
            binding.btnGenerateAnother.isEnabled = !loading
        }

        viewModel.message.observe(this) { msg ->
            if (!msg.isNullOrEmpty()) {
                Toast.makeText(this, msg, Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.outfit.observe(this) { outfit ->
            if (outfit == null) return@observe

            binding.tvScoreBadge.text = "Harmonie : ${outfit.score}%"
            binding.tvOccasionBadge.text = "Occasion : ${outfit.occasion}"
            binding.tvWeatherSummary.text = "☀️ ${outfit.temperature.toInt()}°C · ${outfit.weather}"

            // Afficher les photos des articles composant la tenue
            binding.llOutfitPhotos.removeAllViews()
            if (outfit.items.isEmpty()) {
                binding.tvOutfitItems.text = "Votre dressing est vide ou incomplet pour créer une tenue."
            } else {
                val inflater = LayoutInflater.from(this)
                for (item in outfit.items) {
                    val partView = inflater.inflate(R.layout.item_outfit_part, binding.llOutfitPhotos, false)
                    val iv = partView.findViewById<ImageView>(R.id.ivOutfitPart)
                    val tvName = partView.findViewById<TextView>(R.id.tvOutfitPartName)
                    val tvCat = partView.findViewById<TextView>(R.id.tvOutfitPartCategory)

                    tvName.text = item.name
                    tvCat.text = item.category

                    val fullPhotoUrl = Constants.getFullImageUrl(item.photo_url)
                    iv.load(fullPhotoUrl) {
                        crossfade(true)
                        placeholder(android.R.drawable.ic_menu_gallery)
                        error(android.R.drawable.ic_menu_gallery)
                    }

                    binding.llOutfitPhotos.addView(partView)
                }

                val sb = StringBuilder()
                for (item in outfit.items) {
                    sb.append("• ${item.name} (${item.color})\n")
                }
                binding.tvOutfitItems.text = sb.toString().trimEnd()
            }

            binding.tvOutfitExplanation.text = outfit.explanation
        }
    }

    override fun onResume() {
        super.onResume()
        viewModel.generateDailyOutfit()
    }
}
