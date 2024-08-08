import sys
from django.apps import AppConfig

class CoreConfig(AppConfig):
	name = 'core'

	def ready(self):

		if 'migrate' in sys.argv:
			return

		print("-- Démarage du Core --")
		print(">> Vérification des variables d'environement")

		from core.models import Data
		
		print(">>> check site-name")
		try :
			data = Data.objects.get(d_titre_slugify = "site-name")
		except:
			data = Data()
			data.d_titre = "site-name"
			data.d_type = "txt"
			data.d_variable = "Duhaz Core"
			data.save()
		print(">>> check site-logo")
		try :
			data = Data.objects.get(d_titre_slugify = "site-logo")
		except:
			data = Data()
			data.d_titre = "site-logo"
			data.d_type = "txt"
			data.d_variable = "far fa-clone"
			data.save()

		print(">>> heck site-version")
		try :
			data = Data.objects.get(d_titre_slugify = "site-version")
		except :
			data = Data()
			data.d_titre = "site-version"
			data.d_type = "txt"
			data.d_variable = "Jan. 2024"
			data.save()

		print(">>> check background-color")
		try :
			data = Data.objects.get(d_titre_slugify = "background-color")
		except :
			data = Data()
			data.d_titre = "background-color"
			data.d_type = "txt"
			data.d_variable = "#999"
			data.save()

		print(">>> check background")
		try :
			data = Data.objects.get(d_titre_slugify = "background")
		except :
			data = Data()
			data.d_titre = "background"
			data.d_type = "txt"
			data.d_variable = "background.jpeg"
			data.save()
		
		print(">>> check background-logo")
		try :
			data = Data.objects.get(d_titre_slugify = "background-logo")
		except :
			data = Data()
			data.d_titre = "background-logo"
			data.d_type = "txt"
			data.d_variable = "logo-txt-Mrduhaz.png"
			data.save()

		print(">>> check login-menu")
		try :
			data = Data.objects.get(d_titre_slugify = "login-menu")
		except :
			data = Data()
			data.d_titre = "login-menu"
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()

		print(">>> check includ-right-panel")
		try :
			data = Data.objects.get(d_titre_slugify = "includ-right-panel")
		except :
			data = Data()
			data.d_titre = "includ-right-panel"
			data.d_type = "txt"
			data.d_variable = "None"
			data.save()

		print(">>> check card-main-panel")
		try :
			data = Data.objects.get(d_titre_slugify = "card-main-panel")
		except :
			data = Data()
			data.d_titre = "card-main-panel"
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()

		print(">>> check card-right-panel")
		try :
			data = Data.objects.get(d_titre_slugify = "card-right-panel")
		except :
			data = Data()
			data.d_titre = "card-right-panel"
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()

		print(">> Vérification des pages par default")

		from core.models import Page
		print(">>> check bienvenus ")
		try :
			page = Page.objects.get(p_titre_slugify = "bienvenus")
		except :
			page = Page()
			page.p_titre = "Bienvenus"
			page.p_icone = "fas fa-home"
			page.p_contenu = "Bravo,</br>Ceci est votre 1er page."
			page.p_description = "Bravo, ceci est votre 1er page."
			page.p_adresse = "/"
			page.p_publier = True
			page.p_type = "sys"

			page.save()

		

