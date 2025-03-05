<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'bso_wp1' );

/** Database username */
define( 'DB_USER', 'bso_wp1' );

/** Database password */
define( 'DB_PASSWORD', 'ej6c2r2z4g' );

/** Database hostname */
define( 'DB_HOST', 'mysql508b.xserver.jp' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '^xz?-t;/CqjFpW&Foy%MXRXJ@h!LxOp3v{,nHiCuGLB^oY@S[$25wrIPBF&0(@kA' );
define( 'SECURE_AUTH_KEY',  'p$d?`=7amSZCQNijmk|O`8#gV))V4c@YzC}]rM`;eQw}(4u>$zhafM[i%6@&gO@r' );
define( 'LOGGED_IN_KEY',    '6j!j/ne@Mx5c(ml@[;05WmzQ{*mLtcu:nDjY4EV!0.QqU84P~Q*e4,Q)yT$_=y3X' );
define( 'NONCE_KEY',        '2<Ek%H,NviPbm[ 1&x%y&p_@M1008.tQr=,Yn+<?;?n_ei 8Ic} FPN2<9wzVFal' );
define( 'AUTH_SALT',        '^E!GKLQO{Sk|[PWCf,;x8[=#W+a.Hc02/K=c5~}9)%=j6G8PvX,wbQu^j%xd!r|7' );
define( 'SECURE_AUTH_SALT', '}zz&r0U$Tc&(LdO(f.ZR[zt105vV2xNE;N7SpFo4uDmVQ`vM$*`L-h)ax41H:iqC' );
define( 'LOGGED_IN_SALT',   'l}krUCChJS;Kw{VcL>yC|Tfl~Ubh(cebSeF9YKY`!kB^Y@6YK<4r`x3o06Xy)lfE' );
define( 'NONCE_SALT',       '3#4[=FUtC:Le$CP[z,=A{eJ!rXg0n@U>mG,bv=(*6Lp{54Q*%)Jrkl8eye[d#Pjl' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
