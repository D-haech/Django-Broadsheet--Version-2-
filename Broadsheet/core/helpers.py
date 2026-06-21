from academics.models import Session, Term
from django.core.exceptions import ValidationError

def get_current_session(school):

    return Session.objects.filter(school=school, is_current=True).first()


def get_current_term(school):

    return Term.objects.filter(school=school, is_current=True).first()





def require_current_session(school):

    session = Session.objects.filter(school=school, is_current=True).first()

    if not session:

        raise ValidationError("No current session configured.")

    return session


def require_current_term(school):

    term = Term.objects.filter(school=school, is_current=True).first()

    if not term:

        raise ValidationError("No current term configured.")

    return term
