	<div id="contents">
		<noscript>
			<div class="red_txt">
				このページは javascript を利用しています。<br />
				javascript が利用できる設定に変更してください。<br />
			</div>
		</noscript>

		<h3>メールフォーム設置用のHTMLタグ</h3>
		<div class="inner">
				<div class="left_txt">
				<p>メールフォームを使用するサイトに、以下HTMLタグをコピーして設置してください。</p>
				</div>

				<table border="1" summary="設置先URLを確認するフォーム" cellspacing="0" class="text_center">
					<tr><td>
						<textarea name="set_html" rows="4" cols="90" readonly onclick="this.select();">&lt;a href="{$form_seturl}"&gt;お問い合わせフォーム&lt;/a&gt;</textarea>
					</td></tr>
				</table>

				<br />

				<div class="left_txt">
				<p>※HTMLタグは必要に応じて変更してご利用ください。<br />
				※SSL暗号化通信を利用する場合は、URL部分を変更してHTMLタグを設置してください。<br />
				　詳しくはマニュアル「<a href="http://www.xserver.ne.jp/man_install_cgi_mailform.php#ssl_explanation">メールフォームCGI &gt; SSLの利用</a>」の項目を参照してください。</p>
				</div>
		</div>
		<!-- /inner -->

		<br />
		<br />
    </div><!-- /contents -->
