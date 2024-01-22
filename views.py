from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from core.models import *

def get_get_value(request):
	get_value = {}
	if request.method == 'GET':
		get = request.GET
		for element in get:
			get_value[element] = get[element]
			print(get_value)
	return get_value

def gen_menu(position):
	try:
		menu = Page.objects.all().exclude(p_publier = 0).filter(p_menu_position = position).order_by('p_menu_parent')
	except:
		menu = Page.objects.none()
	return menu

def gen_speeddial():
	try:
		speeddial = Speed_Dial.objects.order_by('-sd_poid')
	except:
		speeddial = Speed_Dial.objects.none()
	return speeddial

def get_data_value(name):
	try:
		data = Data.objects.get(d_titre_slugify = name)
	except:
		data = Data()
		if name == "site-name":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "Duhaz Core"
			data.save()
		elif name == "site-logo":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "far fa-clone"
			data.save()
		elif name == "background-color":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "#999"
			data.save()
		elif name == "background":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "background.jpeg"
			data.save()
		elif name == "background-logo":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "logo-txt-Mrduhaz.png"
			data.save()
		elif name == "login-menu":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()
		elif name == "includ-right-panel":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "None"
			data.save()
		elif name == "card-main-panel":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()
		elif name == "card-right-panel":
			data.d_titre = name
			data.d_type = "txt"
			data.d_variable = "True"
			data.save()
		else :
			data.d_variable = "Blop"
	return data.d_variable


def update_data_value(name, value):
	try:
		data = Data.objects.get(d_titre_slugify = name)
		data.d_variable = value
		data.save()
	except:
		data = Data.objects.none()
		data.d_variable = "Blop"
	return data.d_variable

def gen_page_base():
	page = Page.objects.none()
	page.p_menu_haut = gen_menu('haut')
	page.p_menu_pied = gen_menu('pied')
	page.p_see_title_and_des_in_templates = True

	page.c_sitename = get_data_value('site-name')
	page.c_sitelogo = get_data_value('site-logo')
	page.c_bgcolor = get_data_value('background-color')
	page.c_bgimage = get_data_value('background')
	page.c_bgimagelogo = get_data_value('background-logo')
	page.c_menulogin = get_data_value('login-menu')
	page.c_includ_rp = get_data_value('includ-right-panel')
	page.c_card_mp = get_data_value('card-main-panel')
	page.c_card_rp = get_data_value('card-right-panel')

	return page

def gen_page_sys(p_titre_slugify):
	#print(p_titre_slugify)
	try :
		page = Page.objects.get(p_titre_slugify = p_titre_slugify)
	except:
		page = gen_page_base()
		page.p_contenu = "<h1>Erreur la page demandé n'existe pas </h1>"
		page.p_titre = "404 ! Erreur sur la page demmandé"
		page.p_icone = "fas fa-bug"

	page.p_menu_haut = gen_menu('haut')
	page.p_menu_pied = gen_menu('pied')
	page.p_meta_title = page.p_titre

	page.c_sitename = get_data_value('site-name')
	page.c_sitelogo = get_data_value('site-logo')
	page.c_bgcolor = get_data_value('background-color')
	page.c_bgimage = get_data_value('background')
	page.c_bgimagelogo = get_data_value('background-logo')
	page.c_menulogin = get_data_value('login-menu')
	page.c_includ_rp = get_data_value('includ-right-panel')
	page.c_card_mp = get_data_value('card-main-panel')
	page.c_card_rp = get_data_value('card-right-panel')
	
	return page


def index(request):
	page = gen_page_sys('bienvenus')
	page.speeddial = gen_speeddial()

	template = loader.get_template('page.html')
	context = {
		'page' : page,
	} 
	return HttpResponse(template.render(context, request))

def page(request, p_url):
	#print(p_url)
	p_url = "/"+p_url
	template = loader.get_template('page.html')
	try:
		page = Page.objects.get(p_adresse = p_url)
		page.p_menu_haut = gen_menu('haut')
		page.p_menu_pied = gen_menu('pied')
		page.p_meta_title = page.p_titre
		page.c_sitename = get_data_value('site-name')
		page.c_sitelogo = get_data_value('site-logo')
		page.c_bgcolor = get_data_value('background-color')
		page.c_bgimage = get_data_value('background')
		page.c_bgimagelogo = get_data_value('background-logo')
		page.c_menulogin = get_data_value('login-menu')
	except:
		page = gen_page_base()
		page.p_contenu = "<h1>Erreur la page demandé n'existe pas </h1>"

	context = {
		'page' : page,
	}
	return HttpResponse(template.render(context, request))

def contact(request,):
	page = gen_page_base()
	template = loader.get_template('page.html')
	page.p_titre = "Nous Contacter"
	page.p_description = "Formulaire de prise de contact"
	page.p_contenu = "<p>Merci de remplir le formulaire pour nous contacter.</p>"
	page.p_adresse = "/contact"

	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			n_contact = form.save()
			page.p_contenu = "<p>Merci. Nous vous répondrons au vite.</p>"
	else :
		form = ContactForm()
	
	context = {
		'page' : page,
		'form' : form,
	}
	return HttpResponse(template.render(context, request))

def p_login(request):
	next = request.GET.get('next','')
	page = gen_page_base()
	template = loader.get_template('login.html')
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.add_message(request, messages.INFO, 'Bonjour, vous êtes maintenant connecté')
				if next :
					return HttpResponseRedirect(next)
				else :
					return HttpResponseRedirect(reverse('core_index'))
			else :
				pass
	else :
		form = AuthenticationForm(request)
	context = {
		'page' : page,
		'form' : form,
	}
	return HttpResponse(template.render(context, request))

def p_logout(request):
	logout(request)
	messages.add_message(request, messages.INFO, 'A bientôt')
	return HttpResponseRedirect(reverse('core_index'))

def p_registration(request):
	page = gen_page_sys("inscription-sur-le-site")
	template = loader.get_template('page.html')
	page.p_f_titre = "Inscription"
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user=User.objects.create_user(username=username, password=password)
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.add_message(request, messages.INFO, 'Merci pour votre inscription')
			return HttpResponseRedirect(reverse('flux_control_panel'))
	else :
		form = UserCreationForm()
	context = {
			'page' : page,
			'form' : form,
		}
	return HttpResponse(template.render(context, request))

