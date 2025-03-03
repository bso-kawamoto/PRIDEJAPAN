    <div id="contents">
        <form name="main_menu" method="post" action="./">

            <div id="basic_conf" class="setting_section">
                <h3>基本設定</h3>
                <div class="inner">
                    <table border="1" summary="メールの基本設定をするフォーム" cellspacing="0">
                        <tr>
                            <th scope="row" style="width : 220px ;">ページのタイトル</th>
                            <td>{$basic_pagetitle}</td>
                        </tr>
                        <tr>
                            <th scope="row">メールフォームの名前</th>
                            <td>{$basic_formname}</td>
                        </tr>
                        <tr>
                            <th scope="row">サイトへの戻りURL</th>
                            <td>{$basic_moveurl}</td>
                        </tr>
                        <tr>
                            <th scope="row">受信するメールアドレス</th>
                            <td>{$basic_mailaddress}</td>
                        </tr>
                        <tr>
                            <th scope="row">受信するメールの件名</th>
                            <td>{$basic_mailsubject}</td>
                        </tr>
                        <tr>
                            <th scope="row">メールの連続送信を制限する時間</th>
                            <td>{$basic_maillimittime}分</td>
                        </tr>
                    </table>
                    <input type="hidden" name="page_title" value="{$basic_pagetitle}" />
                    <input type="hidden" name="form_name" value="{$basic_formname}" />
                    <input type="hidden" name="form_width" value="{$basic_formwidth}" />
                    <input type="hidden" name="move_url" value="{$basic_moveurl}" />
                    <input type="hidden" name="mail_address" value="{$basic_mailaddress}" />
                    <input type="hidden" name="mail_subject" value="{$basic_mailsubject}" />
                    <input type="hidden" name="mail_limit_time" value="{$basic_maillimittime}" />

                </div>
                <!-- /inner -->
            </div>
            <!-- /setting_section -->

            <div id="item_conf" class="setting_section">
            <h3>メールフォームの表示項目</h3>
                <div class="inner">
                    <table class="conf_table" border="1" summary="入力項目の確認を行うフォーム" cellspacing="0">
                        <tr>
                            <th>項目名</th>
                            <th>表示名</th>
                            <th>必須</th>
                            <th>入力タイプ</th>
                            <th>オプション</th>
                        </tr>
                        {$form_view_data}

                    </table>
                </div>
                <!-- /inner -->
            </div>
            <!-- /setting_section -->
            
            <div class="button_box">
                <strong>・</strong>
                上記の内容で保存を行う場合は、「<strong>設定を保存する(確定)</strong>」ボタンを押してください。<br />
                <br />

                <input type="hidden" name="nowpage" value="system_page" />
                <input type="submit" name="submit_button" value="設定を保存する(確定)" />
                <input type="submit" name="submit_button" value="戻る" />
                <input type="button" name="preview_button" value="プレビュー" onclick="OpenPreview(this.form, '');" />
            </div>
            <!-- /button_box -->
            
        </form>

        <br />

    </div><!-- /contents -->
