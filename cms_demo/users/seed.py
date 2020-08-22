import logging
import random
import string

from django.contrib.auth.models import Group

from .models import CustomUser
from .generic_variables import Groups


def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


def random_digits(y):
    return ''.join(random.choice(string.digits) for x in range(y))


def clear_data():
    """Deletes all the table data"""
    logging.info("Delete Address instances")
    CustomUser.objects.all().delete()


def create_admin_user():
    """
        Creates an admin_user object combining different
        elements from the list
    """
    logging.info("Creating address")
    email = [random_char(7)+"@gmail.com" for _ in range(15)]
    full_name = ["Baker Parker", "Rajori Nas",
                 "Park Walt", "MG Bager", "Kollin"]
    mobile_number = [int(random_digits(10)) for _ in range(15)]
    address = ["221 B Illonis, 209", "101 A Be-lin", "550I Saul Street",
               "420G Brad Heights", "A13 Inspire Garden"]
    city = ["Santa Chara", "Kings", "New York", "Chicago"]
    state = ["California", "Texas", "Arizona", "Alaska"]
    country = ["United States", "U.S", "America"]
    pincodes = ["101234", "101232", "101231", "101236", "101239"]
    password = [random_char(5)+"P@1" for _ in range(15)]
    admin_password = random.choice(password)
    admin_user = CustomUser(
        email=random.choice(email),
        full_name=random.choice(full_name),
        mobile_number=random.choice(mobile_number),
        address=random.choice(address),
        city=random.choice(city),
        state=random.choice(state),
        country=random.choice(country),
        pin_code=random.choice(pincodes),
        password=admin_password
    )
    admin_user.set_password(admin_password)
    admin_user.save()
    groups = Group.objects.get(name=Groups.Admin)
    groups.user_set.add(admin_user)
    logging.info("{} Admin user created.".format(admin_user.email))
    return admin_user


def run_seed(number):
    """
        Seed database for admin user creation
        How to use seed:
            # python manage.py shell
            # from users.seed import run_seed

            # to create 10 admin users
            # run_seed(number=10)

            # to delete all custom user data
            # clear_data()
        :argument number: number of admin user wish to create
        :return: None
    """
    if number <= 0:
        return
    # Creating 15 admin user
    for i in range(number):
        create_admin_user()