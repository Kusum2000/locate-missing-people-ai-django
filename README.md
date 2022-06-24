# AI based Django application to locate Missing People using Facial Features

An example of Django project with basic user functionality.

## Functionality

### The following features were forked from <https://github.com/egorsmkv/simple-django-login-and-register>

- Log in
  - via username & password
  - via email & password
  - via email or username & password
  - with a remember me checkbox (optional)
- Create an account
- Log out
- Reset password
- Send/ Resend activation code
- Remind a username
- Change password
- Change profile

### Additional features added

- File Missing Case
- Match found person with missing people in database
- Admin Privilege
  - Delete records
  - View user activities
- Live dashboard for:
  - Total people missing, people found, users registered
  - Details of people found
  - Users Leaderboard
- Mail: activation code, reset password link, found missing person
- Multiple languages: English, Hindi, Kannada.

## Project Tree

```text
locate-missing-people-ai-django
├─ .git
├─ .gitignore
├─ conda-requirements.txt
├─ dcaFuse.m
├─ fuse.m
├─ LICENSE
├─ README.md
├─ requirments.txt
├─ screenshots
│  ├─ authorized_page.png
│  ├─ create_an_account.png
│  ├─ login.png
│  ├─ password_change.png
│  ├─ password_reset.png
│  └─ set_new_password.png
└─ source
   ├─ accounts
   │  ├─ admin.py
   │  ├─ apps.py
   │  ├─ detect_face.py
   │  ├─ face_recog.ipynb
   │  ├─ FeatureExtraction.ipynb
   │  ├─ forms.py
   │  ├─ match_face.py
   │  ├─ migrations
   │  ├─ models.py
   │  ├─ templates
   │  │  └─ accounts
   │  │     ├─ emails
   │  │     │  ├─ activate_profile.html
   │  │     │  ├─ activate_profile.txt
   │  │     │  ├─ change_email.html
   │  │     │  ├─ change_email.txt
   │  │     │  ├─ forgotten_username.html
   │  │     │  ├─ forgotten_username.txt
   │  │     │  ├─ restore_password_email.html
   │  │     │  └─ restore_password_email.txt
   │  │     ├─ log_in.html
   │  │     ├─ log_out.html
   │  │     ├─ profile
   │  │     │  ├─ change_email.html
   │  │     │  ├─ change_password.html
   │  │     │  ├─ change_profile.html
   │  │     │  ├─ file_missing.html
   │  │     │  ├─ found_missing.html
   │  │     │  ├─ match.html
   │  │     │  ├─ missing_list.html
   │  │     │  └─ user_list.html
   │  │     ├─ remind_username.html
   │  │     ├─ resend_activation_code.html
   │  │     ├─ restore_password.html
   │  │     ├─ restore_password_confirm.html
   │  │     ├─ restore_password_done.html
   │  │     └─ sign_up.html
   │  ├─ urls.py
   │  ├─ utils.py
   │  ├─ views.py
   │  └─ __init__.py
   ├─ app
   │  ├─ conf
   │  │  ├─ development
   │  │  │  ├─ settings.py
   │  │  │  └─ __init__.py
   │  │  ├─ production
   │  │  │  ├─ settings.py
   │  │  │  └─ __init__.py
   │  │  └─ __init__.py
   │  ├─ settings.py
   │  ├─ urls.py
   │  ├─ wsgi.py
   │  └─ __init__.py
   ├─ content
   │  ├─ assets
   │  │  ├─ css
   │  │  ├─ favicon.png
   │  │  ├─ js
   │  │  └─ vendor
   │  │     ├─ bootstrap
   │  │     ├─ jquery
   │  │     └─ popper
   │  ├─ locale
   │  │  ├─ hi
   │  │  └─ kn
   │  └─ templates
   │     ├─ layouts
   │     │  └─ default
   │     │     └─ page.html
   │     └─ main
   │        ├─ change_language.html
   │        └─ index.html
   ├─ main
   │  ├─ apps.py
   │  ├─ views.py
   │  └─ __init__.py
   └─ manage.py

```

## Installing

### Clone the project

```
git clone https://github.com/egorsmkv/simple-django-login-and-register
cd simple-django-login-and-register
```

### Install dependencies & activate virtualenv

```
pip install pipenv

pipenv install
pipenv shell
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

1. Edit `source/app/conf/development/settings.py` if you want to develop the project.

2. Edit `source/app/conf/production/settings.py` if you want to run the project in production.

### Apply migrations

```
python source/manage.py migrate
```

### Collect static files (only on a production server)

```
python source/manage.py collectstatic
```

### Running

#### A development server

Just run this command:

```bash
python source/manage.py runserver
```

