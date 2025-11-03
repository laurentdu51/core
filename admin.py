from django.contrib import admin
from core.models import *

def bt_p_publier(modeladmin, request, queryset):
	queryset.update(p_publier=True)
bt_p_publier.short_description = "Passer en Public"
def bt_p_not_publier(modeladmin, request, queryset):
	queryset.update(p_publier=True)
bt_p_not_publier.short_description = "Passer en Priver"
def bt_p_menu_poid_plus(modeladmin, request, queryset):
	for obj in queryset:
		obj.p_menu_poid=obj.p_menu_poid+5
		obj.save()
bt_p_menu_poid_plus.short_description = "Augmenter le poid de 5"
def bt_p_menu_poid_moin(modeladmin, request, queryset):
	for obj in queryset:
		obj.p_menu_poid=obj.p_menu_poid-5
		obj.save()
bt_p_menu_poid_moin.short_description = "Diminuer le poid de 5"

def bt_sd_poid_plus(modeladmin, request, queryset):
	for obj in queryset:
		obj.sd_poid=obj.sd_poid+5
		obj.save()
bt_sd_poid_plus.short_description = "Augmenter le poid de 5"
def bt_sd_poid_moin(modeladmin, request, queryset):
	for obj in queryset:
		obj.sd_poid=obj.sd_poid-5
		obj.save()
bt_sd_poid_moin.short_description = "Diminuer le poid de 5"

class Page_Admin(admin.ModelAdmin):
	form = Page_Admin_Form  # Réactivé
	list_display = ('p_titre', 'p_titre_slugify', 'p_adresse', 'p_contenu', 'p_right', 'p_type', 'p_menu_poid', 'p_publier','p_see_title_and_des_in_templates')
	list_filter = ('p_type', 'p_menu_parent', 'p_publier', 'p_see_title_and_des_in_templates')
	actions = [bt_p_menu_poid_plus, bt_p_menu_poid_moin, bt_p_publier, bt_p_not_publier]
admin.site.register(Page, Page_Admin)

class Speed_Dial_Admin(admin.ModelAdmin):
	pass
	list_display = ('sd_titre', 'sd_adresse' ,'sd_groupe', 'sd_icone', 'sd_color', 'sd_poid')
	actions = [bt_sd_poid_plus, bt_sd_poid_moin]
admin.site.register(Speed_Dial, Speed_Dial_Admin)

class Data_Admin(admin.ModelAdmin):
	pass
	exclude = ('d_titre_slugify',)
	list_display = ('d_titre', 'd_titre_slugify', 'd_type', 'd_variable',)
admin.site.register(Data, Data_Admin)

class Groupe_Admin(admin.ModelAdmin):
	pass
	exclude = ('g_nom_slugify',)
	list_display = ('g_nom', 'g_description')
admin.site.register(Groupe, Groupe_Admin)

class Contact_Admin(admin.ModelAdmin):
	pass
	list_display = ('c_type', 'c_name', 'c_email', 'c_description', 'c_statut',)
	search_fields = ['c_name', 'c_email', 'c_description']
	list_filter = ('c_type', 'c_statut',)

admin.site.register(Contact, Contact_Admin)

class Fichier_Admin(admin.ModelAdmin):
	list_display = ('f_nom', 'f_date',)
	search_fields = ['f_nom',]
	list_filter = ('f_date',)

admin.site.register(Fichier, Fichier_Admin)


