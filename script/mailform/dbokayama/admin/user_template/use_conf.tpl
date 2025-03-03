<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>{$basic_pagetitle}</title>
    <link type="text/css" rel="stylesheet" href="./css/form.css" />
</head>

<body>

<div id="contents_wrapper">

	<div id="contents">
		<form method="post" action="./">

		<div class="form_section">
			<h3>{$basic_formname}(確認)</h3>
			<div class="inner">
				<div id="txt_explain">
				<p>記入事項をご確認の上、問題がなければ「送信」をクリックしてください。<br /></p>
				</div>

				<table id="main_table" border="1" cellspacing="0">
				{$form_data}
				</table>

				<div class="button_box">
					<input type="submit" name="submit_button" value="送信">
					<input type="submit" name="submit_button" value="戻る">
				</div>
				<!-- /buttonbox -->

			</div>
			<!-- /inner -->

		</div>
		<!-- /form_section -->
		
		</form>

		<div class="button_box">
			[<a href="{$basic_moveurl}">サイトへ戻る</a>]
		</div>

	</div>
	<!-- /contents -->
</div><!-- /contents_wrapper  -->
 
</body>
</html> 


