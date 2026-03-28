import { useState } from 'react';
import type { Event } from '../types/types';

interface BookingFormProps {
  events: Event[];
  selectedEventId: number | null;
  onSelectEvent: (id: number) => void;
  onSubmit: (userName: string, eventId: number, seatsToBook: number) => void;
}

export const BookingForm = ({ events, selectedEventId, onSelectEvent, onSubmit }: BookingFormProps) => {
  const [userName, setUserName] = useState('');
  const [seats, setSeats] = useState<number | ''>('');
  const [error, setError] = useState('');

  const selectedEvent = events.find(e => e.id === selectedEventId);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!userName || !selectedEventId || !seats) {
      setError('All fields are required');
      return;
    }

    if (seats <= 0) {
      setError('Please book at least 1 seat');
      return;
    }

    if (selectedEvent && seats > selectedEvent.seats) {
      setError('Not enough seats available');
      return;
    }

    setError('');
    onSubmit(userName, selectedEventId, Number(seats));
    setUserName('');
    setSeats('');
  };

  return (
    <div>
      <h2>Book Seats</h2>
      {error && <div style={{ color: 'red' }} data-testid="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '8px' }}>
          <label>Name: </label>
          <input
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="Your name"
            data-testid="input-name"
          />
        </div>
        <div style={{ marginBottom: '8px' }}>
          <label>Event: </label>
          <select
            value={selectedEventId || ''}
            onChange={(e) => onSelectEvent(Number(e.target.value))}
            data-testid="select-event"
          >
            <option value="" disabled>Select an event</option>
            {events.map(event => (
              <option key={event.id} value={event.id}>{event.name}</option>
            ))}
          </select>
        </div>
        <div style={{ marginBottom: '8px' }}>
          <label>Seats: </label>
          <input
            type="number"
            value={seats}
            onChange={(e) => setSeats(e.target.value ? Number(e.target.value) : '')}
            min="1"
            data-testid="input-seats"
          />
        </div>
        <button
          type="submit"
          disabled={selectedEvent?.seats === 0}
          data-testid="btn-book"
        >
          Book Now
        </button>
      </form>
    </div>
  );
};