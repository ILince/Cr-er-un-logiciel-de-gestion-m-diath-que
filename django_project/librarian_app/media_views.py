from django.shortcuts import render, redirect, get_object_or_404
from librarian_app.forms import LivreForm, DVDForm, CDForm, BoardGameForm
from librarian_app.models import Livre, DVD, CD, BoardGame


# AFFICHER la liste des médias et des jeux de plateau __________________________________________________________________

def list_media(request):
    # Requêtes pour récupérer tous les objets depuis la base de données.
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    boardgames = BoardGame.objects.all()

    # Requêtes HTTP avec les objets récupérés.
    return render(request, 'librarian_media_list/media_list.html', {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'boardgames': boardgames,

    })


# AJOUTER un média (livre, dvd, cdv) et un jeu de plateau  _____________________________________________________________

def add_livre(request):
    # Si le formulaire a été soumis 'POST'.
    if request.method == 'POST':
        form = LivreForm(request.POST)
        # Et si les données du formulaire sont valides.
        if form.is_valid():
            # Alors création d'un nouvel objet.
            form.save()
            # Puis redirection vers la vue 'list_media'.
            return redirect('list_media')
    else:
        # Sinon affichage d'un formulaire vide.
        form = LivreForm()
        # Et redirection vers le template du formulaire.
    return render(request, 'librarian_media_list/mediaAdd/add_livre.html',
                  {'form': form})


def add_dvd(request):
    if request.method == 'POST':
        form = DVDForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_media')
    else:
        form = DVDForm()
    return render(request, 'librarian_media_list/mediaAdd/add_dvd.html', {'form': form})


def add_cd(request):
    if request.method == 'POST':
        form = CDForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_media')
    else:
        form = CDForm()
    return render(request, 'librarian_media_list/mediaAdd/add_cd.html', {'form': form})


def add_boardgame(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_media')
    else:
        form = BoardGameForm()
    return render(request, 'librarian_media_list/board_game/add_boardgame.html', {'form': form})


# SUPPRIMER un média (livre, dvd, cdv) et un jeu de plateau ____________________________________________________________

def delete_media(request, media_type, media_id):
    # Détermine le type de média.
    if media_type == 'livre':
        # Récupération de l'objet correspondant grace à son identifiant depuis la base de données.
        media_item = get_object_or_404(Livre,
                                       id=media_id)
    elif media_type == 'dvd':
        media_item = get_object_or_404(DVD, id=media_id)
    elif media_type == 'cd':
        media_item = get_object_or_404(CD, id=media_id)
    else:
        return redirect('list_media')

    if request.method == 'POST':
        # Supprime l'objet de la base de données.
        media_item.delete()
        return redirect('list_media')
    # Sinon Affichage du template avec les détails de l'objet qui s'apprête à être supprimé.
    return render(request, 'librarian_media_list/media_delete.html', {
        'media_item': media_item})


def delete_boardgame(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    if request.method == 'POST':
        boardgame.delete()
        return redirect('list_media')
    return render(request, 'librarian_media_list/board_game/delete_boardgame.html', {'boardgame': boardgame})


# MODIFIER un média (livre, dvd, cdv) et un jeu de plateau _____________________________________________________________

def edit_media(request, media_type, media_id):
    if media_type == 'livre':
        media_item = get_object_or_404(Livre, id=media_id)
        form_class = LivreForm
    elif media_type == 'dvd':
        media_item = get_object_or_404(DVD, id=media_id)
        form_class = DVDForm
    elif media_type == 'cd':
        media_item = get_object_or_404(CD, id=media_id)
        form_class = CDForm
    else:
        return redirect('list_media')

    if request.method == 'POST':
        form = form_class(request.POST, instance=media_item)
        if form.is_valid():
            form.save()
            return redirect('list_media')
    else:
        # Sinon, création d'un formulaire pré-rempli avec les données existantes de media_item.
        form = form_class(
            instance=media_item)

    return render(request, 'librarian_media_list/media_edit.html', {'form': form, 'media_type': media_type})


def edit_boardgame(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    if request.method == 'POST':
        form = BoardGameForm(request.POST, instance=boardgame)
        if form.is_valid():
            form.save()
            return redirect('list_media')
    else:
        form = BoardGameForm(instance=boardgame)
    return render(request, 'librarian_media_list/board_game/edit_boardgame.html',
                  {'form': form, 'boardgame': boardgame})
