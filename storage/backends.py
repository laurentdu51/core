from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class StaticStorage(FileSystemStorage):
    """
    Storage personnalisé pour sauvegarder les fichiers dans le dossier static
    au lieu du dossier media (pour compatibilité avec les liens historiques)
    """
    def __init__(self, *args, **kwargs):
        kwargs['location'] = os.path.join(settings.BASE_DIR, 'static')
        kwargs['base_url'] = '/static/'
        super().__init__(*args, **kwargs)
