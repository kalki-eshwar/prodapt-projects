import type { Event } from '../types/types';

interface EventCardProps {
  event: Event;
  selectedEventId: number | null;
  onSelectEvent: (id: number) => void;
}

export const EventCard = ({ event, selectedEventId, onSelectEvent }: EventCardProps) => {
  const isSelected = selectedEventId === event.id;
  const isSoldOut = event.seats === 0;

  return (
    <div
      style={{
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '16px',
        margin: '8px',
        backgroundColor: isSelected ? '#e0f7fa' : '#fff',
        cursor: "pointer",
        opacity: isSoldOut ? 0.6 : 1
      }}
      onClick={() => onSelectEvent(event.id)}
      data-testid={`event-card-${event.id}`}
    >
      <h3>{event.name}</h3>
      <p>Seats Available: {event.seats}</p>
      {isSoldOut && <p style={{ color: 'red' }}>Sold Out</p>}
    </div>
  );
};