def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_test_mc(client):
    # Grade 5, 1 Question, MC
    # We seeded 1 MC for grade 5 in conftest
    response = client.get("/generate-test", params={
        "grade": 5, "count": 1, "test_type": "Multiple Choice"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "Multiple Choice"
    assert data[0]["points"] == 100

def test_generate_test_essay(client):
    # Grade 5, 1 Question, Essay
    response = client.get("/generate-test", params={
        "grade": 5, "count": 1, "test_type": "Essay"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "Essay"

def test_generate_test_empty(client):
    # Grade 1 (no data in mock fixture)
    response = client.get("/generate-test", params={
        "grade": 1, "count": 1, "test_type": "Multiple Choice"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0 # Should return empty list, not crash
