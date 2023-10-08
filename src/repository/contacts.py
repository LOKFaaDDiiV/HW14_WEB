from typing import List
from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate


async def find_contacts(db: Session, user: User,
                        firstname: str = None, lastname: str = None, email: str = None) -> List[Contact]:
    """
    The find_contacts function is used to search for contacts in the database.

    :param db: Session: Connect to the database
    :type db: Session
    :param user: User: Get the user id from the user table
    :type user: User
    :param firstname: Filter the contacts by firstname
    :type firstname: str
    :param lastname: Filter the contacts by lastname
    :type lastname: str
    :param email: Filter the contacts by email
    :type email: str
    :return: A list of contacts with given parameters
    :rtype: list[Contact]
    """
    query = db.query(Contact).filter(Contact.user_id == user.id)

    if firstname:
        query = query.filter(Contact.firstname.ilike(f"%{firstname}%"))
    if lastname:
        query = query.filter(Contact.lastname.ilike(f"%{lastname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contact = query.all()

    return contact


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the specified user.

    :param user: Get the user_id from the user object
    :type user: User
    :param skip: Skip the first n contacts
    :type skip: int
    :param limit: Limit the number of contacts that are returned
    :type limit: int
    :param db: Pass the database session to the function
    :type db: Session
    :return: A list of contacts for a user
    :rtype: list[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a current contact for the specified user.

    :param user: Get the user from the database
    :type user: User
    :param contact_id: Filter the contact by id
    :type contact_id: int
    :param db: Get the database session
    :type db: Session
    :return: The first contact found in the database that matches the user_id and contact_id
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_birthdays(num_days: int, user: User, db: Session) -> List[Contact]:
    """
    The get_birthdays function returns a list of contacts whose birthdays are within the next 7 days.

    :param user: Get the user id from the database
    :type user: User
    :param db: Session: Pass in the database session to the function
    :type db: Session
    :return: A list of contacts that have birthdays within the next 7 days
    :rtype: list[Contact]
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    today = datetime.now().date()
    end_date = today + timedelta(days=num_days)
    nearest_birthdays = []

    for contact in contacts:

        contact_birth_in_this_year = contact.born_date.replace(year=today.year)

        if today <= contact_birth_in_this_year <= end_date:
            nearest_birthdays.append(contact)

    return nearest_birthdays


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact for the specified user in the database.

    :param body: Get the data from the request body
    :type body: ContactModel
    :param user: Get the user id from the token
    :type user: User
    :param db: Get the database session
    :type db: Session
    :return: New contact
    :rtype: Contact
    """
    contact = Contact(firstname=body.firstname, lastname=body.lastname, phone_number=body.phone_number,
                      email=body.email, born_date=body.born_date, user=user)

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.

    :param user: Get the user id from the token
    :type user: User
    :param contact_id: Identify the contact that is being updated
    :type contact_id: int
    :param body: Get the data from the request body
    :type body: ContactUpdate
    :param db: Access the database
    :type db: Session
    :return: An updated contact object
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone_number = body.phone_number
        contact.email = body.email
        contact.born_date = body.born_date
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a current contact from the database.

    :param user: Identify the user who is making the request
    :type user: User
    :param contact_id: Identify the contact to be removed
    :type contact_id: int
    :param db: Pass the database session to the function
    :type db: Session
    :return: The contact object if it was deleted, otherwise none
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact
