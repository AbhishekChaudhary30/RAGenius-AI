class ParserError(Exception):

    """Base parser exception."""

    pass


class UnsupportedFileTypeError(ParserError):

    """Raised when uploaded file type is not supported."""

    pass


class EmptyDocumentError(ParserError):

    """Raised when document has no readable text."""

    pass


class CorruptedDocumentError(ParserError):

    """Raised when document is corrupted."""

    pass


class FileTooLargeError(ParserError):

    """Raised when uploaded file exceeds maximum size."""

    pass