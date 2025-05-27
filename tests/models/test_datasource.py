from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import HttpUrl, ValidationError

from ferrea.models.datasource import BookDatasource

COVER_URL_1 = HttpUrl("https://somehost1.provider.country/cover1")
COVER_URL_2 = HttpUrl("https://somehost2.provider.country/some/randon/path/cover1")
PORTRAIT_1 = HttpUrl("https://somehost1.provider.country/portrait1")
PORTRAIT_2 = HttpUrl("https://somehost1.provider.country/portrait2")
PORTRAIT_3 = HttpUrl(
    "https://somehost2.provider.country/some_even-more/randon/path/portarait1?q=1234"
)
AUTHORS = [
    "Robert Jordan",
    "Brandon Sanderson",
]


@pytest.mark.parametrize(
    "cover_url, portrait_url, year, authors, expectation",
    [
        (
            COVER_URL_1,
            [
                PORTRAIT_1,
                PORTRAIT_2,
            ],
            2024,
            AUTHORS,
            does_not_raise(),
        ),
        (
            COVER_URL_2,
            [PORTRAIT_3],
            2025,
            [AUTHORS[0]],
            does_not_raise(),
        ),
    ],
)
def test_happy_path(
    cover_url: HttpUrl,
    portrait_url: list[HttpUrl],
    year: int,
    authors: list[str],
    expectation,
) -> None:
    """Test the happy path, where everything is fine."""
    with expectation as _:
        BookDatasource(
            title="The wheel of time",
            authors=authors,
            publishing="Don't remember",
            published_on=year,
            cover=cover_url,
            languages=["en"],
            book_formats=["physical", "ebook"],
            authors_portrait=portrait_url,
        )


def test_different_number_of_authors_and_portraits() -> None:
    """Test that a different number of authors and portraits has to raise a ValidationError"""
    with pytest.raises(ValidationError):
        BookDatasource(
            title="The wheel of time",
            authors=AUTHORS,
            publishing="Don't remember",
            published_on=2000,
            cover=COVER_URL_1,
            languages=["en"],
            book_formats=["physical", "ebook"],
            authors_portrait=[PORTRAIT_3],
        )


def test_wrong_year_format() -> None:
    """Test that a not four digits year has to raise a ValidationError."""
    with pytest.raises(ValidationError):
        BookDatasource(
            title="The wheel of time",
            authors=AUTHORS,
            publishing="Don't remember",
            published_on=20,
            cover=COVER_URL_1,
            languages=["en"],
            book_formats=["physical", "ebook"],
            authors_portrait=[PORTRAIT_3, PORTRAIT_1],
        )
