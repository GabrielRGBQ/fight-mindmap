from app.model import schemas
from fastapi import status

def test_create_mindmap(client, test_user):
    test_data = {"name": "string", "description": "string", "owner_id": test_user["id"]}
    res = client.post(
        "/mindmaps/", json=test_data
    )
    new_mindmap = schemas.MindmapOut(**res.json())
    assert new_mindmap.name == test_data["name"]
    assert new_mindmap.description == test_data["description"]
    assert new_mindmap.owner_id == test_data["owner_id"]
    assert new_mindmap.owner.name == test_user["name"]
    assert new_mindmap.owner.email == test_user["email"]
    assert res.status_code == 201

def test_create_mindmap_wrong_owner(client):
    """
    Since no user is created in the db prior to the execution, the creation of the
    mindmap should fail for there is no user to set as owner
    """
    test_data = {"name": "string", "description": "string", "owner_id": 1}
    res = client.post(
        "/mindmaps/", json=test_data
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_get_mindmaps(test_user, authorized_client, test_mindmaps):
    res = authorized_client.get("/mindmaps/")
    assert len(res.json()) == len([mindmap for mindmap in test_mindmaps if mindmap.owner_id == test_user["id"]])
    assert res.status_code == 200

def test_unauthorized_get_mindmaps(client):
    res = client.get("/mindmaps/")
    assert res.status_code == 401

def test_get_mindmap(authorized_client, test_mindmaps):
    res = authorized_client.get(f"/mindmaps/{test_mindmaps[0].id}")
    mindmap = schemas.MindmapOut(**res.json())
    assert mindmap.name == test_mindmaps[0].name
    assert mindmap.description == test_mindmaps[0].description
    assert mindmap.owner_id == test_mindmaps[0].owner_id
    assert res.status_code == 200

def test_unauthorized_get_mindmap(client, test_mindmaps):
    res = client.get(f"/mindmaps/{test_mindmaps[0].id}")
    assert res.status_code == 401

def test_not_existing_get_mindmap(authorized_client):
    res = authorized_client.get("/mindmaps/2000")
    assert res.status_code == 404

def test_unauthorized_get_mindmap(authorized_client, test_mindmaps):
    res = authorized_client.get(f"/mindmaps/{test_mindmaps[3].id}")
    assert res.status_code == 403