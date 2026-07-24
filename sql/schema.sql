-- MARKET MEMORY V2
-- Run this entire file in a NEW Supabase project's SQL Editor.
-- Raw tables remain private. Streamlit reads only selected clean/model tables.

create extension if not exists pgcrypto;
create extension if not exists vector with schema extensions;

create table if not exists public.ingestion_runs (
    id uuid primary key default gen_random_uuid(),
    source_type text not null check (source_type in ('news', 'market')),
    source_name text not null,
    status text not null default 'running'
        check (status in ('running', 'completed', 'partial', 'failed')),
    input_path text,
    started_at timestamptz not null default now(),
    finished_at timestamptz,
    records_seen integer not null default 0,
    records_inserted integer not null default 0,
    records_failed integer not null default 0,
    error_message text,
    metadata jsonb not null default '{}'::jsonb
);

create table if not exists public.raw_news_items (
    id uuid primary key default gen_random_uuid(),
    ingestion_run_id uuid references public.ingestion_runs(id) on delete set null,
    source_name text not null,
    external_id text,
    source_url text,
    fetched_at timestamptz not null default now(),
    payload jsonb not null,
    payload_hash text not null,
    processing_status text not null default 'pending'
        check (processing_status in ('pending', 'promoted', 'duplicate', 'failed')),
    processing_error text,
    unique (source_name, payload_hash)
);

create table if not exists public.raw_market_bars (
    id uuid primary key,
    ingestion_run_id uuid references public.ingestion_runs(id) on delete set null,
    provider text not null,
    ticker text not null,
    interval text not null default '1d',
    observed_at timestamptz not null,
    fetched_at timestamptz not null default now(),
    payload jsonb not null,
    payload_hash text not null,
    processing_status text not null default 'pending'
        check (processing_status in ('pending', 'promoted', 'duplicate', 'failed')),
    processing_error text,
    unique (provider, ticker, interval, observed_at, payload_hash)
);

create table if not exists public.assets (
    id uuid primary key default gen_random_uuid(),
    ticker text not null unique,
    asset_name text not null,
    asset_class text not null,
    benchmark_asset_id uuid references public.assets(id),
    currency text not null default 'USD',
    exchange_name text,
    exchange_timezone text,
    calendar_name text,
    is_active boolean not null default true,
    created_at timestamptz not null default now()
);

create table if not exists public.event_clusters (
    id uuid primary key default gen_random_uuid(),
    cluster_key text unique,
    event_title text,
    event_type text,
    first_event_at timestamptz,
    last_event_at timestamptz,
    notes text,
    created_at timestamptz not null default now()
);

create table if not exists public.news_articles (
    id uuid primary key default gen_random_uuid(),
    raw_news_item_id uuid references public.raw_news_items(id) on delete set null,
    event_cluster_id uuid references public.event_clusters(id) on delete set null,
    primary_asset_id uuid references public.assets(id) on delete set null,
    source_name text not null,
    external_id text,
    title text not null,
    summary text,
    body_text text,
    language text not null default 'en',
    published_at timestamptz not null,
    modified_at timestamptz,
    author text,
    url text,
    canonical_url text not null unique,
    topic text,
    article_type text not null default 'news',
    leakage_status text not null default 'not_reviewed'
        check (leakage_status in (
            'not_reviewed', 'predictive_event', 'market_recap',
            'ambiguous', 'excluded'
        )),
    duplicate_group_key text,
    content_hash text,
    manual_notes text,
    reviewed_at timestamptz,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    unique (source_name, external_id)
);

create table if not exists public.article_assets (
    article_id uuid not null references public.news_articles(id) on delete cascade,
    asset_id uuid not null references public.assets(id) on delete cascade,
    relevance_source text not null default 'model'
        check (relevance_source in ('provider', 'rule', 'model', 'manual')),
    relevance_score numeric not null default 0
        check (relevance_score >= 0 and relevance_score <= 1),
    is_primary boolean not null default false,
    created_at timestamptz not null default now(),
    primary key (article_id, asset_id)
);

create table if not exists public.market_prices (
    id uuid primary key,
    raw_market_bar_id uuid references public.raw_market_bars(id) on delete set null,
    asset_id uuid not null references public.assets(id) on delete cascade,
    provider text not null,
    interval text not null default '1d',
    observed_at timestamptz not null,
    open numeric,
    high numeric,
    low numeric,
    close numeric not null,
    adjusted_close numeric not null,
    volume numeric,
    is_complete boolean not null default true,
    created_at timestamptz not null default now(),
    unique (asset_id, provider, interval, observed_at)
);

create table if not exists public.article_asset_labels (
    id uuid primary key default gen_random_uuid(),
    article_id uuid not null references public.news_articles(id) on delete cascade,
    asset_id uuid not null references public.assets(id) on delete cascade,
    benchmark_asset_id uuid references public.assets(id) on delete set null,
    alignment_method text not null,
    reference_time timestamptz not null,
    reference_price numeric not null,

    return_1d numeric,
    return_3d numeric,
    return_5d numeric,
    return_10d numeric,
    return_20d numeric,

    benchmark_return_1d numeric,
    benchmark_return_3d numeric,
    benchmark_return_5d numeric,
    benchmark_return_10d numeric,
    benchmark_return_20d numeric,

    abnormal_return_1d numeric,
    abnormal_return_3d numeric,
    abnormal_return_5d numeric,
    abnormal_return_10d numeric,
    abnormal_return_20d numeric,

    direction_1d text,
    direction_3d text,
    direction_5d text,
    direction_10d text,
    direction_20d text,

    peak_positive_return numeric,
    peak_positive_day integer,
    peak_negative_return numeric,
    peak_negative_day integer,
    reversal_flag boolean,
    impact_shape text,
    label_status text not null default 'pending'
        check (label_status in ('pending', 'complete', 'insufficient_prices', 'excluded')),
    created_at timestamptz not null default now(),
    unique (article_id, asset_id)
);

create table if not exists public.model_versions (
    id uuid primary key default gen_random_uuid(),
    model_name text not null,
    model_type text not null
        check (model_type in ('embedding', 'classifier', 'regressor', 'hybrid')),
    version text not null,
    embedding_dimension integer,
    parameters jsonb not null default '{}'::jsonb,
    training_start date,
    training_end date,
    metrics jsonb not null default '{}'::jsonb,
    artifact_uri text,
    is_active boolean not null default false,
    created_at timestamptz not null default now(),
    unique (model_name, version)
);

create table if not exists public.news_embeddings (
    id bigint generated by default as identity primary key,
    article_id uuid not null references public.news_articles(id) on delete cascade,
    model_version_id uuid not null references public.model_versions(id) on delete cascade,
    text_variant text not null default 'title_summary',
    embedding extensions.vector(384) not null,
    created_at timestamptz not null default now(),
    unique (article_id, model_version_id, text_variant)
);

create table if not exists public.prediction_runs (
    id uuid primary key default gen_random_uuid(),
    query_article_id uuid not null references public.news_articles(id) on delete cascade,
    asset_id uuid not null references public.assets(id) on delete cascade,
    model_version_id uuid references public.model_versions(id) on delete set null,
    generated_at timestamptz not null default now(),
    k_neighbors integer not null,
    similarity_threshold numeric not null,
    evidence_count integer not null default 0,
    mean_text_similarity numeric,
    mean_regime_similarity numeric,
    reliability text,
    abstained boolean not null default false,
    abstention_reason text,
    status text not null default 'completed'
        check (status in ('running', 'completed', 'failed')),
    metadata jsonb not null default '{}'::jsonb
);

create table if not exists public.prediction_horizons (
    id bigint generated by default as identity primary key,
    prediction_run_id uuid not null references public.prediction_runs(id) on delete cascade,
    horizon_days integer not null check (horizon_days in (1, 3, 5, 10, 20)),
    direction text not null check (direction in ('UP', 'NEUTRAL', 'DOWN')),
    probability_up numeric not null check (probability_up between 0 and 1),
    probability_neutral numeric not null check (probability_neutral between 0 and 1),
    probability_down numeric not null check (probability_down between 0 and 1),
    expected_abnormal_return numeric not null,
    lower_bound numeric not null,
    upper_bound numeric not null,
    created_at timestamptz not null default now(),
    unique (prediction_run_id, horizon_days)
);

create table if not exists public.historical_analogues (
    id bigint generated by default as identity primary key,
    prediction_run_id uuid not null references public.prediction_runs(id) on delete cascade,
    historical_article_id uuid references public.news_articles(id) on delete set null,
    rank integer not null,
    historical_title text not null,
    historical_published_at timestamptz not null,
    text_similarity numeric not null,
    regime_similarity numeric not null,
    combined_similarity numeric not null,
    neighbour_weight numeric,
    abnormal_return_1d numeric,
    abnormal_return_5d numeric,
    abnormal_return_20d numeric,
    impact_shape text,
    source_url text,
    created_at timestamptz not null default now(),
    unique (prediction_run_id, rank)
);

create table if not exists public.model_evaluations (
    id uuid primary key default gen_random_uuid(),
    model_version_id uuid not null references public.model_versions(id) on delete cascade,
    split_name text not null,
    horizon_days integer not null,
    balanced_accuracy numeric,
    macro_f1 numeric,
    brier_score numeric,
    return_mae numeric,
    coverage numeric,
    confusion_matrix jsonb,
    evaluated_at timestamptz not null default now(),
    unique (model_version_id, split_name, horizon_days)
);

create index if not exists raw_news_pending_idx
    on public.raw_news_items (processing_status, fetched_at);
create index if not exists raw_market_pending_idx
    on public.raw_market_bars (processing_status, observed_at);
create index if not exists news_articles_published_idx
    on public.news_articles (published_at desc);
create index if not exists article_assets_asset_idx
    on public.article_assets (asset_id, relevance_score desc);
create index if not exists market_prices_lookup_idx
    on public.market_prices (asset_id, interval, observed_at desc);
create index if not exists labels_lookup_idx
    on public.article_asset_labels (asset_id, article_id);
create index if not exists prediction_runs_lookup_idx
    on public.prediction_runs (query_article_id, asset_id, generated_at desc);
create index if not exists analogues_lookup_idx
    on public.historical_analogues (prediction_run_id, rank);

-- RLS: raw data, labels, embeddings and evaluations stay private.
alter table public.ingestion_runs enable row level security;
alter table public.raw_news_items enable row level security;
alter table public.raw_market_bars enable row level security;
alter table public.assets enable row level security;
alter table public.event_clusters enable row level security;
alter table public.news_articles enable row level security;
alter table public.article_assets enable row level security;
alter table public.market_prices enable row level security;
alter table public.article_asset_labels enable row level security;
alter table public.model_versions enable row level security;
alter table public.news_embeddings enable row level security;
alter table public.prediction_runs enable row level security;
alter table public.prediction_horizons enable row level security;
alter table public.historical_analogues enable row level security;
alter table public.model_evaluations enable row level security;

-- Streamlit publishable-key read policies.
create policy "app read assets"
on public.assets for select to anon, authenticated
using (is_active = true);

create policy "app read active news"
on public.news_articles for select to anon, authenticated
using (is_active = true);

create policy "app read article assets"
on public.article_assets for select to anon, authenticated
using (true);

create policy "app read market prices"
on public.market_prices for select to anon, authenticated
using (true);

create policy "app read active model versions"
on public.model_versions for select to anon, authenticated
using (is_active = true);

create policy "app read completed predictions"
on public.prediction_runs for select to anon, authenticated
using (status = 'completed');

create policy "app read prediction horizons"
on public.prediction_horizons for select to anon, authenticated
using (true);

create policy "app read historical analogues"
on public.historical_analogues for select to anon, authenticated
using (true);
