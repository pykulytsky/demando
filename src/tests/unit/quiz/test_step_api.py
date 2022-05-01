def test_create_step(quiz, auth_client):
    response = auth_client.post(
        "/quiz/steps/", json={"title": "first quistion", "quiz": quiz.pk}
    )

    assert response.status_code == 201
    assert response.json()["done"] is False
