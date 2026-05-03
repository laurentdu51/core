from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(self.create_default_site_content, sender=self)

    def create_default_site_content(self, sender, **kwargs):
        if kwargs.get('raw', False):
            return

        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM core_data LIMIT 1")
        except Exception:
            return

        from core.models import Data, Page

        defaults = [
            ("site-name", "txt", "Duhaz Core"),
            ("site-logo", "txt", "far fa-clone"),
            ("site-version", "txt", "Jan. 2024"),
            ("background-color", "txt", "#999"),
            ("background", "txt", "background.jpeg"),
            ("background-logo", "txt", "logo-txt-Mrduhaz.png"),
            ("login-menu", "txt", "True"),
            ("includ-right-panel", "txt", "None"),
            ("card-main-panel", "txt", "True"),
            ("card-right-panel", "txt", "True"),
            ("rss-mode", "txt", "False"),
        ]

        for title, d_type, value in defaults:
            Data.objects.get_or_create(
                d_titre=title,
                defaults={
                    'd_titre_slugify': title,
                    'd_type': d_type,
                    'd_variable': value,
                },
            )

        Page.objects.get_or_create(
            p_titre="Bienvenus",
            defaults={
                'p_titre_slugify': "bienvenus",
                'p_icone': "fas fa-home",
                'p_contenu': "Bravo,</br>Ceci est votre 1er page.",
                'p_description': "Bravo, ceci est votre 1er page.",
                'p_adresse': "/",
                'p_publier': True,
                'p_type': "sys",
            },
        )

		

