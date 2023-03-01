from crm import User
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


# Fixture to initialize the in-memory database for each test
@pytest.fixture
def setupDb():
    User.DB = TinyDB(storage=MemoryStorage)


# Fixture to initialize a test user in the database
@pytest.fixture
def user(setupDb):
    u = User(firstName="Patrick",
             lastName="Martin",
             address="1 rue du chemin, 75000 Paris",
             phoneNumber="0123456789")
    # Save the user to the database
    u.save()
    # Return the user for use in tests
    return u


# Test method to verify that the user's first name is correct
def test_firstName(user):
    assert user.firstName == "Patrick"


# ...

# Test method to verify that the user's full name is correct
def test_full_name(user):
    assert user.fullName == "Patrick Martin"


# Test method to verify that the user's database instance is correct
def test_dbInstance(user):
    assert isinstance(user.dbInstance, table.Document)
    assert user.dbInstance["firstName"] == "Patrick"
    assert user.dbInstance["lastName"] == "Martin"
    assert user.dbInstance["address"] == "1 rue du chemin, 75000 Paris"
    assert user.dbInstance["phoneNumber"] == "0123456789"


# Test method to verify that an unsaved user has no database instance
def test_not_dbInstance(setupDb):
    u = User(firstName="Patrick",
             lastName="Martin",
             address="1 rue du chemin, 75000 Paris",
             phoneNumber="0123456789")
    assert u.dbInstance is None


# Test method to verify that phone numbers are validated correctly
def test__check_phone_number(setupDb):
    # Create a user with a good phone number
    userGood = User(firstName="Patrick",
                    lastName="Martin",
                    address="1 rue du chemin, 75000 Paris",
                    phoneNumber="0123456789")
    # Create a user with a bad phone number
    userBad = User(firstName="Robert",
                   lastName="Martin",
                   address="7 rue du moulin, 13000 Marseille",
                   phoneNumber="012345678")

    # Verify that the bad phone number raises a know exception
    with pytest.raises(Exception) as err:
        userBad._checkPhoneNumber()
        assert "invalide" in str(err.value)

    # Save the good user to the database and verify that it exists
    userGood.save(validate_data=True)
    assert userGood.exists()


# Test method to verify that names are not empty
def test__check_name_empty(setupDb):
    userBad = User(firstName="",
                   lastName="",
                   address="7 rue du moulin, 13000 Marseille",
                   phoneNumber="012345678")

    # Verify that the empty name raises a known value error
    with pytest.raises(ValueError) as err:
        userBad._checkName()

    assert "Prénom et nom ne peuvent pas être vide" in str(err.value)


# Test method to verify that names not contains invalid char
def test__check_name_invalid_char(setupDb):
    # Create a user with invalid characters in their first and last names
    userBad = User(firstName="Patrick%&#",
                   lastName="Martin--/",
                   address="7 rue du moulin, 13000 Marseille",
                   phoneNumber="012345678")

    # Verify that the invalid name raises a known value error
    with pytest.raises(ValueError) as err:
        userBad._checkName()

    assert "Nom invalide" in str(err.value)


# Test method to verify that user exist in db after saving
def test_exists(user):
    assert user.exists()


# Test method to verify that user not exist in db if not saving
def test_not_exists(setupDb):
    u = User(firstName="Test",
             lastName="Tes")
    assert not u.exists()


# Test method to verify that user has been deleted
def test_delete(setupDb):
    user_test = User(firstName="Robert",
                     lastName="Machin",
                     address="7 rue du moulin, 75012 Paris",
                     phoneNumber="012345678")
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()

    assert isinstance(first, list)
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0


# Test method to verify that user has been saved
def test_save(setupDb):
    user_test = User(firstName="Robert",
                     lastName="Machin",
                     address="7 rue du moulin, 75012 Paris",
                     phoneNumber="012345678")
    user_test_duplicate = User(firstName="Robert",
                               lastName="Machin",
                               address="7 rue du moulin, 75012 Paris",
                               phoneNumber="012345678")

    first = user_test.save()
    second = user_test_duplicate.save()

    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
