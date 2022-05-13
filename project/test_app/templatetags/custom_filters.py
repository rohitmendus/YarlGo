from django import template

register = template.Library()

@register.filter(name='chr')
def chr_(value):
    return chr(value + 64)

@register.simple_tag(name='get_qn_val')
def get_question_type(session, i, item):
    return session['user_questions'][i-1][item]
