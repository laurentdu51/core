**Prérequis :**

- Python 3.12+
- Un environnement virtuel activé (recommandé)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ../requirements.txt
```

**Installation :**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Installation sur un environnement Docker :**

voir "Installation.md sur docker"

**Changelog :**

* Avril 2026 - Migration vers TinyMCE 5, mise à jour Django 6.0
* Jan 2024 - Mise à jour gestion menu et amélioration mise en page
* 2023 - Version initiale