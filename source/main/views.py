from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count
from marshmallow import missing
from requests import request
from accounts.models import FileMissing, Found
from django.contrib.auth.models import User

class IndexPageView(TemplateView):
    template_name = 'main/index.html'


    # override context data
    def get_context_data(self, *args, **kwargs):
        

        missing= FileMissing.objects.filter(status='Found').values('user_id','img_id','status','first_name','last_name').annotate(total_filed=Count('user_id')) 

        missing_count = FileMissing.objects.filter(status='Not found').values('user_id','img_id','status').annotate(total_filed=Count('img_id')).count()

        found_cases1 = Found.objects.values('user_id','img_id','img','found_at','phone_number','street','area','city','state','zip_code').annotate(total_filed=Count('user_id')).order_by('-found_at')

        found_cases = Found.objects.values('user_id').annotate(total_filed=Count('user_id'))
        print(found_cases1,found_cases)
        fc=len(found_cases)
        found_count = Found.objects.all().count()
        users_count = User.objects.all().count()

        users=User.objects.values('id','is_staff','username')

        if fc==0:
            r1=''
            r2=''
            r3=''
            r4=''
            r5=''
        elif fc==1:
            r1=found_cases[0]
            r2=''
            r3=''
            r4=''
            r5=''
        elif fc==2:
            r1=found_cases[0]
            r2=found_cases[1]
            r3=''
            r4=''
            r5=''
        elif fc==3:
            r1=found_cases[0]
            r2=found_cases[1]
            r3=found_cases[2]
            r4=''
            r5=''
        elif fc==4:
            r1=found_cases[0]
            r2=found_cases[1]
            r3=found_cases[2]
            r4=found_cases[3]
            r5=''    
        else:
            r1=found_cases[0]
            r2=found_cases[1]
            r3=found_cases[2]
            r4=found_cases[3]
            r5=found_cases[4:]
        context={'missing_count':missing_count,'found_count':found_count,'users_count':users_count,'users':users,'missing':missing,'found':found_cases1,'rank1':r1,'rank2':r2,'rank3':r3,'rank4':r4,'rank_rest':r5}
        return context

    


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
