select a.ticker,a.asset_name,a.provider_symbol,b.ticker as benchmark from public.assets a left join public.assets b on b.id=a.benchmark_asset_id order by a.ticker;

select 'raw_source_items' as table_name,count(*) from public.raw_source_items
union all select 'market_events',count(*) from public.market_events
union all select 'market_prices',count(*) from public.market_prices
union all select 'macro_observations',count(*) from public.macro_observations
union all select 'event_outcomes',count(*) from public.event_outcomes;

select source_name,external_id,count(*) from public.market_events group by source_name,external_id having count(*)>1;
