-- ============================
-- Users
-- ============================

-- Original user
INSERT INTO public.users (uuid, preferred_username, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('b1116ed1-cab0-4dcd-8e8a-817ef3ebbc6a', 'jk', 'jawid00786', 'jawid00786@gmail.com', '7632b2e4-6091-70d2-1d03-73979cf7e32b', '2025-09-23 14:56:16.507539', NULL, NULL);

-- Dummy user 1 (Alice)
INSERT INTO public.users (uuid, preferred_username, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('a2227ff2-dde1-4abc-9f1e-1234567890ab', 'alice', 'alice123', 'alice123@example.com', 'alice-cognito-001', current_timestamp, NULL, NULL);

-- Dummy user 2 (Bob)
INSERT INTO public.users (uuid, preferred_username, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('d4449ff4-ffee-4def-8b2c-123456abcdef', 'bob', 'bob456', 'bob456@example.com', 'bob-cognito-002', current_timestamp, NULL, NULL);


-- ============================
-- Activities
-- ============================

-- Activity by original user
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'jawid00786'), 'Hello from Jawid! 👋', 5, 1, 0, current_timestamp + interval '7 days', current_timestamp - interval '1 hour');

-- Reply by original user
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'jawid00786'), 'This is my first reply! 🎉', 2, 0, 0, 
 (SELECT uuid FROM public.activities WHERE message LIKE 'Hello from Jawid!%'), current_timestamp - interval '30 minutes');

-- Activity by Alice
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'alice123'), 'Hello from Alice! 🌟', 3, 0, 1, current_timestamp + interval '7 days', current_timestamp - interval '2 hours');

-- Reply by Alice to Jawid's activity
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'alice123'), 'Welcome Jawid! 👋', 1, 0, 0, 
 (SELECT uuid FROM public.activities WHERE message LIKE 'Hello from Jawid!%'), current_timestamp - interval '15 minutes');

-- Activity by Bob
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'bob456'), 'Hey everyone! I am Bob. 😎', 2, 0, 0, current_timestamp + interval '7 days', current_timestamp - interval '90 minutes');

-- Reply by Bob to Alice's activity
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'bob456'), 'Hi Alice! Nice to meet you.', 0, 0, 0, 
 (SELECT uuid FROM public.activities WHERE message LIKE 'Hello from Alice!%'), current_timestamp - interval '30 minutes');
