from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken
import requests
from django.shortcuts import render, redirect


def friend_list(request):
    vk_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='vk')
    if vk_uid.exists():
        vk_uid = vk_uid[0].uid
        tolken = SocialToken.objects.filter(account__user=request.user, account__provider='vk').first()

        # getting friends

        friends_json_responce = requests.get(
            "https://api.vk.com/method/friends.get?user_id=" + str(vk_uid) +
            "&order=random" +
            "&fields=uid,first_name,last_name,photo_50" +
            "&count=5&access_token=" + str(tolken) +
            "&v=5.120"
        )

        first_five_friends = friends_json_responce.json()['response']['items']

        friends_list = []
        for friend in first_five_friends:
            # параметры запрашиваемые из урл запроса друзяшек - имя фамилия фото
            #friends_list.append('%s %s' % (friend['first_name'], friend['last_name']))
            friends_list.append(friend['first_name'])

        return render(request, 'profile.html', context={'friends': friends_list})
    else:
        return render(request, 'profile.html', None)



def full_bio(request):
    vk_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='vk')
    if vk_uid.exists():
        vk_uid = vk_uid[0].uid
        tolken = SocialToken.objects.filter(account__user=request.user, account__provider='vk').first()
        # getting friends

        friends_json_responce = requests.get(
            "https://api.vk.com/method/friends.get?user_id=" + str(vk_uid) +
            "&order=name" +
            "&fields=uid,first_name,last_name,photo_50" +
            "&access_token=" + str(tolken) + # отличие от копипаста с предыдущей функции что тут нет ограничения count на колличество друзяшек, выводит всех
            "&v=5.120"
        )

        first_five_friends = friends_json_responce.json()['response']['items']

        friends_list = []
        for friend in first_five_friends:
            # параметры запрашиваемые из урл запроса друзяшек - имя фамилия фото
            # friends_list.append('%s %s' % (friend['first_name'], friend['last_name']))
            friends_list.append(friend['first_name'])




        # getting logged user info

        # доступные поля смотреть тут и в fields записать через запятую: https://vk.com/dev/users.get
        # users.get?params[user_ids]=210700286&params[fields]=photo_50%2Ccity%2Cverified&params[name_case]=Nom&params[v]=5.120
        logged_in_user_info_json_response = requests.get(
            "https://api.vk.com/method/users.get?user_id=" + vk_uid +
            "&fields=movies,about,photo_200_orig,schools,music,personal" +
            "&name_case=Nom" +
            "&access_token=" + str(tolken) +
            "&v=5.120"
        )

        logged_in_user_info = logged_in_user_info_json_response.json()['response'][0]

        profile = {'кино': logged_in_user_info['movies'],
                   'о себе': logged_in_user_info['about']
                   }

        return render(request, 'home.html', context={'friends': friends_list, 'profile': profile})
    else:
        return render(request, 'home.html', None)
