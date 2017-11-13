from django import template
register = template.Library()

@register.filter(name='addstyle')
def addCss(field, style):
   return field.as_widget(attrs={"style":style})

@register.filter(name='addcss')
def addCss(field, css):
   return field.as_widget(attrs={"class":css})

