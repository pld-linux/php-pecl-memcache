<?php
/*
 * Config for memcache.php administrative interface.
 */

// Admin Username
define('ADMIN_USERNAME', 'memcache');
// Admin Password
define('ADMIN_PASSWORD', 'memcache');

define('DATE_FORMAT', 'Y-m-d H:i:s');
define('GRAPH_SIZE', 200);
define('MAX_ITEM_DUMP', 50);

// add more as an array
$MEMCACHE_SERVERS[] = 'localhost:11211';
