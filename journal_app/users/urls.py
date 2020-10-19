from django.urls import path

from journal_app.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_checkin_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/<uuid:checkin_link>/", view=user_checkin_view, name='checkin'),
    path("<str:username>/", view=user_detail_view, name="detail"),

]
