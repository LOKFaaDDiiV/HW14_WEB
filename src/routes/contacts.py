from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.database.models import Contact, User
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/find", response_model=List[ContactResponse])
async def find_contacts(firstname: str = Query(None), lastname: str = Query(None), email: str = Query(None),
                        user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The find_contacts function is used to find contacts in the database.

    :param db: Get the database session
    :type db: Session
    :param user: Get the user id from the token
    :type user: User
    :param firstname: Search for contacts by firstname
    :type firstname: str
    :param lastname: Search for a contact by lastname
    :type lastname: str
    :param email: Filter the contacts by email
    :type email: str
    :return: A list of contacts
    :rtype: list[Contacts]
    """
    contacts = await repository_contacts.find_contacts(db, user, firstname, lastname, email)

    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")

    return contacts


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10,
                        user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_contacts function returns a list of contacts for the current user.

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
    contacts = await repository_contacts.get_contacts(skip, limit, user, db)

    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int,
                       user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_contact function returns a contact by its ID.

    :param user: Get the user from the database
    :type user: User
    :param contact_id: Filter the contact by id
    :type contact_id: int
    :param db: Get the database session
    :type db: Session
    :return: The first contact found in the database that matches the user_id and contact_id
    :rtype: Contact | None
    """
    contact = await repository_contacts.get_contact(contact_id, user, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def nearest_birthdays(days: int | None = 7,
                            user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The nearest_birthdays function returns the nearest birthdays of a user's contacts.

    :param user: Get the user id from the database
    :type user: User
    :param days: Number of days to search
    :type days: int | None
    :param db: Session: Pass in the database session to the function
    :type db: Session
    :return: A list of contacts that have birthdays within the next 7 days
    :rtype: list[Contact]
    """
    contacts = await repository_contacts.get_birthdays(days, user, db)

    if not len(contacts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No birthdays found in {days} days")

    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel,
                         user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: Get the data from the request body
    :type body: ContactModel
    :param user: Get the user id from the token
    :type user: User
    :param db: Get the database session
    :type db: Session
    :return: New contact
    :rtype: Contact
    """
    return await repository_contacts.create_contact(body, user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate,
                         user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
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
    contact = await repository_contacts.update_contact(contact_id, body, user, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int,
                         user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.

    :param user: Identify the user who is making the request
    :type user: User
    :param contact_id: Identify the contact to be removed
    :type contact_id: int
    :param db: Pass the database session to the function
    :type db: Session
    :return: The contact object if it was deleted, otherwise none
    :rtype: Contact | None
    """
    contact = await repository_contacts.remove_contact(contact_id, user, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact
