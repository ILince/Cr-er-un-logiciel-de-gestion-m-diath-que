from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Media(models.Model):
    name = models.CharField(max_length=150)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey('Emprunteur', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Livre(Media):
    auteur = models.CharField(max_length=150)


class DVD(Media):
    realisateur = models.CharField(max_length=150)


class CD(Media):
    artiste = models.CharField(max_length=150)


class BoardGame(models.Model):
    name = models.CharField(max_length=150)
    createur = models.CharField(max_length=150)


class Emprunteur(models.Model):
    nom = models.CharField(max_length=150)
    bloquer = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Emprunt(models.Model):
    # Création d'une relation de clé étrangère avec le modèle Emprunteur. Si l'emprunteur est supprimé, tous les emprunts associés sont également supprimés.
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)

    # Création d'une relations de clé étrangère avec les modèles Livre, DVD, et CD. Ces champs peuvent être nuls ou vides, et si l'un des modèle est supprimé, la relation est définie à NULL.
    livre = models.ForeignKey(Livre, null=True, blank=True, on_delete=models.SET_NULL)
    dvd = models.ForeignKey(DVD, null=True, blank=True, on_delete=models.SET_NULL)
    cd = models.ForeignKey(CD, null=True, blank=True, on_delete=models.SET_NULL)

    # Définition automatique de la date et l'heure lors de la création de l'emprunt.
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)

    # Méthode de vérification des emprunts en retard.
    def is_late(self):
        return self.date_retour is None and self.date_emprunt + timedelta(weeks=1) < timezone.now()

    # Méthode d'ajout des contraintes aux emprunts avant sauvegarde.
    def clean(self):
        # Si un membre a déja plus de trois emprunts simultanés non retournés.
        if Emprunt.objects.filter(emprunteur=self.emprunteur, date_retour__isnull=True).count() >= 3:
            # Alors affichage du message erreur.
            raise ValidationError('Un membre ne peut pas avoir plus de 3 emprunts à la fois.')

        # Si membre a un emprunt en retard.
        if Emprunt.objects.filter(emprunteur=self.emprunteur, date_retour__isnull=True,
                                  date_emprunt__lt=timezone.now() - timedelta(weeks=1)).exists():
            # Alors affichage du message erreur.
            raise ValidationError('Un membre ayant un emprunt en retard ne peut plus emprunter.')

    # Méthode de sauvegarde des emprunts.
    def save(self, *args, **kwargs):
        # Appelle self.clean() pour valider l'emprunt à la sauvegarde.
        self.clean()
        # Sauvegarde de l'emprunt.
        super().save(*args, **kwargs)
        # Si un livre, un DVD ou un CD est emprunté, sa disponibilité est mise à False et sauvegardée.
        if self.livre:
            self.livre.disponible = False
            self.livre.save()
        if self.dvd:
            self.dvd.disponible = False
            self.dvd.save()
        if self.cd:
            self.cd.disponible = False
            self.cd.save()

    # Méthode d'affichage en chaîne de caractères des emprunts sauvegardés, avec l'emprunteur lié.
    def __str__(self):
        return f"{self.emprunteur.nom} - {self.livre or self.dvd or self.cd}"
