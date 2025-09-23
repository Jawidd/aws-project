-- Insert users with diverse handles
INSERT INTO public.users (display_name, handle, cognito_user_id) VALUES
('Andrew Brown', 'andrewbrown', 'MOCK'),
('Worf', 'worf', 'MOCK'),
('Data', 'data', 'MOCK'),
('Picard', 'picard', 'MOCK');

-- Insert activities
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'andrewbrown'), 'Cloud computing is absolutely amazing! 🚀☁️✨', 247, 2, 56, current_timestamp + interval '5 days', current_timestamp - interval '2 days'),
((SELECT uuid FROM public.users WHERE handle = 'picard'), 'Make it so! 🖖✨🌟', 156, 1, 23, current_timestamp + interval '7 days', current_timestamp - interval '1 day'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Fascinating calculations! 🤖📊💫', 92, 0, 12, current_timestamp + interval '6 days', current_timestamp - interval '3 hours'),
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'Today is a good day! ⚔️', 45, 0, 5, current_timestamp + interval '9 days', current_timestamp - interval '7 days');

-- Insert replies
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
-- 2 Replies to Andrew's post
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'Cloud has no honor! ⚔️', 45, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud computing is absolutely amazing!%'), current_timestamp - interval '1 day'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Intriguing perspective 🤔', 67, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud computing is absolutely amazing!%'), current_timestamp - interval '12 hours'),

-- 1 Reply to Picard's post
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Command acknowledged 🤖', 78, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Make it so!%'), current_timestamp - interval '18 hours');
