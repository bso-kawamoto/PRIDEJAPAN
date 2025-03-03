<div id="contents">
	<noscript>
		<div class="red_txt">
			このページは javascript を利用しています。<br />
			javascript が利用できる設定に変更してください。<br />
		</div>
	</noscript>

	<form name="main_menu" method="post" action="./option.php">
		<h3>自動返信メールの設定</h3>
		<div class="inner">
			<div class="left_txt">
				<p>
				お問い合わせを受信した時に自動的に返信するメールを設定することができます。<br />
				自動返信メールを使用するには、フォームに「ご連絡先メールアドレス」の項目を設置する必要があります。<br />
				「ご連絡先メールアドレス」が未記入の場合は、自動返信メールは送信されません。
				</p>
			</div>

			<div class="red_txt">{$automail_error}</div>

			<div style="text-align:left;">
				<select name="auto_mail" onchange="ViewChangeAutoMail();">
					<option value="0" {$used_auto_0} />自動返信メールを使用しない
					<option value="1" {$used_auto_1} />自動返信メールを使用する
				</select>
			</div>

			<br />

			<div id="auto_mail_table" {$set_used_automail}>

				<table id="main_table" border="1" summary="自動返信メールの設定を行うフォーム" cellspacing="0">
					<tr>
						<th scope="row">メールの件名</th>
						<td>
							<input type="text" name="rmail_subject" value="{$mail_subject}" size="40" style="ime-mode: active" />
						</td>
					</tr>
					<tr>
						<th>メールの本文</th>
						<td>
							<textarea name="rmail_body" cols="80" rows="10" style="ime-mode: active" />{$mail_body}</textarea><br />
							<div class="attention_txt">
								※###お問い合わせ内容### はお客様にてご入力いただいた内容に変換されます<br />
							</div>
						</td>
					</tr>
					<tr>
						<th>差出人のアドレス</th>
						<td>
							<input type="text" name="from_address" value="{$from_address}" size="40" style="ime-mode: inactive" />
							<div class="attention_txt">
								※自動返信メールの差出人(From)を記入します<br />
							</div>
						</td>
					</tr>
				</table>

			</div>

		</div>
		<!-- /inner -->

		<div class="button_box">
			<strong>・</strong>
			「自動返信メール」の変更を行う場合は、「<strong>設定を保存する(確認)</strong>」ボタンを押してください。<br />
			<br />
			<input type="hidden" name="nowpage" value="system_page" />
			<input type="submit" name="submit_button" value="設定を保存する(確認)" />
			<input type="button" name="reset_button" value="リセット" onclick="document.location = document.location.href" />
		</div>
		<!-- /button_box -->

	</form>

	<br />

</div><!-- /contents -->
