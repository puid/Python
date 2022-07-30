class PuidError(Exception):
    """Base class for Puid Errors"""

    pass


class BitsError(PuidError):
    """
    Raised when
      - bits is non-negative
      - bits specified with total/risk
    """
    pass


class TotalRiskError(PuidError):
    """
    Raised when
      - total or risk are not non-negative
      - total and risk are not both specified
    """
    pass
