package com.wearia.app.ui.auth

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.wearia.app.databinding.ActivityRegisterBinding
import com.wearia.app.ui.MainActivity
import com.wearia.app.viewmodel.AuthViewModel
import com.wearia.app.viewmodel.ViewModelFactory

class RegisterActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRegisterBinding
    private val viewModel: AuthViewModel by viewModels { ViewModelFactory(this) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
        observeViewModel()
    }

    private fun setupListeners() {
        binding.btnBack.setOnClickListener {
            finish()
        }

        binding.btnRegister.setOnClickListener {
            val name = binding.etName.text.toString().trim()
            val email = binding.etEmail.text.toString().trim()
            val password = binding.etPassword.text.toString().trim()
            val city = binding.etCity.text.toString().trim()

            if (name.isEmpty()) {
                binding.etName.error = "Nom obligatoire"
                return@setOnClickListener
            }
            if (email.isEmpty()) {
                binding.etEmail.error = "E-mail obligatoire"
                return@setOnClickListener
            }
            if (password.length < 8) {
                binding.etPassword.error = "Le mot de passe doit comporter au moins 8 caractères"
                return@setOnClickListener
            }

            viewModel.register(name, email, password, "FEMME", city)
        }

        binding.tvGoToLogin.setOnClickListener {
            finish()
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { loading ->
            binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
            binding.btnRegister.isEnabled = !loading
        }

        viewModel.authState.observe(this) { result ->
            result?.onSuccess {
                Toast.makeText(this, "Compte créé avec succès !", Toast.LENGTH_SHORT).show()
                val intent = Intent(this, MainActivity::class.java)
                startActivity(intent)
                finishAffinity()
            }?.onFailure { error ->
                Toast.makeText(this, error.localizedMessage ?: "Erreur d'inscription", Toast.LENGTH_LONG).show()
            }
        }
    }
}
