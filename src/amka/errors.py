"""Application error types for Amka."""


class AmkaError(Exception):
    """Base class for all Amka errors."""


class InvalidScheduleError(AmkaError):
    """Raised when an alarm schedule cannot be parsed or resolved."""


class AlarmNotFoundError(AmkaError):
    """Raised when an alarm cannot be found."""


class InvalidStateTransitionError(AmkaError):
    """Raised when an alarm state transition is not allowed."""


class PersistenceError(AmkaError):
    """Raised when alarm persistence fails."""


class VersionConflictError(AmkaError):
    """Raised when an alarm version conflict is detected."""


class NotificationError(AmkaError):
    """Raised when notification delivery fails."""
