/* going_home blog id = 14 */
/* based on script at: http://themikecam.com/downloads/import-b2evolution-wp2.php.txt */
/* that script is referenced by: http://codex.wordpress.org/Importing_Content#b2evolution */
/* for B2E version 1.10.2 */

/* ========================================================================== */
/* Get blogs */
/* ========================================================================== */

SELECT blog_ID,blog_name,blog_description,blog_shortname,blog_links_blog_ID
FROM evo_blogs
ORDER BY blog_id;

/* ========================================================================== */
/* Get users */
/* ========================================================================== */

SELECT DISTINCT *
FROM evo_users
WHERE user_login <> 'admin';

/* lots of spam users */
SELECT DISTINCT *
FROM evo_users
WHERE user_login <> 'admin'
    AND user_email != 'naukajazdywolsztynie@prokonto.pl';

/* use user_level to cull non-admins? No - need all, even if we do not migrate all */    
SELECT DISTINCT *
FROM evo_users
WHERE user_login <> 'admin'
    AND user_level > 1;
    
/* Rob Smith (1473 - aaaqqq@mailinator.com) password: fsjtk64sj6ri6736t43j6trk7rlw5sk5ejtdyth */

/* ========================================================================== */
/* Get categories */
/* ========================================================================== */

SELECT cat_name, cat_ID, cat_parent_id, cat_blog_ID, cat_description
FROM evo_categories
WHERE cat_blog_ID IN ( 14 )
ORDER BY cat_blog_ID, cat_parent_id, cat_ID;

/* ========================================================================== */
/* Get posts. */
/* ========================================================================== */

/* -------------------------------------------------------------------------- */
/* Use post categories to just get posts for a given blog. */
/* -------------------------------------------------------------------------- */

SELECT *
FROM evo_posts ep
INNER JOIN evo_categories ec
    ON ec.cat_ID = ep.post_main_cat_ID
    WHERE ec.cat_blog_ID IN ( 14 )
ORDER BY ep.post_datecreated DESC;

/* -------------------------------------------------------------------------- */
/* Get posts with author information. */
/* -------------------------------------------------------------------------- */

SELECT *
FROM evo_posts ep, evo_users eu
WHERE ep.post_creator_user_ID = eu.user_ID
ORDER BY ep.post_datecreated DESC;

/* ========================================================================== */
/* Get comments (per post). */
/* ========================================================================== */

SELECT
    CASE
        WHEN u.user_ID IS NULL THEN c.comment_author
        ELSE
            CASE u.user_idmode
                WHEN 'nickname' THEN u.user_nickname
                WHEN 'login' THEN u.user_login
                WHEN 'namefl' THEN CONCAT(u.user_firstname, ' ', u.user_lastname)
                WHEN 'namelf' THEN CONCAT(u.user_lastname, ' ', u.user_firstname)
                WHEN 'firstname' THEN u.user_firstname
                WHEN 'lastname' THEN u.user_lastname
                ELSE u.user_nickname
            END
        END AS 'author',
	CASE WHEN u.user_ID IS NULL THEN c.comment_author_email ELSE u.user_email END AS 'author_email',
	CASE WHEN u.user_ID IS NULL THEN c.comment_author_url ELSE u.user_url END AS 'author_url',
	comment_id, comment_status, comment_author_IP, comment_content, comment_post_ID, comment_date, comment_karma, comment_type, comment_author_ID
FROM evo_comments as c
    LEFT JOIN evo_users as u
    ON u.user_ID = c.comment_author_id
WHERE comment_status = 'published'
    AND comment_post_ID = <post_id>;

/* test post ID: 1124 (one comment), 1119 (two comments) */

/* ========================================================================== */
/* Get all categories (per post). */
/* ========================================================================== */

SELECT *
FROM evo_postcats
WHERE postcat_post_ID = <post_id>;
