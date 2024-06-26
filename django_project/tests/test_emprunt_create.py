import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Emprunteur, Emprunt, Livre


@pytest.fixture
# Simulation de requêtes HTTP vers les vues.
def client():
    return Client()


@pytest.fixture
# Création d'un objet "Emprunteur" test dans la base de données.
def emprunteur():
    return Emprunteur.objects.create(nom="Nom de l'Emprunteur", bloquer=False)


# Création d'un objet "Livre" test dans la base de données avec le statut disponible.
@pytest.fixture
def livre_disponible():
    return Livre.objects.create(name="Titre du Livre", auteur="Auteur du Livre", disponible=True)


@pytest.mark.django_db
def test_create_emprunt_view_post_valid_livre(client, emprunteur, livre_disponible):
    # Récupération de l'URL de la vue.
    url = reverse('create_emprunt')
    # Simulation des données POST pour créer un nouvel emprunt .
    post_data = {
        'livre': livre_disponible.id,
        'emprunteur': emprunteur.id,
    }

    # Effectue une requête POST vers l'URL en soumettant les données valides (post_data).
    response = client.post(url, post_data)

    # Vérifie que la réponse HTTP a un code de statut 302 (redirection).
    assert response.status_code == 302

    # Vérifie que l'objet Emprunt a bien été ajouté à la base de données.
    assert Emprunt.objects.filter(emprunteur=emprunteur, livre=livre_disponible, date_retour__isnull=True).exists()
