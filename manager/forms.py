from django import forms
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, FormView

from core.utils import json_response
from topic.models import SliderImage
from django.utils.translation import ugettext_lazy as _

# class OperateFieldWidget(forms.Widget):
#     def render(self, name, value, attrs=None):
#         print name,value,attrs
#         return "<div>adsfaf</div><div>gogogo</div>"


class SliderImagesForm(forms.ModelForm):
    # showurl = forms.CharField(label=_("image show"),required=False,initial="")
    oper = forms.CharField(label=_("Operation"),required=False)

    class Meta:
        model = SliderImage
        fields = ('order','url','enabled','oper')



class SliderImageFormView(FormView):
    form_class = SliderImagesForm
    template_name = "manager/forum/sliderimage/list.html"


class SliderImageListView(ListView):
    model = SliderImage
    template_name = "manager/forum/sliderimage/list.html"

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print request.POST
        print request.FILES
        id = request.POST.get("id",None)
        opertype = request.POST.get("opertype")
        if not id and opertype=="delete":
            return json_response({'result':-1})


        if id and opertype == "delete":
            try:
                SliderImage.objects.get(id=int(id)).delete()
            except Exception as ex:
                return json_response({'result':-2})
            return json_response({'result':0})

        if id and opertype == "save":
            form = SliderImagesForm(request.POST,request.FILES,instance=SliderImage.objects.get(id=int(id)))
            if form.is_valid():
                slider = form.save()
                return json_response({'result':1,'showimg':slider.url.url,'showname':slider.url.name})
            else:
                return json_response({'result':-3})

        if not id and opertype=="save":
            form = SliderImagesForm(request.POST,request.FILES)
            if form.is_valid():
                slider = form.save()
                return json_response({'result':2,'id':slider.id,'showimg':slider.url.url,'showname':slider.url.name})
            else:
                return json_response({'result':-3})
