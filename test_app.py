import pytest
from unittest.mock import patch, MagicMock
from app import app
from event_entry import EventEntry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_event():
    mock_entry = MagicMock()
    mock_entry.id = "test-id-123"
    mock_entry.title = "Test Event"
    mock_entry.link = "https://example.com/event"
    mock_entry.summary = "<strong>January 15, 2025 | 2:00 PM - 4:00 PM | Library</strong>"

    event = EventEntry(mock_entry)
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
    mock_entry2 = MagicMock()
    mock_entry2.id = "test-id-456"
    mock_entry2.title = "Another Test Event"
    mock_entry2.link = "https://example.com/event2"
    mock_entry2.summary = "<strong>January 20, 2025 | 10:00 AM - 12:00 PM | Humanities</strong>"

    event2 = EventEntry(mock_entry2)
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

class TestCoordRoute:
    """Test cases for the /coord route."""

    @patch('app.feed.get_events')
    def test_coord_returns_200(self, mock_get_events, client, mock_events):
        """Test that coord route returns 200 status code."""
        mock_get_events.return_value = mock_events
        response = client.get('/coord')
        assert response.status_code == 200

    @patch('app.feed.get_events')
    def test_coord_renders_template(self, mock_get_events, client, mock_events):
        """Test that coord route renders HTML content."""
        mock_get_events.return_value = mock_events
        response = client.get('/coord')
        assert response.content_type.startswith('text/html')

    @patch('app.feed.get_events')
    def test_coord_calls_get_events(self, mock_get_events, client, mock_events):
        """Test that coord route calls get_events function."""
        mock_get_events.return_value = mock_events
        client.get('/coord')
        mock_get_events.assert_called_once()

    @patch('app.feed.get_events')
    def test_coord_with_empty_events(self, mock_get_events, client):
        """Test coord route with no events."""
        mock_get_events.return_value = []
        response = client.get('/coord')
        assert response.status_code == 200


class TestTimesRoute:
    """Test cases for the /times route."""

    @patch('app.feed.get_events')
    def test_times_returns_200(self, mock_get_events, client, mock_events):
        """Test that times route returns 200 status code."""
        mock_get_events.return_value = mock_events
        response = client.get('/times')
        assert response.status_code == 200

    @patch('app.feed.get_events')
    def test_times_renders_template(self, mock_get_events, client, mock_events):
        """Test that times route renders HTML content."""
        mock_get_events.return_value = mock_events
        response = client.get('/times')
        assert response.content_type.startswith('text/html')

    @patch('app.feed.get_events')
    def test_times_calls_get_events(self, mock_get_events, client, mock_events):
        """Test that times route calls get_events function."""
        mock_get_events.return_value = mock_events
        client.get('/times')
        mock_get_events.assert_called_once()

    @patch('app.feed.get_events')
    def test_times_with_empty_events(self, mock_get_events, client):
        """Test times route with no events."""
        mock_get_events.return_value = []
        response = client.get('/times')
        assert response.status_code == 200


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


class TestHTTPMethods:
    """Test cases for HTTP methods."""

    @patch('app.feed.get_events')
    def test_index_post_not_allowed(self, mock_get_events, client, mock_events):
        """Test that POST to index is not allowed."""
        mock_get_events.return_value = mock_events
        response = client.post('/')
        assert response.status_code == 405

    @patch('app.feed.get_events')
    def test_events_post_not_allowed(self, mock_get_events, client, mock_events):
        """Test that POST to events is not allowed."""
        mock_get_events.return_value = mock_events
        response = client.post('/events')
        assert response.status_code == 405

    @patch('app.feed.get_events')
    def test_events_head_request(self, mock_get_events, client, mock_events):
        """Test HEAD request to events route."""
        mock_get_events.return_value = mock_events
        response = client.head('/events')
        assert response.status_code == 200


class TestIntegration:
    """Integration tests for the Flask application."""

    @patch('app.feed.get_events')
    def test_multiple_routes_sequential(self, mock_get_events, client, mock_events):
        """Test accessing multiple routes sequentially."""
        mock_get_events.return_value = mock_events

        response1 = client.get('/')
        assert response1.status_code == 200

        response2 = client.get('/events')
        assert response2.status_code == 200

        response3 = client.get('/coord')
        assert response3.status_code == 200

        response4 = client.get('/times')
        assert response4.status_code == 200

        # Verify get_events was called for each route
        assert mock_get_events.call_count == 4

    @patch('app.feed.get_events')
    def test_events_data_consistency(self, mock_get_events, client, mock_events):
        """Test that event data is consistent across multiple calls."""
        mock_get_events.return_value = mock_events

        response1 = client.get('/events')
        data1 = response1.get_json()

        response2 = client.get('/events')
        data2 = response2.get_json()

        assert data1 == data2