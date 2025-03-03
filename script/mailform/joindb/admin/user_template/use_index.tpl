&lt;!DOCTYPE html PUBLIC &quot;-//W3C//DTD XHTML 1.0 Strict//EN&quot; &quot;http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd&quot;&gt;
&lt;html xmlns=&quot;http://www.w3.org/1999/xhtml&quot;&gt;
&lt;head&gt;
    &lt;meta http-equiv=&quot;Content-Type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;
    &lt;title&gt;{$basic_pagetitle}&lt;/title&gt;
    &lt;link type=&quot;text/css&quot; rel=&quot;stylesheet&quot; href=&quot;./css/form.css&quot; /&gt;
&lt;/head&gt;

&lt;body&gt;

&lt;div id=&quot;contents_wrapper&quot;&gt;

    &lt;div id=&quot;contents&quot;&gt;

        &lt;form method=&quot;post&quot; action=&quot;./&quot;&gt;

            &lt;div class=&quot;setting_section&quot;&gt;
                &lt;h3&gt;{$basic_formname}&lt;/h3&gt;
                &lt;div class=&quot;inner&quot;&gt;
                    &lt;div id=&quot;txt_explain&quot;&gt;
                        &lt;p&gt;第14回ドームバトル（本戦）への参加をご希望のチーム様は、以下のフォームに必要事項をご記入の上、「確認」をクリックしてください。 &lt;br /&gt;
*の付いている項目は必須項目です。 &lt;br /&gt; &lt;br /&gt;

&lt;font color=&quot;red&quot;&gt;&lt;b&gt;ご確認ください！&lt;/b&gt;&lt;/font&gt; &lt;br /&gt;
お申込を受け付けましたら、システムより自動返信メールを送信いたしますので、迷惑メール対策等でメールの受信制限を行っている場合は、&lt;font color=&quot;red&quot;&gt;info@pridejapan.netからのメールを受け取れるように設定&lt;/font&gt;したのち、お申込を行ってください。&lt;/p&gt;
                    &lt;/div&gt;

                    &lt;div class=&quot;red_txt&quot;&gt;{$form_error}&lt;/div&gt;

                    &lt;table id=&quot;main_table&quot; border=&quot;1&quot; cellspacing=&quot;0&quot;&gt;
                        {$form_data}
                    &lt;/table&gt;

                    &lt;div class=&quot;button_box&quot;&gt;
                        &lt;input type=&quot;submit&quot; name=&quot;submit_button&quot; value=&quot;確認&quot;&gt;
                    &lt;/div&gt;

                &lt;/div&gt;
                &lt;!-- /inner --&gt;
        
            &lt;/div&gt;
            &lt;!-- /form_section --&gt;

        &lt;/form&gt;

        &lt;div class=&quot;button_box&quot;&gt;
            [&lt;a href=&quot;{$basic_moveurl}&quot;&gt;サイトへ戻る&lt;/a&gt;]
        &lt;/div&gt;

    &lt;/div&gt;
    &lt;!-- /contents --&gt;

&lt;/div&gt;&lt;!-- /contents_wrapper --&gt;
 
&lt;/body&gt;
&lt;/html&gt;