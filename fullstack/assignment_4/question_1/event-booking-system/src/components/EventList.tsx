import type { Event } from '../types/types';
import { EventCard } from './EventCard';

interface EventListProps {
  events: Event[];
  selectedEventId: number | null;
  onSelectEvent: (id: number) => void;
}

export const EventList = ({ events, selectedEventId, onSelectEvent }: EventListProps) => {
  return (
    <div>
      <h2>Available Events</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {events.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            selectedEventId={selectedEventId}
            onSelectEvent={onSelectEvent}
          />
        ))}
      </div>
    </div>
  );
};