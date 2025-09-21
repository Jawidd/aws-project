-- Insert users with diverse handles
INSERT INTO public.users (display_name, handle, cognito_user_id) VALUES
('Andrew Brown', 'andrewbrown', 'MOCK'),
('Worf', 'worf', 'MOCK'),
('Garek', 'garek', 'MOCK'),
('Data', 'data', 'MOCK'),
('Picard', 'picard', 'MOCK'),
('Riker', 'riker', 'MOCK'),
('Troi', 'troi', 'MOCK'),
('Geordi', 'geordi', 'MOCK'),
('Beverly', 'beverly', 'MOCK'),
('Guinan', 'guinan', 'MOCK'),
('Q', 'q', 'MOCK'),
('Odo', 'odo', 'MOCK'),
('Kira', 'kira', 'MOCK'),
('Sisko', 'sisko', 'MOCK'),
('Dax', 'dax', 'MOCK');

-- Insert viral activities with stickers and high engagement (replies_count will be updated dynamically)
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, expires_at, created_at) VALUES
((SELECT uuid FROM public.users WHERE handle = 'andrewbrown'), 'Cloud is fun! 🚀☁️', 1247, 4, 156, current_timestamp + interval '5 days', current_timestamp - interval '2 days'),
((SELECT uuid FROM public.users WHERE handle = 'picard'), 'Make it so! 🖖✨ #StarfleetLife', 2156, 4, 89, current_timestamp + interval '7 days', current_timestamp - interval '1 day'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Fascinating! The probability of success is 47.3% 🤖📊', 892, 0, 23, current_timestamp + interval '6 days', current_timestamp - interval '3 hours'),
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'I am out of prune juice 🥤😤', 445, 0, 5, current_timestamp + interval '9 days', current_timestamp - interval '7 days'),
((SELECT uuid FROM public.users WHERE handle = 'garek'), 'My dear doctor, I am just simple tailor 🧵✂️', 678, 0, 12, current_timestamp + interval '12 hours', current_timestamp - interval '1 hour'),
((SELECT uuid FROM public.users WHERE handle = 'riker'), 'Number One reporting for duty! 🎺🌟', 1834, 0, 78, current_timestamp + interval '8 days', current_timestamp - interval '4 hours'),
((SELECT uuid FROM public.users WHERE handle = 'troi'), 'I sense great joy in this post 💫🔮', 923, 0, 34, current_timestamp + interval '10 days', current_timestamp - interval '6 hours'),
((SELECT uuid FROM public.users WHERE handle = 'geordi'), 'These warp core readings are off the charts! ⚡🔧', 567, 1, 45, current_timestamp + interval '5 days', current_timestamp - interval '8 hours'),
((SELECT uuid FROM public.users WHERE handle = 'beverly'), 'Medical bay is ready for action 🏥💉', 789, 0, 23, current_timestamp + interval '7 days', current_timestamp - interval '12 hours'),
((SELECT uuid FROM public.users WHERE handle = 'guinan'), 'Time has many layers, like an onion 🧅⏰', 1456, 0, 67, current_timestamp + interval '6 days', current_timestamp - interval '18 hours'),
((SELECT uuid FROM public.users WHERE handle = 'q'), 'Mon Capitaine! 🎭✨ #Omnipotent', 3456, 4, 234, current_timestamp + interval '365 days', current_timestamp - interval '30 minutes'),
((SELECT uuid FROM public.users WHERE handle = 'odo'), 'Order must be maintained 🛡️⚖️', 234, 2, 12, current_timestamp + interval '4 days', current_timestamp - interval '2 hours'),
((SELECT uuid FROM public.users WHERE handle = 'kira'), 'The Prophets guide us 🙏✨', 567, 0, 23, current_timestamp + interval '8 days', current_timestamp - interval '3 hours'),
((SELECT uuid FROM public.users WHERE handle = 'sisko'), 'I can live with it 💪🌟', 1123, 0, 45, current_timestamp + interval '9 days', current_timestamp - interval '5 hours'),
((SELECT uuid FROM public.users WHERE handle = 'dax'), 'I have lived many lifetimes 🔄💫', 834, 1, 34, current_timestamp + interval '7 days', current_timestamp - interval '4 hours');

-- Insert replies
INSERT INTO public.activities (user_uuid, message, likes_count, replies_count, reposts_count, reply_to_activity_uuid, created_at) VALUES
-- 4 Replies to Andrew cloud post
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'This post has no honor! ⚔️', 45, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud is fun!%'), current_timestamp - interval '2 days'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Intriguing perspective on cloud computing 🤔', 67, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud is fun!%'), current_timestamp - interval '1 day'),
((SELECT uuid FROM public.users WHERE handle = 'picard'), 'Engage with the cloud! 🚀', 89, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud is fun!%'), current_timestamp - interval '1 day'),
((SELECT uuid FROM public.users WHERE handle = 'geordi'), 'The technical specs are impressive! 🔧', 34, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Cloud is fun!%'), current_timestamp - interval '12 hours'),

-- 4 Replies to Picard post
((SELECT uuid FROM public.users WHERE handle = 'riker'), 'Aye aye, Captain! 🫡', 123, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Make it so!%'), current_timestamp - interval '20 hours'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Command protocols acknowledged 🤖', 78, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Make it so!%'), current_timestamp - interval '18 hours'),
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'A glorious command! ⚔️', 56, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Make it so!%'), current_timestamp - interval '16 hours'),
((SELECT uuid FROM public.users WHERE handle = 'troi'), 'I sense determination 💫', 45, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Make it so!%'), current_timestamp - interval '14 hours'),

-- 4 Replies to Q post
((SELECT uuid FROM public.users WHERE handle = 'picard'), 'Q, what do you want now? 😤', 234, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Mon Capitaine!%'), current_timestamp - interval '25 minutes'),
((SELECT uuid FROM public.users WHERE handle = 'worf'), 'Begone, foul creature! ⚔️', 156, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Mon Capitaine!%'), current_timestamp - interval '20 minutes'),
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Fascinating display of power 🤖', 89, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Mon Capitaine!%'), current_timestamp - interval '15 minutes'),
((SELECT uuid FROM public.users WHERE handle = 'guinan'), 'Some things never change 🧅', 67, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Mon Capitaine!%'), current_timestamp - interval '10 minutes'),

-- 2 Replies to Odo post
((SELECT uuid FROM public.users WHERE handle = 'sisko'), 'The Dominion would disagree 💪', 45, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Order must be maintained%'), current_timestamp - interval '1 hour'),
((SELECT uuid FROM public.users WHERE handle = 'kira'), 'Justice over order! ⚖️', 67, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'Order must be maintained%'), current_timestamp - interval '45 minutes'),

-- 1 Reply to Dax post
((SELECT uuid FROM public.users WHERE handle = 'beverly'), 'Fascinating experiences 🏥', 23, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'I have lived many lifetimes%'), current_timestamp - interval '3 hours'),

-- 1 Reply to Geordi post
((SELECT uuid FROM public.users WHERE handle = 'data'), 'Analyzing readings now 🤖', 12, 0, 0, (SELECT uuid FROM public.activities WHERE message LIKE 'These warp core readings%'), current_timestamp - interval '6 hours');
