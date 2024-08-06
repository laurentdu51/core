from django.db import models
from django import forms

from django.template.defaultfilters import slugify

from trumbowyg.widgets import TrumbowygWidget

menu_pos = (
	(u'no', u'No'),
	(u'haut', u'En haut'),
	(u'cote', u'Sur le coté'),
	(u'pied', u'En pied de page'),
)

page_type = (
	(u'page', u'Une page'),
	(u'sys', u'Une page interne'),
	(u'lien', u'Un lien'),
	(u'lien_ext', u'Un lien Externe'),
)

page_color = (
	(u'primary', u'Bleu'),
	(u'secondary', u'Gris'),
	(u'success', u'Vert'),
	(u'danger', u'Rouge'),
	(u'warning', u'Orange'),
	(u'info', u'Bleu clair'),
	(u'dark', u'Noir'),
	(u'white', u'Blanc'),
)

page_bordure = (
	(u'def', u'Default'),
	(u'oui', u'Oui'),
	(u'non', u'Non'),
)

class Groupe (models.Model) : #group pour organisation
	g_nom = models.CharField("Nom du groupe", max_length = 128, unique = True)
	g_nom_slugify = models.CharField("Nom Slugify", max_length = 128, blank = True, editable = False)
	g_description = models.TextField("Description", blank = True)

	class Meta :
		verbose_name = 'Groupe'
		verbose_name_plural = 'Groupes'

	def save(self, *args, **kwargs) :
		self.g_nom_slugify = slugify(self.g_nom)
		super(Groupe, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.g_nom
	def __str__(self):
		return '%s' % (self.g_nom)

class Data (models.Model) : #stocage de donnée dynamique
	d_titre = models.CharField("Nom", max_length = 128, unique = True)
	d_titre_slugify = models.CharField("Nom Slugify", max_length = 128, blank = True, editable = False)
	d_type = models.CharField("Type", max_length = 64)
	d_variable = models.CharField("Valeur", max_length = 64)

	class Meta :
		verbose_name = 'Stocage de données'
		verbose_name_plural = 'Stocage de données'
		ordering = ['d_titre']

	def save(self, *args, **kwargs) :
		self.d_titre_slugify = slugify(self.d_titre)
		super(Data, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.d_titre
	def __str__(self):
		return '%s' % (self.d_titre)
	
class Fichier (models.Model) : # Upload de fichier pour réutilisation dans les pages
	f_nom = models.CharField("Nom du fichier", max_length = 128, blank = True, editable = False)
	f_date = models.DateTimeField("Date", auto_now_add=True)
	f_fichier = models.FileField("Fichier", upload_to='static/uploads/')

	class Meta :
		verbose_name = 'Stocage de fichiers'
		verbose_name_plural = 'Stocage de fichiers'
		ordering = ['f_date']

	def save(self, *args, **kwargs) :
		self.f_nom = slugify(self.f_fichier.name)
		super(Fichier, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.f_nom
	def __str__(self):
		return '%s' % (self.f_nom)

class Page (models.Model) : #Architecture pour les pages static est dynamique
	p_titre = models.CharField("Titre", max_length = 128, unique = True)
	p_titre_slugify = models.CharField("Titre Slugify", max_length = 128, blank = True, editable = False)
	p_icone = models.CharField("Code de l'icone", max_length = 64, blank = True)
	p_type = models.CharField("Type de page",choices=page_type, max_length=8, default='page')
	p_adresse = models.CharField("Adresse", max_length = 64)
	p_menu_position = models.CharField("A utiliser dans un menu ?",choices=menu_pos, max_length=4, default='no')
	p_menu_est_parent = models.BooleanField("Utilisé comme parent", default = False)
	p_menu_parent = models.ForeignKey('self',verbose_name="Parent", blank = True, null = True, on_delete=models.PROTECT, limit_choices_to={'p_menu_est_parent': True})
	p_menu_poid = models.PositiveSmallIntegerField("Poid si utilisé dans les menus", default=50)
	p_mots_clefs = models.CharField("Mots clefs", max_length = 512, blank = True)
	p_description = models.TextField("Description", blank = True)
	p_contenu = models.TextField("Contenu", blank = True)
	p_right = models.TextField("Contenu à droite", blank = True)
	p_groupe = models.BooleanField("Afficher les groupes", default = False)
	p_speedial = models.BooleanField("Afficher le Speedial", default = False)
	p_publier = models.BooleanField("Publié", default = False)
	p_proteger = models.BooleanField("Disponible que si authentifier", default = False)
	p_see_title_and_des_in_templates = models.BooleanField("Description et titre visible dans les templates", default = True)
	c_card_mp = models.CharField("Afficage du cadre central",choices=page_bordure, max_length=3, default='def')
	c_card_rp = models.CharField("Afficage du cadre de droite",choices=page_bordure, max_length=3, default='def')

	class Meta :
		verbose_name = 'Gestion des pages'
		verbose_name_plural = 'Gestion des pages'
		ordering = ['p_adresse']

	def save(self, *args, **kwargs) :
		if self.p_type == "sys" and self.p_titre_slugify == "":
			self.p_titre_slugify = slugify(self.p_titre)
		elif self.p_type != "sys":
			self.p_titre_slugify = slugify(self.p_titre)

		if self.p_type == "lien":
			self.p_description = "."
			self.p_contenu = "."

		super(Page, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.p_titre
	def __str__(self):
		return '%s' % (self.p_titre)
	
class Speed_Dial (models.Model) : # model pour génération de page SpeedDial
	sd_titre = models.CharField("Titre", max_length = 128)
	sd_groupe = models.ForeignKey(Groupe,verbose_name="Groupe", blank = True, null = True, on_delete=models.PROTECT)
	sd_icone = models.CharField("Code de l'icone", max_length = 64, blank = True)
	sd_color = models.CharField("Couleur du cadre",choices=page_color, max_length=10, default='primary')
	sd_adresse = models.CharField("Adresse", max_length = 256)
	sd_poid = models.PositiveSmallIntegerField("Poid", default=50)
	
	def __str__(self):
		return self.sd_titre

	class Meta:
		verbose_name = "Speed Dial"
		verbose_name_plural = "Speed Dial"

class Contact (models.Model): # model de contact et retour de bug
	c_type_liste = (
		('contact', 'Pour un contact'),
		('beug', 'Pour un beug'),
		('plainte', 'Pour une plainte'),
	)
	c_statut_liste = (
		('non_lu', 'Non Lu'),
		('lu', 'Lu'),
		('archive', 'Archivé'),
	)
	c_name = models.CharField("Votre nom", max_length = 128)
	c_email = models.EmailField("Votre emails")
	c_type = models.CharField("Type de demande", max_length=16, choices=c_type_liste, default = 'contact')
	c_description = models.TextField("Votre demande")
	c_statut = models.CharField("Statut de la demande", max_length=16, choices=c_statut_liste, default = 'non_lu')

	def __unicode__(self):
		return self.c_name
	def __str__(self):
		return '%s' % (self.c_name)

class ContactForm(forms.ModelForm):# formulaire de contact lié au model 
	class Meta:
		model = Contact
		fields = ['c_name', 'c_email', 'c_type', 'c_description']

class Page_Admin_Form(forms.ModelForm):
	class Meta:
		model = Page
		exclude = ['p_titre_slugify']
		widgets = {
			'p_contenu': TrumbowygWidget(),
			'p_right': TrumbowygWidget(),
			}

