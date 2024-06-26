from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from librarian_app.forms import EmprunteurForm, EmpruntForm
from librarian_app.models import Emprunteur, Emprunt


# AFFICHER la liste des emprunteurs ____________________________________________________________________________________

def list_emprunteurs(request):
    # Requêtes pour récupérer tous les objets liés au modèle des emprunteurs depuis la base de données.
    emprunteurs = Emprunteur.objects.all()
    # Requêtes HTTP avec les objets récupérés.
    return render(request, 'librarian_member_list/member_list.html', {'emprunteurs': emprunteurs})


# AJOUTER un membre ____________________________________________________________________________________________________

def add_emprunteur(request):
    # Si le formulaire a été soumis 'POST'.
    if request.method == 'POST':
        form = EmprunteurForm(request.POST)
        # Et si les données du formulaire sont valides.
        if form.is_valid():
            # Alors création d'un nouvel objet.
            form.save()
            # Puis redirection vers la vue 'list_emprunteurs'.
            return redirect('list_emprunteurs')
    else:
        # Sinon affichage d'un formulaire vide.
        form = EmprunteurForm()
    # Et redirection vers le template du formulaire.
    return render(request, 'librarian_member_list/member_add.html', {'form': form})


# AJOUTER un emprunt  __________________________________________________________________________________________________

def create_emprunt(request):
    # Si le formulaire a été soumis 'POST'.
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        # Et si les données du formulaire sont valides.
        if form.is_valid():
            # Alors, Crée une instance de l'emprunt à partir des données valides du formulaire sans la sauvegarde en
            # base de données.
            emprunt = form.save(commit=False)
            # Si l'emprunteur a déjà 3 emprunts en cours.
            if Emprunt.objects.filter(emprunteur=emprunt.emprunteur, date_retour__isnull=True).count() >= 3:
                # Alors, une erreur est ajoutée au formulaire.
                form.add_error(None, 'Un membre ne peut pas avoir plus de 3 emprunts à la fois.')
            # Sinon, si l'emprunteur a un emprunt en retard.
            elif Emprunt.objects.filter(emprunteur=emprunt.emprunteur, date_retour__isnull=True,
                                        date_emprunt__lt=timezone.now() - timedelta(weeks=1)).exists():
                # Alors, une erreur est ajoutée au formulaire.
                form.add_error(None, 'Un membre ayant un emprunt en retard ne peut plus emprunter.')
            # Sinon, le formulaire est validé et sauvegardé dans base de données.
            else:
                emprunt.save()
                # Et redirection vers le template du formulaire.
                return redirect('list_emprunteurs')

    else:
        form = EmpruntForm()
    return render(request, 'librarian_member_list/create_emprunt.html', {'form': form})


# SUPPRIMER un emprunteurs _____________________________________________________________________________________________

def delete_emprunteur(request, pk):
    # Récupération de l'objet Emprunteur correspondant à la clé primaire spécifiée.
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    # Si le formulaire a été soumis 'POST'.
    if request.method == 'POST':
        # Suppression de l'emprunteur.
        emprunteur.delete()
        # Puis redirection vers la vue 'list_emprunteurs'.
        return redirect('list_emprunteurs')
    # Sinon redirection vers le template du formulaire.
    return render(request, 'librarian_member_list/member_delete.html', {'emprunteur': emprunteur})


# MODIFIER un emprunteurs _____________________________________________________________________________________________

def update_emprunteur(request, pk):
    # Récupération de l'objet Emprunteur correspondant à la clé primaire spécifiée.
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    if request.method == 'POST':
        # Si le formulaire a été soumis 'POST'.
        form = EmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():
            # Alors création d'un nouvel objet.
            form.save()
            # Puis redirection vers la vue 'list_emprunteurs'.
            return redirect('list_emprunteurs')
    else:
        # Sinon, création d'un formulaire pré-rempli avec les données existant de l'objet "emprunteur" récupéré.
        form = EmprunteurForm(instance=emprunteur)
        # Et redirection vers le template du formulaire.
    return render(request, 'librarian_member_list/member_update.html', {'form': form, 'emprunteur': emprunteur})


# DETAILS des emprunts d'un membre _____________________________________________________________________________________
def emprunteur_detail(request, pk):
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    emprunts = Emprunt.objects.filter(emprunteur=emprunteur)
    return render(request, 'librarian_member_list/member_emprunt_detail.html',
                  {'emprunteur': emprunteur, 'emprunts': emprunts})


def delete_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    if request.method == 'POST':
        if emprunt.livre:
            emprunt.livre.disponible = True
            emprunt.livre.save()
        elif emprunt.dvd:
            emprunt.dvd.disponible = True
            emprunt.dvd.save()
        elif emprunt.cd:
            emprunt.cd.disponible = True
            emprunt.cd.save()

        emprunt.delete()
        return redirect('emprunteur_detail', pk=emprunt.emprunteur.id)
    return render(request, 'librarian_member_list/delete_emprunt.html', {'emprunt': emprunt})
