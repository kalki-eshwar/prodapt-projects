export interface Event {
  id: number;
  name: string;
  seats: number;
}

export interface Booking {
  userName: string;
  eventId: number;
  seatsBooked: number;
}