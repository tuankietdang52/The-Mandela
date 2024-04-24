import abc

from src.hud.hudcomp import *


class MenuContract(abc.ABC):
    class IView(abc.ABC):
        @abc.abstractmethod
        def setup(self):
            pass

        @abc.abstractmethod
        def get_elements(self):
            pass

        @abc.abstractmethod
        def get_screen(self):
            pass

        @abc.abstractmethod
        def set_choice(self, choice: int):
            pass

        @abc.abstractmethod
        def get_choice(self) -> int:
            pass

        @abc.abstractmethod
        def draw(self):
            pass

        @abc.abstractmethod
        def update(self):
            pass

    class IPresenter(abc.ABC):
        @abc.abstractmethod
        def get_pointer(self) -> Pointer:
            pass

        @abc.abstractmethod
        def set_pointer_position(self, pos: tuple[float, float]):
            pass

        @abc.abstractmethod
        def selecting(self):
            """checking user input"""
            pass

    class IModel(abc.ABC):
        @abc.abstractmethod
        def increase_choice(self):
            pass

        @abc.abstractmethod
        def decrease_choice(self):
            pass

        @abc.abstractmethod
        def get_choice(self) -> int:
            pass
