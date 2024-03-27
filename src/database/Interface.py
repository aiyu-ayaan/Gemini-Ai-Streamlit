from abc import abstractmethod, ABC

from database.Session import Role


class ChatRepository(ABC):
    """
    Interface for the ChatRepository class,
    Defines the methods that the ChatRepository class should implement.
    """

    @abstractmethod
    def create_new_session(self):
        """
        Method to create a new session.
        """
        pass

    @abstractmethod
    def get_all_session(self):
        """
        Method to get all the sessions.
        :return: List of all the sessions
        """
        pass

    @abstractmethod
    def get_current(self):
        """
        Method to get the current session.
        :return: The current session
        """
        pass

    @abstractmethod
    def get_current_session(self, session_id: int):
        """
        Method to get session by id
        :param session_id: Session id to get the session.
        :return: Session with the given id or None if not found
        """
        pass

    @abstractmethod
    def add_message(self, message: str, role: Role):
        """
        Method to add a message to the current session.
        :param message: Message to add
        :param role: the Role of the user who sent the message
        """
        pass
