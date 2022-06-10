import os
from re import template
import cv2
from PIL import Image
from django.http.response import StreamingHttpResponse
import imutils
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.expressions import RawSQL
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.db.models import Count
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView, TemplateView
from django.conf import settings
import numpy as np
from operator import itemgetter
import phonenumbers
from requests import request
import matplotlib.pyplot as plt
from datetime import datetime

# datetime object containing current date and time
now = datetime.date(datetime.now())
now2 = datetime.now()
from accounts.detect_face import detect_face, FaceAligner
from accounts.match_face import preprocess,feature_extraction, encode_img, match_faces
from oct2py import octave

from .utils import (
    send_activation_email, send_found_person, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)
from .forms import (
    FoundForm, MissingForm, SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm, ChangeEmailForm,
)
from .models import Activation, FileMissing, Found

fa = FaceAligner(desiredFaceWidth=224)

class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)



class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = url_has_allowed_host_and_scheme(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)



class SignUpView(GuestOnlyView, FormView):
    template_name = 'accounts/sign_up.html'
    form_class = SignUpForm
    
    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect('index')


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('accounts:log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'accounts/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('accounts:resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'accounts/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('accounts:restore_password_done')



class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('accounts:change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('accounts:change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('accounts:change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'accounts/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('accounts:remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'accounts/profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('accounts:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('accounts:log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/log_out.html'


class FoundMissingView(LoginRequiredMixin, FormView):
    template_name= 'accounts/profile/found_missing.html'
    form_class= FoundForm
    img_list=[]
    label_list = []
    #FileMissing.objects.filter(status="Found").update(status="Not found")
    missing_imgs = FileMissing.objects.filter(status='Not found').values('img')
    missing_labels = FileMissing.objects.filter(status='Not found').values('img_id')
    print(len(missing_imgs),len(missing_labels))
    for img in missing_imgs:
        img_list.append(img['img'])

    for img_id in missing_labels:
        label_list.append(img_id['img_id'])

    def form_valid(self, form):
        #FileMissing.objects.filter(status="Found").update(status="Not found")
        request = self.request
        data=request.POST
        missing_imgs = self.img_list
        missing_labels= self.label_list
        # Change the password
        #form.save()
        img= request.FILES.get('img')
        print(img.name)
        img_save_path =  settings.MEDIA_ROOT+'/check/'+'check.'+img.name.split(".")[-1]
        with open(img_save_path, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        faces = detect_face(img)
        if len(faces)>0:
            messages.success(self.request, _('Checking database for the person. Please wait, do not refresh.'))
            aligned_img = fa.align(cv2.imread(img_save_path), faces[0]['keypoints']['left_eye'], faces[0]['keypoints']['right_eye'])

            final_img_list, labels_encoded, final_labels_list = preprocess(settings.MEDIA_ROOT, missing_imgs,missing_labels,aligned_img)
            #print(final_img_list)
            
            flatten_new,fc7_new,fc6_new,missing_labels_en= feature_extraction(final_img_list,labels_encoded)
            
            print(flatten_new.shape,fc7_new.shape,fc6_new.shape,len(missing_labels_en))
            encoded_missing_imgs=octave.fuse(flatten_new,fc7_new,fc6_new,missing_labels_en)
            encoded_predict_img = encode_img(labels_encoded,aligned_img)
            predicted_id,predicted_score,predicted_list = match_faces(encoded_missing_imgs,encoded_predict_img,final_labels_list)
            
            newlist = sorted(predicted_list.items(),reverse=True, key=lambda x: x[1])
            print(newlist,now)
            
            if predicted_score>=5.04:
                messages.error(self.request, _('Person not found in the database'))
                return redirect('accounts:found_missing')
            else:
                raw = 'Select {}-date_of_missing from accounts_filemissing u where u.id=accounts_filemissing.id'.format(now)

                unique_missing = FileMissing.objects.filter(img_id=predicted_id).values('img_id','user_id', 'first_name',
                'last_name','gender', 'dob', 
                    'date_of_missing','time_of_missing', 'extra_info',
                    'street','area','city','state','zip_code').annotate(total_filed=Count('img_id'),days_lost=RawSQL(raw, ()))
                if unique_missing[0]['days_lost']>1 and unique_missing[0]['state'] != data['state']:
                    messages.error(self.request, _('Person not found in the database'))
                    return redirect('accounts:found_missing')

                print(unique_missing)
                missing = FileMissing.objects.filter(img_id=predicted_id).values('img_id','user_id', 'first_name',
                    'last_name','gender', 'dob', 
                        'date_of_missing','time_of_missing', 'extra_info',
                        'street','area','city','state','zip_code').annotate(total_filed=Count('img_id')).order_by()
                missing_user=missing[0]
                #print(missing_user)
                send_to = User.objects.filter(id=missing_user['user_id']).values('email')
                #print(missing_user,send_to)
                
                found = Found.objects.create(
                    img_id=predicted_id,
                    img=img,
                    user_id = request.user.username,
                    phone_number=data['phone_number'],
                    street=data['street'],
                    area=data['area'],
                    city=data['city'],
                    state=data['state'],
                    zip_code=data['zip_code'],
                )
                FileMissing.objects.filter(img_id=found.img_id).update(status="Found") # this will update only
                dt_string = now2.strftime("%d/%m/%Y %H:%M:%S")
                context = {'subject': str('Found '+predicted_id),
                            "person_name": str(missing_user['first_name']+" "+missing_user['last_name']),
                            "address": str(data['street']+" "+data['area']+" "+data['city']+" "+ data['state']+"-"+data['zip_code']),
                            "found_at" : dt_string,
                            "message_user": "We have sent the alert message to the police. You can reply to this chain of mail. Contact the following number:"+str(data['phone_number']),
                        }
                print(send_to[0]['email'],context)
                try:
                    send_found_person(send_to[0]['email'],context)
                except:
                    print("Unable to send mail currently")
                messages.success(self.request, _('You have found a missing person! '+str(predicted_id)))
        else:
            messages.error(self.request, _('Face not found in the Image. Upload again.'))     
        



        return redirect('accounts:found_missing')

class FileMissingView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/file_missing.html'
    form_class= MissingForm
    missing_labels= FileMissing.objects.values_list('img_id', flat=True)
    missing_imgs= FileMissing.objects.values_list('img', flat=True)
    #for i in range(len(missing_labels)):
        #print("'{}'".format(missing_labels[i]))
    #for i in range(len(missing_labels)):
        #print("'{}'".format(missing_imgs[i]))
    def form_valid(self, form):
        request = self.request
        images= request.FILES.getlist('img')
        data = request.POST
        user = request.user
        face_list=[]
        for image in images:
            faces = detect_face(image)
            face_list.append((faces, image))
        for faces, image in face_list:
            if len(faces)==0:
                messages.error(request,_(str(len(faces))+' face(s) found in the Image: '+ str(image)))
                return redirect('accounts:file_missing')
        for faces,image in face_list:
            
            face=faces[0]
            person= FileMissing.objects.create(
                    user_id= user.id,
                    img_id = data['first_name']+data['last_name']+'_'+str(data['date_of_missing']),
                    img = image,
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    dob = data['dob'],
                    date_of_missing = data['date_of_missing'],
                    time_of_missing = data['time_of_missing'],
                    extra_info = data['extra_info'],

                    street = data['street'],
                    area = data['area'],
                    city = data['city'],
                    state = data['state'],
                    zip_code = data['zip_code'],
                )
            print(person.img)
            img = cv2.imread(settings.MEDIA_ROOT+'/'+ str(person.img))
            aligned_img = fa.align(img, face['keypoints']['left_eye'], face['keypoints']['right_eye'])
            cv2.imwrite(settings.MEDIA_ROOT+'/'+str(person.img),aligned_img)
            
        
        messages.success(request, _('Your case has been submitted.'))
        return redirect('accounts:file_missing')


    

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret, frame = self.cap.read()
        missing_labels= FileMissing.objects.values_list('img_id', flat=True)
        missing_imgs= FileMissing.objects.values_list('img', flat=True)
        print(missing_imgs,missing_labels)
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)
        return frame.tobytes()
def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
        return StreamingHttpResponse(gen(VideoCamera()),
                        content_type='multipart/x-mixed-replace; boundary=frame')

class MatchView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile/match.html'


    
    
class ViewMissingView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile/missing_list.html'

    raw = 'Select date_of_missing-dob from accounts_filemissing u where u.id=accounts_filemissing.id'
    path = settings.MEDIA_ROOT
    missing_cases = FileMissing.objects.filter(status='Not found').order_by('-date_of_missing').values('img_id','img')
    unique_missing = FileMissing.objects.filter(status='Not found').values('img_id','user_id', 'first_name',
    'last_name','gender', 'dob', 
        'date_of_missing','time_of_missing', 'extra_info',
        'street','area','city','state','zip_code').annotate(total_filed=Count('img_id'),age=RawSQL(raw, ())).order_by('-date_of_missing','time_of_missing')
    found_cases = Found.objects.values('user_id','img_id').annotate(total_filed=Count('img_id')).order_by()
    #print(unique_missing)
    extra_context={'individual_cases':unique_missing,'missing_cases':missing_cases, 'path':path}

class ViewUsersView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile/user_list.html'
    users=User.objects.all()
    missing_cases = FileMissing.objects.values('user_id','img_id','status').annotate(total_filed=Count('user_id')).order_by('-date_of_missing')
    found_cases = Found.objects.values('user_id','img_id','found_at').annotate(total_filed=Count('img_id')).order_by('-found_at')
    extra_context={'users':users,'missing':missing_cases,'found':found_cases}