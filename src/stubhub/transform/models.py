"""
Pydantic models for query response
"""

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, RootModel, field_serializer


class Item(BaseModel):
    """
    Picks out desired Fields to validate
    """

    model_config = ConfigDict(extra="ignore")

    eventId: int
    name: str
    url: HttpUrl
    dayOfWeek: str
    formattedDate: str
    formattedTime: str | None = Field(default=None)
    formattedDateYear: str | None = Field(default=None)
    formattedDateWithoutYear: str | None = Field(default=None)
    isTbd: bool
    isDateConfirmed: bool
    isTimeConfirmed: bool
    eventState: int
    venueId: int
    venueName: str
    formattedVenueLocation: str
    countryCode: str
    formattedMinPrice: str
    hasActiveListings: bool
    venueCity: str

    @field_serializer("url", when_used="always")
    def serialize_url(self, url: HttpUrl):
        """
        Ensures when model is serialized URL is converted to string
        """
        return url.unicode_string()


class Items(RootModel):
    """
    Root Model for Response
    """

    root: list[Item]

    def to_df(self):
        """
        Simple json to dataframe conversion
        """
        return pl.from_dicts(self.model_dump())
