from django.urls import path

from . import borrower_views
from . import login_views
from . import media_views

urlpatterns = [
    # Connexion et menu biblibothécaire ________________________________________________________________________________
    path('login/', login_views.login_view, name='login'),
    path('menu/', login_views.librarian_menu, name='librarian_menu'),
    # medias ___________________________________________________________________________________________________________
    path('librarian_media_list/', media_views.list_media, name='list_media'),
    path('librarian_media_list/add_livre/', media_views.add_livre, name='add_livre'),
    path('librarian_media_list/add_dvd/', media_views.add_dvd, name='add_dvd'),
    path('librarian_media_list/add_cd/', media_views.add_cd, name='add_cd'),
    path('boardgames/edit/<int:pk>/', media_views.edit_boardgame, name='edit_boardgame'),
    path('boardgames/add/', media_views.add_boardgame, name='add_boardgame'),
    path('boardgames/delete/<int:pk>/', media_views.delete_boardgame, name='delete_boardgame'),
    path('librarian_media_list/edit/<str:media_type>/<int:media_id>/', media_views.edit_media, name='edit_media'),
    path('librarian_media_list/delete/<str:media_type>/<int:media_id>/', media_views.delete_media, name='delete_media'),
    # Emprunteurs ______________________________________________________________________________________________________
    path('emprunteurs_list/', borrower_views.list_emprunteurs, name='list_emprunteurs'),
    path('emprunteurs/add/', borrower_views.add_emprunteur, name='add_emprunteur'),
    path('emprunteurs/<int:pk>/mettre_a_jour/', borrower_views.update_emprunteur, name='update_emprunteur'),
    path('emprunteurs/<int:pk>/supprimer/', borrower_views.delete_emprunteur, name='delete_emprunteur'),
    path('emprunteurs/create_emprunt/', borrower_views.create_emprunt, name='create_emprunt'),
    path('emprunteurs/<int:pk>/', borrower_views.emprunteur_detail, name='emprunteur_detail'),
    path('emprunts/delete/<int:emprunt_id>/', borrower_views.delete_emprunt, name='delete_emprunt'),
]
