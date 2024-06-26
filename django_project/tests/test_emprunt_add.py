import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.forms import EmprunteurForm
from librarian_app.models import Emprunteur


@pytest.fixture
# Simulation de requêtes HTTP vers les vues.
def client():
    return Client()


@pytest.mark.django_db
def test_add_emprunteur_view(client):
    # Récupération de l'URL de la vue.
    url = reverse('add_emprunteur')

    # Effectue une requête vers l'URL  récupéré.
    response = client.get(url)

    # Vérifie que la réponse HTTP a un code de statut 200 (succès).
    assert response.status_code == 200
    # Vérifie que le formulaire 'form' est présent dans le contexte de la réponse.
    assert 'form' in response.context
    # Vérifie que le formulaire est correctement initialisé dans la vue.
    assert isinstance(response.context['form'], EmprunteurForm)

    # Simulation des données POST pour créer un nouveau membre .
    post_data = {
        'nom': 'Nouveau Nom de l\'Emprunteur',
        'bloquer': False,
    }
    # Effectue une requête POST vers l'URL de la vue en soumettant les données valides (post_data).
    response = client.post(url, post_data)

    # Vérifie que la réponse HTTP a un code de statut 302 (redirection).
    assert response.status_code == 302
    # Vérifie que la redirection se fait vers l'URL de 'list_emprunteurs' avec l'ajout de l'emprunteur réussi.
    assert response.url == reverse('list_emprunteurs')

    # Vérifie que l'objet Emprunteur a été ajouté à la base de données.
    assert Emprunteur.objects.filter(nom=post_data['nom']).exists()
