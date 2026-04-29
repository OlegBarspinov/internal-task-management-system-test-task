import { redirect } from 'next/navigation';

export default function Home() {
  redirect('/bookings/1'); // Redirect to a default booking page
}
