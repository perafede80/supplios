from enum import Enum

class Status(Enum):
    """Defines the set of possible states for any stateful component."""
    # TODO: Think if dividing these enums in three different categories would make the code more readable and robust
    # Generic lifecycle states
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    # Generic outcome states
    SUCCESSFUL = "Successful"
    FAILED = "Failed"

    # User type specific
    GUEST_USER = "Guest User"
    REGISTERED_USER = "Registered User"

    def __str__(self):
        return self.value