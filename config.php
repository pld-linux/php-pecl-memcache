<?php
/*
 * Config for memcache.php administrative interface.
 */

// Admin Username, use <null> (language construct, not string) to skip the check.
// For example if you want to restrict the access with webserver.
define('ADMIN_USERNAME', null);
// Admin Password
define('ADMIN_PASSWORD', 'memcache');

define('DATE_FORMAT', 'Y-m-d H:i:s');
define('GRAPH_SIZE', 200);
define('MAX_ITEM_DUMP', 50);

// add more as an array
$MEMCACHE_SERVERS[] = 'localhost:11211';
