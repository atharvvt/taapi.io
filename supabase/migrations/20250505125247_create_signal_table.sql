-- Create the signals table if it doesn't exist
create table if not exists public.signals (
  id uuid primary key default gen_random_uuid(),
  symbol text not null,
  exchange text not null,
  interval text not null,
  prev_rsi double precision,
  last_signal text,
  updated_at timestamptz default timezone('utc', now())
);
