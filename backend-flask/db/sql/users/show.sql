SELECT
      users.uuid,
      users.handle,
      users.full_name as display_name,
      users.bio,
      (
       SELECT 
        count(true) 
       FROM public.activities 
       WHERE 
        activities.user_uuid = users.uuid
       ) as cruds_count
FROM public.users
WHERE 
  users.handle = %(handle)s