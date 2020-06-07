from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        print(f'GOOGLE answer: {response.keys()}')
        print(f'profile:{response["profile"]}')
        print(f'picture:{response["picture"]}')

        if 'gender' in response.keys():
            if response['gender'] == 'male':
               user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
               user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.about_me = response['aboutMe']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
               user.delete()
               raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        user.save()

    return
