<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	{$system_js}
	<script type="text/javascript" src="./js/design_func.js"></script>
	<script type="text/javascript" src="./js/other_func.js"></script>
	<link type="text/css" rel="stylesheet" href="./css/admin.css" />
	<title>メールフォーム 設定ページ</title>
</head>

<body id="{$setting_body_id}">

<div id="contents_wrapper">

	<div id="header">
		<h1>エックスサーバー</h1>
		<h2>メールフォーム設定</h2>

		<ul id="header_navi">
			<li id="view_form_button"><a href="{$form_seturl}" target="_blank">メールフォームを表示</a></li>
			<li><a href="http://www.xserver.ne.jp/man_install_cgi_mailform.php">マニュアル</a></li>
			<li><a href="./?logout=on">ログアウト</a></li>
		</ul>
	</div>
	<!-- /header -->

	<div id="setting_navi">
		<ul>
			<li id="setting_navi_form"><a href="./">基本項目の設定</a></li>
			<li id="setting_navi_design"><a href="./design.php">デザインの設定</a></li>
			<li id="setting_navi_option"><a href="./option.php">自動返信メールの設定</a></li>
			<li id="setting_navi_sethtml" class="list_end"><a href="./sethtml.php">設置用のHTMLタグ</a></li>
		</ul>
	</div>

