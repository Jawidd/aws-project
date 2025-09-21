-- Insert sample users
INSERT INTO public.users (display_name, handle, cognito_user_id) VALUES
('Andrew Brown', 'andrewbrown', 'MOCK'),
('Andrew Bayko', 'bayko', 'MOCK'),
('Londo Mollari', 'londo', 'MOCK');

-- Insert sample activities for each user
INSERT INTO public.activities (user_uuid, message, expires_at) VALUES
-- Andrew Brown's activities
((SELECT uuid FROM public.users WHERE handle = 'andrewbrown'), 'This was imported as seed data!', current_timestamp + interval '10 day'),
((SELECT uuid FROM public.users WHERE handle = 'andrewbrown'), 'Learning AWS Cloud Development', current_timestamp + interval '7 day'),
-- Andrew Bayko's activities  
((SELECT uuid FROM public.users WHERE handle = 'bayko'), 'I am the other!', current_timestamp + interval '10 day'),
((SELECT uuid FROM public.users WHERE handle = 'bayko'), 'Building microservices with Flask', current_timestamp + interval '5 day'),
-- Londo Mollari's activities
((SELECT uuid FROM public.users WHERE handle = 'londo'), 'Welcome to Cruddur!', current_timestamp + interval '10 day'),
((SELECT uuid FROM public.users WHERE handle = 'londo'), 'The future is bright for cloud computing', current_timestamp + interval '8 day');
