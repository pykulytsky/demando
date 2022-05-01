def test_create_quiz(auth_client, user):
    response = auth_client.post(
        "/quiz/quizzes/", json={"name": "quiz", "enter_code": "1234"}
    )

    assert response.status_code == 201
    assert response.json()["owner"]["pk"] == user.pk
    assert response.json()["done"] is False
    assert response.json()["enter_code"] == "1234"


def test_create_quiz_with_auto_enter_code_gen(auth_client, user):
    response = auth_client.post("/quiz/quizzes/", json={"name": "quiz"})

    assert response.status_code == 201
    assert response.json()["owner"]["pk"] == user.pk
    assert response.json()["done"] is False


def test_get_quiz(quiz, client, step):
    response = client.get(f"/quiz/quizzes/{quiz.pk}")

    assert response.status_code == 200
    assert response.json()["pk"] == quiz.pk
    assert len(response.json()["steps"]) == 1


def test_patch_quiz(quiz, auth_client, db):
    response = auth_client.patch(f"/quiz/quizzes/{quiz.pk}", json={"name": "changed"})

    assert response.status_code == 200
    assert response.json()["name"] == "changed"
