CREATE TABLE IF NOT EXISTS public.likes (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL REFERENCES public.users(uuid) ON DELETE CASCADE,
  activity_uuid UUID NOT NULL REFERENCES public.activities(uuid) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_uuid, activity_uuid)
);

CREATE INDEX IF NOT EXISTS idx_likes_user_uuid ON public.likes(user_uuid);
CREATE INDEX IF NOT EXISTS idx_likes_activity_uuid ON public.likes(activity_uuid);