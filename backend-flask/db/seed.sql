-- ============================
-- Users
-- ============================

INSERT INTO public.users (uuid, preferred_username, full_name, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('b1116ed1-cab0-4dcd-8e8a-817ef3ebbc6a', 'jk', 'Jawid Khan', 'jawid00786', 'jawid00786@gmail.com', '7632b2e4-6091-70d2-1d03-73979cf7e32b', '2025-09-23 14:56:16.507539', NULL, NULL);

INSERT INTO public.users (uuid, preferred_username, full_name, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('a2227ff2-dde1-4abc-9f1e-1234567890ab', 'alice', 'Alice Wonderland', 'alice123', 'alice123@example.com', 'alice-cognito-001', '2025-09-27 10:00:00.776082', NULL, NULL);

INSERT INTO public.users (uuid, preferred_username, full_name, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('d4449ff4-ffee-4def-8b2c-123456abcdef', 'bob', 'Bob Builder', 'bob456', 'bob456@example.com', 'bob-cognito-002', '2025-09-27 10:00:00.819351', NULL, NULL);

INSERT INTO public.users (uuid, preferred_username, full_name, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('e5551aa1-1234-4eab-9c7f-9876543210ff', 'charlie', 'Charlie Developer', 'charliedev', 'charlie@example.com', 'charlie-cognito-003', '2025-09-27 10:00:00.877466', NULL, NULL);

INSERT INTO public.users (uuid, preferred_username, full_name, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('6f2328ea-7818-4373-93cd-cbf15e2dc6f9', 'jack-com', 'Jack Company', 'Jawid00776', 'Jawid00776@gmail.com', 'e6324254-b0a1-7037-8d3e-e64b2df99e43', '2025-09-27 10:04:11.705895', NULL, NULL);

-- ============================
-- Activities
-- ============================

INSERT INTO public.activities (uuid, user_uuid, message, replies_count, reposts_count, likes_count, expires_at, created_at) VALUES
('11111111-1111-1111-1111-111111111111', 'b1116ed1-cab0-4dcd-8e8a-817ef3ebbc6a', 'Just deployed my new app to AWS! 🚀', 0, 0, 5, NULL, '2025-01-15 10:00:00');

INSERT INTO public.activities (uuid, user_uuid, message, replies_count, reposts_count, likes_count, expires_at, created_at) VALUES
('22222222-2222-2222-2222-222222222222', 'a2227ff2-dde1-4abc-9f1e-1234567890ab', 'Learning React and loving it! Any tips for beginners?', 2, 1, 8, NULL, '2025-01-15 11:30:00');

INSERT INTO public.activities (uuid, user_uuid, message, replies_count, reposts_count, likes_count, expires_at, created_at) VALUES
('33333333-3333-3333-3333-333333333333', 'd4449ff4-ffee-4def-8b2c-123456abcdef', 'Building something amazing with Flask and PostgreSQL 💪', 0, 0, 3, NULL, '2025-01-15 12:15:00');

INSERT INTO public.activities (uuid, user_uuid, message, replies_count, reposts_count, likes_count, expires_at, created_at) VALUES
('44444444-4444-4444-4444-444444444444', 'e5551aa1-1234-4eab-9c7f-9876543210ff', 'Coffee + Code = Perfect Morning ☕️', 1, 0, 12, NULL, '2025-01-15 09:45:00');

INSERT INTO public.activities (uuid, user_uuid, message, replies_count, reposts_count, likes_count, expires_at, created_at) VALUES
('55555555-5555-5555-5555-555555555555', '6f2328ea-7818-4373-93cd-cbf15e2dc6f9', 'Working on the next big feature for Cruddur! Stay tuned 🎯', 0, 0, 0, NULL, '2025-01-15 14:20:00');
