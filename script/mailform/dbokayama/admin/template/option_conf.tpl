    <div id="contents">
        <form name="main_menu" method="post" action="./option.php">

            <div id="basic_conf" class="setting_section">
                <h3>自動返信メールの設定</h3>
                <div class="inner">

                    <table border="1">
                        <tr>
                            <th style="width:30%">自動返信の設定</th>
                            <td>{$html_auto_mail}</td>
                        </tr>
                    </table>

                    <br />

                    <div id="auto_mail_table" {$set_used_automail}>
                        <table id="main_table" border="1" summary="自動返信メールの設定を行うフォーム" cellspacing="0">
                            <tr>
                                <th style="width:30%">メールの件名</th>
                                <td>{$mail_subject}</td>
                            </tr>
                            <tr>
                                <th>メールの本文</th>
                                <td>{$html_mail_body}</td>
                            </tr>
                            <tr>
                                <th>差出人のアドレス</th>
                                <td>{$from_address}</td>
                            </tr>
                        </table>

                    </div>

                    <input type="hidden" name="auto_mail" value="{$auto_mail}" />
                    <input type="hidden" name="rmail_subject" value="{$mail_subject}" />
                    <input type="hidden" name="rmail_body" value="{$mail_body}" />
                    <input type="hidden" name="from_address" value="{$from_address}" />
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
            </div>
            <!-- /button_box -->
            
        </form>

