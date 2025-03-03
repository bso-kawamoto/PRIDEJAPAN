	<div id="contents">
		<noscript>
			<div class="red_txt">
				このページは javascript を利用しています。<br />
				javascript が利用できる設定に変更してください。<br />
			</div>
		</noscript>

		<form name="main_menu" method="post" action="./">

			<div id="basic_setting" class="setting_section">
			<h3>基本設定</h3>
			<div class="inner">

			<p>メールフォームの基本の設定を行うことができます。</p>

			<div class="red_txt">{$form_error}</div>

			<table id="main_table" border="1" summary="メールの基本設定を行うフォーム" cellspacing="0">
				<tr>
					<th scope="row" style="width : 220px ;">ページのタイトル</th>
					<td>
						<input type="text" name="page_title" value="{$basic_pagetitle}" size="40" style="ime-mode: active" onchange="ClosePreview();" />
					</td>
				</tr>
				<tr>
					<th scope="row">メールフォームの名前</th>
					<td>
						<input type="text" name="form_name" value="{$basic_formname}" size="40" style="ime-mode: active" onchange="ClosePreview();" />
					</td>
				</tr>
				<tr>
					<th scope="row">サイトへの戻りURL</th>
					<td>
						<input type="text" name="move_url" value="{$basic_moveurl}" size="40" style="ime-mode: inactive" onchange="ClosePreview();" /><br />
						<div class="attention_txt">
							※メールフォームからサイトに戻るためのリンクに使用します<br />
						</div>
					</td>
				</tr>
				<tr>
					<th scope="row">受信するメールアドレス</th>
					<td>
						<input type="text" name="mail_address" value="{$basic_mailaddress}" size="40" style="ime-mode: inactive" onchange="ClosePreview();" />
						<div class="attention_txt">
							※お問い合わせの内容を受信するメールアドレスを設定します<br />
						</div>
					</td>
				</tr>
				<tr>
					<th scope="row">受信するメールの件名</th>
					<td>
						<input type="text" name="mail_subject" value="{$basic_mailsubject}" size="40" style="ime-mode: active" onchange="ClosePreview();" />
					</td>
				</tr>
				<tr>
					<th scope="row">メールの連続送信を制限する時間</th>
					<td>
						<select name="mail_limit_time">
							{$basic_maillimittime}
						</select>
						分<br />
						<div class="attention_txt">
							※同一IPによるメールの連続送信を制限する時間を設定します<br />
						</div>
					</td>
				</tr>
			</table>

			</div>
			<!-- /inner -->

			<br />
			<br />

			<div id="item_setting" class="setting_section">
			<h3>メールフォーム項目の設定</h3>

				<div class="inner">

				<p>メールフォームの項目内容を設定することができます。<br />
				「使用可能な項目」から使用する項目を選び、「追加」をクリックしてください。また、「使用中の項目」で使用しないものは「除外」をクリックしてください。<br />
				「使用中の項目」を並べ替える場合は、「▲」「▼」ボタンをクリックしてください。<br />
				※予備項目は各項目ごとに９つまで追加することができます。</p>


				<div class="red_txt">{$form_items_error}</div>

				<div id="left_container">
					<h4>使用中の項目</h4>

					<div class="display_item_wrapper">
					{$form_view_data}

					</div>
					<!-- /display_item_wrapper -->

				</div>
				<!-- /left_container -->

				<div id="right_container">
					<h4>使用可能な項目</h4>
<table id="input_table" border="1" summary="入力項目の設定を行うフォーム">
	<tr><th colspan="2">基本項目</th></tr>
	<tr><th class="sub_th">お名前</th><td><input type="button" name="btn_item_name" value="追加" onclick="addItem('item_name','お名前','お名前','fullname','none','0',false);" /></td></tr>
	<tr><th class="sub_th">ふりがな</th><td><input type="button" name="btn_item_kana" value="追加" onclick="addItem('item_kana','ふりがな','ふりがな','fullname','kana','0',false);" /></td></tr>
	<tr><th class="sub_th">ＵＲＬ</th><td><input type="button" name="btn_item_hp" value="追加" onclick="addItem('item_hp','ＵＲＬ','ホームページ','text','url','0',false);" /></td></tr>
	<tr><th class="sub_th">年齢</th><td><input type="button" name="btn_item_age" value="追加" onclick="addItem('item_age','年齢','年齢','text','numeric','64',false);" /></td></tr>
	<tr><th class="sub_th">性別</th><td><input type="button" name="btn_item_sex" value="追加" onclick="addItem('item_sex','性別','性別','sex','none','0',false);" /></td></tr>
	<tr><th class="sub_th">郵便番号</th><td><input type="button" name="btn_item_poscode" value="追加" onclick="addItem('item_poscode','郵便番号','郵便番号','code','numeric','1',false);" /></td></tr>
	<tr><th class="sub_th">都道府県</th><td><input type="button" name="btn_item_selarea" value="追加" onclick="addItem('item_selarea','都道府県','都道府県','selarea','none','0',false);" /></td></tr>
	<tr><th class="sub_th">住所</th><td><input type="button" name="btn_item_address" value="追加" onclick="addItem('item_address','住所','ご住所','address','none','0',false);" /></td></tr>
	<tr><th class="sub_th">ＴＥＬ</th><td><input type="button" name="btn_item_tel" value="追加" onclick="addItem('item_tel','ＴＥＬ','お電話番号','text','tel','0',false);" /></td></tr>
	<tr><th class="sub_th">ＦＡＸ</th><td><input type="button" name="btn_item_fax" value="追加" onclick="addItem('item_fax','ＦＡＸ','ＦＡＸ','text','fax','0',false);" /></td></tr>
	<tr><th class="sub_th">ご連絡先メールアドレス</th><td><input type="button" name="btn_item_mail" value="追加" onclick="addItem('item_mail','ご連絡先メールアドレス','ご連絡先メールアドレス','mail','mail','0',false);" /></td></tr>
	<tr><th class="sub_th">件名</th><td><input type="button" name="btn_item_subject" value="追加" onclick="addItem('item_subject','件名','件名','text','none','0',false);" /></td></tr>
	<tr><th class="sub_th">お問い合わせ内容</th><td><input type="button" name="btn_item_contents" value="追加" onclick="addItem('item_contents','お問い合わせ内容','お問い合わせ内容','textarea','none','6',false);" /></td></tr>
	<tr><td colspan="2">
		<input type="hidden" name="chk_item_stext01" value="0" /><input type="hidden" name="chk_item_stext02" value="0" /><input type="hidden" name="chk_item_stext03" value="0" />
		<input type="hidden" name="chk_item_stext04" value="0" /><input type="hidden" name="chk_item_stext05" value="0" /><input type="hidden" name="chk_item_stext06" value="0" />
		<input type="hidden" name="chk_item_stext07" value="0" /><input type="hidden" name="chk_item_stext08" value="0" /><input type="hidden" name="chk_item_stext09" value="0" />

		<input type="hidden" name="chk_item_sarea01" value="0" /><input type="hidden" name="chk_item_sarea02" value="0" /><input type="hidden" name="chk_item_sarea03" value="0" />
		<input type="hidden" name="chk_item_sarea04" value="0" /><input type="hidden" name="chk_item_sarea05" value="0" /><input type="hidden" name="chk_item_sarea06" value="0" />
		<input type="hidden" name="chk_item_sarea07" value="0" /><input type="hidden" name="chk_item_sarea08" value="0" /><input type="hidden" name="chk_item_sarea09" value="0" />

		<input type="hidden" name="chk_item_sselect01" value="0" /><input type="hidden" name="chk_item_sselect02" value="0" /><input type="hidden" name="chk_item_sselect03" value="0" />
		<input type="hidden" name="chk_item_sselect04" value="0" /><input type="hidden" name="chk_item_sselect05" value="0" /><input type="hidden" name="chk_item_sselect06" value="0" />
		<input type="hidden" name="chk_item_sselect07" value="0" /><input type="hidden" name="chk_item_sselect08" value="0" /><input type="hidden" name="chk_item_sselect09" value="0" />

		<input type="hidden" name="chk_item_sradio01" value="0" /><input type="hidden" name="chk_item_sradio02" value="0" /><input type="hidden" name="chk_item_sradio03" value="0" />
		<input type="hidden" name="chk_item_sradio04" value="0" /><input type="hidden" name="chk_item_sradio05" value="0" /><input type="hidden" name="chk_item_sradio06" value="0" />
		<input type="hidden" name="chk_item_sradio07" value="0" /><input type="hidden" name="chk_item_sradio08" value="0" /><input type="hidden" name="chk_item_sradio09" value="0" />

		<input type="hidden" name="chk_item_scheckbox01" value="0" /><input type="hidden" name="chk_item_scheckbox02" value="0" /><input type="hidden" name="chk_item_scheckbox03" value="0" />
		<input type="hidden" name="chk_item_scheckbox04" value="0" /><input type="hidden" name="chk_item_scheckbox05" value="0" /><input type="hidden" name="chk_item_scheckbox06" value="0" />
		<input type="hidden" name="chk_item_scheckbox07" value="0" /><input type="hidden" name="chk_item_scheckbox08" value="0" /><input type="hidden" name="chk_item_scheckbox09" value="0" />
	</td></tr>
	<tr><th colspan="2">予備項目</th></tr>
	<tr>
		<th class="sub_th">テキスト</th>
		<td><input type="button" name="btn_item_stext" value="追加" onclick="addSubItem('item_stext','予備テキスト','text','none','0');" /></td>
	</tr>
	<tr>
		<th class="sub_th">テキストボックス</th>
		<td><input type="button" name="btn_item_sarea" value="追加" onclick="addSubItem('item_sarea','予備テキストボックス','textarea','none','6');" /></td>
	</tr>
	<tr>
		<th class="sub_th">プルダウンメニュー</th>
		<td><input type="button" name="btn_item_sselect" value="追加" onclick="addSubItem('item_sselect','予備プルダウンメニュー','select','none','0');" /></td>
	</tr>
	<tr>
		<th class="sub_th">ラジオボタン</th>
		<td><input type="button" name="btn_item_sradio" value="追加" onclick="addSubItem('item_sradio','予備ラジオボタン','radio','none','0');" /></td>
	</tr>
	<tr>
		<th class="sub_th">チェックボックス</th>
		<td><input type="button" name="btn_item_scheckbox" value="追加" onclick="addSubItem('item_scheckbox','予備チェックボックス','checkbox','none','0');" /></td>
	</tr>
</tr>
					</table>
				</div>
				<!-- /right_container -->

				</div>
				<!-- /inner -->
            
			</div>
			<!-- /setting_section -->

			</div>
			<!-- /setting_section -->

			<div class="space_box">
			<div>
            
			</div>
            
			</div>

			<div class="button_box">
				<strong>・</strong>
				「基本設定」または「メールフォーム項目」の変更を行う場合は、「<strong>設定を保存する(確認)</strong>」ボタンを押してください。<br />
				<br />
				<input type="hidden" name="nowpage" value="system_page" />
				<input type="submit" name="submit_button" value="設定を保存する(確認)" />
				<input type="button" name="reset_button" value="リセット" onclick="document.location = document.location.href" />
				<input type="button" name="preview_button" value="プレビュー" onclick="OpenPreview(this.form, '');" />
			</div>
			<!-- /button_box -->
            
		</form>

		<br />

    </div><!-- /contents -->
