<?php
/* Instructions: Upload to your wp-admin directory after installing WordPress and run.
*
* NOTE: You MUST install wordpress and b2evo in the same database BEFORE running the script!
*
* Original script by Fahim Farook, modified by David Appleyard and:
*
* Tom Everett - March 3, 2005
* 1. WP "post_date" is now populated from B2 "post_issue_date"
* 2. Post statuses are now migrated across
* 3. Image URLs are now updated in posts, and made relative urls rather than absolute urls
*
* Michael Rodriguez-Torrent - June 9, 2005
* 1. Now checks for WordPress install and loads DB info automatically: no more step 2!
* 2. Inserts post_name data so that permalinks on imported posts will work.
* 3. Cleaned up coding style and switched to WP functions wherever possible (i.e. for string sanitizing and db operations).
*   June 11: 
* 1. Now preserves category hierarchy from b2evo (parents and children).
*   August 16: 
* 1. Now inserts a comment_date_gmt so comments are sorted correctly (just copies local comment_date).
* 2. Reverted to ignoring the admin user by logon name instead of ID. This way users with a different login name will get the name they changed it to in b2evo.
*
* Isaac Z. Schlueter - August, 2005
* 1. Removed option to change the Image URL, since you'll most likely keep the images where they are.
* 2. Added option to import your b2evolution blogs as top-level categories.
* 3. Added option to import just the blog(s) you want.
* 		(No way to select from a menu at this point, but that would have required putting
* 		back the step 2 that MRT removed.)
* 4. Corrected a bug where a ' in the category name would fry the thing.
* 5. Got rid of all the hard-coded "evo_"s, and replaced with the $b2_prefix variable.
* 6. Added the option to import the linkblog into "Links" in Wordpress.
* 7. Since WP posts don't have a "url" attribute by default, it will now create a Meta 'URL' with the post URL,
* 		or import the post url into the contents, both, or neither.
* 8. Changed stat mapping to hide deprecated posts.
* 9. Import chops up post_contents to create an excerpt for posts with a <!--more--> or <!--nextpage-->
* 10. Imports ALL users, and comments from registered users get denormalized properly.
*
* --> Special thanks to Graham http://tin-men.net for graciously rooting out annoying bugs.
*
*	Isaac Z. Schlueter, August 2005
*	Removed importing the post_excerpt, since that isn't really necessary at all, and just makes
* certain cool tricks harder to perform later on.
*
* David J. Leach, Jr - August 7, 2006
*   ** Note that these changes have only been tested against WP 2.0.4 **
* 1. Added conditional porting of trackback comments. Mainly because my blog had a ton of spam trackbacks.
* 2. Fixed importing of users to import into the format required by WP2.0.4. This includes adding support for the metauser 
*    user data
* 3. Attempted to map the b2evolution user level to the wp_user_level and wp_capabilities settings of WP2.0.4
* 4. Fixed importing of comments to set all of the proper fields (gmt, user, etc..).
* 5. Fixed importing of posts to get correct author, GMT values, correct comment count.
* 
*
* Bodo Tasche - November 18th, 2008
* Fixed the import script for b2evolution 2.x
*
* Walter Cruz - July, 2009 (http://bitbucket.org/waltercruz/b2evolution2wordpress/)
* Update for latest version of WordPress
*/


if (!file_exists('../wp-config.php')) die("There doesn't seem to be a wp-config.php file. You must install WordPress before you import any entries.");
require('../wp-config.php');
$wpdb->show_errors =1;

$linkblogs_imported = array();
function import_linkblog( $lbid )
{
	global $linkblogs_imported;
	if( in_array($lbid, $linkblogs_imported) ) return true;
	else $linkblogs_imported[] = $lbid;
	echo '<p>Importing Links from Blog #' . $lbid . '</p>';

	global $resb2, $b2_prefix, $wpdb;
	// map the linkblog cats to wp_linkcategories
	$querycats = 'SELECT cat_ID, cat_name, cat_urlname FROM `' . $b2_prefix . 'categories` WHERE cat_blog_ID = ' . $lbid;
	$evocats = mysql_query( $querycats );
	$catcnt = 0;
	$catmap = array();
	$linkcats = array();
	$wpdb->select(DB_NAME);
	while( $evocat = mysql_fetch_object($evocats) )
	{
		$evocat->cat_name = $wpdb->escape($evocat->cat_name);
		$querycat="INSERT INTO $wpdb->terms (name, slug) VALUES ('$evocat->cat_name','$evocat->cat_urlname')";
		$wpdb->query($querycat);
		$lastid= $wpdb->insert_id;
		$catmap[$evocat->cat_ID] = $lastid;
		$catcnt++;
	}

/*
	echo '<pre>$catmap: ';
	print_r($catmap);
	echo '</pre>';
*/

	$cnt = 0;
	// now import the linkblog posts.
//	$wpdb->select($b2_db);
	$lbquery = "SELECT post_URL as 'link_url', post_datemodified as 'link_updated', post_status, post_title as 'link_name', post_main_cat_ID, post_content as 'link_description' from `" . $b2_prefix . "items__item` " .
		'INNER JOIN `' . $b2_prefix . 'categories` ON post_main_cat_ID = cat_ID ' .
		' AND cat_blog_id = ' . $lbid;
	$lbposts = mysql_query($lbquery);

	while( $lbpost = mysql_fetch_object($lbposts) )
	{
		if( preg_match('#<img src="([^"]+)"[^>]+>#', $lbpost->link_name, $matches) )
		{
			// link has an image in the title. - i do this sometimes with my linkblog posts.
//				echo 'image found!<pre>$matches: ';
//				print_r($matches);
//				echo '</pre>';

			$lbpost->link_image = $matches[1];
			$lbpost->link_name = strip_tags($lbpost->link_name);
			if(!$lbpost->link_name) $lbpost->link_name = '[Image]';
		}
		else
		{
			$lbpost->link_image = '';
		}
		$lbpost->link_category = $catmap[$lbpost->post_main_cat_ID];

		$post_content = $lbposts->post_content;
		

		$post_excerpt = $post_content;

		if( strpos(strtolower($post_excerpt), '<!--nextpage-->') !== false ) {
			$post_excerpt = preg_replace('/<!--nextpage-->/i','<!--more-->',$post_excerpt);
		}
		if( strpos(strtolower($post_excerpt), '<!--more-->') !== false ) {
			$post_excerpt = preg_replace('/<!--more-->/i','<!--more-->',$post_excerpt);
			$post_excerpt = explode('<!--more-->', $post_excerpt);
			$post_excerpt = $post_excerpt[0];
		}

		$post_content = $wpdb->escape($lbpost->link_description);
		$post_excerpt = $wpdb->escape($post_excerpt);
		$lbpost->link_description = substr($post_excerpt, 0, 255);
		$lbpost->link_notes = $post_content;
		$lbpost->link_name = $wpdb->escape($lbpost->link_name);
		$lbpost->link_visible = ($lbpost->post_status == 'published' ? 'Y' : 'N');

		$sql = "INSERT INTO $wpdb->links (link_url, link_name , link_description, link_visible, link_updated, link_notes, link_image) " .
			"VALUES ('$lbpost->link_url', '$lbpost->link_name', '$lbpost->link_description', '$lbpost->link_visible', '$lbpost->link_updated', '$lbpost->link_notes', '$lbpost->link_image')";
		$res = $wpdb->query($sql);
		$cnt ++;
		echo '<br />Imported link: ' . $lbpost->link_name;
	}
	echo '<br />Done.  Imported ' . $cnt . ' links in ' . $catcnt . ' link categories.</p>';
}



$step = $_GET['step'];
if (!$step)
	$step = 0;
header( 'Content-Type: text/html; charset=utf-8' );

echo "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"; 
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>WordPress &rsaquo; Import b2evolution Data</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<style media="screen" type="text/css">
<!--
	body {
		font-family: Georgia, "Times New Roman", Times, serif;
		margin-left: 15%;
		margin-right: 15%;
	}
	#logo {
		margin: 0;
		padding: 0;
		background-image: url(http://wordpress.org/images/logo.png);
		background-repeat: no-repeat;
		height: 60px;
		border-bottom: 4px solid #333;
	}
	#logo a {
		display: block;
		height: 60px;
	}
	#logo a span {
		display: none;
	}
	p, li {
		line-height: 140%;
	}
-->
</style>
</head>
<body>
<h1 id="logo"><a href="http://wordpress.org"><span>WordPress</span></a></h1>
<?php

switch($step) {
case 0:
?>
<p>Welcome to the WordPress b2evolution import utility. Before getting started, we need some information on your b2evolution database.</p>
<form method="post" action="import-b2evolution-wp2.php?step=1">
  <p>Below you should enter your b2evolution database connection details. If you're not sure about these, contact your host. </p>
  <table>
    <tr>
      <th scope="row">Database Name</th>
      <td><input name="b2db" type="text" size="45" value="b2evolution" /></td>
      <td>The name of the database you have b2evolution installed in.
	You should have <strong>already</strong> installed WordPress into this database. </td>
    </tr>
    <tr>
      <th scope="row">User Name</th>
      <td><input name="b2usr" type="text" size="45" value="username" /></td>
      <td>Your MySQL username</td>
    </tr>
    <tr>
      <th scope="row">Password</th>
      <td><input name="b2pwd" type="password" size="45" value="password" /></td>
      <td>...and MySQL password.</td>
    </tr>
    <tr>
      <th scope="row">Database Host</th>
      <td><input name="b2host" type="text" size="45" value="localhost" /></td>
      <td>99% chance you won't need to change this value.</td>
    </tr>
    <tr>
      <th scope="row">Table Prefix</th>
      <td><input name="b2prefix" type="text" size="45" value="evo_" /></td>
      <td>Prefix for the database tables, "evo_" is default.</td>
    </tr>
    <tr>
    	<th scope="row">Blog to Import</th>
    	<td><input name="b2blog" type="text" size="45" value="2" /></td>
    	<td>Do you want to import a single blog, or all blogs in the database?
    	  If you just want to import a single blog, then enter the blog <strong>ID (number)</strong> in this box -
    	  <strong>not</strong> the blog name!  Enter multiple blog IDs as a comma-separated list, like
    	  "<code>2, 3, 4</code>", or "all" for all blogs.</td>
    </tr>
    <tr>
    	<th scope="row">Import blog names as top-level categories?</th>
    	<td>
    		<input name="b2blogs_as_cat" id="bac_yes" value="1" type="radio" /> <label for="bac_yes">Yes, import blogs
    			as top-level categories.  (This is useful when importing multiple blogs.)</label>
    		<br />
    		<input name="b2blogs_as_cat" checked="checked" id="bac_no" value="0" type="radio" /> <label for="bac_no">No, just import the
    			categories normally.</label></td>
    	<td> </td>
    </tr>
    <tr>
    	<th scope="row">Import linkblog as "Links"?</th>
    	<td>
    		<input type="text" id="lb_id" name="b2linkblog" size="2" /> <label for="lb_yes">ID of linkblog to import as "Links" (leave empty for don't import linkblog).</label>
    		<br />
    	</td>
    	<td>If you're only importing one blog, and have a Linkblog associated with it, then checking "yes" will
    		import your linkblog posts as "Links" in WordPress.</td>
    </tr>
    <tr>
    	<th scope="row">What should I do with posts that have a URL?</th>
    	<td>
    		<input type="radio" id="url_meta" value="meta" name="b2posturl" checked="checked" />
    		<label for="url_meta">Create a WP Meta field called "URL" for posts with urls.
			(If you do this, you might want to get the <a href="http://isaacschlueter.com/plugins/i-made/meta-url/">Meta
			URL Plugin</a> if you do this.)</label>
    		<br />
    		<input type="radio" id="url_post" value="post" name="b2posturl" />
    		<label for="url_post">Put a link to the URL at the start of the post body.</label>
    		<br />
    		<input type="radio" id="url_postandmeta" value="postandmeta" name="b2posturl" />
    		<label for="url_postandmeta">Create a Meta field and also put the URL in the post body.</label>
    		<br />
    		<input type="radio" id="url_ignore" value="ignore" name="b2posturl" />
    		<label for="url_ignore">Just get rid of the post URLs.  I don't want to keep them at all.</label>
    	</td>
    	<td>
    		In b2evolution, you can post a URL with each post.  In some skins, the post title links to the url you choose.
    		WordPress doesn't support this, but it does support the use of "Meta" tags to attach additional info
    		to posts.  I can also put the URL in the post body, if you'd like.
    	</td>
    </tr>
    <tr>
    	<th scope="row">Should I import posts marked "deprecated", or just abandon them?</th>
    	<td>
    		<input type="radio" id="impdep_priv" name="b2importdep" value="private" checked="checked" />
    		<label for="impdep_priv">Import them, but make them private.</label>
    		<br />
    		<input type="radio" id="impdep_draft" name="b2importdep" value="draft" />
    		<label for="impdep_draft">Import them, but make them drafts.</label>
    		<br />
    		<input type="radio" id="impdep_pub" name="b2importdep" value="publish" />
    		<label for="impdep_pub">Import them, and re-publish them.</label>
    		<br />
    		<input type="radio" id="impdep_none" name="b2importdep" value="abandon" />
    		<label for="impdep_none">Don't import them at all.</label>
    	</td>
    	<td>
    		WordPress doesn't support the "protected" or "deprecated" statuses.  However, you CAN individually
    		protect posts with a password, which is pretty sweet.  Protected posts are going to be imported
    		as "private", since that's the closest match.  "Deprecated" is a bit weird though, so I need your help.<br /><br />
	</td>
    </tr>
    <tr>
    	<th scope="row">Should I import trackbacks or just abandon them?</th>
    	<td>
    		<input type="radio" id="tb_yes" name="b2tb" value="1" type="radio" /> <label for="tb_yes">Yes, import
    			trackback comments.</label>
    		<br />
    		<input type="radio" id="tb_no" checked="checked" name="b2tb" value="0" type="radio" /> <label for="tb_no">No, don't
    			import trackback comments.</label>
    	</td>
    	<td>
    		Because of B2Evolution's problems with spam trackback this option was added to purge all trackbacks when 
		porting to WordPress.
	</td>
    </tr>
  </table>
  <input name="submit" type="submit" value="Submit" />
</form>
<?php
break;

case 1:
	$b2_prefix = $_POST['b2prefix'];
	$b2_db = $_POST['b2db'];
	$b2_usr = $_POST['b2usr'];
	$b2_pwd = $_POST['b2pwd'];
	$b2_host = $_POST['b2host'];
	$b2_blog = $_POST['b2blog'];
	$b2_bac = $_POST['b2blogs_as_cat'];
	$b2_lb = $_POST['b2linkblog'];
	$b2_posturl = $_POST['b2posturl'];
	$b2_importdep = $_POST['b2importdep'];
	$b2_importtb = $_POST['b2tb'];

	//echo $b2_posturl;

	// connect to the b2evo database
	$resB2=mysql_connect($b2_host,$b2_usr,$b2_pwd);
	if (!$resB2)
  	exit("Connection failed! host: $b2_host, user: $b2_usr, pass: $b2_pwd");

	if (!mysql_select_db($b2_db,$resB2))
		exit("Couldn't select database: $b2_db");

	// get blogs
	$sql = 'SELECT blog_ID,blog_name,blog_description,blog_shortname,blog_links_blog_ID FROM `' . $b2_prefix . 'blogs` ';
	if( $b2_blog == 'all' )
	{
		// check for cats in blog #1.  rare, but possible;
		$blog1cats = mysql_query( 'SELECT cat_ID FROM `' . $b2_prefix . 'categories` WHERE cat_blog_ID = 1' );
		if( !mysql_fetch_object($blog1cats) )
			$sql .= ' WHERE blog_ID > 1 ';
	}
	else
	{
		$sql .= ' WHERE blog_ID IN (' . $b2_blog . ')';
	}
	$sql .= ' ORDER BY blog_ID';

	$b2blogs = mysql_query($sql,$resB2);


	if (!$b2blogs)
		exit("No blogs returned from the b2evolution database! " . $sql);
?>

<p>All right sparky, this is where the actual import takes place! Do you feel lucky today? :p</p>

<?php
	// setup arrays to store ID changes
	$arUser = array();
	$arBlogToCat = array();
	$arCat = array();
	$taxonomyCat = array();
	$arUser[1] = 1;

//	$filepath_wp = $wpdb->get_var("SELECT option_value FROM $wpdb->options WHERE option_name='fileupload_url'");
//	$filepath_b2 = "http://".$b2_url."/media/";

//	echo "b2Evolution file path: ".$filepath_b2."<br />";
//	echo "WordPress file path: ".$filepath_wp."<br /><br />";

	// get authors for blog
	echo "Importing User records ... <br />";
	$sql = "SELECT DISTINCT * FROM `" . $b2_prefix . "users` WHERE `user_login` <> 'admin'";
	$results = mysql_query($sql,$resB2) or die("Invalid query: " . mysql_error() . "<br /> SQL : " . $sql);
	if ($results) {
		$cnt = 0;
		while ($result = mysql_fetch_object($results)) {

//
// DJL: 8/7/06
//
			$wpdb->select(DB_NAME);
			$wpdb->query("INSERT INTO $wpdb->users (user_login, user_pass, user_email, user_url, user_registered, user_nicename, display_name)
				VALUES ('$result->user_login', '$result->user_pass', '$result->user_email', '$result->user_url',
					'$result->dateYMDhour', '$result->user_login', '$result->user_nickname')");

			$user_id = $wpdb->insert_id;
			$arUser[$result->ID] = $user_id;

			if ($result->user_level > 9 ) {
				$user_level = 10;
				$wp_capabilities = serialize(array("administrator" => TRUE));
			} else if ($result->user_level > 6 ) {
				$user_level = 7;
				$wp_capabilities = serialize(array("editor" => TRUE));
			} else if ($result->user_level > 1 ) {
				$user_level = 2;
				$wp_capabilities = serialize(array("author" => TRUE));
			} else if ($result->user_level > 0 ) {
				$user_level = 1;
				$wp_capabilities = serialize(array("contributor" => TRUE));
			} else {
				$user_level = 0;
				$wp_capabilities = serialize(array("subscriber" => TRUE));
			}


			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'first_name', '$result->user_firstname' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'last_name', '$result->user_lastname' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'nickname', '$result->user_nickname' )");
//			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
//				VALUES ( '$user_id', 'description', '' )");
//			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
//				VALUES ( '$user_id', 'jabber', '' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'aim', '$result->user_aim' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'yim', '$result->user_yim' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'wp_user_level', '$user_level' )");
			$wpdb->query("INSERT INTO $wpdb->usermeta ( user_id, meta_key, meta_value)
				VALUES ( '$user_id', 'wp_capabilities', '$wp_capabilities' )");


			$cnt = $cnt + 1;
		}
		echo $cnt . " User record(s) imported! <br />";
	} else {
		echo "No User records found!<br />";
	}
	//
	// get categories
	//
	echo "Importing Category records ... <br />";

	$wpdb->select($b2_db); //come back to b2evolution

	$sql = 'SELECT cat_name, cat_ID, cat_parent_id, cat_blog_ID, cat_description FROM `' . $b2_prefix . 'categories`';
	if( $b2_blog != 'all' ) $sql .= ' WHERE cat_blog_ID IN (' . $b2_blog . ')';
	$sql .= ' ORDER BY cat_blog_ID, cat_parent_id, cat_ID';


	$results = mysql_query($sql,$resB2) or die("Invalid query: " . mysql_error() . "<br /> SQL : " . $sql);
	if ($results) {
		$cnt = 0;

		// fake the blogs as top-level categories
		while($b2blog = mysql_fetch_object($b2blogs))
		{
			if( ! empty($b2_lb)) import_linkblog( $b2_lb ); //import linkblog

			if( $b2_bac ) {
				$b2blog->cat_name = $wpdb->escape(wp_specialchars($b2blog->blog_name));
	   		        $b2blog->cat_nicename = sanitize_title($b2blog->blog_shortname);
				$b2blog->cat_description = $wpdb->escape(  $b2blog->blog_description);
				$b2blog->cat_parent_id = 0;
				$b2blog->cat_blog_id = 0;
				$b2blog->cat_ID = $b2blog->blog_ID * -1;
				$arCat[$b2blog->cat_ID] = 0;
				$categories[$cnt ++] = $b2blog;
			}
		}

//		echo '<pre>categories (just blogs so far)';
//		print_r ($categories);
//		echo '</pre>';

		// now the "real" cats!
		//$id_result = $wpdb->get_row("SHOW TABLE STATUS LIKE '$wpdb->categories'");
		//$newCatID = $id_result->Auto_increment;
		while ($result = mysql_fetch_object($results)) {
			$result->cat_name = $wpdb->escape( wp_specialchars($result->cat_name));
			$result->cat_nicename = sanitize_title($result->cat_name);
			$result->cat_description = $wpdb->escape(  wp_specialchars($result->cat_description) );
			$arCat[$result->cat_ID] = 0;
			$categories[$cnt ++] = $result;
		}
		// remap category parent IDs and insert

		foreach($categories as $result) {
			if($b2_bac) {
				if( !$result->cat_parent_id ) $result->cat_parent_id = $result->cat_blog_ID * -1;
			}
//			$result->cat_parent_id = $arCat[$result->cat_parent_id];
//			$result->cat_ID = $arCat[$result->cat_ID];
			$insert_category = "INSERT INTO $wpdb->terms (name, slug) VALUES ('$result->cat_name', '$result->cat_nicename')";
			$wpdb->query($insert_category);
			$new_id = $wpdb->insert_id;
			$arCat[$result->cat_ID] = $new_id;
//			$wpdb->query("INSERT INTO $wpdb->categories (cat_ID, cat_name, category_nicename, category_parent, category_description) VALUES ('$result->cat_ID', '$result->cat_name', '$result->cat_nicename', '$result->cat_parent_id', '$result->cat_description')");
		}
		foreach($categories as $result) {
			$wpdb->query("INSERT INTO $wpdb->term_taxonomy (term_ID, taxonomy, description, parent, count) VALUES (" .$arCat[$result->cat_ID] . ", 'category','$result->cat_description', '" . $arCat[$result->cat_parent_id] . "','0')");
			$taxonomyCat[$result->cat_ID] = $wpdb->insert_id;
		}
		echo $cnt . " category record(s) imported! <br />";
	} else {
		echo "No category records found!<br />";
	}

	/*
	echo('<pre>');
	print_r($taxonomyCat);
	echo('</pre>');
	*/

	// get entries for blog
	echo "Importing Entry records ... <br />";
    $sql = 'SELECT * FROM `' . $b2_prefix . 'items__item` INNER JOIN `' . $b2_prefix . 'categories` ON cat_ID = post_main_cat_ID';
    if( $b2_blog != 'all' ) $sql .= ' WHERE cat_blog_ID IN (' . $b2_blog . ')';

    echo "SQL for Blog-Entries : " . $sql;
	$wpdb->select($b2_db);
	$results = mysql_query($sql,$resB2) or die("Invalid query: " . mysql_error() . "<br /> SQL : " . $sql);

	if ($results) {
		$cnt = 0;
		$cntCom = 0;
		$cntCat = 0;
		while ($result = mysql_fetch_object($results)) {
			// TODO: Import ALL posts with ANY cats in ANY selected blogs, not just main cat.
			// check to make sure it's got an allowed category from the postcats table.
			// if not, then continue.
			// this will slow things down a bit, but no biggie.
			// Comment out the 'where cat_blog_ID IN...' line above.


			// author ID must be switched to new author ID
			$post_author = $arUser[$result->post_creator_user_ID];

			// category ID must be switched to new category ID
			$post_cat = $arCat[$result->post_main_cat_ID];
			if (!$cid) {
				$cid = '1';
			}

			// status mapping
			$stat = $result->post_status;
			switch($stat) {
				case 'published':
					$stat='publish';
					break;
				case 'deprecated':
					switch($b2_importdep) {
						case 'private': $stat = 'private'; break;
						case 'draft': $stat = 'draft'; break;
						case 'abandon': continue; break;
						case 'publish': $stat = 'publish';
					}
					break;
				case 'published': $stat = 'publish'; break;
				case 'protected': $stat = 'private'; break;
				case 'draft': $stat = 'draft'; break;
			}


			// update urls in the post content
			// IZS - removed this bit.  I'm keeping my files where they are!
//			$post_content = str_replace($filepath_b2, $filepath_wp, $result->post_content);

			$post_content = $result->post_content;

			// if there is a post_URL, then put it at the start of the post in its own paragraph.
			$dometa = false;
			$metaurl = '';
			if( $result->post_url && $b2_posturl != 'ignore' ) {
				if( $b2_posturl == 'meta' || $b2_posturl == 'postandmeta' ) {
					$dometa = true;
					$metaurl = $wpdb->escape($result->post_url);
					// echo 'url: [' . $metaurl . ']';
				}
				if( $b2_posturl == 'post' || $b2_posturl == 'postandmeta' ) {
					$link = '<p class="bloglink"><a href="' . $result->post_url . '">';
					if( strlen($result->post_url) > 50 )
						$link .= substr($result->post_url, 0, 25) . '...' . substr($result->post_url, -15, 15);
					else
						$link .= $result->post_url;
					$link .= '</a></p>' . "\n\n";
					$post_content = $link . $post_content;
				}
			}
			$post_excerpt = $post_content;
			
			/* IZS: Removed Post_excerpt stuff. Comment the next line to bring it back: */
			$post_excerpt = '';
			

			
			if( strpos(strtolower($post_excerpt), '<!--nextpage-->') !== false ) {
				$post_excerpt = preg_replace('/<!--nextpage-->/i','<!--more-->',$post_excerpt);
			}
			if( strpos(strtolower($post_excerpt), '<!--more-->') !== false ) {
				//had a weird problem here with <!--more--> vs <!--More--> vs <!--MORE--> etc.
				//that's why the next line with the /i switch, which looks like it does nothing.
				//actually, this is LCase-ing all the <!--mOrE--> stuff.
				$post_excerpt = preg_replace('/<!--more-->/i','<!--more-->',$post_excerpt);
				$post_excerpt = explode('<!--more-->', $post_excerpt);
				$post_excerpt = $post_excerpt[0];
			}

			$metaimg = '';
			if( preg_match('#<img src="([^"]+)"[^>]+>#', $result->post_title, $matches) )
			{
				// title has an image in the title. - i do this sometimes, and it fubars the importer a little.
//				echo 'image found!<pre>$matches: ';
//				print_r($matches);
//				echo '</pre>';

				$metaimg = $matches[1];
				$dometa = true;
				$result->post_title = strip_tags($result->post_title);
				if(!$result->post_title) $result->post_title = '[Image]';
			}

			$post_content = $wpdb->escape($post_content);
			$post_excerpt = $wpdb->escape($post_excerpt);
			$post_title = $wpdb->escape($result->post_title);
			$post_name = sanitize_title($result->post_urltitle);
			$post_date_gmt = get_gmt_from_date( $result->post_datecreated );
			$post_moddate_gmt = get_gmt_from_date( $result->post_datemodified );

			$wpdb->select(DB_NAME);
			$wpdb->query("INSERT INTO $wpdb->posts 
				(post_author, post_date, post_date_gmt, post_content, post_title, 
				   post_status, post_name, post_excerpt, post_modified, post_modified_gmt) 
				VALUES 
				('$post_author', '$result->post_datemodified', '$post_date_gmt', '$post_content', 
				   '$post_title', '$stat', '$post_name', '$post_excerpt', 
				   '$result->post_datemodified', '$post_moddate_gmt')");
			echo "Inserted ".$post_title."<br />";
			$post_id = $wpdb->insert_id;
			$eid = $result->post_ID;
			$cnt = $cnt + 1;

			// get comments for entry
			$sql = 'SELECT ' .
						'CASE WHEN u.user_ID IS NULL THEN c.comment_author ELSE ' .
							'CASE u.user_idmode ' .
							"WHEN 'nickname' THEN u.user_nickname " .
							"WHEN 'login' THEN u.user_login " .
							"WHEN 'namefl' THEN CONCAT(u.user_firstname, ' ', u.user_lastname) " .
							"WHEN 'namelf' THEN CONCAT(u.user_lastname, ' ', u.user_firstname) " .
							"WHEN 'firstname' THEN u.user_firstname " .
							"WHEN 'lastname' THEN u.user_lastname " .
							'ELSE u.user_nickname END ' .
						"END AS 'author', " .
						"CASE WHEN u.user_ID IS NULL THEN c.comment_author_email ELSE u.user_email END AS 'author_email', " .
						"CASE WHEN u.user_ID IS NULL THEN c.comment_author_url ELSE u.user_url END AS 'author_url', " .
						'comment_author_IP, comment_content, comment_post_ID, comment_date, comment_karma, comment_type, comment_author_ID ' .
						'FROM `' . $b2_prefix . 'comments` as c ' .
						'LEFT JOIN `' . $b2_prefix . 'users` as u ON ' .
						'u.user_ID = c.comment_author_id ' .
						'WHERE comment_post_ID=' . $eid;
			$wpdb->select($b2_db);
			$subResults = mysql_query($sql, $resB2) or die("Invalid query: " . mysql_error() . "<br /> SQL : " . $sql);
			if ($subResults) {
				while ($result = mysql_fetch_object($subResults)) {
					if ($b2_importtb || ($result->comment_type != 'trackback')) {

						$author  = $wpdb->escape( apply_filters('pre_comment_author_name', $result->author));
						$email   = $wpdb->escape( apply_filters('pre_comment_author_email', $result->author_email));
						$url     = $wpdb->escape( apply_filters('pre_comment_author_url', $result->author_url));
						$comment = apply_filters('pre_comment_content', $result->comment_content);
						$comment = apply_filters('post_comment_text', $comment);
						$comment = apply_filters('comment_content_presave', $comment);
						$user_ip = apply_filters('pre_comment_user_ip', $result->comment_author_IP);
						$comment_date_gmt = get_gmt_from_date("$result->comment_date");
						// author ID must be switched to new author ID
						$post_author = $arUser[$result->comment_author_ID];

						$wpdb->select(DB_NAME);
						$wpdb->query(
							"INSERT INTO $wpdb->comments (
							comment_post_ID, comment_author, comment_author_email, comment_author_url, 
							comment_author_IP, comment_date, comment_date_gmt, comment_content, 
							comment_karma, comment_type, user_id) 
							VALUES (
							'$post_id', '$author', '$email', '$url', '$user_ip', '$result->comment_date', 
							'$comment_date_gmt', '$comment', '$result->comment_karma', '$result->comment_type', '$post_author')");
						//
						// djl
						//
						$count = $wpdb->get_var("SELECT COUNT(*) FROM $wpdb->comments WHERE comment_post_ID = '$post_id' AND comment_approved = '1'");
						$wpdb->query( "UPDATE $wpdb->posts SET comment_count = $count WHERE ID = '$post_id'" );


						$cntCom = $cntCom + 1;
					}
				}
			}

			// do meta for url if requested
			if( $dometa ) {
				if($metaurl) {
					$metasql = "INSERT INTO $wpdb->postmeta (post_id, meta_key, meta_value) VALUES (" .
						$id . ", 'URL', '" . $metaurl . "')";
					$wpdb->query($metasql);
				}
				if($metaimg) {
					$metasql = "INSERT INTO $wpdb->postmeta (post_id, meta_key, meta_value) VALUES (" .
						$id . ", 'IMG', '" . $metaimg . "')";
					$wpdb->query($metasql);
				}
			}

			// get categories for entry
			$cntTmp = 0;
			$wpdb->select($b2_db);
			$post_cats_query = "SELECT * FROM `" . $b2_prefix . "postcats` WHERE postcat_post_ID=" . $eid;
			$sql = $post_cats_query;
			$subResults = mysql_query($sql, $resB2) or die("Invalid query: " . mysql_error() . "<br /> SQL : " . $sql);
			if ($subResults) {
				while ($result = mysql_fetch_object($subResults)) {
					print_r($taxonomyCat);
					$tax_post_id = $taxonomyCat[$result->postcat_cat_ID];
					if ($tax_post_id)
					{
						$wpdb->select(DB_NAME);
						$query_post_cats = "INSERT INTO $wpdb->term_relationships (object_id, term_taxonomy_id) VALUES ('$post_id', '$tax_post_id')";
						$wpdb->query($query_post_cats);
						$cntCat = $cntCat + 1;
						$cntTmp = $cntTmp + 1;
					}
				}
			}
			if ($cntTmp == 0) {
				// No categories defined in b2evo - put it in the default category
//				$wpdb->query("INSERT INTO $wpdb->post2cat (post_id, category_id) VALUES ('$id', '1')");
				$cntCat = $cntCat + 1;
			}
		}
		echo "$cnt entry record(s) imported! <br />";
		echo "$cntCom comment record(s) imported! <br />";
		echo "$cntCat entry category record(s) imported! <br />";
	} else {
		echo "No entry records found!<br />";
	}
	mysql_close($resB2);
	echo "That's all folks!";
break;
}
?>
</body>
</html>
