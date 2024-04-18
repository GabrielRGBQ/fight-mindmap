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
    assert new_mindmap.owner.id == test_data["owner_id"]
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