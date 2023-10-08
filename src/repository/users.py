from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.

    :param email: Pass the email address of the user to be retrieved
    :type email: str
    :param db: Pass the database session to the function
    :type db: Session
    :return: User with given email
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: Create a new user
    :type body: UserModel
    :param db: Access the database
    :type db: Session
    :return: New user
    :rtype: User
    """
    avatar = None

    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: Identify the user that is being updated
    :type user: User
    :param token: Set the refresh token for a user
    :Type token: str | None
    :param db: Commit the changes to the database
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.

    :param email: Get the email address of the user
    :type email: str
    :param db: Pass the database session into the function
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.


    :param email: Get the user from the database
    :type email: str
    :param url: Specify the type of data that is being passed in
    :type url: str
    :param db: Pass the database session to the function
    :type db: Session
    :return: User with given email
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()

    return user
