from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    datail = "There are no available rooms left"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_409_CONFLICT
    datail = "Date from cannot be after date to"


class DateFromMustBeAfterCurrentDate(BookingException):
    status_code = status.HTTP_409_CONFLICT
    datail = "Date from must be after current date"


class HotelDoesNotExists(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotel does not exists"
