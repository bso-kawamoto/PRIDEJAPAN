<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<link type="text/css" rel="stylesheet" href="css/admin.css" />

	<title>メールフォーム 設定ページ</title>
</head>

<body id="form_setting">

<div id="contents_wrapper">

    <div id="header">
		<h1>エックスサーバー</h1>
		<h2>メールフォーム設定</h2>
        
		<ul id="header_navi">
			<li><a href="http://www.xserver.ne.jp/man_install_cgi_mailform.php">マニュアル</a></li>
			<li><a href="./?logout=on">ログアウト</a></li>
		</ul>
	</div>
	<!-- /header -->

    <div id="contents">
		<p>
			エラー項目があります。<br />
			下記の内容を修正後、再度「プレビュー」ボタンを押下してください。
        </p>

		<br />
		<div class="inner">
			{$error_txt}
		</div>
		<!-- /inner -->

    </div><!-- /contents -->


	<div id="footer">
        <address>Copyright(c) 2012 XSERVER Inc. All rights reserved.</address>
        <span id="tool_name">Custom MailForm Ver 1.1.0</span>
    </div>
    
</div><!-- /contents_wrapper -->
 
 
</body>
</html>

