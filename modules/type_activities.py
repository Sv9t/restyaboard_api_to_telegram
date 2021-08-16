from datetime import datetime

def activities_list_name_cut(card_name):
    """
    Если сообщение боле 50 знаков обрезаем и ставим многоточие в конце
    """

    if len(card_name) > 50:
        return f"{card_name[0:50].rstrip()}..."
    return card_name


def activities_list_comment_cut(comment):
    """
    Вырезаем из comment имя пользователя
    """

    return comment.split(" ")[2]


def activities_time_cut(modified):
    """
    Преобразуем время в читабельный вид без секунд
    """
    
    return str(datetime.strptime(modified, "%Y-%m-%dT%H:%M:%S"))[:-3]


def type_add_card(*args):
    """
    Добавил карточку
    """
    modified, full_name, card_id, card_name, list_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} добавил карточку #{card_id} "{card_name}" в "{list_name}"'


def type_move_card(*args):
    """
    Переместил карточку
    """

    modified, full_name, card_id, card_name, list_name, moved_list_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} переместил карточку #{card_id} "{card_name}" из "{list_name}" в "{moved_list_name}"'


def type_add_comment(*args):
    """
    Добавил комментарий
    """
    modified, full_name, card_id, card_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} добавил комментарий в карточку #{card_id} "{card_name}"'


def type_add_card_desc(*args):
    """
    Добавил описание
    """
    modified, full_name, card_id, card_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} добавил описание в карточку #{card_id} "{card_name}"'


def type_add_card_user(*args):
    """
    Добавил в карточку пользователя
    """
    modified, full_name, card_id, card_name, comment = args
    time_cut = activities_time_cut(modified)
    add_card_user = activities_list_comment_cut(comment)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} добавил {add_card_user} в карточку #{card_id} "{card_name}"'


def type_edit_card_desc(*args):
    """
    Изменил описание
    """
    modified, full_name, card_id, card_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} изменил описание карточки #{card_id} "{card_name}"'


def type_add_card_duedate(*args):
    """
    Добавил дату
    """
    modified, full_name, duedate, card_id, card_name = args
    time_cut = activities_time_cut(modified)
    card_name = activities_list_name_cut(card_name)

    return f'{time_cut} - {full_name} установил срок {duedate} в карточку #{card_id} "{card_name}"'
