SELECT
  users.uuid,
  users.handle,
  users.display_name,
  users.bio,
  users.created_at
FROM public.users
WHERE 
  users.handle = %(handle)s