"""HW00 — Analysis: Songs Dataset

Implement the pieces below using plain Python: file I/O, a Counter-based
aggregation, and a small class hierarchy for ranking songs. The dataset is
data/songs.csv (open it to see the raw rows). Its columns are:

    title             str    song title
    artist            str    performing artist
    genre             str    e.g. Pop, Rock, Hip-Hop
    year              int    year the song charted
    weeks_on_chart    int    total weeks the song spent on the chart
    peak_position     int    best chart position reached (1 = number one)
    streams_millions  float  total streams, in millions

After completing the functions, run this script to print your results:

    uv run python analysis.py

Use the printed output to answer the questions in writeup.md.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


def load_songs(path: Path) -> list[dict]:
    """Load the songs CSV and return a list of records, one dict per row.

    Casts year, weeks_on_chart, and peak_position to int, and
    streams_millions to float. All other fields stay strings.

    Args:
        path: Path to the songs CSV file.

    Returns:
        A list of dicts, one per song, with the correct field types.

    Example:
        >>> songs = load_songs(Path("data/songs.csv"))
        >>> isinstance(songs[0]["year"], int)
        True
    """
    with path.open(mode="r", encoding="utf-8") as songs_csv:
        r_songs = csv.DictReader(songs_csv)
        return [{
                **song,
                'year':int(song['year']),
                'weeks_on_chart':int(song['weeks_on_chart']),
                'peak_position':int(song['peak_position']),
                'streams_millions':float(song['streams_millions'])
            }
            for song in r_songs]
    # raise NotImplementedError("Implement load_songs()")


class SongRanker:
    """Base class for ranking a list of songs by some criterion.

    Subclasses implement score() to define what "best" means; rank() is
    shared logic that works for any scoring rule.
    """

    def score(self, song: dict) -> float:
        """Return the value used to rank this song. Higher is better.

        Subclasses must override this.
        """
        raise NotImplementedError("Implement SongRanker.score()")

    def rank(self, songs: list[dict], n: int = 10) -> list[dict]:
        """Return the top n songs, highest score() first.

        Args:
            songs: List of song records (as returned by load_songs).
            n: Number of songs to return (default 10).

        Returns:
            A list of the n songs with the highest score(), sorted
            highest-first. Ties may break in any order.

        Example:
            >>> top = StreamsRanker().rank(songs, n=3)
            >>> len(top)
            3
            >>> top[0]["streams_millions"] >= top[1]["streams_millions"]
            True
        """
        return sorted(songs, key=lambda song: self.score(song), reverse=True)[:n]
        # raise NotImplementedError("Implement SongRanker.rank()")


class StreamsRanker(SongRanker):
    """Ranks songs by total streams_millions."""

    def score(self, song: dict) -> float:
        return song['streams_millions']
        # raise NotImplementedError("Implement StreamsRanker.score()")


class LongevityRanker(SongRanker):
    """Ranks songs by weeks_on_chart (how long they stuck around)."""

    def score(self, song: dict) -> float:
        return song['weeks_on_chart']
        # raise NotImplementedError("Implement LongevityRanker.score()")


def avg_weeks_by_genre(songs: list[dict]) -> dict[str, float]:
    """Return the average weeks_on_chart for each genre.

    Args:
        songs: List of song records.

    Returns:
        A dict mapping genre name (str) to average weeks (float).

    Example:
        >>> avgs = avg_weeks_by_genre(songs)
        >>> isinstance(avgs, dict)
        True
        >>> all(isinstance(v, float) for v in avgs.values())
        True
    """
    genre_weeks = {}
    genre_counts = {}
    for song in songs:
        genre = song['genre']
        genre_weeks[genre] = genre_weeks.get(genre, 0) + song['weeks_on_chart']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    for key in genre_weeks:
        genre_weeks[key] /= genre_counts[key]

    return genre_weeks
    # raise NotImplementedError("Implement avg_weeks_by_genre()")


def most_streamed_artist(songs: list[dict]) -> str:
    """Return the name of the artist with the highest total streams_millions.

    If an artist has multiple songs, sum all their streams.

    Args:
        songs: List of song records.

    Returns:
        The artist name as a string.

    Example:
        >>> artist = most_streamed_artist(songs)
        >>> isinstance(artist, str)
        True
    """
    artist_streams = {}
    for song in songs:
        artist = song['artist']
        artist_streams[artist] = artist_streams.get(artist, 0) + song['streams_millions']

    return max(artist_streams, key=artist_streams.get) #type: ignore
    # raise NotImplementedError("Implement most_streamed_artist()")


def hits_per_year(songs: list[dict], max_position: int = 10) -> dict[int, int]:
    """Count songs with peak_position <= max_position, grouped by year.

    A "hit" is any song that reached position max_position or better (lower
    number). Only years that have at least one hit appear in the result; a
    year with no qualifying songs is omitted entirely (do not include it with
    a count of 0).

    Args:
        songs: List of song records.
        max_position: Peak position threshold (default 10).

    Returns:
        A dict mapping year (int) to hit count (int).

    Example:
        >>> hits = hits_per_year(songs, max_position=5)
        >>> all(isinstance(k, int) for k in hits.keys())
        True
    """
    return Counter([song['year'] for song in songs if song['peak_position'] <= max_position])
    # raise NotImplementedError("Implement hits_per_year()")


# ── Main: print results for writeup.md ────────────────────────────────────────

if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "songs.csv"
    songs = load_songs(data_path)

    print("=== Top 10 Songs by Streams ===")
    top = StreamsRanker().rank(songs, n=10)
    for song in top:
        print(f"  {song['title']} — {song['artist']} ({song['streams_millions']:.0f}M streams)")

    print("\n=== Top 10 Songs by Weeks on Chart ===")
    longest = LongevityRanker().rank(songs, n=10)
    for song in longest:
        print(f"  {song['title']} — {song['artist']} ({song['weeks_on_chart']} weeks)")

    print("\n=== Average Weeks on Chart by Genre ===")
    avg_weeks = avg_weeks_by_genre(songs)
    for genre, avg in sorted(avg_weeks.items(), key=lambda x: -x[1]):
        n_songs = sum(1 for s in songs if s["genre"] == genre)
        label = "song" if n_songs == 1 else "songs"
        print(f"  {genre}: {avg:.1f} weeks  ({n_songs} {label})")

    print("\n=== Most Streamed Artist ===")
    artist = most_streamed_artist(songs)
    total_streams = sum(s["streams_millions"] for s in songs if s["artist"] == artist)
    print(f"  {artist} ({total_streams:.0f}M total streams)")

    print("\n=== Top-10 Hits per Year (peak position <= 10) ===")
    hits = hits_per_year(songs, max_position=10)
    for year, count in sorted(hits.items()):
        print(f"  {year}: {count} hit(s)")