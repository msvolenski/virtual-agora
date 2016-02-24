# -*- coding: utf-8 -*-
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django import template
import re 
register = template.Library()






class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context.dicts[0][self.var_name] = value
        return u""
 
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
@register.filter
def votos_distintos(value):
    
    a = value.first() 
    if a.question.question_type   == '1':   
        question = a.question
        choices = question.choice_set.all()  
        return choices
        
    if a.question.question_type   == '2':   
        question = a.question
        choices = question.choice_set.all()  
        return choices
        
    if a.question.question_type   == '3':       
        return value.order_by('text').values_list('text',flat=True).distinct()
   
    

register.tag('set', set_var)

@register.filter
def to_class_name(value):
    return value.__class__.__name__
    
    
    


readmore_showscript = ''.join([
"this.parentNode.style.display='none';",
"this.parentNode.parentNode.getElementsByClassName('more')[0].style.display='inline';",
"return false;",
]);

@register.filter
def readmore(txt, showwords=15):
    global readmore_showscript
    words = txt.split(' ')

    if len(words) <= showwords:
        return mark_safe(txt)

    # wrap the more part
    words.insert(showwords, '<span class="more" style="display:none;">')
    words.append('</span>')

    # insert the readmore part
    words.insert(showwords, '<span class="readmore">... <a href="#" onclick="')
    words.insert(showwords+1, readmore_showscript)
    words.insert(showwords+2, '">read more</a>')
    words.insert(showwords+3, '</span>')

    # Wrap with <p>
    words.insert(0, '<p>')
    words.append('</p>')

    return mark_safe(' '.join(words))




