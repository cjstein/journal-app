from django.db import models


def test_user_owns(request, model: models.Model, pk):
    test_model = model.objects.get(pk=pk)
    return request.user == test_model.user
