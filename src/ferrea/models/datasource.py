from pydantic import BaseModel, HttpUrl, field_validator, model_validator
from typing_extensions import Self

_AFTER_MODE = "after"


class BookDatasource(BaseModel):
    """
    This class describes how a Datasource instance should be structured.
    """

    title: str
    authors: list[str]
    publishing: str | None = None
    published_on: int | None = None
    cover: HttpUrl | None = None
    plot: str | None = None
    languages: list[str] | None = None
    book_formats: list[str] | None = None
    authors_portrait: list[HttpUrl] | None = None

    @field_validator("published_on", mode=_AFTER_MODE)
    @classmethod
    def is_year(cls, value: int) -> int:
        """Check that the year is a four digit number."""
        is_four_digits_len = value // 1_000 > 0 and value // 10_000 == 0
        if not is_four_digits_len:
            raise ValueError(f"{value} is not a four digits year.")
        return value

    @model_validator(mode=_AFTER_MODE)
    def check_len_of_authors_and_portraits(self) -> Self:
        """Check that the len of authors and portraits match."""
        if self.authors_portrait is not None:
            if len(self.authors) != len(self.authors_portrait):
                raise ValueError(
                    "The number of authors portrait should match the number of authors."
                    f" Received {len(self.authors)} authors and {len(self.authors_portrait)} portraits."
                )
        return self
