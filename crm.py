import re
import string
from tinydb import TinyDB, where, table
from pathlib import Path


class User:
    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

    def __init__(self, firstName: str, lastName: str, phoneNumber: str = "", address: str = ""):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.address = address

    def __repr__(self):
        return f"User({self.firstName},{self.lastName})"

    def __str__(self):
        return f"{self.fullName}\n{self.phoneNumber}\n{self.address}\n"

    @property
    def fullName(self):
        return f"{self.firstName} {self.lastName}"

    @property
    def dbInstance(self) -> table.Document:
        return User.DB.get((where('firstName') == self.firstName) & (where('lastName') == self.lastName))

    def _checks(self):
        self._checkPhoneNumber()
        self._checkName()

    def _checkPhoneNumber(self):
        phoneNumber = re.sub(r"[+()\s]*", "", self.phoneNumber)
        if len(phoneNumber) < 0 or not phoneNumber.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phoneNumber} invalide")

    def _checkName(self):
        if not self.firstName or not self.lastName:
            raise ValueError(f"Prénom et nom ne peuvent pas être vide")
        specialChar = string.punctuation + string.digits

        for character in self.firstName + self.lastName:
            if character in specialChar:
                raise ValueError(f"Nom invalide {self.fullName}")

    def exists(self):
        return bool(self.dbInstance)

    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.dbInstance.doc_id])
        else:
            return []

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()
        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)


def getAllUsers():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
    from faker import Faker

    fake = Faker(locale="fr_FR")
    for _ in range(100):
        user = User(firstName=fake.first_name(),
                    lastName=fake.last_name(),
                    phoneNumber=fake.phone_number(),
                    address=fake.address())
        user.save()

    martin = User(firstName="Martin", lastName="Voisin")
    martin.save()
    martin.delete()
    for user in getAllUsers():
        print(user)
        print("-"*25)

