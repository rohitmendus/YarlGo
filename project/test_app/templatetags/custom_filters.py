from django import template
from test_app.models import Test
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='chr')
def chr_(value):
    return chr(value + 64)

@register.simple_tag(name='get_qn_val')
def get_question_type(session, i, item):
    return session['user_questions'][i-1][item]

@register.simple_tag(name='check_test_taken')
def check_test_taken(test_id, user_id):
    test = Test.objects.get(id=test_id)
    user = User.objects.get(id=user_id)
    return test.test_taken(user)
