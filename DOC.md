# Core — Django CMS Framework

A Django framework for building and managing websites with a built-in admin interface.

---

## Installation

### Prérequis

```bash
pip install django==4.2.30
pip install django-tinymce
```

### Démarrage

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

L'admin Django est accessible à `/admin/`.

---

## Architecture

### Main URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | `index` | Home page (gen_page_sys 'bienvenus') |
| `/page/<address>` | `page` | Generic page by address |
| `/admin/` | Django admin | Admin interface |
| `/account/login` | `p_login` | Login |
| `/account/logout` | `p_logout` | Logout |
| `/account/registration` | `p_registration` | Registration |

---

## Data Models

### Page (main model)

Central model for creating web pages.

**Main fields:**

| Field | Type | Description |
|-------|------|-------------|
| `p_titre` | CharField | Page title |
| `p_titre_slugify` | CharField | Auto-generated slug (readonly) |
| `p_adresse` | CharField | URL path (e.g. `/contact`) |
| `p_type` | Choice | `page`, `sys`, `lien`, `lien_ext` |
| `p_icone` | CharField | FontAwesome icon code |
| `p_contenu` | TextField | Main content (TinyMCE) |
| `p_right` | TextField | Right panel content |
| `p_publier` | Boolean | Published / unpublished |
| `p_proteger` | Boolean | Auth required |
| `p_groupe` | Boolean | Show groups |

**Page types:**

- `page` — Standard page
- `sys` — System page (uses p_titre_slugify for lookup)
- `lien` — Internal link (address in p_adresse)
- `lien_ext` — External link (new window)

**Menu positions:**

- `no` — Not in menu
- `haut` — Top horizontal menu
- `cote` — Side menu (not implemented)
- `pied` — Footer menu

**Display options:**

- `c_card_mp` / `c_card_rp` : `def`, `oui`, `non`
- `p_see_title_and_des_in_templates` : Show title/description in template
- `p_speedial` : Enable speed dial

---

### Groupe

Organization of pages and speed dials.

| Field | Description |
|-------|-------------|
| `g_nom` | Group name |
| `g_description` | Description |

---

### Data

Key-value storage for dynamic configuration.

| Field | Description |
|-------|-------------|
| `d_titre` | Variable name |
| `d_type` | Data type |
| `d_variable` | Value |

**Used variables:**

- `site-name` — Site name
- `site-version` — Displayed version
- `site-logo` — FontAwesome logo class
- `background-color` — Background color (navbar/footer)
- `background` — Background image
- `background-logo` — Overlay logo
- `login-menu` — Show login menu (`True`/`False`)
- `includ-right-panel` — Right panel
- `card-main-panel` / `card-right-panel` — Card display

---

### Speed_Dial

Quick shortcuts for speed dial page.

| Field | Description |
|-------|-------------|
| `sd_titre` | Shortcut title |
| `sd_groupe` | FK to Groupe (optional) |
| `sd_icone` | FontAwesome class |
| `sd_color` | Color (primary, success, danger...) |
| `sd_adresse` | Shortcut URL |
| `sd_poid` | Sort order |

---

### Contact

Contact form / bug feedback.

| Field | Description |
|-------|-------------|
| `c_name` | Name |
| `c_email` | Email |
| `c_type` | `contact`, `beug`, `plainte` |
| `c_description` | Message |
| `c_statut` | `non_lu`, `lu`, `archive` |

---

### Fichier

File upload for reuse in pages.

| Field | Description |
|-------|-------------|
| `f_fichier` | FileField (upload_to=`static/uploads/`) |
| `f_nom` | Slugified name (auto) |
| `f_date` | Upload date |

---

## Main Views

### `index(request)`

Home page. Loads system page `bienvenus`. If `p_speedial=True`, generates a speed dial.

### `page(request, p_url)`

Loads a page by its `p_adresse`. Exact lookup.

### `p_login(request)`

Standard Django login with `next` redirect.

### `p_logout(request)`

Logout and redirect to home.

### `p_registration(request)`

Registration, creates a Django User, auto-logs in.

### `contact(request)`

Contact form. Saves Contact, shows confirmation.

---

## Utility Functions

### `gen_menu(position)`

Returns the menu for a position (`haut`, `pied`, `cote`). Filters on `p_publier=True`, orders by `p_menu_parent`.

### `gen_speeddial(grp)`

Returns speed dials, optionally filtered by group.

### `get_data_value(name)`

Returns the value of a `Data` variable. Returns `"Blop"` if not found.

### `gen_page_base()`

Generates a base page object with site-wide data (name, logo, colors...).

### `gen_page_sys(p_titre_slugify)`

Loads a system page by its slug. Returns a visual 404 if not found.

---

## Configuration via Data

Create in admin `/admin/core/data/add/`:

```
d_titre: site-name
d_type: text
d_variable: My Site
```

---

## Templates

### Hierarchy

```
base.html          — Parent template (navbar, footer, Bootstrap 4 layout)
├── page.html      — Generic page
├── link.html      — Link page
├── login.html     — Login page
├── 404.html      — 404 error
└── base_no_card.html — Without card (unused)
```

### Main blocks

| Block | Description |
|-------|-------------|
| `{% block title %}` | Page title |
| `{% block main %}` | Main content |
| `{% block left_panel %}` | Left panel |
| `{% block right_panel %}` | Right panel |
| `{% block script %}` | Additional JavaScript |
| `{% block modals %}` | Bootstrap modals |

---

## Dependencies

- **Django 4.2.8** — Framework
- **django-crispy-forms** — Styled forms
- **django-tinymce** — WYSIWYG editor
- **Bootstrap 4.6** — CSS (CDN)
- **FontAwesome 7** — Icons (CDN)
- **jQuery 3.5** — JavaScript (CDN)

---

## File Structure

```
core/
├── models.py          # All models
├── views.py           # Views and utility functions
├── admin.py           # Django admin configuration
├── apps.py            # Django app config
├── DOC.md             # This documentation
├── URL.md             # URL documentation
├── README.md          # Original README
├── templates/
│   ├── base.html       # Parent template
│   ├── page.html       # Page template
│   ├── link.html       # Link template
│   └── login.html      # Login template
├── static/
│   └── uploads/        # Uploaded files
└── migrations/
```

---

## Useful Commands

```bash
# Apply migrations
python manage.py migrate

# Create superuser (admin access)
python manage.py createsuperuser

# Start dev server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic
```
