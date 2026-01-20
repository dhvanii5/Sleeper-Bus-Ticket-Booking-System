from fastapi import HTTPException, status


class SeatNotAvailableException(HTTPException):
    def __init__(self, detail: str = "Seat is not available for the selected route"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class BookingNotFoundException(HTTPException):
    def __init__(self, detail: str = "Booking not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class InvalidStationException(HTTPException):
    def __init__(self, detail: str = "Invalid station combination"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class CancellationNotAllowedException(HTTPException):
    def __init__(self, detail: str = "Cancellation is not allowed for this booking"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class DoubleBookingException(HTTPException):
    def __init__(self, detail: str = "Seat is already booked for this route segment"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class InvalidBookingException(HTTPException):
    def __init__(self, detail: str = "Invalid booking details"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
