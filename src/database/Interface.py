from abc import abstractmethod, ABC

from database.Session import Role


class ChatRepository(ABC):

    @abstractmethod
    def create_new_session(self):
        pass

    @abstractmethod
    def get_all_session(self):
        pass

    @abstractmethod
    def get_current(self):
        pass

    @abstractmethod
    def get_current_session(self, session_id: int):
        pass

    @abstractmethod
    def add_message(self, message: str, role: Role):
        pass
