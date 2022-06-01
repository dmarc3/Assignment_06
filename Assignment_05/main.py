'''
main driver for a simple social network project
'''
import csv
import re
import logging
import pymongo
import Assignment_05.users as users
import Assignment_05.user_status as user_status


def init_user_collection(mongo, name='UserAccounts'):
    '''
    Creates and returns a new instance of UserCollection
    '''
    return users.UserCollection(mongo, name)


def init_status_collection(mongo, name='StatusUpdates'):
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    return user_status.UserStatusCollection(mongo, name)


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    # Loop through each row in csv file
    keys = {'USER_ID':  {'validate': validate_user_id,  'key': 'user_id'},
            'EMAIL':    {'validate': validate_email,    'key': 'user_email'},
            'NAME':     {'validate': validate_name,     'key': 'user_name'},
            'LASTNAME': {'validate': validate_name,     'key': 'user_last_name'}}
    return load_collection(filename, keys, user_collection)


def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.

    Author: Marcus Bakke
    '''
    keys = {'STATUS_ID':   {'validate': validate_status_id,   'key': 'status_id'},
            'USER_ID':     {'validate': validate_user_id,     'key': 'user_id'},
            'STATUS_TEXT': {'validate': validate_status_text, 'key': 'status_text'}}
    return load_collection(filename, keys, status_collection)


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    if not validate_user_inputs(user_id, email, user_name, user_last_name):
        return False
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # Validate inputs
    if not validate_user_inputs(user_id, email, user_name, user_last_name):
        return False
    return user_collection.modify_user(user_id, email, user_name, user_last_name)


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    return user_collection.search_user(user_id)


def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    # Validate inputs
    if not validate_status_inputs(status_id, user_id, status_text):
        return False
    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # Validate inputs
    if not validate_status_inputs(status_id, user_id, status_text):
        return False
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    return status_collection.search_status(status_id)

# New functions

def load_collection(filename, keys, collection):
    '''
    Method which loads status or user collection from CSV file
    '''
    # Loop through each row in csv file
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                new_row = row.copy()
                # Check for errors in current row
                for key, value in row.items():
                    if value.replace(' ', '') == '':
                        print(f'Empty value found for {key} on ' \
                            f'line {reader.line_num} of {filename}.')
                        return False
                    # Validate input
                    try:
                        if not keys[key]['validate'](value):
                            return False
                    except KeyError:
                        return False
                    # Replace keys
                    new_row[keys[key]['key']] = new_row.pop(key)
                # Append data
                data.append(new_row)
            # Add data to database
            try:
                with collection.mongo:
                    collection.database.insert_many(data)
                    logging.info("Inserting %i %s from %s into database at %s.",
                                 len(data),
                                 collection.name,
                                 filename,
                                 str(collection.mongo.host)+':'+str(collection.mongo.port))
            except pymongo.errors.BulkWriteError as exc:
                logging.error('pymongo BulkWriteError encountered.')
                logging.error(exc.details['writeErrors'][0]['errmsg'])
                return False
        return True
    except FileNotFoundError:
        return False


def validate_user_id(user_id):
    '''
    Validates user_id
    '''
    user_id = user_id.replace(' ', '_')
    # Checks if user_id be converted to integer
    try:
        int(user_id)
        return False
    except ValueError:
        return True


def validate_email(email):
    '''
    Validates email
    '''
    email = email.replace(' ', '')
    # Validates email address via regex
    # Source: https://stackoverflow.com/a/8022584
    regex = r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$"
    if not re.match(regex, email):
        return False
    return True


def validate_name(name):
    '''
    Validates user_name
    '''
    name = name.replace(' ', '')
    # Check if name contains only letters
    for chars in ['-', "'"]:
        name = name.replace(chars, '')
    if not name.isalpha():
        return False
    return True


def validate_status_id(status_id):
    '''
    Validates status_id
    '''
    # Check if first half is valid user_id
    status_id = status_id.split('_')
    # Check if more than _
    if len(status_id) > 2 or len(status_id) == 1:
        return False
    # Check if first half is valid user_id
    if not validate_user_id(status_id[0]):
        return False
    # Check if second half of string can be converted to int
    try:
        int(status_id[1])
        return True
    except ValueError:
        return False


def validate_status_text(status_text):
    '''
    Accept any text input
    '''
    if isinstance(status_text, str):
        return True
    return False


def validate_user_inputs(user_id, email, user_name, user_last_name):
    '''
    Validates all user inputs
    '''
    # Validate inputs
    if not validate_user_id(user_id):
        logging.error('Invalid user_id: %s', user_id)
        return False
    if not validate_email(email):
        logging.error('Invalid email: %s', email)
        return False
    if not validate_name(user_name):
        logging.error('Invalid user_name: %s', user_name)
        return False
    if not validate_name(user_last_name):
        logging.error('Invalid user_last_name: %s', user_last_name)
        return False
    return True


def validate_status_inputs(status_id, user_id, status_text):
    '''
    Validates all status inputs
    '''
    # Validate inputs
    if not validate_status_id(status_id):
        logging.error('Invalid status_id: %s', status_id)
        return False
    if not validate_user_id(user_id):
        logging.error('Invalid user_id: %s', user_id)
        return False
    if not validate_status_text(status_text):
        logging.error('Invalid status_text: %s', status_text)
        return False
    return True
