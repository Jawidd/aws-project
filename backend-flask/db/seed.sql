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

-- Dummy user 3 (Charlie)
INSERT INTO public.users (uuid, preferred_username, handle, email, cognito_user_id, created_at, bio, avatar_url) VALUES
('e5551aa1-1234-4eab-9c7f-9876543210ff', 'charlie', 'charliedev', 'charlie@example.com', 'charlie-cognito-003', current_timestamp, NULL, NULL);
