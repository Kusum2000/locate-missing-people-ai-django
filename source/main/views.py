from django.views.generic import TemplateView
from django.db.models import Count
from marshmallow import missing
from requests import request
from accounts.models import FileMissing, Found
from django.contrib.auth.models import User

class IndexPageView(TemplateView):
    template_name = 'main/index.html'
    missing= FileMissing.objects.filter(status='Found').values('user_id','img_id','status').annotate(total_filed=Count('user_id'))
    missing_count = FileMissing.objects.values('user_id','img_id','status').annotate(total_filed=Count('user_id')).count()
    found_cases = Found.objects.values('user_id','img_id','found_at','street','area','city','state','zip_code').annotate(total_filed=Count('img_id')).order_by('-found_at')
    found_count = Found.objects.all().count()
    users_count = User.objects.all().count()
    users=User.objects.values('id','is_staff','username')
    extra_context={'missing_count':missing_count,'found_count':found_count,'users_count':users_count,'users':users,'missing':missing,'found':found_cases}


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
