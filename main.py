import json
import requests
import traceback
from modules.type_activities import *
from modules.check_os import check_os


def read_json(*args):
    """
    Читаем JSON из файлов
    """
    with open(f"{args[0]}.json", "r") as read_file:
        data = json.load(read_file)
        return data
    return EOFError


def restya_write_id_activities_json(*args):
    """
    Пишем в JSON id последней активности
    """
    new_last_id_activities, db_json_path = args
    data_json = read_json(db_json_path)
    data_json["last_id_activities"] = new_last_id_activities

    with open(f"{db_json_path}.json", "w") as w:
        w.write(json.dumps(data_json, indent=4, sort_keys=True))


def restya_new_token_json(*args):
    """
    Пишем в JSON новый токен авторизации
    """
    oauth_token, access_token, last_id_activities, db_json_path = args
    data_json = read_json(db_json_path)

    data_json["last_id_activities"] = last_id_activities
    data_json["token_aouth_api"] = oauth_token
    data_json["token_login_api"] = access_token

    with open(f"{db_json_path}.json", "w") as w:
        w.write(json.dumps(data_json, indent=4, sort_keys=True))


def write_json_from_example(db_json_path):
    """
    Читаем JSON из файлов
    """

    data_example = """
    {
        "token_aouth_api": "", 
        "token_login_api": "", 
        "last_id_activities": ""
    }
    """
    with open(f"{db_json_path}.json", "w") as w:
        w.write(json.dumps(json.loads(data_example), indent=4, sort_keys=True))


def restya_oauth():
    """
    Отправляем API запрос в RESTYA для получения токена аутентификации
    """
    r = requests.get(
        'http://RESTYA_DOMEN/api/v1/oauth.json?Content-Type=application/json')
    return r.json()


def restya_login(*args):
    """
    Отправляем API запрос в RESTYA для получения токена авторизации
    """
    r = requests.post(f'http://RESTYA_DOMEN/api/v1/users/login.json?token={args[0]}&Content-Type=application/json', json=args[1])
    return r.json()


def restya_activities(*args):
    """
    Отправляем API запрос на получение последних активностей
    """
    r = requests.get(f'http://RESTYA_DOMEN/api/v1/activities.json?token={args[0]}&Content-Type=application/json')
    if r.status_code != 200:
        return False
    return r.json()


def restya_compare_activities(*args):
    """
    Сверяем id активностей
    """

    if args[0]['data'][0]['id'] != args[1]:
        return False
    return True


def restya_last_compare_activities(*args):
    """
    Собираем id активностей
    """
    response_activities, last_id_activities = args
    list_response_activities = []
    new_last_id_activities = response_activities['data'][0]['id']

    for j in response_activities['data']:

        if j['id'] > last_id_activities and j['board_name'] == "Поручения":

            if j['type'] == 'add_card':
                type_processed = type_add_card(j['modified'], j['full_name'], j['card_id'],
                                            j['card_name'], j['list_name'])

            elif j['type'] == 'move_card':
                type_processed = type_move_card(j['modified'], j['full_name'], j['card_id'],
                                            j['card_name'], j['list_name'], j['moved_list_name'])

            elif j['type'] == 'add_comment':
                type_processed = type_add_comment(j['modified'], j['full_name'], 
                                                j['card_id'], j['card_name'])

            elif j['type'] == 'add_card_desc':
                type_processed = type_add_card_desc(j['modified'], j['full_name'], 
                                                    j['card_id'], j['card_name'])

            elif j['type'] == 'add_card_user':
                type_processed = type_add_card_user(j['modified'], j['full_name'], j['card_id'],
                                                    j['card_name'], j['comment'])

            elif j['type'] == 'change_card_position':
                type_processed = False

            elif j['type'] == 'edit_card_desc':
                type_processed = type_edit_card_desc(j['modified'], j['full_name'], 
                                                    j['card_id'], j['card_name'])

            elif j['type'] == 'add_card_duedate':
                type_processed = type_add_card_duedate(j['modified'], j['full_name'], 
                                                    j['revisions']['new_value']['to_date'], j['card_id'], j['card_name'])
            else:
                type_processed = False
        else:
            # Раскомментировать и закомментировать "type_processed = False", если нужно собирать иные типы активности
            # list_response_activities.append(f"{j['id']}(type: {j['type']}) - {j['username']}: {j['comment']}")
            type_processed = False

        if type_processed:
            list_response_activities.append(type_processed)
            
    return list_response_activities, new_last_id_activities


def restya_send_last_activities_telegram(list_last_compare_activities):
    """
    Запускаем запросы в API RESTYABOARD
    """
    data_activities = "\n".join(list_last_compare_activities)
    
    token = "TOKEN_BOT_API"
    url = "https://api.telegram.org/bot"
    channel_id = "CHANNEL_ID_GROUP"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": data_activities
    })

    if r.status_code != 200:
        raise Exception("HTTP not 200OK")


def restya_send_last_activities_mattermost(list_last_compare_activities):
    """
    Запускаем запросы в API RESTYABOARD
    """
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    data_activities = "\n".join(list_last_compare_activities)
    req = Request("http://MATTERMOST_DOMEN/")
    try:
        urlopen(req)
    except HTTPError as e:
        err = 'Error code: {}'.format(e.code)
        print(err)
    else:
        icon_url = "https://stickergrad.ru/wp-content/uploads/2019/07/7772.png"

        URL = 'http://MATTERMOST_DOMEN/hooks/ymjth5kffjyj5nxaze1qtpju6r'
        payload = {"channel": "MATTERMOST_CHANNEL",
                   "username": "MATTERMOST_USERNAME_BOT",
                   "icon_url": icon_url,
                   "text": f"{data_activities}"}
        requests.post(URL, data=json.dumps(payload))


def restya_news_tokens(last_id_activities, admin_json_path):
    """
    Запускаем запросы в API RESTYABOARD для получения новых токенов
    """
    # Получаем токен аутентификации
    oauth = restya_oauth()
    oauth_token = oauth['access_token']

    # Получаем токен авторизации
    admin_data = read_json(admin_json_path)
    login_requests = restya_login(oauth_token, admin_data)
    access_token = login_requests['access_token']

    return oauth_token, access_token, last_id_activities


def main():
    """
    Запускаем запросы в API RESTYABOARD
    """
    try:
        db_json_path, admin_json_path = check_os()
        while True:
            # Читаем db.json для получения токена авторизации
            read_data_db = read_json(db_json_path)

            access_token = read_data_db['token_login_api']
            last_id_activities  = read_data_db['last_id_activities']

            if access_token == "":
                # Значит db.json пустой, начинае заполнять все поля
                last_id_activities = 0
                oauth_token, access_token, last_id_activities = restya_news_tokens(
                    last_id_activities, admin_json_path)
                
                # Пишем токен в db.json
                restya_new_token_json(
                    oauth_token, access_token, last_id_activities, db_json_path)

            # Получаем список последних активностей
            response_activities = restya_activities(access_token)

            if response_activities is False:
                oauth_token, access_token, last_id_activities = restya_news_tokens(last_id_activities, admin_json_path)
                restya_new_token_json(oauth_token, access_token, last_id_activities, db_json_path)
            else:
                break

        # Сверяем последний id активности с последним сохраненнем id активности
        boolean = restya_compare_activities(response_activities, last_id_activities)
        
        if boolean is False:
            # Собираем список активностей, которых надо отправить
            list_last_compare_activities, new_last_id_activities = restya_last_compare_activities(
                response_activities, last_id_activities)

            if list_last_compare_activities:
                # Отправляем активности в Телеграм
                restya_send_last_activities_telegram(list_last_compare_activities)
                # Отправляем активности в Mattermost
                restya_send_last_activities_mattermost(list_last_compare_activities)
            # Пишем последний новый id активности в json
            restya_write_id_activities_json(new_last_id_activities, db_json_path)
    except Exception as e:
        print(e.args, traceback.format_exc())


if __name__ == "__main__":
    main()
