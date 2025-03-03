<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link type="text/css" rel="stylesheet" href="./css/admin.css" />
    <title>メールフォーム ログインページ</title>
</head>

<body>
 
<div id="contents_wrapper">

	<div id="header">
    	<h1>エックスサーバー</h1>
		<h2>メールフォーム設定</h2>
	</div>
	<!-- /header -->

	<div id="contents">

		<form name="main_menu" method="post" action="./">
			<div id="basic_conf" class="setting_section">
				<h3>ログイン</h3>
				<div class="inner">
					<table border="1" summary="ログイン" cellspacing="0">
						<tr>
							<th scope="row">ユーザーID</th>
							<td><input type="text" name="username" size="40" /></td>
						</tr>
						<tr>
							<th scope="row">パスワード</th>
							<td><input type="password" name="password" size="40" /></td>
						</tr>
					</table>
					{$error_txt}
				</div>
				<!-- /inner -->
			</div>
			<!-- /setting_section -->

			<div class="button_box">
				<input type="submit" name="login_button" value="ログイン" />
			</div>
			<!-- /button_box -->
		</form>

	</div><!-- /contents -->

	<div id="footer">
		<address>Copyright(c) 2012 XSERVER Inc. All rights reserved.</address>
		<span id="tool_name">Custom MailForm Ver 1.1.0</span>
	</div>
    
</div><!-- /contents_wrapper -->


</body>
</html>

