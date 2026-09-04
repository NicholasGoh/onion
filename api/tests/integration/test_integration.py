def test_create_and_get_item(client):
    resp = client.post("/items/", json={"name": "Widget", "description": "A widget"})
    assert resp.status_code == 200
    item_id = resp.json()["id"]

    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Widget"


def test_create_item_validation_returns_400(client):
    resp = client.post("/items/", json={"name": ""})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"]


def test_get_missing_item_returns_404(client):
    resp = client.get("/items/9999")
    assert resp.status_code == 404


def test_list_items(client):
    client.post("/items/", json={"name": "A"})
    client.post("/items/", json={"name": "B"})
    resp = client.get("/items/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_items(client):
    client.post("/items/", json={"name": "Bluetooth Speaker"})
    client.post("/items/", json={"name": "USB Cable"})
    resp = client.get("/items/search", params={"q": "bluetooth"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["name"] == "Bluetooth Speaker"


def test_create_order_with_valid_items(client):
    item_resp = client.post("/items/", json={"name": "Widget"})
    item_id = item_resp.json()["id"]

    resp = client.post("/orders/", json={
        "itemIds": [item_id],
        "quantity": {str(item_id): 2},
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"


def test_create_order_with_missing_items_returns_400(client):
    resp = client.post("/orders/", json={
        "itemIds": [9999],
        "quantity": {"9999": 1},
    })
    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"].lower()


def test_order_response_uses_camel_case(client):
    item_resp = client.post("/items/", json={"name": "Widget"})
    item_id = item_resp.json()["id"]

    resp = client.post("/orders/", json={
        "itemIds": [item_id],
        "quantity": {str(item_id): 1},
    })
    data = resp.json()
    assert "itemIds" in data
    assert "item_ids" not in data
