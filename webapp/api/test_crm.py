import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage

from crm import User


@pytest.fixture
def setup_bd():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_bd):
    u = User(first_name="Patrick", last_name="Titouan", phone_number="0658274554",
             address="14 oupi julo")
    u.save()
    return u


@pytest.fixture
def user_not_save(setup_bd):
    u = User(first_name="Patrick", last_name="Titouan", phone_number="0658274554",
             address="14 oupi julo")
    return u


def test_full_name(user):
    assert user.full_name == "Patrick Titouan"


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Patrick"
    assert user.db_instance["last_name"] == "Titouan"
    assert user.db_instance["phone_number"] == "0658274554"
    assert user.db_instance["address"] == "14 oupi julo"


def test_not_db_instance(user_not_save):
    assert user_not_save.db_instance is None


def test__check_phone_number(setup_bd):
    user_good = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0623456789")
    user_bad = User(first_name="Jean",
                    last_name="Smith",
                    address="1 rue du chemin, 75015, Paris",
                    phone_number="+33623456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()
    assert f"Numéro de téléphone {user_bad.phone_number} invalide." in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True


def test__check_names_empty(setup_bd):
    user_bad = User(first_name="",
                    last_name="",
                    address="1 rue du chemin, 75015, Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert "Le prénom et le nom de famille ne peuvent pas être vides." in str(err.value)


def test__check_names_invalid_characters(setup_bd):
    user_bad = User(first_name="Patr!ck",
                    last_name="titouan%",
                    address="1 rue du chemin, 75015, Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert f"Nom invalide {user_bad.full_name}." in str(err.value)


def test_exists(user):
    assert user.exists() is True


def test_not_exists(user_not_save):
    assert user_not_save.exists() is False


def test_delete(user):
    first = user.delete()
    second = user.delete()
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)


def test_save():
    user_test = User(first_name="John",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_test_dup = User(first_name="John",
                         last_name="Smith",
                         address="1 rue du chemin, 75015, Paris",
                         phone_number="0123456789")
    first = user_test.save()
    second = user_test.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
