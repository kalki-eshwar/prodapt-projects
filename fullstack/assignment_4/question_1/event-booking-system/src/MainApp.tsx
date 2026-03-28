import { useState } from 'react';
import { EventList } from './components/EventList';
import { BookingForm } from './components/BookingForm';
import { BookingSummary } from './components/BookingSummary';
import type { Event, Booking } from './types/types';

const INITIAL_EVENTS: Event[] = [
  { id: 1, name: 'React Workshop', seats: 20 },
  { id: 2, name: 'AI Bootcamp', seats: 15 },
  { id: 3, name: 'Cloud Training', seats: 10 },
  { id: 4, name: 'Sold Out Event', seats: 0 }
];

export function MainApp() {
  const [events, setEvents] = useState<Event[]>(INITIAL_EVENTS);
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
  const [lastBooking, setLastBooking] = useState<Booking | null>(null);

  const handleBookingSubmit = (userName: string, eventId: number, seatsBooked: number) => {
    setEvents(prevEvents =>
      prevEvents.map(event =>
        event.id === eventId
          ? { ...event, seats: event.seats - seatsBooked }
          : event
      )
    );

    setLastBooking({ userName, eventId, seatsBooked });
    setSelectedEventId(null);
  };

  const bookedEvent = events.find(e => e.id === lastBooking?.eventId) || null;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Event Registration & Seat Booking</h1>
      
      <EventList
        events={events}
        selectedEventId={selectedEventId}
        onSelectEvent={setSelectedEventId}
      />

      <hr style={{ margin: '20px 0' }} />

      <BookingForm
        events={events}
        selectedEventId={selectedEventId}
        onSelectEvent={setSelectedEventId}
        onSubmit={handleBookingSubmit}
      />

      {lastBooking && (
        <BookingSummary
          booking={lastBooking}
          event={bookedEvent}
        />
      )}
    </div>
  );
}