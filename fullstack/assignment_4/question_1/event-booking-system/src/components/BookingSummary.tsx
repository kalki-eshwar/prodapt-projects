import type { Event, Booking } from '../types/types';

interface BookingSummaryProps {
  booking: Booking | null;
  event: Event | null;
}

export const BookingSummary = ({ booking, event }: BookingSummaryProps) => {
  if (!booking || !event) return null;

  return (
    <div style={{ border: '1px solid green', padding: '16px', marginTop: '16px', borderRadius: '8px', backgroundColor: '#e8f5e9' }} data-testid="booking-summary">
      <h3>Booking Confirmed 🎉</h3>
      <p>Name: {booking.userName}</p>
      <p>Event: {event.name}</p>
      <p>Seats Booked: {booking.seatsBooked}</p>
      <p>Remaining Seats: {event.seats}</p>
    </div>
  );
};