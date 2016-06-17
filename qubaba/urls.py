from django.conf.urls import url

#from . import views_design as views
from . import views

urlpatterns = [		
	url(r'^get_slideimages',views.get_slideimages, name='get_slideimages'),	
	url(r'^get_forums',views.get_forums, name='get_forums'),		
	url(r'^bonus_remain',views.bonus_remain, name='bonus_remain'),	
	url(r'^has_bonus',views.has_bonus, name='has_bonus'),		
	url(r'^qubaba_bonus_list',views.qubaba_bonus_list, name='qubaba_bonus_list'),	
	url(r'^prompt_bonus',views.prompt_bonus, name='prompt_bonus'),	
	url(r'^ajax_bonus_remain',views.ajax_bonus_remain, name='ajax_bonus_remain'),			
]
