-- Insert user
INSERT INTO public.users (preferred_username, handle, email, cognito_user_id) VALUES
('jk', 'jawid00786', 'jawid00786@gmail.com', '7632b2e4-6091-70d2-1d03-73979cf7e32b');

-- Insert activity
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'jawid00786'), 'Hello from jawid! 👋', 5, 1, 0, current_timestamp + interval '7 days', current_timestamp - interval '1 hour');

-- Insert reply
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'jawid00786'), 'This is my first reply! 🎉', 2, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Hello from jawid!%'), current_timestamp - interval '30 minutes');
