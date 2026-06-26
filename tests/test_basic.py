def test_that_passes():
    """This test will always pass"""
    assert 1 + 1 == 2

def test_mongo_uri_exists():
    """Check that MONGO_URI environment variable is set"""
    import os
    mongo_uri = os.getenv("MONGO_URI")
    assert mongo_uri is not None, "MONGO_URI is missing!"

def test_intentional_failure():
    """THIS WILL FAIL ON PURPOSE — to test our pipeline catches errors"""
    assert 1 + 1 == 5, "Math is broken!"  