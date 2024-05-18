from abc import ABC, abstractmethod

class BasePage(ABC):

    @abstractmethod
    def show_page(self):
        """Display the page content."""
        pass

    @abstractmethod
    def label(self):
        """Return the label for the menu."""
        pass

    @abstractmethod
    def icon(self):
        """Return the icon for the menu."""
        pass

    @abstractmethod
    def order(self):
        """Return the order for the menu."""
        pass
