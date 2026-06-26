def test_that_passes():
    """This test will always pass"""
    assert 1 + 1 == 2

def test_mongo_uri_exists(): 
    import os
    mongo_uri = os.getenv("MONGO_URI")
    assert mongo_uri is not None, "MONGO_URI is missing!"

def test_intentional_failure(): 
    assert 1 + 1 == 2, "Math is broken!"  