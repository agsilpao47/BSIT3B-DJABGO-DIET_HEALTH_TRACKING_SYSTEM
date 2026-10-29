from django.shortcuts import get_object_or_404

from apps.info.models import HealthProfile


def scoped_profile(user):
    return get_object_or_404(HealthProfile, user=user)
