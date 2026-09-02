"""Tests for HW00 Part 2 — analysis.py

Tests use a synthetic list of song records instead of the real songs.csv so
that:
  - Tests check your logic, not whether you hardcoded the right answer.
  - Tests are fast and self-contained.

Run with: uv run pytest -m songs
"""

from __future__ import annotations

from pathlib import Path

import pytest

from analysis import (
    LongevityRanker,
    SongRanker,
    StreamsRanker,
    avg_weeks_by_genre,
    hits_per_year,
    load_songs,
    most_streamed_artist,
)

# ── Shared fixture ─────────────────────────────────────────────────────────────

SAMPLE: list[dict] = [
    {
        "title": "Song A",
        "artist": "Artist X",
        "genre": "Pop",
        "year": 2021,
        "weeks_on_chart": 20,
        "peak_position": 1,
        "streams_millions": 1000.0,
    },
    {
        "title": "Song B",
        "artist": "Artist Y",
        "genre": "Rock",
        "year": 2021,
        "weeks_on_chart": 10,
        "peak_position": 5,
        "streams_millions": 500.0,
    },
    {
        "title": "Song C",
        "artist": "Artist X",
        "genre": "Pop",
        "year": 2022,
        "weeks_on_chart": 30,
        "peak_position": 2,
        "streams_millions": 800.0,
    },
    {
        "title": "Song D",
        "artist": "Artist Z",
        "genre": "Hip-Hop",
        "year": 2022,
        "weeks_on_chart": 15,
        "peak_position": 8,
        "streams_millions": 300.0,
    },
    {
        "title": "Song E",
        "artist": "Artist Y",
        "genre": "Rock",
        "year": 2023,
        "weeks_on_chart": 25,
        "peak_position": 12,
        "streams_millions": 600.0,
    },
    {
        "title": "Song F",
        "artist": "Artist X",
        "genre": "Pop",
        "year": 2023,
        "weeks_on_chart": 5,
        "peak_position": 3,
        "streams_millions": 400.0,
    },
]


@pytest.fixture
def sample_songs() -> list[dict]:
    return [dict(song) for song in SAMPLE]


# ── Tests ──────────────────────────────────────────────────────────────────────


@pytest.mark.songs
class TestLoadSongs:
    def test_returns_list_of_dicts(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
        )
        songs = load_songs(csv_path)
        assert isinstance(songs, list), (
            f"load_songs should return a list; got {type(songs).__name__}"
        )
        assert isinstance(songs[0], dict), (
            f"each record should be a dict; got {type(songs[0]).__name__}"
        )

    def test_year_is_int(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
        )
        songs = load_songs(csv_path)
        assert isinstance(songs[0]["year"], int), (
            f"'year' should be an int; got {type(songs[0]['year']).__name__}"
        )

    def test_weeks_on_chart_is_int(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
        )
        songs = load_songs(csv_path)
        assert isinstance(songs[0]["weeks_on_chart"], int), (
            f"'weeks_on_chart' should be an int; got {type(songs[0]['weeks_on_chart']).__name__}"
        )

    def test_peak_position_is_int(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
        )
        songs = load_songs(csv_path)
        assert isinstance(songs[0]["peak_position"], int), (
            f"'peak_position' should be an int; got {type(songs[0]['peak_position']).__name__}"
        )

    def test_streams_is_float(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
        )
        songs = load_songs(csv_path)
        assert isinstance(songs[0]["streams_millions"], float), (
            f"'streams_millions' should be a float; "
            f"got {type(songs[0]['streams_millions']).__name__}"
        )

    def test_loads_all_rows(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "songs.csv"
        csv_path.write_text(
            "title,artist,genre,year,weeks_on_chart,peak_position,streams_millions\n"
            "Song A,Artist X,Pop,2021,20,1,1000.0\n"
            "Song B,Artist Y,Rock,2021,10,5,500.0\n"
        )
        songs = load_songs(csv_path)
        assert len(songs) == 2, f"expected 2 rows; got {len(songs)}"


@pytest.mark.songs
class TestSongRanker:
    def test_base_score_not_implemented(self) -> None:
        with pytest.raises(NotImplementedError):
            SongRanker().score(SAMPLE[0])

    def test_streams_ranker_returns_n_rows(self, sample_songs: list[dict]) -> None:
        result = StreamsRanker().rank(sample_songs, n=3)
        assert len(result) == 3, f"rank(songs, n=3) should return 3 songs; got {len(result)}"

    def test_streams_ranker_sorted_descending(self, sample_songs: list[dict]) -> None:
        result = StreamsRanker().rank(sample_songs, n=6)
        streams = [s["streams_millions"] for s in result]
        assert streams == sorted(streams, reverse=True), (
            f"Songs should be sorted by streams_millions descending; got {streams}"
        )

    def test_streams_ranker_top_song(self, sample_songs: list[dict]) -> None:
        result = StreamsRanker().rank(sample_songs, n=1)
        # Song A has 1000.0 -- the highest in SAMPLE
        assert result[0]["streams_millions"] == 1000.0, (
            f"Top song by streams should have 1000.0 streams; got {result[0]['streams_millions']}"
        )

    def test_default_n_is_10(self, sample_songs: list[dict]) -> None:
        result = StreamsRanker().rank(sample_songs)
        assert len(result) == min(10, len(sample_songs)), (
            f"Default n=10 with {len(sample_songs)} songs should return all of "
            f"them; got {len(result)}"
        )

    def test_longevity_ranker_sorted_descending(self, sample_songs: list[dict]) -> None:
        result = LongevityRanker().rank(sample_songs, n=6)
        weeks = [s["weeks_on_chart"] for s in result]
        assert weeks == sorted(weeks, reverse=True), (
            f"Songs should be sorted by weeks_on_chart descending; got {weeks}"
        )

    def test_longevity_ranker_top_song(self, sample_songs: list[dict]) -> None:
        result = LongevityRanker().rank(sample_songs, n=1)
        # Song C has 30 weeks on chart -- the highest in SAMPLE
        assert result[0]["title"] == "Song C", (
            f"Top song by weeks_on_chart should be Song C (30 weeks); got {result[0]['title']}"
        )


@pytest.mark.songs
class TestAvgWeeksByGenre:
    def test_returns_dict(self, sample_songs: list[dict]) -> None:
        result = avg_weeks_by_genre(sample_songs)
        assert isinstance(result, dict), (
            f"avg_weeks_by_genre should return a dict; got {type(result).__name__}"
        )

    def test_all_genres_present(self, sample_songs: list[dict]) -> None:
        result = avg_weeks_by_genre(sample_songs)
        assert set(result.keys()) == {"Pop", "Rock", "Hip-Hop"}, (
            f"Expected genres Pop, Rock, Hip-Hop; got {set(result.keys())}"
        )

    def test_pop_average(self, sample_songs: list[dict]) -> None:
        # Pop songs: 20, 30, 5 -> avg = 55/3 ~ 18.33
        result = avg_weeks_by_genre(sample_songs)
        expected = (20 + 30 + 5) / 3
        assert abs(result["Pop"] - expected) < 1e-6, (
            f"Pop avg weeks: expected {expected:.4f}; got {result['Pop']}"
        )

    def test_rock_average(self, sample_songs: list[dict]) -> None:
        # Rock songs: 10, 25 -> avg = 17.5
        result = avg_weeks_by_genre(sample_songs)
        assert abs(result["Rock"] - 17.5) < 1e-6, (
            f"Rock avg weeks: expected 17.5; got {result['Rock']}"
        )

    def test_hiphop_average(self, sample_songs: list[dict]) -> None:
        # Hip-Hop songs: 15 -> avg = 15.0
        result = avg_weeks_by_genre(sample_songs)
        assert abs(result["Hip-Hop"] - 15.0) < 1e-6, (
            f"Hip-Hop avg weeks: expected 15.0; got {result['Hip-Hop']}"
        )


@pytest.mark.songs
class TestMostStreamedArtist:
    def test_returns_string(self, sample_songs: list[dict]) -> None:
        result = most_streamed_artist(sample_songs)
        assert isinstance(result, str), (
            f"most_streamed_artist should return a string; got {type(result).__name__}"
        )

    def test_correct_artist(self, sample_songs: list[dict]) -> None:
        # Artist X: 1000 + 800 + 400 = 2200
        # Artist Y: 500 + 600 = 1100
        # Artist Z: 300
        result = most_streamed_artist(sample_songs)
        assert result == "Artist X", f"Artist X has 2200M total streams (highest); got {result!r}"

    def test_uses_total_not_single(self, sample_songs: list[dict]) -> None:
        # Artist Y has the highest single song (600M) but Artist X wins on
        # total (2200M vs 1100M)
        result = most_streamed_artist(sample_songs)
        assert result == "Artist X", (
            f"Artist X has 2200M total; Artist Y only has 1100M total — "
            f"sum all songs, don't just take the highest single; got {result!r}"
        )

    def test_custom_data(self) -> None:
        songs = [
            {"artist": "Solo", "streams_millions": 900.0},
            {"artist": "Multi", "streams_millions": 500.0},
            {"artist": "Multi", "streams_millions": 600.0},
        ]
        result = most_streamed_artist(songs)
        # Multi: 500+600=1100 > Solo: 900
        assert result == "Multi", f"Multi has 1100M total vs Solo's 900M; got {result!r}"


@pytest.mark.songs
class TestHitsPerYear:
    def test_returns_dict(self, sample_songs: list[dict]) -> None:
        result = hits_per_year(sample_songs)
        assert isinstance(result, dict), (
            f"hits_per_year should return a dict; got {type(result).__name__}"
        )

    def test_correct_counts_default(self, sample_songs: list[dict]) -> None:
        # peak_position <= 10: Song A(1), Song B(5), Song C(2), Song D(8), Song F(3)
        # Song E has peak_position=12 -- excluded
        # 2021: A(1), B(5) = 2 hits
        # 2022: C(2), D(8) = 2 hits
        # 2023: F(3) = 1 hit  [E is excluded]
        result = hits_per_year(sample_songs, max_position=10)
        assert result.get(2021) == 2, (
            f"2021 should have 2 hits (positions 1 and 5); got {result.get(2021)}"
        )
        assert result.get(2022) == 2, (
            f"2022 should have 2 hits (positions 2 and 8); got {result.get(2022)}"
        )
        assert result.get(2023) == 1, (
            f"2023 should have 1 hit (position 3 only; position 12 is excluded); "
            f"got {result.get(2023)}"
        )

    def test_strict_cutoff(self, sample_songs: list[dict]) -> None:
        # max_position=5: only positions 1, 5, 2, 3 qualify (not 8, 12)
        result = hits_per_year(sample_songs, max_position=5)
        assert result.get(2021) == 2, (
            f"2021 with max_position=5: positions 1 and 5 both qualify; got {result.get(2021)}"
        )
        assert result.get(2022) == 1, (
            f"2022 with max_position=5: only position 2 qualifies (8 is excluded); "
            f"got {result.get(2022)}"
        )

    def test_year_with_no_hits_excluded(self, sample_songs: list[dict]) -> None:
        # max_position=1: only Song A (position 1) qualifies -> 2021 only
        result = hits_per_year(sample_songs, max_position=1)
        assert 2021 in result, "2021 has a song at position 1 and should appear"
        assert 2022 not in result, "2022 has no songs at position 1 and should not appear in result"
        assert 2023 not in result, "2023 has no songs at position 1 and should not appear in result"
