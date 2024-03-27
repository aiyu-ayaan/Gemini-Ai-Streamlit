from abc import abstractmethod, ABC

from database.Session import Role


class ChatRepository(ABC):
    """Interface for the ChatRepository class,Defines the methods that the ChatRepository class should implement.

    Args:
        ABC (ABC): Abstract Base Class
    """

    @abstractmethod
    def create_new_session(self):
        """Method to create a new session.
        """
        pass

    @abstractmethod
    def get_all_session(self):
        """Method to get all the sessions.
        Returns:
            list: List of all the sessions
        """
        pass

    @abstractmethod
    def get_current(self):
        """Method to create a new session.
        Returns:
            Session: Current session
        """
        pass

    @abstractmethod
    def get_current_session(self, session_id: int):
        """Method to get session by id

        Args:
            session_id (int): Session id
        Returns:
            Session: Session with the given id
        """
        pass

    @abstractmethod
    def add_message(self, message: str, role: Role):
        """_summary_

        Args:
            message (str): Message to be added
            role (Role): Role of the user
        """
        pass
