<p align="center">
  <img src="https://img.shields.io/github/languages/top/Ollopic/Filmy-api "Language"" alt=" Language" />
  <img src="https://img.shields.io/github/stars/Ollopic/Filmy-api "Stars"" alt=" Stars" />
  <img src="https://img.shields.io/github/contributors/Ollopic/Filmy-api "Contributors"" alt=" Contributors" />
</p>

# Filmy

API de Filmy

## Auteurs

Maréchal Antoine
Lemont Gaétan

[![Contributors](https://contrib.rocks/image?repo=Ollopic/Filmy-api)](https://github.com/Ollopic/Filmy-api/graphs/contributors)


## Prérequis

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git): Téléchargez et installez Git en suivant les instructions de votre OS. Pour vérifier que Git a été installé avec succès, exécutez `git --version`.
- [Docker](https://docs.docker.com/get-docker/): Téléchargez et installez Docker en suivant les instructions de votre OS. Pour vérifier que Docker a été installé avec succès, exécutez `docker --version`.

## Lancer localement

1. Cloner le dépôt Filmy-api :  
```bash  
git clone https://github.com/Ollopic/Filmy-api  
```
2. Vous pouvez lancer l'api en faisant simplement une de ces deux commandes :  
```bash  
make init
docker compose up -d
```

L'API est alors accessible à l'adresse suivante : [http://localhost:8002](http://localhost:8002)

Un utilisateur par défaut est créé :

- email : `admin@example.com`
- mot de passe : `admin`

## Déploiement global
Pour lancer l'ensemble du projet, y compris l'app et l'API, un fichier Docker Compose est disponible dans le projet. Vous pouvez le retrouver ici : [compose.yml](./docker/compose.yml)
Un compte The Movie Database est nécessaire pour lancer l'API. Afin de pouvoir tester l'app directement, un compte spécial a été fait uniquement pour cette utilisation. Le token est déjà renseigné dans les variables dans le compose.
Vous retrouverez également le Dockerfile ayant servi a build l'image de l'API ici : [Dockerfile](./docker/Dockerfile.prod)


## Api Reference


### Collections


#### Récupérer toutes les collections
```bash
GET /collection
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Créer une nouvelle collection
```bash
POST /collection
```
| Nom      | Type   | Optionnel | Description                                   |
| -------- | ------ | --------- | --------------------------------------------- |
| name     | string | Non       | Nom de la collection.                        |
| picture  | string | Oui       | URL de l'image associée à la collection.     |

#### Mettre à jour une collection
```bash
PATCH /collection/<identifier>
```
| Nom      | Type   | Optionnel | Description                                   |
| -------- | ------ | --------- | --------------------------------------------- |
| name     | string | Oui       | Nouveau nom de la collection.                |
| picture  | string | Oui       | Nouvelle URL de l'image associée.            |

#### Supprimer une collection
```bash
DELETE /collection/<identifier>
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer une collection spécifique
```bash
GET /collection/<identifier>
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Ajouter un film à une collection
```bash
POST /collection/<identifier>
```
| Nom         | Type   | Optionnel | Description                                   |
| ----------- | ------ | --------- | --------------------------------------------- |
| film_id     | string | Non       | Identifiant du film à ajouter.               |
| state       | string | Non       | État du film (ex. "Vu", "À voir").        |
| borrowed    | bool   | Oui       | Statut d'emprunt du film.                    |
| borrowed_at | string | Oui       | Date d'emprunt du film (si applicable).      |
| borrowed_by | string | Oui       | Emprunteur du film (si applicable).          |
| favorite    | bool   | Oui       | Marquer le film comme favori.                |

#### Mettre à jour un film dans une collection
```bash
PATCH /collection/<collection_id>/<film_id>
```
| Nom         | Type   | Optionnel | Description                                   |
| ----------- | ------ | --------- | --------------------------------------------- |
| state       | string | Oui       | Nouvel état du film.                         |
| borrowed    | bool   | Oui       | Mise à jour du statut d'emprunt.             |
| favorite    | bool   | Oui       | Mise à jour du statut favori.                |

#### Supprimer un film d'une collection
```bash
DELETE /collection/<collection_id>/<film_id>
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer la wishlist
```bash
GET /collection/wishlist
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Ajouter un film à la wishlist
```bash
POST /collection/wishlist
```
| Nom      | Type   | Optionnel | Description                                   |
| -------- | ------ | --------- | --------------------------------------------- |
| film_id  | string | Non       | Identifiant du film à ajouter.               |

#### Transférer un film de la wishlist vers une collection
```bash
PATCH /collection/wishlist
```
| Nom          | Type   | Optionnel | Description                                   |
| ------------ | ------ | --------- | --------------------------------------------- |
| film_id      | string | Non       | Identifiant du film à transférer.            |
| state        | string | Non       | État du film après transfert.                |
| collection_id| int    | Non       | Identifiant de la collection cible.          |

---
### Authentification

#### Créer un jeton d'authentification
```bash
POST /token
```
| Nom       | Type   | Optionnel | Description                                   |
| --------- | ------ | --------- | --------------------------------------------- |
| mail      | string | Non       | Adresse email de l'utilisateur.              |
| password  | string | Non       | Mot de passe de l'utilisateur.               |

---
### Films

#### Récupérer les films populaires
```bash
GET /movies/popular
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer les films tendances
```bash
GET /movies/trending
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer les films les mieux notés
```bash
GET /movies/top_rated
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer les films à venir
```bash
GET /movies/upcoming
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Récupérer les films actuellement en salle
```bash
GET /movies/now_playing
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Rechercher un film par titre
```bash
GET /movies
```
| Nom   | Type   | Optionnel | Description                  |
| ----- | ------ | --------- | ---------------------------- |
| title | string | Non       | Titre du film recherché.     |
| page  | int    | Oui       | Numéro de la page à afficher.|

#### Récupérer les détails d'un film
```bash
GET /movies/<identifier>
```
| Nom        | Type   | Optionnel | Description                  |
| ---------- | ------ | --------- | ---------------------------- |
| identifier | int    | Non       | Identifiant TMDB du film.    |

#### Récupérer les crédits d'un film
```bash
GET /movies/<identifier>/credits
```
| Nom        | Type   | Optionnel | Description                  |
| ---------- | ------ | --------- | ---------------------------- |
| identifier | int    | Non       | Identifiant TMDB du film.    |

#### Récupérer la liste des genres de films
```bash
GET /movies/genres
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| -    | -      | -         | Néant                       |

#### Découvrir des films avec des filtres
```bash
GET /movies/discover
```
| Nom               | Type   | Optionnel | Description                                    |
| ----------------- | ------ | --------- | --------------------------------------------- |
| with_genres       | string | Oui       | Liste des genres (séparés par des virgules).  |
| sort_by           | string | Oui       | Critère de tri.                               |
| release_date.gte  | string | Oui       | Date de sortie minimum (format AAAA-MM-JJ).   |
| release_date.lte  | string | Oui       | Date de sortie maximum (format AAAA-MM-JJ).   |
| with_runtime.gte  | int    | Oui       | Durée minimum en minutes.                     |
| with_runtime.lte  | int    | Oui       | Durée maximum en minutes.                     |
| page              | int    | Oui       | Numéro de la page à afficher.                 |

---
### Acteurs

#### Rechercher une personne par nom
```bash
GET /person
```
| Nom   | Type   | Optionnel | Description                  |
| ----- | ------ | --------- | ---------------------------- |
| name  | string | Non       | Nom de la personne recherchée.|
| page  | int    | Oui       | Numéro de la page à afficher.|

#### Récupérer les détails d'une personne
```bash
GET /person/<identifier>
```
| Nom        | Type   | Optionnel | Description                  |
| ---------- | ------ | --------- | ---------------------------- |
| identifier | int    | Non       | Identifiant TMDB de la personne.|

#### Récupérer les personnes populaires
```bash
GET /person/popular
```
| Nom  | Type   | Optionnel | Description                  |
| ---- | ------ | --------- | ---------------------------- |
| page | int    | Oui       | Numéro de la page à afficher.|

---
### Utilisateurs

#### Récupérer les détails de l'utilisateur connecté

```bash
GET /user/me
```

| Nom           | Type   | Optionnel | Description                         |
|---------------|--------|-----------|-------------------------------------|
| Authorization | string | non       | Token JWT dans l'en-tête de la requête |


#### Récupérer les détails d'un utilisateur par son ID

```bash
GET /user/<identifier>
```

| Nom           | Type   | Optionnel | Description                          |
|---------------|--------|-----------|--------------------------------------|
| identifier    | int    | non       | ID de l'utilisateur à récupérer      |
| Authorization | string | non       | Token JWT dans l'en-tête de la requête |


#### Créer un nouvel utilisateur

```bash
POST /user
```

| Nom         | Type   | Optionnel | Description                            |
|-------------|--------|-----------|----------------------------------------|
| username    | string | non       | Nom d'utilisateur unique              |
| mail        | string | non       | Adresse email unique                  |
| password    | string | non       | Mot de passe de l'utilisateur         |
| is_admin    | bool   | oui       | Indique si l'utilisateur est admin    |


#### Mettre à jour les détails de l'utilisateur

```bash
PATCH /user
PATCH /user/<identifier>
```

| Nom            | Type   | Optionnel | Description                               |
|----------------|--------|-----------|-------------------------------------------|
| identifier     | int    | oui       | ID de l'utilisateur à mettre à jour       |
| username       | string | oui       | Nouveau nom d'utilisateur                |
| mail           | string | oui       | Nouvelle adresse email                   |
| password       | string | oui       | Nouveau mot de passe                     |
| is_admin       | bool   | oui       | Indique si l'utilisateur devient admin   |
| profile_image  | string | oui       | URL de la nouvelle image de profil       |
| Authorization  | string | non       | Token JWT dans l'en-tête de la requête    |


#### Supprimer un utilisateur

```bash
DELETE /user/<identifier>
```

| Nom           | Type   | Optionnel | Description                          |
|---------------|--------|-----------|--------------------------------------|
| identifier    | int    | non       | ID de l'utilisateur à supprimer      |
| Authorization | string | non       | Token JWT dans l'en-tête de la requête |
