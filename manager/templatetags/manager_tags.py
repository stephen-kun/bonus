from django import template

from manager.forms import SliderImagesForm

register = template.Library()

@register.inclusion_tag('manager/forum/tags/lineform.html')
def getobjectform(model):
    form = SliderImagesForm(instance=model)
    return {'form':form,'model':model}