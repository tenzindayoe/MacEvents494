import pytest
from unittest.mock import patch
from app import app
from event_entry import EventEntry

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_event():
    event = object.__new__(EventEntry)
    event.id = "test-id-123"
    event.title = "Test Event"
    event.location = "Library"
    event.date = "January 15, 2025"
    event.time = "2:00 PM - 4:00 PM"
    event.start_time = "14:00"
    event.end_time = "16:00"
    event.link = "https://example.com/event"
    event.coord = [44.93855, -93.16822]
    event.desc = "This is a test event description"

    return event

@pytest.fixture
def mock_events(mock_event):
    event2 = object.__new__(EventEntry)
    event2.id = "test-id-456"
    event2.title = "Another Test Event"
    event2.location = "Humanities"
    event2.date = "January 20, 2025"
    event2.time = "10:00 AM - 12:00 PM"
    event2.start_time = "10:00"
    event2.end_time = "12:00"
    event2.link = "https://example.com/event2"
    event2.coord = [44.93712, -93.16928]
    event2.desc = "Another test event description"

    return [mock_event, event2]

# ============================================================================
# FLASK ROUTE TESTS
# ============================================================================

class TestIndexRoute:
   """Test cases for the index route (/)."""
   
   @patch('app.feed.get_events')
   def test_index_returns_200(self, mock_get_events, client, mock_events):
       """Test that index route returns 200 status code."""
       mock_get_events.return_value = mock_events
       response = client.get('/')
       assert response.status_code == 200

   @patch('app.feed.get_events')
   def test_index_renders_template(self, mock_get_events, client, mock_events):
       """Test that index route renders HTML content."""
       mock_get_events.return_value = mock_events
       response = client.get('/')
       assert response.content_type.startswith('text/html')

   @patch('app.feed.get_events')
   def test_index_calls_get_events(self, mock_get_events, client, mock_events):
       """Test that index route calls get_events function."""
       mock_get_events.return_value = mock_events
       client.get('/')
       mock_get_events.assert_called_once()

   @patch('app.feed.get_events')
   def test_index_with_empty_events(self, mock_get_events, client):
       """Test index route with no events."""
       mock_get_events.return_value = []
       response = client.get('/')
       assert response.status_code == 200

class TestEventsRoute:
    """Test cases for the /events route."""

    @patch('app.feed.get_events')
    def test_events_returns_200(self, mock_get_events, client, mock_events):
        """Test that events route returns 200 status code."""
        mock_get_events.return_value = mock_events
        response = client.get('/events')
        assert response.status_code == 200

    @patch('app.feed.get_events')
    def test_events_returns_json(self, mock_get_events, client, mock_events):
        """Test that events route returns JSON data."""
        mock_get_events.return_value = mock_events
        response = client.get('/events')
        data = response.get_json()
        assert isinstance(data, list)

    @patch('app.feed.get_events')
    def test_events_json_structure(self, mock_get_events, client, mock_events):
        """Test that events JSON has correct structure."""
        mock_get_events.return_value = mock_events
        response = client.get('/events')
        data = response.get_json()

        required_keys = ['id', 'title', 'location', 'date', 'time',
                       'starttime', 'endtime', 'link', 'coord', 'description']

        for event in data:
            for key in required_keys:
                assert key in event

    @patch('app.feed.get_events')
    def test_events_json_values(self, mock_get_events, client, mock_event):
        """Test that events JSON contains correct values."""
        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()

        assert len(data) == 1
        event = data[0]
        assert event['id'] == "test-id-123"
        assert event['title'] == "Test Event"
        assert event['location'] == "Library"
        assert event['date'] == "January 15, 2025"
        assert event['time'] == "2:00 PM - 4:00 PM"
        assert event['starttime'] == "14:00"
        assert event['endtime'] == "16:00"
        assert event['link'] == "https://example.com/event"
        assert event['coord'] == [44.93855, -93.16822]
        assert event['description'] == "This is a test event description"

    @patch('app.feed.get_events')
    def test_events_reverse_order(self, mock_get_events, client, mock_events):
        """Test that events are returned in reverse order."""
        mock_get_events.return_value = mock_events
        response = client.get('/events')
        data = response.get_json()

        # The first event in mock_events should be last in response
        assert data[0]['id'] == "test-id-456"
        assert data[1]['id'] == "test-id-123"

    @patch('app.feed.get_events')
    def test_events_with_empty_list(self, mock_get_events, client):
        """Test events route with no events."""
        mock_get_events.return_value = []
        response = client.get('/events')
        data = response.get_json()
        assert data == []

    @patch('app.feed.get_events')
    def test_events_calls_get_events(self, mock_get_events, client, mock_events):
        """Test that events route calls get_events function."""
        mock_get_events.return_value = mock_events
        client.get('/events')
        mock_get_events.assert_called_once()

    @patch('app.feed.get_events')
    def test_events_handles_none_values(self, mock_get_events, client, mock_event):
        """Test events route handles None values gracefully."""
        mock_event.time = None
        mock_event.start_time = None
        mock_event.end_time = None
        mock_event.coord = None

        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()

        assert response.status_code == 200
        assert data[0]['time'] is None
        assert data[0]['starttime'] is None
        assert data[0]['endtime'] is None
        assert data[0]['coord'] is None

    # ========================================================================
    # NEW TESTS: Field Mapping & Format Validation
    # ========================================================================

    @patch('app.feed.get_events')
    def test_events_json_key_mapping(self, mock_get_events, client, mock_event):
        """Test that EventEntry attributes map to correct JSON keys."""
        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()[0]

        # Verify the mapping from EventEntry to JSON
        assert data['id'] == mock_event.id
        assert data['title'] == mock_event.title
        assert data['location'] == mock_event.location
        assert data['date'] == mock_event.date
        assert data['time'] == mock_event.time
        assert data['starttime'] == mock_event.start_time  # Note: different key name!
        assert data['endtime'] == mock_event.end_time  # Note: different key name!
        assert data['link'] == mock_event.link
        assert data['coord'] == mock_event.coord
        assert data['description'] == mock_event.desc  # Note: different key name!

    @patch('app.feed.get_events')
    def test_events_json_content_type(self, mock_get_events, client):
        """Test that response has correct Content-Type header."""
        mock_get_events.return_value = []
        response = client.get('/events')

        assert 'application/json' in response.content_type

    @patch('app.feed.get_events')
    def test_events_coordinates_are_list_of_two_numbers(self, mock_get_events, client, mock_event):
        """Test that coordinates are always [lat, lon] format."""
        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()

        coord = data[0]['coord']
        assert isinstance(coord, list)
        assert len(coord) == 2
        assert isinstance(coord[0], (int, float))
        assert isinstance(coord[1], (int, float))

    @patch('app.feed.get_events')
    def test_events_times_are_24hr_format(self, mock_get_events, client, mock_event):
        """Test that start/end times are in HH:MM 24-hour format."""
        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()

        import re
        time_pattern = re.compile(r'^\d{2}:\d{2}$')

        if data[0]['starttime']:
            assert time_pattern.match(data[0]['starttime'])
        if data[0]['endtime']:
            assert time_pattern.match(data[0]['endtime'])

    # ========================================================================
    # Edge Cases for App
    # ========================================================================

    @patch('app.feed.get_events')
    def test_events_with_all_none_values(self, mock_get_events, client):
        """Test that iOS app can handle events where everything is None."""
        event = object.__new__(EventEntry)
        event.id = None
        event.title = None
        event.location = None
        event.date = None
        event.time = None
        event.start_time = None
        event.end_time = None
        event.link = None
        event.coord = None
        event.desc = None

        mock_get_events.return_value = [event]
        response = client.get('/events')
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == 1

    @patch('app.feed.get_events')
    def test_events_with_missing_coordinates(self, mock_get_events, client, mock_event):
        """Test events without coordinates (off-campus events)."""
        # Modify the fixture for this specific test
        mock_event.location = "Downtown Minneapolis"
        mock_event.coord = None  # No coordinates for off-campus

        mock_get_events.return_value = [mock_event]
        response = client.get('/events')
        data = response.get_json()

        assert data[0]['coord'] is None
        assert response.status_code == 200

# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test cases for error handling."""

    def test_404_on_invalid_route(self, client):
        """Test that invalid routes return 404."""
        response = client.get('/invalid-route')
        assert response.status_code == 404

    @patch('app.feed.get_events')
    def test_events_route_handles_exception(self, mock_get_events, client):
        """Test that events route handles exceptions gracefully."""
        mock_get_events.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            client.get('/events')

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for the Flask application."""

    @patch('app.feed.get_events')
    def test_events_data_consistency(self, mock_get_events, client, mock_events):
        """Test that event data is consistent across multiple calls."""
        mock_get_events.return_value = mock_events

        response1 = client.get('/events')
        data1 = response1.get_json()

        response2 = client.get('/events')
        data2 = response2.get_json()

        assert data1 == data2

    @patch('app.feed.get_events')
    def test_events_ordering_is_consistent(self, mock_get_events, client, mock_events):
        """Test that events are always returned in the same order."""
        # Add a third event to the existing mock_events
        event3 = object.__new__(EventEntry)
        event3.id = "test-id-789"
        event3.title = "Third Event"
        event3.location = "Library"
        event3.date = "January 25, 2025"
        event3.time = "1:00 PM - 3:00 PM"
        event3.start_time = "13:00"
        event3.end_time = "15:00"
        event3.link = "https://example.com/event3"
        event3.coord = [44.93855, -93.16822]
        event3.desc = "Third event description"

        events = mock_events + [event3]
        mock_get_events.return_value = events

        # Call multiple times
        response1 = client.get('/events')
        response2 = client.get('/events')
        response3 = client.get('/events')

        data1 = response1.get_json()
        data2 = response2.get_json()
        data3 = response3.get_json()

        # Should be identical every time
        assert data1 == data2 == data3

        # Should be reversed from input
        assert data1[0]['id'] == "test-id-789"
        assert data1[1]['id'] == "test-id-456"
        assert data1[2]['id'] == "test-id-123"