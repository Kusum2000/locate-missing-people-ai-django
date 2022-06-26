# AI based Django application to locate Missing People using Facial Features

A Django based age invariant face recognition project, to find missing people with the joint help of common people and organizations.

## Functionalities

- File Missing Cases
  - Images are verified for faces and preprocessed using MTCNN (Multi-task Cascaded Convolutional Networks developed for both face detection and face alignment)
- Match found person with missing people in database
  - MTCNN: is again used to detect face in the uploaded image
  - VGG16: is a type of CNN (Convolutional Neural Network) used for object detection and classification algorithm. Classify 1000 images of 1000 different categories with 92.7% accuracy. Used here for extracting features from last 3 layers and transfer learning.
  - PCA (Principal Component Analysis): is a dimensionality-reduction method that is often used to reduce the dimensionality of large data sets, by transforming a large set of variables into a smaller one that still contains most of the information in the large set.
  - [MDCA](https://github.com/hosein-srj/Age-invariant-face-recognition-based-on-deep-features-analysis.git) (multimodal discriminant correlation analysis): a cascade version of DCA (Discriminant correlation analysis) maximize the correlation of corresponding features across the two input feature sets (as done in CCA-methods) in addition to performing a correlation for features that belong to different classes within each feature set. In addition to feature-level fusion, DCA performs significant dimension reduction, which implies low computational complexity.
- Admin Privilege
  - Delete records from database
  - View user activity
- Live dashboard for:
  - Total people missing, people found, users registered
  - Details of people found
  - Users Leaderboard
- Mail: activation code, reset password link, found missing person
  - [Courier](https://www.courier.com/): A multi-channel notifications service that allows you to bring your own email provider, including support for SMTP and most popular transactional email APIs.
- Multilingual: English, Hindi, Kannada.
  
### The following basic features were forked from [egorsmkv GitHub](https://github.com/egorsmkv/simple-django-login-and-register)

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

## Requirements

- Anaconda
- Python
- Django
- Tensorflow
- Octave (Free Open source alternative to read matlab files)

## Demo

Note: The images of people used belong to the FGNet Dataset.

### Basic Features

#### Account Activation

#### Forgot Password / Username

### Start match with Missing People in the database

### Email is sent to Admin and the user who filed the FIR if, the person is found

### File a new missing case

## Project Structure

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

### Install dependencies & activate virtualenv

For this project Anaconda environment is used. Dependencies are mentioned in conda-requirements.txt and requirements.txt

```bash
conda create -n tf_gpu_env -c conda-forge cudatoolkit cudnn python=3.8
        or
conda create -n tf_gpu_env python=3.8        
conda activate tf_gpu_env
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

1. Edit `source/app/conf/development/settings.py` if you want to develop the project.

2. Edit `source/app/conf/production/settings.py` if you want to run the project in production.

### Apply migrations

```bash
python source/manage.py migrate
```

### Collect static files (only on a production server)

```bash
python source/manage.py collectstatic
```

### Running

#### A development server

Just run this command:

```bash
python source/manage.py runserver
```

## Reference

```text
Age-invariant face recognition based on deep features analysis
Paper: Moustafa, A.A., Elnakib, A. & Areed, N.F.F. Age-invariant face recognition based on deep features analysis. SIViP 14, 1027–1034 (2020). https://doi.org/10.1007/s11760-020-01635-1

FGNET Dataset Description
Homepage: https://yanweifu.github.io/FG_NET_data/
Paper: Yanwei Fu, Timothy M. Hospedales, Tao Xiang, Jiechao Xiong, Shaogang Gong, Yizhou Wang, and Yuan Yao. Robust Subjective Visual Property Prediction from Crowdsourced Pairwise Labels. IEEE TPAMI 2016
Point of Contact: y.fu@qmul.ac.uk
```
