import pytest


@pytest.fixture
def create_login_user(client):
    """Фикстура создания и логин пользователя"""
    user_data = {
        'username': 'archi',
        'first_name': 'Artur',
        'last_name': 'Olenberg',
        'email': 'olenberg.ai@yandex.ru',
        'password': 'developer789!',
        'password_repeat': 'developer789!'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/core/login',
        {'username': user_data['username'], 'password': user_data['password']},
        content_type='application/json')

    return create_user_response, login_user_response

@pytest.fixture
def create_another_user(client):
    """Фикстура создания и логин второго пользователя"""
    user_data = {
        'username': 'archi1',
        'first_name': 'Artur1',
        'last_name': 'Olenberg1',
        'email': 'olenberg.ai@yandex.ru1',
        'password': 'developer789!1',
        'password_repeat': 'developer789!1'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    return create_user_response


@pytest.fixture
def create_board(client, create_login_user):
    """Фикстура создания доски"""
    create_board_response = client.post(
        '/goals/board/create',
        data={'title': 'test board'},
        content_type='application/json')
    return create_board_response


@pytest.fixture
def create_category(client, create_board):
    """Фикстура создания категории"""
    create_category = client.post('/goals/goal_category/create',
                                  {'title': 'test category',
                                   'board': create_board.data["id"]},
                                  format='json')

    return create_category


@pytest.fixture
def create_goal(client, create_category):
    """Фикстура создания цели"""
    create_goal = client.post('/goals/goal/create',
                              {'title': 'new goal', 'category': create_category.data['id']},
                              content_type='application/json')
    return create_goal
