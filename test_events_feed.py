import pytest
from unittest.mock import patch
import events_feed as feed
from event_entry import EventEntry


# ============================================================================
# MOCK RSS ENTRY CLASS
# ============================================================================

class MockRSSEntry:
    """Simple mock class to represent an RSS entry with required attributes."""

    def __init__(self, id, title, link, summary):
        self.id = id
        self.title = title
        self.link = link
        self.summary = summary


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_rss_entry():
    """Create a mock RSS entry as returned by reader.get_entries()."""
    return MockRSSEntry(
        id="rss-id-123",
        title="Test RSS Event",
        link="https://webapps.macalester.edu/event/123",
        summary="<strong>November 15, 2025 | 2:00 PM - 4:00 PM | Library</strong><p>Event description</p>"
    )


@pytest.fixture
def mock_rss_entries(mock_rss_entry):
    """Create multiple mock RSS entries."""
    entry2 = MockRSSEntry(
        id="rss-id-456",
        title="Another RSS Event",
        link="https://webapps.macalester.edu/event/456",
        summary="<strong>November 20, 2025 | 10:00 AM - 12:00 PM | Humanities</strong><p>Another event</p>"
    )

    return [mock_rss_entry, entry2]


# ============================================================================
# EVENTS FEED TESTS
# ============================================================================

class TestGetEvents:
    """Test cases for the get_events() function."""

    @patch('events_feed.reader.get_entries')
    def test_get_events_returns_list_of_event_entries(self, mock_get_entries, mock_rss_entry):
        """Test that get_events returns a list of EventEntry objects."""
        mock_get_entries.return_value = [mock_rss_entry]

        events = feed.get_events()

        assert isinstance(events, list)
        assert len(events) == 1
        assert isinstance(events[0], EventEntry)

    @patch('events_feed.reader.get_entries')
    def test_get_events_returns_empty_list_when_no_entries(self, mock_get_entries):
        """Test that get_events returns empty list when RSS has no entries."""
        mock_get_entries.return_value = []

        events = feed.get_events()

        assert events == []

    @patch('events_feed.reader.get_entries')
    def test_get_events_transforms_multiple_entries(self, mock_get_entries, mock_rss_entries):
        """Test that multiple RSS entries are all transformed to EventEntry objects."""
        mock_get_entries.return_value = mock_rss_entries

        events = feed.get_events()

        assert len(events) == 2
        assert all(isinstance(event, EventEntry) for event in events)

    @patch('events_feed.reader.get_entries')
    def test_get_events_passes_correct_arguments_to_event_entry(self, mock_get_entries, mock_rss_entry):
        """Test that RSS entry attributes are passed to EventEntry constructor correctly."""
        mock_get_entries.return_value = [mock_rss_entry]

        with patch('events_feed.EventEntry') as mock_event_entry:
            feed.get_events()

            # Verify EventEntry was called with correct arguments
            mock_event_entry.assert_called_once_with(
                mock_rss_entry.id,
                mock_rss_entry.title,
                mock_rss_entry.link,
                mock_rss_entry.summary
            )

    @patch('events_feed.reader.get_entries')
    def test_get_events_calls_reader_get_entries(self, mock_get_entries):
        """Test that get_events calls reader.get_entries()."""
        mock_get_entries.return_value = []

        feed.get_events()

        mock_get_entries.assert_called_once()

    @patch('events_feed.reader.get_entries')
    def test_get_events_handles_none_values(self, mock_get_entries):
        """Test that get_events handles RSS entries with None values."""
        entry = MockRSSEntry(
            id=None,
            title=None,
            link=None,
            summary=None
        )

        mock_get_entries.return_value = [entry]

        # EventEntry should handle None values gracefully
        events = feed.get_events()

        assert len(events) == 1
        assert isinstance(events[0], EventEntry)