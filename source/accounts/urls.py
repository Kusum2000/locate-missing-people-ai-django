
from django.urls import path


from .views import (
    FoundMissingView, LogInView, MatchView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView,
    FileMissingView, ViewMissingView, ViewUsersView, delete_found, delete_missing, delete_user, video_stream,
)

app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),

    path('missing/file', FileMissingView.as_view(), name='file_missing'),
    path('missing/view', ViewMissingView.as_view(), name='view_missing'),
    path('missing/matchlive', MatchView.as_view(), name='match_missing'),

    path('missing/delete_found/<img_id>', delete_found, name='delete_found'),
    path('missing/delete_missing/<img_id>', delete_missing, name='delete_missing'),
    path('user-list/delete_user/<username>', delete_user, name='delete_user'),

    path('missing/match', FoundMissingView.as_view(), name='found_missing'),
    path('monitor/', video_stream, name='monitor'),
    path('user-list/', ViewUsersView.as_view(), name='user_list'),
]
