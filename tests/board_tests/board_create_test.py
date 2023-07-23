import pytest


@pytest.mark.django_db
def test_board_create(client, create_login_user):
    """Testing the creation of a board"""
    board_create = client.post(
        '/goals/board/create',
        {'title': 'test board'},
        content_type='application/json'
    )

    expected_response = {
        "id": board_create.data['id'],
        "title": "test board",
        "is_deleted": False
    }

    assert board_create.status_code == 201
    assert board_create.data['title'] == expected_response['title']
    assert board_create.data['id'] == expected_response['id']
    assert board_create.data['is_deleted'] == expected_response['is_deleted']