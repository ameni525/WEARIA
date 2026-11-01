import uvicorn

if __name__ == "__main__":
    # Host 0.0.0.0 permet la connexion depuis l'émulateur Android (10.0.2.2) ou un téléphone réel
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
