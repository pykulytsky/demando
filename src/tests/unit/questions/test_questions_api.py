def test_get_question(client, question):
    response = client.get(f"/qa/questions/{question.pk}")

    assert response.status_code == 200
    assert response.json()["body"] == question.body


def test_get_questions_list(client, question):
    response = client.get("/qa/questions/")

    assert response.status_code == 200
    assert response.json()[0]["body"] == question.body


def test_ask_question(auth_client, event, user):
    response = auth_client.post(
        "/qa/questions/", json={"body": "how to use TDD?", "event": event.pk}
    )

    assert response.status_code == 201
    assert response.json()["body"] == "how to use TDD?"
    assert response.json()["author"]["username"] == user.username


def test_get_my_questions(auth_client, question):
    response = auth_client.get("/qa/questions/my/")

    assert response.status_code == 200
    assert response.json()[0]["body"] == question.body
