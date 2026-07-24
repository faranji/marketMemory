insert into public.assets
(ticker, asset_name, asset_class, currency, exchange_name, exchange_timezone, calendar_name)
values
('QQQ', 'Invesco QQQ Trust', 'etf', 'USD', 'NASDAQ', 'America/New_York', 'XNYS'),
('GOOGL', 'Alphabet Class A', 'equity', 'USD', 'NASDAQ', 'America/New_York', 'XNYS'),
('TSLA', 'Tesla', 'equity', 'USD', 'NASDAQ', 'America/New_York', 'XNYS'),
('NVDA', 'Nvidia', 'equity', 'USD', 'NASDAQ', 'America/New_York', 'XNYS')
on conflict (ticker) do update set
asset_name = excluded.asset_name,
asset_class = excluded.asset_class,
currency = excluded.currency;

update public.assets child
set benchmark_asset_id = benchmark.id
from public.assets benchmark
where child.ticker in ('GOOGL', 'TSLA', 'NVDA')
  and benchmark.ticker = 'QQQ';
