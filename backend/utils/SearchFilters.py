class SearchFilters:
    def __init__(self, filters: dict(
        postalCode = None,
        price_range = (None, None),
        amenities = [],
        availabilityWindow = (None, None),
        minRating = 1,
        ascending = True
    )):
        self.filters = filters