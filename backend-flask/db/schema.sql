CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS public.activities CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;

CREATE TABLE IF NOT EXISTS public.users (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    display_name text,
    handle text,
    cognito_user_id text,
    created_at TIMESTAMP DEFAULT now()
    -- updated_at timestamp DEFAULT now()
    -- created_at timestamp DEFAULT current_timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS public.activities (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    message text NOT NULL,
    replies_count integer DEFAULT 0,
    reposts_count integer DEFAULT 0,
    likes_count integer DEFAULT 0,
    reply_to_activity_uuid integer, --UUID instead of integer
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    user_uuid UUID NOT NULL REFERENCES public.users(uuid)
    -- updated_at timestamp DEFAULT now()
);