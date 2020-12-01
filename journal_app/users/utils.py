from journal_app.users.models import User


def user_viewing_own_profile(request, profile_username_viewed):
    """
    This tests whether the profile viewed is owned by the user requesting it
    """
    profile_owner = User.objects.get(username=profile_username_viewed)
    return request.user == profile_owner
