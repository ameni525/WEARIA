package com.wearia.app.ui.auth

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.wearia.app.databinding.ActivityLoginBinding
import com.wearia.app.ui.MainActivity
import com.wearia.app.viewmodel.AuthViewModel
import com.wearia.app.viewmodel.ViewModelFactory

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private val viewModel: AuthViewModel by viewModels { ViewModelFactory(this) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Session check : si déjà connecté, accès direct à l'accueil
        if (viewModel.isLoggedIn()) {
            startActivity(Intent(this, MainActivity::class.java))
            finish()
            return
        }

        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
        observeViewModel()
    }

    private fun setupListeners() {
        binding.btnLogin.setOnClickListener {
            val email = binding.etEmail.text.toString().trim()
            val password = binding.etPassword.text.toString().trim()

            if (email.isEmpty()) {
                binding.etEmail.error = "Veuillez saisir votre e-mail"
                return@setOnClickListener
            }
            if (password.length < 8) {
                binding.etPassword.error = "Le mot de passe doit comporter au moins 8 caractères (BR05)"
                return@setOnClickListener
            }

            viewModel.login(email, password)
        }

        binding.tvGoToRegister.setOnClickListener {
            val intent = Intent(this, RegisterActivity::class.java)
            startActivity(intent)
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { loading ->
            binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
            binding.btnLogin.isEnabled = !loading
        }

        viewModel.authState.observe(this) { result ->
            result?.onSuccess {
                Toast.makeText(this, "Connexion réussie ! Bienvenue ${it.nom}", Toast.LENGTH_SHORT).show()
                val intent = Intent(this, MainActivity::class.java)
                startActivity(intent)
                finish()
            }?.onFailure { error ->
                Toast.makeText(this, error.localizedMessage ?: "Erreur de connexion", Toast.LENGTH_LONG).show()
            }
        }
    }
}
