#!/usr/bin/perl

use utf8;
binmode STDOUT, ':utf8';
use CGI::Carp qw(fatalsToBrowser);
#use Data::Dumper;

require 'system/common.cgi';

#履歴保存
$sql_str9 = qq{INSERT INTO entrylist_rireki(refara,remoteaddr,host,cgi,querystring) VALUES (?,?,?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$ENV{'HTTP_REFERER'},
$ENV{'REMOTE_ADDR'},
$ENV{'HTTP_HOST'},
"system.cgi",
$ENV{'QUERY_STRING'},
);

# -----------------------------------------------------------------
#クッキー前処理
# -----------------------------------------------------------------
if($code eq "mypagelogin"){&mypagelogin;exit;}
if($code eq "mypage"){&mypage;exit;}
if($code eq "logout"){&logout;exit;}

$loginuser = &getcook2($cookiename);


# -----------------------------------------------------------------
print "Content-type: text/html;\n\n";


# -----------------------------------------------------------------
# 処理開始
# -----------------------------------------------------------------

if($code eq "gameschedule"){&gameschedule;exit;}
if($code eq "gameresult"){&gameresult;exit;}
if($code eq "resistration"){&resistration;exit;}
if($code eq "taikaibanner"){&taikaibanner;exit;}
if($code eq "taikaibanner2"){&taikaibanner2;exit;}

if($code eq "convention"){&convention;exit;}
if($code eq "outline"){&outline;exit;}
if($code eq "result"){&result;exit;}
if($code eq "ranking"){&ranking;exit;}
if($code eq "ranking2"){&ranking2;exit;}
if($code eq "report"){&report;exit;}
if($code eq "schedule"){&schedule;exit;}
if($code eq "taikaireport"){&taikaireport;exit;}
if($code eq "taikairesult"){&taikairesult;exit;}
if($code eq "scheduleall"){&scheduleall;exit;}
if($code eq "entrysituation"){&entrysituation;exit;}

if($code eq "newteamlist"){&newteamlist;exit;}
if($code eq "sokuhou"){&sokuhou;exit;}

if($code eq "whatnew"){&whatnew;exit;}
if($code eq "link"){&link;exit;}

if($code eq "mypage_team"){&mypage_team;exit;}


if($code eq "forgetpassword_form"){&forgetpassword_form;exit;}
if($code eq "forgetpassword_check"){&forgetpassword_check;exit;}

if($code eq "forgetpassword_form_noframe"){&forgetpassword_form_noframe;exit;}
if($code eq "forgetpassword_check_noframe"){&forgetpassword_check_noframe;exit;}






#リファラ無しは弾く
if($ENV{'HTTP_REFERER'} eq "" && $loginuser eq ""){
$mes =<<"END_HTML";
ログイン期限が過ぎております。もう一度ログインをお願いします。<br>
<br>
<input type="button" value="　TOPへ　" onclick="location.href='$sitefulladr'" />
END_HTML
&mypagehtmldisp($mes);
exit;

}


if($code eq "member_new"){&member_new;exit;}
if($code eq "member_check"){&member_check;exit;}
if($code eq "member_add"){&member_add;exit;}
if($code eq "member_ok"){&member_ok;exit;}


if($code eq "member_new_noframe"){&member_new_noframe;exit;}
if($code eq "member_check_noframe"){&member_check_noframe;exit;}
if($code eq "member_add_noframe"){&member_add_noframe;exit;}


if($code eq "member_edit"){&member_edit;exit;}
if($code eq "member_check2"){&member_check2;exit;}
if($code eq "member_add2"){&member_add2;exit;}

if($code eq "gamescheduleform"){&gamescheduleform;exit;}
if($code eq "gamescheduleformadd"){&gamescheduleformadd;exit;}

if($code eq "gameresultform"){&gameresultform;exit;}
if($code eq "gameresultformadd"){&gameresultformadd;exit;}

if($code eq "gameentry"){&gameentry;exit;}
if($code eq "gameentry_check"){&gameentry_check;exit;}
if($code eq "gameentry_add"){&gameentry_add;exit;}

if($code eq "ajaxsave_payment"){&ajaxsave_payment;exit;}

if($code eq "membercontact_form"){&membercontact_form;exit;}
if($code eq "membercontact_check"){&membercontact_check;exit;}
if($code eq "membercontact_ok"){&membercontact_ok;exit;}

if($code eq "membercontact_form_noframe"){&membercontact_form_noframe;exit;}
if($code eq "membercontact_check_noframe"){&membercontact_check_noframe;exit;}
if($code eq "membercontact_ok_noframe"){&membercontact_ok_noframe;exit;}

if($code eq "contact_form"){&contact_form;exit;}
if($code eq "contact_check"){&contact_check;exit;}
if($code eq "contact_ok"){&contact_ok;exit;}

if($code eq "contact_form_noframe"){&contact_form_noframe;exit;}
if($code eq "contact_check_noframe"){&contact_check_noframe;exit;}
if($code eq "contact_ok_noframe"){&contact_ok_noframe;exit;}


if($code eq "bannercategory"){&bannercategory;exit;}


if($code eq "member_new_test"){&member_new_test;exit;}
if($code eq "member_check_test"){&member_check_test;exit;}
if($code eq "member_add_test"){&member_add_test;exit;}

if($code eq "deleterecord_user"){&deleterecord_user;exit;}


&mypage;
exit;

# -----------------------------------------------------------------
# ログアウト処理
# -----------------------------------------------------------------

sub logout {
print "Set-Cookie: $cookiename=; expires=Thu, 1-Jan-1970 00:00:00 GMT;\n";
$mes =<<"END_HTML";
ログアウトしました。<p>
END_HTML
&mypagehtmldisp($mes,1);
exit;
}


# -----------------------------------------------------------------
# チーム：新規登録
# -----------------------------------------------------------------
sub member_new {
#セッション作成
$session = sprintf("%02d%02d%02d",$sec,$min,$hour);
for (1..15) { $session .= ((0..9,a..z,A..Z)[int rand 62])};
$session .= sprintf("%02d%02d%02d",$mday,$month,$year-2000);

#
if($paramhash_dec{'_都道府県名'} ne ""){$PFLAG{$paramhash_dec{'_都道府県名'}} = "selected";}
if($paramhash_dec{'_代表者都道府県名'} ne ""){$PFLAG2{$paramhash_dec{'_代表者都道府県名'}} = "selected";}
if($paramhash_dec{'_メールマガジン配信の選択'} ne ""){
$MAILMAGAZINEFLAG{$paramhash_dec{'_メールマガジン配信の選択'}}="checked=checked";
}else{
$MAILMAGAZINEFLAG{1}="checked=checked";
}	#if
###
print << "END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
<script>
function kakunin(){

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_kana').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('team_abbr').value == "") {
alert('「チーム省略名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_year').value == "") {
alert('「チーム結成年」が入力されていません。');
return(false);
}
var str = document.getElementById("team_year").value;
if( str.match(/[^0-9]/) ){
alert("「チーム結成年」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('team_year').value < 1800) {
alert('「チーム結成年」にエラーがあります。');
return(false);
}


if (document.getElementById('katsudou_week').value == "") {
alert('「主な活動曜日」が入力されていません。');
return(false);
}

if (document.getElementById('average_age').value == "") {
alert('「平均年齢」が入力されていません。');
return(false);
}
var str = document.getElementById("average_age").value;
if( str.match(/[^0-9]/) ){
alert("「平均年齢」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('average_age').value < 5) {
alert('「平均年齢」にエラーがあります。');
return(false);
}


if (document.getElementById('pref').selectedIndex == 0) {
alert('「主な活動場所（都道府県）」が選択されていません。');
return(false);
}

if (document.getElementById('team_cities').value == "") {
alert('「主な活動場所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei1').value == "") {
alert('「代表者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana1').value == "") {
alert('「代表者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('mailadr1').value == "") {
alert('「代表者メールアドレス」が入力されていません。');
return(false);
}
var str = document.getElementById("mailadr1").value;
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス」が不正です。");
return false;
}	//if

if (document.getElementById('mailadr2').value == "") {
alert('「代表者メールアドレス（ドメイン）」が入力されていません。');
return(false);
}
var str = document.getElementById("mailadr2").value;
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス」が不正です。");
return false;
}	//if

if (document.getElementById('tel1').value == "") {
alert('「代表者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel1").value;
if( str.match(/[^0-9-]/) ){
alert("代表者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('zip').value == "") {
alert('「代表者住所（郵便番号）」が入力されていません。');
return(false);
}

if (document.getElementById('pref2').value == "") {
alert('「代表者住所（都道府県）」が入力されていません。');
return(false);
}

if (document.getElementById('cities1').value == "") {
alert('「代表者住所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei2').value == "") {
alert('「第2担当者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana2').value == "") {
alert('「第2担当者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('tel3').value == "") {
alert('「第2担当者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel3").value;
if( str.match(/[^0-9-]/) ){
alert("第2担当者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('mailaddress2').value == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}

if (document.getElementById('pwd').value == "") {
alert('「パスワード」が入力されていません。');
return(false);
}
if (document.getElementById('pwd').value.length < 4) {
alert('「パスワード」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd2').value == "") {
alert('「パスワード（確認用）」が入力されていません。');
return(false);
}
if (document.getElementById('pwd2').value.length < 4) {
alert('「パスワード（確認用）」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd2").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード（確認用）」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd').value != document.getElementById('pwd2').value) {
alert('パスワードが一致していません。');
return(false);
}

return true;
}	//func


</script>
</head>
<body>
<noscript>
<p style="color:red;font-size:16px;">（！）Javascriptを有効にしてください。</p>
</noscript>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="member_check" />
<input type="hidden" name="ses" value="$session" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff"><input name="_チーム正式名称" type="text" id="teamname" value="$paramhash_dec{'_チーム正式名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム正式名称（フリガナ）" type="text" id="team_kana" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム省略名称" type="text" id="team_abbr" value="$paramhash_dec{'_チーム省略名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム結成年" maxlength=4 type="text" id="team_year" value="$paramhash_dec{'_チーム結成年'}" size="4" style="ime-mode: disabled;" />
<font class="type3">年　<font class="type1" color="#ff0000">※半角数字のみ</font><br />
※西暦（例：2012）にてご入力下さい。
</font>

</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_主な活動曜日" type="text" id="katsudou_week" value="$paramhash_dec{'_主な活動曜日'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_平均年齢" type="text" id="average_age" value="$paramhash_dec{'_平均年齢'}" size="4" style="ime-mode: disabled;" />
才　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
都道府県 <select name="_都道府県名" id="pref">
<option value="" >選択して下さい
<option value="北海道" $PFLAG{'北海道'}>北海道
<option value="青森県" $PFLAG{'青森県'}>青森県
<option value="岩手県" $PFLAG{'岩手県'}>岩手県
<option value="宮城県" $PFLAG{'宮城県'}>宮城県
<option value="秋田県" $PFLAG{'秋田県'}>秋田県
<option value="山形県" $PFLAG{'山形県'}>山形県
<option value="福島県" $PFLAG{'福島県'}>福島県
<option value="茨城県" $PFLAG{'茨城県'}>茨城県
<option value="栃木県" $PFLAG{'栃木県'}>栃木県
<option value="群馬県" $PFLAG{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG{'千葉県'}>千葉県
<option value="東京都" $PFLAG{'東京都'}>東京都
<option value="神奈川県" $PFLAG{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG{'新潟県'}>新潟県
<option value="富山県" $PFLAG{'富山県'}>富山県
<option value="石川県" $PFLAG{'石川県'}>石川県
<option value="福井県" $PFLAG{'福井県'}>福井県
<option value="山梨県" $PFLAG{'山梨県'}>山梨県
<option value="長野県" $PFLAG{'長野県'}>長野県
<option value="岐阜県" $PFLAG{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG{'静岡県'}>静岡県
<option value="愛知県" $PFLAG{'愛知県'}>愛知県
<option value="三重県" $PFLAG{'三重県'}>三重県
<option value="滋賀県" $PFLAG{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG{'京都府'}>京都府
<option value="大阪府" $PFLAG{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG{'島根県'}>島根県
<option value="岡山県" $PFLAG{'岡山県'}>岡山県
<option value="広島県" $PFLAG{'広島県'}>広島県
<option value="山口県" $PFLAG{'山口県'}>山口県
<option value="徳島県" $PFLAG{'徳島県'}>徳島県
<option value="香川県" $PFLAG{'香川県'}>香川県
<option value="愛媛県" $PFLAG{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG{'高知県'}>高知県
<option value="福岡県" $PFLAG{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG{'長崎県'}>長崎県
<option value="熊本県" $PFLAG{'熊本県'}>熊本県
<option value="大分県" $PFLAG{'大分県'}>大分県
<option value="宮崎県" $PFLAG{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG{'沖縄県'}>沖縄県
</select> 
　市区町村
<input name="_主な活動場所" type="text" id="team_cities" value="$paramhash_dec{'_主な活動場所'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="過去戦績" cols="60" rows="5" id="past_perform">$paramhash_dec{'過去戦績'}</textarea>
<br />
過去に参加された大会の実績等を具体的にご記入ください。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="チームＰＲ" cols="60" rows="5" id="team_pr">$paramhash_dec{'チームＰＲ'}</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名" type="text" id="shimei1" value="$paramhash_dec{'_代表者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名（フリガナ）" type="text" id="shimei_kana1" value="$paramhash_dec{'_代表者氏名（フリガナ）'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font>
<br>
<font class="type1" color="#ff0000">（ログインID）</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_代表者メールアドレス" type="text" id="mailadr1" value="$paramhash_dec{'_代表者メールアドレス'}" size="20" style="ime-mode: disabled;" />
＠
<input name="_代表者メールアドレス（ドメイン）" type="text" id="mailadr2" value="$paramhash_dec{'_代表者メールアドレス（ドメイン）'}" size="20" style="ime-mode: disabled;" />
<br />
※ログインIDには、PCアドレスを推奨いたします。<br>
<font class="type1" color="#ff0000">※携帯アドレスで登録される方は本登録用のメールがブロックされ届かない場合がありますので、
その場合はお手数ですがＴＯＰページのお問い合わせから事務局までご連絡下さい。<br>
※迷惑メール防止のための受信設定をしている場合は、あらかじめ設定 を解除、あるいはドメイン指定設定（「pridejapan.net」を指定）などを行って下さい。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者電話番号" type="text" id="tel1" value="$paramhash_dec{'_代表者電話番号'}" size="20" style="ime-mode: disabled;" />　（例：0000-00-0000）　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
郵便番号<input name="_郵便番号" type="text" maxlength=8 id="zip" value="$paramhash_dec{'_郵便番号'}" size="10" />　
都道府県 <select name="_代表者都道府県名" id="pref2">
<option value="" >選択して下さい
<option value="北海道" $PFLAG2{'北海道'}>北海道
<option value="青森県" $PFLAG2{'青森県'}>青森県
<option value="岩手県" $PFLAG2{'岩手県'}>岩手県
<option value="宮城県" $PFLAG2{'宮城県'}>宮城県
<option value="秋田県" $PFLAG2{'秋田県'}>秋田県
<option value="山形県" $PFLAG2{'山形県'}>山形県
<option value="福島県" $PFLAG2{'福島県'}>福島県
<option value="茨城県" $PFLAG2{'茨城県'}>茨城県
<option value="栃木県" $PFLAG2{'栃木県'}>栃木県
<option value="群馬県" $PFLAG2{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG2{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG2{'千葉県'}>千葉県
<option value="東京都" $PFLAG2{'東京都'}>東京都
<option value="神奈川県" $PFLAG2{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG2{'新潟県'}>新潟県
<option value="富山県" $PFLAG2{'富山県'}>富山県
<option value="石川県" $PFLAG2{'石川県'}>石川県
<option value="福井県" $PFLAG2{'福井県'}>福井県
<option value="山梨県" $PFLAG2{'山梨県'}>山梨県
<option value="長野県" $PFLAG2{'長野県'}>長野県
<option value="岐阜県" $PFLAG2{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG2{'静岡県'}>静岡県
<option value="愛知県" $PFLAG2{'愛知県'}>愛知県
<option value="三重県" $PFLAG2{'三重県'}>三重県
<option value="滋賀県" $PFLAG2{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG2{'京都府'}>京都府
<option value="大阪府" $PFLAG2{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG2{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG2{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG2{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG2{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG2{'島根県'}>島根県
<option value="岡山県" $PFLAG2{'岡山県'}>岡山県
<option value="広島県" $PFLAG2{'広島県'}>広島県
<option value="山口県" $PFLAG2{'山口県'}>山口県
<option value="徳島県" $PFLAG2{'徳島県'}>徳島県
<option value="香川県" $PFLAG2{'香川県'}>香川県
<option value="愛媛県" $PFLAG2{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG2{'高知県'}>高知県
<option value="福岡県" $PFLAG2{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG2{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG2{'長崎県'}>長崎県
<option value="熊本県" $PFLAG2{'熊本県'}>熊本県
<option value="大分県" $PFLAG2{'大分県'}>大分県
<option value="宮崎県" $PFLAG2{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG2{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG2{'沖縄県'}>沖縄県
</select> 
<br>市区町村
<input name="_代表者住所" type="text" id="cities1" value="$paramhash_dec{'_代表者住所'}" size="60" /><br>
<font class="type1" color="#ff0000">※賞品をお送りすることがございます。マンション名、部屋番号まで正確にご記入ください。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名" type="text" id="shimei2" value="$paramhash_dec{'_第2担当者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名（フリガナ）" type="text" id="shimei_kana2" value="$paramhash_dec{'_第2担当者氏名（フリガナ）'}" size="20" />
<br />
　代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。 </td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者電話番号" type="text" id="tel3" value="$paramhash_dec{'_第2担当者電話番号'}" size="20" style="ime-mode: disabled;" />　（例：0000-00-0000）　<font class="type1" color="#ff0000">※半角数字のみ</font>
<br />
※代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_チームメールアドレス" type="text" id="mailaddress2" value="$paramhash_dec{'_チームメールアドレス'}" size="40" style="ime-mode: disabled;" />
<br />
　登録アドレスはPCに限ります。<br />
　（代表者のメールアドレスがPCの方は、代表者アドレスと同じで構いません）<br />
<font class="type1" color="#ff0000">※このアドレスは、登録をした全てのチームに表示されます。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff"><input name="チームHPアドレス" type="text" id="team_hp" value="$paramhash_dec{'チームHPアドレス'}" size="60" style="ime-mode: disabled;" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード" type="text" id="pwd" value="$paramhash_dec{'_パスワード'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード（確認用）</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード*" type="text" id="pwd2" value="$paramhash_dec{'_パスワード*'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input type="radio" name="_メールマガジン配信の選択" value="1" $MAILMAGAZINEFLAG{1} />
<font class="type3">希望する</font>　
<input type="radio" name="_メールマガジン配信の選択" value="0" $MAILMAGAZINEFLAG{0} />
<font class="type3">希望しない</font></td>
</tr>
</tbody>
</table>
<input type="submit" id="submit" value="　　確認画面へ　　" disabled />
</form>
<script>
//Javascriptが有効ならDisabledを外す
document.getElementById('submit').disabled = false;
</script>
</body>
</html>
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：確認
# -----------------------------------------------------------------
sub member_check {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
#	utf8::decode($p);
#	utf8::decode($v);
$p = Encode::decode('utf8',$p);
$v = Encode::decode('utf8',$v);
	$plist .= "$p:$v<br>\n";
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1 が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#メールアドレス重複チェック
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$pwd = $paramhash_dec{'_パスワード'};
if($mailaddress1 ne "" && $pwd ne ""){
$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailaddress1 = '$mailaddress1' and pwd = '$pwd' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
#&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$errormes .=<<"END_HTML";
・既に登録されているメールアドレスです。<br>
END_HTML
}	#if 
}	#if 


#エラーチェック
if($errormes ne ""){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body>
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="post" enctype="multipart/form-data" accept-charset="UTF-8">
<input type="hidden" name="code" value="member_new" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</body>
</html>
END_HTML
exit;
}	#if

###
print << "END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム省略名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム結成年'}
<font class="type3">年</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_主な活動曜日'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_平均年齢'}才</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_都道府県名'} $paramhash_dec{'_主な活動場所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'過去戦績'}&nbsp;
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームＰＲ'}&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">（ログインID）</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者メールアドレス'}＠$paramhash_dec{'_代表者メールアドレス（ドメイン）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_郵便番号'} 
$paramhash_dec{'_代表者都道府県名'} 
$paramhash_dec{'_代表者住所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チームメールアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームHPアドレス'}&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">*****</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<font class="type3">$MAILMAGAZINENAME{$paramhash_dec{'_メールマガジン配信の選択'}}</font>　
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_new" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_add" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>

</body>
</html>
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：登録
# -----------------------------------------------------------------
sub member_add {

$teamname = $paramhash_dec{'_チーム正式名称'};
$team_kana = $paramhash_dec{'_チーム正式名称（フリガナ）'};
$team_abbr = $paramhash_dec{'_チーム省略名称'};
$team_year = $paramhash_dec{'_チーム結成年'};
$katsudou_week = $paramhash_dec{'_主な活動曜日'};
$average_age = $paramhash_dec{'_平均年齢'};
$team_zip = $paramhash_dec{'_郵便番号'};
$team_pref = $paramhash_dec{'_都道府県名'};
$team_cities = $paramhash_dec{'_主な活動場所'};
$past_perform = $paramhash_dec{'過去戦績'};
$team_pr = $paramhash_dec{'チームＰＲ'};
$shimei1 = $paramhash_dec{'_代表者氏名'};
$shimei_kana1 = $paramhash_dec{'_代表者氏名（フリガナ）'};
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$tel1 = $paramhash_dec{'_代表者電話番号'};
$prefectural1 = $paramhash_dec{'_代表者都道府県名'};
$cities1 = $paramhash_dec{'_代表者住所'};
$shimei2 = $paramhash_dec{'_第2担当者氏名'};
$shimei_kana2 = $paramhash_dec{'_第2担当者氏名（フリガナ）'};
$tel2 = $paramhash_dec{'_第2担当者電話番号'};
$mailaddress2 = $paramhash_dec{'_チームメールアドレス'};
$team_hp = $paramhash_dec{'チームHPアドレス'};
$pwd = $paramhash_dec{'_パスワード'};
$mailmagazine = $paramhash_dec{'_メールマガジン配信の選択'};
$ses = $paramhash_dec{'ses'};

#セッションによる重複登録チェック
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<p style="color:red;font-weight:bold;font-size:20px;">重複登録がされました。</p>
<p>画面をリロードしないようご注意ください。</p>
</body>
</html>
END_HTML
exit;
}	#if 重複


# 新規登録
$sql_str = qq{INSERT INTO $member_tbl(ssid,contents,koukaiflag,mailadr1,mailadr2,pwd,shimei1,shimei_kana1,mailaddress1,tel1,prefectural1,cities1,shimei2,shimei_kana2,tel2,mailaddress2,teamname,team_kana,team_abbr,team_year,team_hp,katsudou_week,average_age,team_zip,team_pref,team_cities,past_perform,team_pr,mailmagazine) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$ses,
21,
2,
$mailadr1,
$mailadr2,
$pwd,
$shimei1,
$shimei_kana1,
$mailaddress1,
$tel1,
$prefectural1,
$cities1,
$shimei2,
$shimei_kana2,
$tel2,
$mailaddress2,
$teamname,
$team_kana,
$team_abbr,
$team_year,
$team_hp,
$katsudou_week,
$average_age,
$team_zip,
$team_pref,
$team_cities,
$past_perform,
$team_pr,
$mailmagazine,
);
&sqlcheck($sql_str);
###
$subject = Unicode::Japanese->new("チーム情報 確認メール",'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@$domain
To:$mailaddress1
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
PRIDE JAPANにご登録いただきありがとうございます。

以下のURLをクリックして登録手続きを完了してください。
$sitefulladr/systemmessage.html?code=member_ok&ses=$ses

また以下の情報はログインする際に必要となりますので大切に保管して下さい。
登録ID（メールアドレス）：$mailaddress1
パスワードについてはメールに記載しておりません。
各自でお控えください。

END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<p style="color:red;font-weight:bold;font-size:20px;">現在はまだ「仮登録」です。</p>
<p>フォームに登録されたメールアドレスに、info\@pridejapan.netよりメールを送信しました。</p>
<p>パソコン等の迷惑メールフォルダに入ってしまわないよう設定を変更してください。</p>
<p>メール内に記載された注意事項に従って本登録をお願いします。</p>
</body>
</html>
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：確認OK
# -----------------------------------------------------------------
sub member_ok {
$ses = $paramhash{'ses'};
#重複チェック
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<p align="center" style="color:red;">チーム情報エラー</p>
<p align="center">お手数をおかけしますが事務局までご連絡ください。</p>
END_HTML
}else{
$REFHASH = $rs->fetchrow_hashref;
$koukaiflag = &paramsetsql('koukaiflag');
if($koukaiflag == 0){
$mes =<<"END_HTML";
<p align="center" style="color:red;">既に本登録が完了しております。</p>
<p align="center">本サイトをご活用ください。</p>
END_HTML
}elsif($koukaiflag == 2){
#本登録
$sql_str = "UPDATE $member_tbl SET koukaiflag = 0 ,createdate = '$nowdate' WHERE ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$mes =<<"END_HTML";
<p align="center" style="color:red;" >本登録が完了しました。</p>
<p align="center"><a href="$sitefulladr">トップページ</a>よりログインし、本サイトをご活用ください。</p>
END_HTML
}	#if
}	#if count
###
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub




# -----------------------------------------------------------------
# チーム：新規登録
# -----------------------------------------------------------------
sub member_new_test {
#セッション作成
$session = sprintf("%02d%02d%02d",$sec,$min,$hour);
for (1..15) { $session .= ((0..9,a..z,A..Z)[int rand 62])};
$session .= sprintf("%02d%02d%02d",$mday,$month,$year-2000);

#
if($paramhash_dec{'_都道府県名'} ne ""){$PFLAG{$paramhash_dec{'_都道府県名'}} = "selected";}
if($paramhash_dec{'_代表者都道府県名'} ne ""){$PFLAG2{$paramhash_dec{'_代表者都道府県名'}} = "selected";}
if($paramhash_dec{'_メールマガジン配信の選択'} ne ""){
$MAILMAGAZINEFLAG{$paramhash_dec{'_メールマガジン配信の選択'}}="checked=checked";
}else{
$MAILMAGAZINEFLAG{1}="checked=checked";
}	#if
###
print << "END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
<script>
function kakunin(){

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_kana').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('team_abbr').value == "") {
alert('「チーム省略名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_year').value == "") {
alert('「チーム結成年」が入力されていません。');
return(false);
}
var str = document.getElementById("team_year").value;
if( str.match(/[^0-9]/) ){
alert("「チーム結成年」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('team_year').value < 1800) {
alert('「チーム結成年」にエラーがあります。');
return(false);
}


if (document.getElementById('katsudou_week').value == "") {
alert('「主な活動曜日」が入力されていません。');
return(false);
}

if (document.getElementById('average_age').value == "") {
alert('「平均年齢」が入力されていません。');
return(false);
}
var str = document.getElementById("average_age").value;
if( str.match(/[^0-9]/) ){
alert("「平均年齢」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('average_age').value < 5) {
alert('「平均年齢」にエラーがあります。');
return(false);
}


if (document.getElementById('pref').selectedIndex == 0) {
alert('「主な活動場所（都道府県）」が選択されていません。');
return(false);
}

if (document.getElementById('team_cities').value == "") {
alert('「主な活動場所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei1').value == "") {
alert('「代表者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana1').value == "") {
alert('「代表者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('mailadr1').value == "") {
alert('「代表者メールアドレス」が入力されていません。');
return(false);
}
var str = document.getElementById("mailadr1").value;
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス」が不正です。");
return false;
}	//if

if (document.getElementById('mailadr2').value == "") {
alert('「代表者メールアドレス（ドメイン）」が入力されていません。');
return(false);
}
var str = document.getElementById("mailadr2").value;
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス」が不正です。");
return false;
}	//if

if (document.getElementById('tel1').value == "") {
alert('「代表者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel1").value;
if( str.match(/[^0-9-]/) ){
alert("代表者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('zip').value == "") {
alert('「代表者住所（郵便番号）」が入力されていません。');
return(false);
}

if (document.getElementById('pref2').value == "") {
alert('「代表者住所（都道府県）」が入力されていません。');
return(false);
}

if (document.getElementById('cities1').value == "") {
alert('「代表者住所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei2').value == "") {
alert('「第2担当者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana2').value == "") {
alert('「第2担当者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('tel3').value == "") {
alert('「第2担当者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel3").value;
if( str.match(/[^0-9-]/) ){
alert("第2担当者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('mailaddress2').value == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}

if (document.getElementById('pwd').value == "") {
alert('「パスワード」が入力されていません。');
return(false);
}
if (document.getElementById('pwd').value.length < 4) {
alert('「パスワード」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd2').value == "") {
alert('「パスワード（確認用）」が入力されていません。');
return(false);
}
if (document.getElementById('pwd2').value.length < 4) {
alert('「パスワード（確認用）」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd2").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード（確認用）」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd').value != document.getElementById('pwd2').value) {
alert('パスワードが一致していません。');
return(false);
}

return true;
}	//func

</script>
</head>
<body>
<noscript>
<p style="color:red;font-size:16px;">（！）Javascriptを有効にしてください。</p>
</noscript>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_check_test" />
<input type="hidden" name="ses" value="$session" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff"><input name="_チーム正式名称" type="text" id="teamname" value="$paramhash_dec{'_チーム正式名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム正式名称（フリガナ）" type="text" id="team_kana" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム省略名称" type="text" id="team_abbr" value="$paramhash_dec{'_チーム省略名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム結成年" maxlength=4 type="text" id="team_year" value="$paramhash_dec{'_チーム結成年'}" size="4" style="ime-mode: disabled;" />
<font class="type3">年　<font class="type1" color="#ff0000">※半角数字のみ</font><br />
※西暦（例：2012）にてご入力下さい。
</font>

</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_主な活動曜日" type="text" id="katsudou_week" value="$paramhash_dec{'_主な活動曜日'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_平均年齢" type="text" id="average_age" value="$paramhash_dec{'_平均年齢'}" size="4" style="ime-mode: disabled;" />
才　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
都道府県 <select name="_都道府県名" id="pref">
<option value="" >選択して下さい
<option value="北海道" $PFLAG{'北海道'}>北海道
<option value="青森県" $PFLAG{'青森県'}>青森県
<option value="岩手県" $PFLAG{'岩手県'}>岩手県
<option value="宮城県" $PFLAG{'宮城県'}>宮城県
<option value="秋田県" $PFLAG{'秋田県'}>秋田県
<option value="山形県" $PFLAG{'山形県'}>山形県
<option value="福島県" $PFLAG{'福島県'}>福島県
<option value="茨城県" $PFLAG{'茨城県'}>茨城県
<option value="栃木県" $PFLAG{'栃木県'}>栃木県
<option value="群馬県" $PFLAG{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG{'千葉県'}>千葉県
<option value="東京都" $PFLAG{'東京都'}>東京都
<option value="神奈川県" $PFLAG{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG{'新潟県'}>新潟県
<option value="富山県" $PFLAG{'富山県'}>富山県
<option value="石川県" $PFLAG{'石川県'}>石川県
<option value="福井県" $PFLAG{'福井県'}>福井県
<option value="山梨県" $PFLAG{'山梨県'}>山梨県
<option value="長野県" $PFLAG{'長野県'}>長野県
<option value="岐阜県" $PFLAG{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG{'静岡県'}>静岡県
<option value="愛知県" $PFLAG{'愛知県'}>愛知県
<option value="三重県" $PFLAG{'三重県'}>三重県
<option value="滋賀県" $PFLAG{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG{'京都府'}>京都府
<option value="大阪府" $PFLAG{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG{'島根県'}>島根県
<option value="岡山県" $PFLAG{'岡山県'}>岡山県
<option value="広島県" $PFLAG{'広島県'}>広島県
<option value="山口県" $PFLAG{'山口県'}>山口県
<option value="徳島県" $PFLAG{'徳島県'}>徳島県
<option value="香川県" $PFLAG{'香川県'}>香川県
<option value="愛媛県" $PFLAG{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG{'高知県'}>高知県
<option value="福岡県" $PFLAG{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG{'長崎県'}>長崎県
<option value="熊本県" $PFLAG{'熊本県'}>熊本県
<option value="大分県" $PFLAG{'大分県'}>大分県
<option value="宮崎県" $PFLAG{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG{'沖縄県'}>沖縄県
</select> 
　市区町村
<input name="_主な活動場所" type="text" id="team_cities" value="$paramhash_dec{'_主な活動場所'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="過去戦績" cols="60" rows="5" id="past_perform">$paramhash_dec{'過去戦績'}</textarea>
<br />
過去に参加された大会の実績等を具体的にご記入ください。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="チームＰＲ" cols="60" rows="5" id="team_pr">$paramhash_dec{'チームＰＲ'}</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名" type="text" id="shimei1" value="$paramhash_dec{'_代表者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名（フリガナ）" type="text" id="shimei_kana1" value="$paramhash_dec{'_代表者氏名（フリガナ）'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font>
<br>
<font class="type1" color="#ff0000">（ログインID）</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_代表者メールアドレス" type="text" id="mailadr1" value="$paramhash_dec{'_代表者メールアドレス'}" size="20" style="ime-mode: disabled;" />
＠
<input name="_代表者メールアドレス（ドメイン）" type="text" id="mailadr2" value="$paramhash_dec{'_代表者メールアドレス（ドメイン）'}" size="20" style="ime-mode: disabled;" />
<br />
※PC、携帯どちらのアドレスでも構いません。<br>
<font class="type1" color="#ff0000">※迷惑メール防止のための受信設定をしている場合は、あらかじめ設定 を解除、あるいはドメイン指定設定（「pridejapan.net」を指定）などを行って下さい。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者電話番号" type="text" id="tel1" value="$paramhash_dec{'_代表者電話番号'}" size="20" style="ime-mode: disabled;" />　（例：0000-00-0000）　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
郵便番号<input name="_郵便番号" type="text" maxlength=8 id="zip" value="$paramhash_dec{'_郵便番号'}" size="10" />　
都道府県 <select name="_代表者都道府県名" id="pref2">
<option value="" >選択して下さい
<option value="北海道" $PFLAG2{'北海道'}>北海道
<option value="青森県" $PFLAG2{'青森県'}>青森県
<option value="岩手県" $PFLAG2{'岩手県'}>岩手県
<option value="宮城県" $PFLAG2{'宮城県'}>宮城県
<option value="秋田県" $PFLAG2{'秋田県'}>秋田県
<option value="山形県" $PFLAG2{'山形県'}>山形県
<option value="福島県" $PFLAG2{'福島県'}>福島県
<option value="茨城県" $PFLAG2{'茨城県'}>茨城県
<option value="栃木県" $PFLAG2{'栃木県'}>栃木県
<option value="群馬県" $PFLAG2{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG2{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG2{'千葉県'}>千葉県
<option value="東京都" $PFLAG2{'東京都'}>東京都
<option value="神奈川県" $PFLAG2{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG2{'新潟県'}>新潟県
<option value="富山県" $PFLAG2{'富山県'}>富山県
<option value="石川県" $PFLAG2{'石川県'}>石川県
<option value="福井県" $PFLAG2{'福井県'}>福井県
<option value="山梨県" $PFLAG2{'山梨県'}>山梨県
<option value="長野県" $PFLAG2{'長野県'}>長野県
<option value="岐阜県" $PFLAG2{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG2{'静岡県'}>静岡県
<option value="愛知県" $PFLAG2{'愛知県'}>愛知県
<option value="三重県" $PFLAG2{'三重県'}>三重県
<option value="滋賀県" $PFLAG2{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG2{'京都府'}>京都府
<option value="大阪府" $PFLAG2{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG2{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG2{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG2{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG2{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG2{'島根県'}>島根県
<option value="岡山県" $PFLAG2{'岡山県'}>岡山県
<option value="広島県" $PFLAG2{'広島県'}>広島県
<option value="山口県" $PFLAG2{'山口県'}>山口県
<option value="徳島県" $PFLAG2{'徳島県'}>徳島県
<option value="香川県" $PFLAG2{'香川県'}>香川県
<option value="愛媛県" $PFLAG2{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG2{'高知県'}>高知県
<option value="福岡県" $PFLAG2{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG2{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG2{'長崎県'}>長崎県
<option value="熊本県" $PFLAG2{'熊本県'}>熊本県
<option value="大分県" $PFLAG2{'大分県'}>大分県
<option value="宮崎県" $PFLAG2{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG2{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG2{'沖縄県'}>沖縄県
</select> 
<br>市区町村
<input name="_代表者住所" type="text" id="cities1" value="$paramhash_dec{'_代表者住所'}" size="60" /><br>
<font class="type1" color="#ff0000">※賞品をお送りすることがございます。マンション名、部屋番号まで正確にご記入ください。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名" type="text" id="shimei2" value="$paramhash_dec{'_第2担当者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名（フリガナ）" type="text" id="shimei_kana2" value="$paramhash_dec{'_第2担当者氏名（フリガナ）'}" size="20" />
<br />
　代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。 </td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者電話番号" type="text" id="tel3" value="$paramhash_dec{'_第2担当者電話番号'}" size="20" style="ime-mode: disabled;" />　<font class="type1" color="#ff0000">※半角数字のみ</font>
<br />
※代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_チームメールアドレス" type="text" id="mailaddress2" value="$paramhash_dec{'_チームメールアドレス'}" size="40" style="ime-mode: disabled;" />
<br />
　登録アドレスはPCに限ります。<br />
　（代表者のメールアドレスがPCの方は、代表者アドレスと同じで構いません）<br />
<font class="type1" color="#ff0000">※このアドレスは、登録をした全てのチームに表示されます。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff"><input name="チームHPアドレス" type="text" id="team_hp" value="$paramhash_dec{'チームHPアドレス'}" size="60" style="ime-mode: disabled;" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード" type="text" id="pwd" value="$paramhash_dec{'_パスワード'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード（確認用）</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード*" type="text" id="pwd2" value="$paramhash_dec{'_パスワード*'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input type="radio" name="_メールマガジン配信の選択" value="1" $MAILMAGAZINEFLAG{1} />
<font class="type3">希望する</font>　
<input type="radio" name="_メールマガジン配信の選択" value="0" $MAILMAGAZINEFLAG{0} />
<font class="type3">希望しない</font></td>
</tr>
</tbody>
</table>
<input type="submit" id="submit" value="　　確認画面へ　　" disabled />
</form>
<script>
//Javascriptが有効ならDisabledを外す
document.getElementById('submit').disabled = false;
</script>
</body>
</html>
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：確認
# -----------------------------------------------------------------
sub member_check_test {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
#	utf8::decode($p);
#	utf8::decode($v);
$p = Encode::decode('utf8',$p);
$v = Encode::decode('utf8',$v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#メールアドレス重複チェック
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$pwd = $paramhash_dec{'_パスワード'};
if($mailaddress1 ne "" && $pwd ne ""){
$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailaddress1 = '$mailaddress1' and pwd = '$pwd' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
#&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$errormes .=<<"END_HTML";
・既に登録されているメールアドレスです。<br>
END_HTML
}	#if 
}	#if 


#エラーチェック
if($errormes ne ""){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body>
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="post" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="member_new_test" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</body>
</html>
END_HTML
exit;
}	#if

###
print << "END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム省略名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム結成年'}
<font class="type3">年</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_主な活動曜日'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_平均年齢'}才</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_都道府県名'} $paramhash_dec{'_主な活動場所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'過去戦績'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームＰＲ'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">（ログインID）</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者メールアドレス'}＠$paramhash_dec{'_代表者メールアドレス（ドメイン）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_郵便番号'} 
$paramhash_dec{'_代表者都道府県名'} 
$paramhash_dec{'_代表者住所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チームメールアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームHPアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">*****</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<font class="type3">$MAILMAGAZINENAME{$paramhash_dec{'_メールマガジン配信の選択'}}</font>　
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_new_test" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_add_test" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>

</body>
</html>
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：登録
# -----------------------------------------------------------------
sub member_add_test {

$teamname = $paramhash_dec{'_チーム正式名称'};
$team_kana = $paramhash_dec{'_チーム正式名称（フリガナ）'};
$team_abbr = $paramhash_dec{'_チーム省略名称'};
$team_year = $paramhash_dec{'_チーム結成年'};
$katsudou_week = $paramhash_dec{'_主な活動曜日'};
$average_age = $paramhash_dec{'_平均年齢'};
$team_zip = $paramhash_dec{'_郵便番号'};
$team_pref = $paramhash_dec{'_都道府県名'};
$team_cities = $paramhash_dec{'_主な活動場所'};
$past_perform = $paramhash_dec{'過去戦績'};
$team_pr = $paramhash_dec{'チームＰＲ'};
$shimei1 = $paramhash_dec{'_代表者氏名'};
$shimei_kana1 = $paramhash_dec{'_代表者氏名（フリガナ）'};
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$tel1 = $paramhash_dec{'_代表者電話番号'};
$prefectural1 = $paramhash_dec{'_代表者都道府県名'};
$cities1 = $paramhash_dec{'_代表者住所'};
$shimei2 = $paramhash_dec{'_第2担当者氏名'};
$shimei_kana2 = $paramhash_dec{'_第2担当者氏名（フリガナ）'};
$tel2 = $paramhash_dec{'_第2担当者電話番号'};
$mailaddress2 = $paramhash_dec{'_チームメールアドレス'};
$team_hp = $paramhash_dec{'チームHPアドレス'};
$pwd = $paramhash_dec{'_パスワード'};
$mailmagazine = $paramhash_dec{'_メールマガジン配信の選択'};
$ses = $paramhash_dec{'ses'};

#セッションによる重複登録チェック
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<p style="color:red;font-weight:bold;font-size:20px;">重複登録がされました。</p>
<p>画面をリロードしないようご注意ください。</p>
</body>
</html>
END_HTML
exit;
}	#if 重複


# 新規登録
$sql_str = qq{INSERT INTO $member_tbl(ssid,contents,koukaiflag,mailadr1,mailadr2,pwd,shimei1,shimei_kana1,mailaddress1,tel1,prefectural1,cities1,shimei2,shimei_kana2,tel2,mailaddress2,teamname,team_kana,team_abbr,team_year,team_hp,katsudou_week,average_age,team_zip,team_pref,team_cities,past_perform,team_pr,mailmagazine) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$ses,
21,
2,
$mailadr1,
$mailadr2,
$pwd,
$shimei1,
$shimei_kana1,
$mailaddress1,
$tel1,
$prefectural1,
$cities1,
$shimei2,
$shimei_kana2,
$tel2,
$mailaddress2,
$teamname,
$team_kana,
$team_abbr,
$team_year,
$team_hp,
$katsudou_week,
$average_age,
$team_zip,
$team_pref,
$team_cities,
$past_perform,
$team_pr,
$mailmagazine,
);
&sqlcheck($sql_str);
###
$subject = Unicode::Japanese->new("チーム情報 確認メール",'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@$domain
To:$mailaddress1
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
PRIDE JAPANにご登録いただきありがとうございます。

以下のURLをクリックして登録手続きを完了してください。
$sitefulladr/systemmessage.html?code=member_ok&ses=$ses

また以下の情報はログインする際に必要となりますので大切に保管して下さい。
登録ID（メールアドレス）：$mailaddress1
パスワードについてはメールに記載しておりません。
各自でお控えください。

END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>
<body>
<p style="color:red;font-weight:bold;font-size:20px;">現在はまだ「仮登録」です。</p>
<p>フォームに登録されたメールアドレスに、info\@pridejapan.netよりメールを送信しました。</p>
<p>パソコン等の迷惑メールフォルダに入ってしまわないよう設定を変更してください。</p>
<p>メール内に記載された注意事項に従って本登録をお願いします。</p>
</body>
</html>
END_HTML
exit;
}	#sub



# -----------------------------------------------------------------
# 大会用表示
# -----------------------------------------------------------------
sub taikaihtmldisp {
my ($data,$flag)=(@_);
if($flag ne ""){print "Content-type: text/html;\n\n";}
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"taikaitemplate.html" or die "taikaitemplate open error";
my @TEMPLATE = <IN>;
close IN;
#
utf8::decode($data);
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%data\%/$data/;
$str .= $line;
}	#foreach
print $str;
exit;
}	#sub




# -----------------------------------------------------------------
# マイページ：ログイン
# -----------------------------------------------------------------
sub mypagelogin {
&setcook2("systemerrormes","");
&setcook2($cookiename,"");

$email = $paramhash{'email'};
$psw = $paramhash{'psw'};
#ログインチェック
$sql_str = "SELECT * FROM $member_tbl WHERE mailaddress1 = '$email' and pwd = '$psw' and contents = 21 and koukaiflag = 0 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
&setcook2($cookiename,"");
&setcook2("systemerrormes","ログイン出来ません。");
}else{
#クッキー保存
$REFHASH = $rs->fetchrow_hashref;
$ses = &paramsetsql('ssid');
&setcook2($cookiename,$ses);
&setcook2("systemerrormes","");
}	#if

$q = "code=mypage";
utf8::encode($q);
$q =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$q =~ tr/ /+/;
utf8::decode($q);
###
print "Location:$sitefulladr/system.cgi\n\n";

=pot
print "Content-type: text/html;\n\n";
print <<"END_HTML";
<html>
<head>
<meta http-equiv="refresh" content="0;URL=$sitefulladr/system.cgi">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>ログイン情報確認中</title>
</head>
<body>
<center>
<p>ログイン情報確認中...</p>
<br>
<p><a href="$sitefulladr/system.cgi" style="font-size:12px;color:#aaaaaa;">ページが自動的に移動しない場合は、お手数ですがここをクリックしてください。</a></p>
</center>

</body>
</html>
END_HTML
=cut
exit;
}	#sub


# -----------------------------------------------------------------
# マイページ：TOP
# -----------------------------------------------------------------
sub mypage {
#エラーの確認
$systemerrormes = &getcook2("systemerrormes");
if($systemerrormes ne ""){
&mypagehtmldisp($systemerrormes);
exit;
}	#if
#ログインの確認
if($loginuser eq ""){
&mypagehtmldisp("ログインしておりません。");
exit;
}	#if
#ログインの確認2
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$loginuser' and contents = 21 and koukaiflag = 0 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
&mypagehtmldisp("もう一度ログインをお願いします。");
}	#if

### メインメニュー
#チーム情報のGET
$REFHASH = $rs->fetchrow_hashref;
$teamname = &paramsetsql('teamname');


###
$mes =<<"END_HTML";
<h2 id="team" style="background-image:url(img/ter8.jpg)"><span>$teamname</span></h2>
<div id="mypage"><a href="?code=mypage_team"><img src="img/team.jpg" width="206" height="32" style="margin-right:8px;" /></a><a href="?code=member_edit"><img src="img/entry2.jpg" width="206" height="32" /></a></div>
<table width="100%" cellspacing="0" class="stane">
<tr>
<th colspan="2" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">マイページメニュー</th>
</tr>
<tr>
<th width="50%" align="center" scope="row"><span class="tebo"><a href="?code=gameschedule"><img src="img/ter1.jpg" width="398" height="48" /></a></span></th>
<th width="50%" align="center" scope="row"><span class="tebo"><a href="?code=gameentry"><img src="img/ter4.jpg" width="398" height="48" /></a></span></th>
</tr>
<tr>
<th align="center" scope="row"><span class="tebo"><a href="?code=gameresult"><img src="img/ter2.jpg" width="398" height="48" /></a></span></th>
<th align="center" scope="row"><span class="tebo"><a href="https://pridejapan-net.ssl-xserver.jp/system.cgi?code=membercontact_form_noframe&ses=$loginuser"><img src="img/ter3.jpg" width="398" height="48" /></a></span></th>
</tr>
</table>
<hr class="clear" />
END_HTML
&mypagehtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# チーム：編集
# -----------------------------------------------------------------
sub member_edit {
#ログインの確認2
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$loginuser' and contents = 21 and koukaiflag = 0 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
&mypagehtmldisp("ログイン出来ません。");
}	#if
foreach $n(0..29){
$TMNAME[$n] = $paramhash_dec{"teammember_name$n"};
$TMNUM[$n] = $paramhash_dec{"teammember_num$n"};
$TMPOSITION[$n] = $paramhash_dec{"teammember_position$n"};
}	#foreach

#リライト？
if($paramhash{'rewrite'} != 1){
#チーム情報のGET
$REFHASH = $rs->fetchrow_hashref;
$paramhash_dec{'_代表者氏名'} = &paramsetsql('shimei1');
$paramhash_dec{'_代表者氏名（フリガナ）'} = &paramsetsql('shimei_kana1');
($temp1,$temp2) = split(/\@/,&paramsetsql('mailaddress1'));
$paramhash_dec{'_代表者メールアドレス'} = $temp1;
$paramhash_dec{'_代表者メールアドレス（ドメイン）'} = $temp2;
$paramhash_dec{'_代表者電話番号'} = &paramsetsql('tel1');
$paramhash_dec{'_代表者都道府県名'} = &paramsetsql('prefectural1');
$paramhash_dec{'_代表者住所'} = &paramsetsql('cities1');
$paramhash_dec{'_第2担当者氏名'} = &paramsetsql('shimei2');
$paramhash_dec{'_第2担当者氏名（フリガナ）'} = &paramsetsql('shimei_kana2');
$paramhash_dec{'_第2担当者電話番号'} = &paramsetsql('tel2');
$paramhash_dec{'_チームメールアドレス'} = &paramsetsql('mailaddress2');
$paramhash_dec{'_チーム正式名称'} = &paramsetsql('teamname');
$paramhash_dec{'_チーム正式名称（フリガナ）'} = &paramsetsql('team_kana');
$paramhash_dec{'_チーム省略名称'} = &paramsetsql('team_abbr');
$paramhash_dec{'_チーム結成年'} = &paramsetsql('team_year');
$paramhash_dec{'チームHPアドレス'} = &paramsetsql('team_hp');
$paramhash_dec{'_主な活動曜日'} = &paramsetsql('katsudou_week');
$paramhash_dec{'_平均年齢'} = &paramsetsql('average_age');
$paramhash_dec{'_郵便番号'} = &paramsetsql('team_zip');
$paramhash_dec{'_都道府県名'} = &paramsetsql('team_pref');
$paramhash_dec{'_主な活動場所'} = &paramsetsql('team_cities');
$paramhash_dec{'過去戦績'} = &paramsetsql('past_perform');
$paramhash_dec{'チームＰＲ'} = &paramsetsql('team_pr');
$paramhash_dec{'_パスワード'} = &paramsetsql('pwd');
$paramhash_dec{'_パスワード*'} = &paramsetsql('pwd');
$paramhash_dec{'_メールマガジン配信の選択'} = &paramsetsql('mailmagazine');
$paramhash_dec{'LINEID'} = &paramsetsql('lineid');
$n = 0;
foreach $line(split(/<>/,&paramsetsql('teammember'))){
($TMNAME[$n],$TMNUM[$n],$TMPOSITION[$n]) = split(/:/,$line);
$n++;
}	#foreach
#画像
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
foreach $i(0..2){
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=system/file/$TEMP[0]pda.jpg>$sfn<br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
}else{
$filename0 = $paramhash_dec{"filename0"};
#画像
@IMGTEMPS = split(/:/,$filename0);
foreach $i(0..2){
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=system/file/$TEMP[0]pda.jpg>$sfn<br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
}	#if rewrite
#
$teammemberlist .=<<"END_HTML";
<table style="border:none;">
<tbody>
<tr>
<td align=center bgcolor="#aaaaaa">No.</td>
<td align=center bgcolor="#aaaaaa">名前</td>
<td align=center bgcolor="#aaaaaa">背番号</td>
<td align=center bgcolor="#aaaaaa">ポジション</td>
</tr>
END_HTML
foreach $n1(0..9){
$n2 = $n1 + 1;
$teammemberlist .=<<"END_HTML";
<tr>
<td align=center>$n2</td>
<td align=center><input type=text name='teammember_name$n1' value='$TMNAME[$n1]' /></td>
<td align=center><input type=text name='teammember_num$n1' value='$TMNUM[$n1]' /></td>
<td align=center><input type=text name='teammember_position$n1' value='$TMPOSITION[$n1]' /></td>
</tr>
END_HTML
}	#foreach
$teammemberlist .=<<"END_HTML";
</tbody>
</table>
END_HTML

$teammemberlist .=<<"END_HTML";
<span style="text-decolation:;color:blue;" onclick="tagopen(2)">さらに表示≫</span>
<div style="display:none;" id="tag2">
<span style="text-decolation:;color:blue;" onclick="tagclose(2)">≪隠す</span>
<table style="border:none;">
<tbody>
<tr>
<td align=center bgcolor="#aaaaaa">No.</td>
<td align=center bgcolor="#aaaaaa">名前</td>
<td align=center bgcolor="#aaaaaa">背番号</td>
<td align=center bgcolor="#aaaaaa">ポジション</td>
</tr>
END_HTML
foreach $n1(10..19){
$n2 = $n1 + 1;
$teammemberlist .=<<"END_HTML";
<tr>
<td>$n2</td>
<td><input type=text name='teammember_name$n1' value='$TMNAME[$n1]' /></td>
<td><input type=text name='teammember_num$n1' value='$TMNUM[$n1]' /></td>
<td><input type=text name='teammember_position$n1' value='$TMPOSITION[$n1]' /></td>
</tr>
END_HTML
}	#foreach
$teammemberlist .=<<"END_HTML";
</tbody>
</table>
<span style="text-decolation:;color:blue;" onclick="tagopen(3)">さらに表示≫</span>
</div>
END_HTML

$teammemberlist .=<<"END_HTML";
<div style="display:none;" id="tag3">
<span style="text-decolation:;color:blue;" onclick="tagclose(3)">≪隠す</span>
<table style="border:none;">
<tbody>
<tr>
<td align=center bgcolor="#aaaaaa">No.</td>
<td align=center bgcolor="#aaaaaa">名前</td>
<td align=center bgcolor="#aaaaaa">背番号</td>
<td align=center bgcolor="#aaaaaa">ポジション</td>
</tr>
END_HTML
foreach $n1(20..29){
$n2 = $n1 + 1;
$teammemberlist .=<<"END_HTML";
<tr>
<td>$n2</td>
<td><input type=text name='teammember_name$n1' value='$TMNAME[$n1]' /></td>
<td><input type=text name='teammember_num$n1' value='$TMNUM[$n1]' /></td>
<td><input type=text name='teammember_position$n1' value='$TMPOSITION[$n1]' /></td>
</tr>
END_HTML
}	#foreach
$teammemberlist .=<<"END_HTML";
</tbody>
</table>
</div>
END_HTML


if($paramhash_dec{'_都道府県名'} ne ""){$PFLAG{$paramhash_dec{'_都道府県名'}} = "selected";}
if($paramhash_dec{'_代表者都道府県名'} ne ""){$PFLAG2{$paramhash_dec{'_代表者都道府県名'}} = "selected";}
if($paramhash_dec{'_メールマガジン配信の選択'} ne ""){
$MAILMAGAZINEFLAG{$paramhash_dec{'_メールマガジン配信の選択'}}="checked=checked";
}else{
$MAILMAGAZINEFLAG{1}="checked=checked";
}	#if
###
$mes =<< "END_HTML";
<h2 class="subti" id="1">チーム情報の編集</h2>
<script>
function kakunin(){

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_kana').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('team_abbr').value == "") {
alert('「チーム省略名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_year').value == "") {
alert('「チーム結成年」が入力されていません。');
return(false);
}
var str = document.getElementById("team_year").value;
if( str.match(/[^0-9]/) ){
alert("「チーム結成年」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('team_year').value < 1800) {
alert('「チーム結成年」にエラーがあります。');
return(false);
}


if (document.getElementById('katsudou_week').value == "") {
alert('「主な活動曜日」が入力されていません。');
return(false);
}

if (document.getElementById('average_age').value == "") {
alert('「平均年齢」が入力されていません。');
return(false);
}
var str = document.getElementById("average_age").value;
if( str.match(/[^0-9]/) ){
alert("「平均年齢」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('average_age').value < 5) {
alert('「平均年齢」にエラーがあります。');
return(false);
}


if (document.getElementById('pref').selectedIndex == 0) {
alert('「主な活動場所（都道府県）」が選択されていません。');
return(false);
}

if (document.getElementById('team_cities').value == "") {
alert('「主な活動場所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei1').value == "") {
alert('「代表者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana1').value == "") {
alert('「代表者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('mailadr1').value == "") {
alert('「代表者メールアドレス」が入力されていません。');
return(false);
}

if (document.getElementById('mailadr2').value == "") {
alert('「代表者メールアドレス（ドメイン）」が入力されていません。');
return(false);
}

if (document.getElementById('tel1').value == "") {
alert('「代表者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel1").value;
if( str.match(/[^0-9-]/) ){
alert("代表者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('zip').value == "") {
alert('「代表者住所（郵便番号）」が入力されていません。');
return(false);
}

if (document.getElementById('pref2').value == "") {
alert('「代表者住所（都道府県）」が入力されていません。');
return(false);
}

if (document.getElementById('cities1').value == "") {
alert('「代表者住所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei2').value == "") {
alert('「第2担当者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana2').value == "") {
alert('「第2担当者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('tel3').value == "") {
alert('「第2担当者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel3").value;
if( str.match(/[^0-9-]/) ){
alert("第2担当者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('mailaddress2').value == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}

if (document.getElementById('pwd').value == "") {
alert('「パスワード」が入力されていません。');
return(false);
}
if (document.getElementById('pwd').value.length < 4) {
alert('「パスワード」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd2').value == "") {
alert('「パスワード（確認用）」が入力されていません。');
return(false);
}
if (document.getElementById('pwd2').value.length < 4) {
alert('「パスワード（確認用）」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd2").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード（確認用）」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd').value != document.getElementById('pwd2').value) {
alert('パスワードが一致していません。');
return(false);
}

return true;
}	//func
</script>
<form action="system.cgi" name="form1" id="form1" method="POST" enctype="multipart/form-data" onsubmit="return kakunin()" >
<input type="hidden" name="code" value="member_check2" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff"><input name="_チーム正式名称" type="text" id="teamname" value="$paramhash_dec{'_チーム正式名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム正式名称（フリガナ）" type="text" id="team_kana" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム省略名称" type="text" id="team_abbr" value="$paramhash_dec{'_チーム省略名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム結成年" maxlength=4  type="text" id="team_year" value="$paramhash_dec{'_チーム結成年'}" size="4" />
<font class="type3">年<br />
※西暦（例：2012）にてご入力下さい</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_主な活動曜日" type="text" id="katsudou_week" value="$paramhash_dec{'_主な活動曜日'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_平均年齢" type="text" id="average_age" value="$paramhash_dec{'_平均年齢'}" size="4" />
才</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
都道府県 <select name="_都道府県名" id="pref">
<option value="" >選択して下さい
<option value="北海道" $PFLAG{'北海道'}>北海道
<option value="青森県" $PFLAG{'青森県'}>青森県
<option value="岩手県" $PFLAG{'岩手県'}>岩手県
<option value="宮城県" $PFLAG{'宮城県'}>宮城県
<option value="秋田県" $PFLAG{'秋田県'}>秋田県
<option value="山形県" $PFLAG{'山形県'}>山形県
<option value="福島県" $PFLAG{'福島県'}>福島県
<option value="茨城県" $PFLAG{'茨城県'}>茨城県
<option value="栃木県" $PFLAG{'栃木県'}>栃木県
<option value="群馬県" $PFLAG{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG{'千葉県'}>千葉県
<option value="東京都" $PFLAG{'東京都'}>東京都
<option value="神奈川県" $PFLAG{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG{'新潟県'}>新潟県
<option value="富山県" $PFLAG{'富山県'}>富山県
<option value="石川県" $PFLAG{'石川県'}>石川県
<option value="福井県" $PFLAG{'福井県'}>福井県
<option value="山梨県" $PFLAG{'山梨県'}>山梨県
<option value="長野県" $PFLAG{'長野県'}>長野県
<option value="岐阜県" $PFLAG{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG{'静岡県'}>静岡県
<option value="愛知県" $PFLAG{'愛知県'}>愛知県
<option value="三重県" $PFLAG{'三重県'}>三重県
<option value="滋賀県" $PFLAG{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG{'京都府'}>京都府
<option value="大阪府" $PFLAG{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG{'島根県'}>島根県
<option value="岡山県" $PFLAG{'岡山県'}>岡山県
<option value="広島県" $PFLAG{'広島県'}>広島県
<option value="山口県" $PFLAG{'山口県'}>山口県
<option value="徳島県" $PFLAG{'徳島県'}>徳島県
<option value="香川県" $PFLAG{'香川県'}>香川県
<option value="愛媛県" $PFLAG{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG{'高知県'}>高知県
<option value="福岡県" $PFLAG{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG{'長崎県'}>長崎県
<option value="熊本県" $PFLAG{'熊本県'}>熊本県
<option value="大分県" $PFLAG{'大分県'}>大分県
<option value="宮崎県" $PFLAG{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG{'沖縄県'}>沖縄県
</select> 
　市区町村
<input name="_主な活動場所" type="text" id="team_cities" value="$paramhash_dec{'_主な活動場所'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="過去戦績" cols="60" rows="5" id="past_perform">$paramhash_dec{'過去戦績'}</textarea>
<br />
過去に参加された大会の実績等を具体的にご記入ください。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="チームＰＲ" cols="60" rows="5" id="team_pr">$paramhash_dec{'チームＰＲ'}</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名" type="text" id="shimei1" value="$paramhash_dec{'_代表者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名（フリガナ）" type="text" id="shimei_kana1" value="$paramhash_dec{'_代表者氏名（フリガナ）'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者メールアドレス" type="text" id="mailadr1" value="$paramhash_dec{'_代表者メールアドレス'}" size="20" style="ime-mode: disabled;" />
＠
<input name="_代表者メールアドレス（ドメイン）" type="text" id="mailadr2" value="$paramhash_dec{'_代表者メールアドレス（ドメイン）'}" size="20" style="ime-mode: disabled;" />
<br />
※ログインIDには、PCアドレスを推奨いたします。<br>
<font class="type1" color="#ff0000">※携帯アドレスで登録される方は本登録用のメールがブロックされ届かない場合がありますので、<br>
　その場合はお手数ですがＴＯＰページのお問い合わせから事務局までご連絡下さい。<br>
※迷惑メール防止のための受信設定をしている場合は、あらかじめ設定 を解除、あるいはドメイン指定設定<br>
（「pridejapan.net」を指定）　などを行って下さい。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者電話番号" type="text" id="tel1" value="$paramhash_dec{'_代表者電話番号'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
郵便番号<input name="_郵便番号" type="text" maxlength=8 id="zip" value="$paramhash_dec{'_郵便番号'}" size="10" />　
都道府県 <select name="_代表者都道府県名" id="pref2">
<option value="" >選択して下さい
<option value="北海道" $PFLAG2{'北海道'}>北海道
<option value="青森県" $PFLAG2{'青森県'}>青森県
<option value="岩手県" $PFLAG2{'岩手県'}>岩手県
<option value="宮城県" $PFLAG2{'宮城県'}>宮城県
<option value="秋田県" $PFLAG2{'秋田県'}>秋田県
<option value="山形県" $PFLAG2{'山形県'}>山形県
<option value="福島県" $PFLAG2{'福島県'}>福島県
<option value="茨城県" $PFLAG2{'茨城県'}>茨城県
<option value="栃木県" $PFLAG2{'栃木県'}>栃木県
<option value="群馬県" $PFLAG2{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG2{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG2{'千葉県'}>千葉県
<option value="東京都" $PFLAG2{'東京都'}>東京都
<option value="神奈川県" $PFLAG2{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG2{'新潟県'}>新潟県
<option value="富山県" $PFLAG2{'富山県'}>富山県
<option value="石川県" $PFLAG2{'石川県'}>石川県
<option value="福井県" $PFLAG2{'福井県'}>福井県
<option value="山梨県" $PFLAG2{'山梨県'}>山梨県
<option value="長野県" $PFLAG2{'長野県'}>長野県
<option value="岐阜県" $PFLAG2{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG2{'静岡県'}>静岡県
<option value="愛知県" $PFLAG2{'愛知県'}>愛知県
<option value="三重県" $PFLAG2{'三重県'}>三重県
<option value="滋賀県" $PFLAG2{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG2{'京都府'}>京都府
<option value="大阪府" $PFLAG2{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG2{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG2{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG2{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG2{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG2{'島根県'}>島根県
<option value="岡山県" $PFLAG2{'岡山県'}>岡山県
<option value="広島県" $PFLAG2{'広島県'}>広島県
<option value="山口県" $PFLAG2{'山口県'}>山口県
<option value="徳島県" $PFLAG2{'徳島県'}>徳島県
<option value="香川県" $PFLAG2{'香川県'}>香川県
<option value="愛媛県" $PFLAG2{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG2{'高知県'}>高知県
<option value="福岡県" $PFLAG2{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG2{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG2{'長崎県'}>長崎県
<option value="熊本県" $PFLAG2{'熊本県'}>熊本県
<option value="大分県" $PFLAG2{'大分県'}>大分県
<option value="宮崎県" $PFLAG2{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG2{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG2{'沖縄県'}>沖縄県
</select> 
<br>市区町村
<input name="_代表者住所" type="text" id="cities1" value="$paramhash_dec{'_代表者住所'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名" type="text" id="shimei2" value="$paramhash_dec{'_第2担当者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名（フリガナ）" type="text" id="shimei_kana2" value="$paramhash_dec{'_第2担当者氏名（フリガナ）'}" size="20" />
<br />
　代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。 </td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者電話番号" type="text" id="tel3" value="$paramhash_dec{'_第2担当者電話番号'}" size="20" />
<br />
※代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チームメールアドレス" type="text" id="mailaddress2" value="$paramhash_dec{'_チームメールアドレス'}" size="40" />
<br />
　登録アドレスはPCに限ります。<br />
　（代表者のメールアドレスがPCの方は、代表者アドレスと同じで構いません） </td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff"><input name="チームHPアドレス" type="text" id="team_hp" value="$paramhash_dec{'チームHPアドレス'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード" type="text" id="pwd" value="$paramhash_dec{'_パスワード'}" size="20" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード（確認用）</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード*" type="text" id="pwd2" value="$paramhash_dec{'_パスワード*'}" size="20" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input type="radio" name="_メールマガジン配信の選択" value="1" $MAILMAGAZINEFLAG{1} />
<font class="type3">希望する</font>　
<input type="radio" name="_メールマガジン配信の選択" value="0" $MAILMAGAZINEFLAG{0} />
<font class="type3">希望しない</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">LINE ID</font></td>
<td align="left" bgcolor="#ffffff"><input name="LINEID" type="text" id="lineid" value="$paramhash_dec{'LINEID'}" size="20" />
<br>
<font class="type1" color="#ff0000">※
メールアプリLINE（ライン）をお使いの方は、LINEのIDをチーム間の連絡用としてチームページに表示させることができます。<br>
※このIDは、プライドジャパンにログインしている全てのチームが閲覧可能になります。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム写真</font></td>
<td align="left" bgcolor="#ffffff">
<input type="file" name="file0" />$IMGSRC[0]$FILENAME[0]$FILEDELETE[0]<br>
<font class="type1" color="#ff0000">※「2MB以下までの画像をお入れください」もしくは「2000px　×　2000px以内」</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">登録選手</font></td>
<td align="left" bgcolor="#ffffff">
$teammemberlist
<script>
function tagopen(n){
document.getElementById('tag'+n).style.display = "block";
}	//func
function tagclose(n){
document.getElementById('tag'+n).style.display = "none";
}	//func
</script>


</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<input type="button" value="　　マイページへ戻る　　" onclick="location.href='system.cgi';" />
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<input type="submit" value="　　確認画面へ　　" />
</td>
</tr>
</table>
</form>
END_HTML
&mypagehtmldisp($mes);

exit;
}	#sub



# -----------------------------------------------------------------
# チーム：確認
# -----------------------------------------------------------------
sub member_check2 {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	if($p =~ /^file[0-9]{1,}$/){next;}
	if($p =~ /^filename[0-9]{1,}$/){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#チームメンバー
$teammemberlist =<<"END_HTML";
<table style="border:none;">
<tr>
<td align=center bgcolor="#aaaaaa">No.</td>
<td align=center bgcolor="#aaaaaa">名前</td>
<td align=center bgcolor="#aaaaaa">背番号</td>
<td align=center bgcolor="#aaaaaa">ポジション</td>
</tr>
END_HTML
foreach(0..29){
$no = $_ +1;
$s1 = $paramhash_dec{"teammember_name$_"};
$s2 = $paramhash_dec{"teammember_num$_"};
$s3 = $paramhash_dec{"teammember_position$_"};
if( $s1 ne "" or $s2 ne "" or $s3 ne ""){
$teammemberlist .=<<"END_HTML";
<tr>
<td align=center>$no</td>
<td align=center>$s1</td>
<td align=center>$s2</td>
<td align=center>$s3</td>
</tr>
END_HTML
}	#if
}	#foreach
$teammemberlist .=<<"END_HTML";
</table>
END_HTML

#エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="post" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="member_edit" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" />
</form>
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if

# 添付ファイルの登録処理
#print "f=".$paramhash{"file0"}."<br>\n";
if($paramhash{"file0"} ne ""){$file = &fileup("file0",21,"system/");}else{$file = $paramhash{"filename0"};}
#print "file=".$file."<br>\n";
if($paramhash{"filedelete0"} == 1){$file = "";}else{
#画像
if($file ne ""){
@TEMP = split(/<>/,$file);
@TEMP = split(/\./,$TEMP[1]);
$IMGSRC[0] = "<img src='system/file/$TEMP[0]pda.jpg'>$sfn<br>";
#$FILENAME[0] = "<input type='hidden' name='filename0' id='filename0' value='$file' >";
$FILEDELETE[0] = "<input type='checkbox' name='filedelete0' id='filedelete0' value=1 >登録ファイルの消去";
}	#if
}	#if
$rewritestr .=<<"END_HTML";
<input type="hidden" name="filename0" value="$file" />
END_HTML



###
$mes =<< "END_HTML";
<h2 class="subti" id="1">チーム情報の編集</h2>
以下の情報で再登録します。<p>
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム省略名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム結成年'}
<font class="type3">年</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_主な活動曜日'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_平均年齢'}才</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_都道府県名'} $paramhash_dec{'_主な活動場所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'過去戦績'}&nbsp;
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームＰＲ'}&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者メールアドレス'}＠$paramhash_dec{'_代表者メールアドレス（ドメイン）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_郵便番号'} 
$paramhash_dec{'_代表者都道府県名'} 
$paramhash_dec{'_代表者住所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チームメールアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームHPアドレス'}&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">*****</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<font class="type3">$MAILMAGAZINENAME{$paramhash_dec{'_メールマガジン配信の選択'}}</font>　
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">LINE ID</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'LINEID'}&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム写真</font></td>
<td align="left" bgcolor="#ffffff">&nbsp;
$IMGSRC[0]$FILENAME[0]$FILEDELETE[0]
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">登録選手</font></td>
<td align="left" bgcolor="#ffffff">
$teammemberlist
</td>
</tr></tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="member_edit" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="member_add2" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>
END_HTML
&mypagehtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：登録
# -----------------------------------------------------------------
sub member_add2 {
$teamname = $paramhash_dec{'_チーム正式名称'};
$team_kana = $paramhash_dec{'_チーム正式名称（フリガナ）'};
$team_abbr = $paramhash_dec{'_チーム省略名称'};
$team_year = $paramhash_dec{'_チーム結成年'};
$katsudou_week = $paramhash_dec{'_主な活動曜日'};
$average_age = $paramhash_dec{'_平均年齢'};
$team_zip = $paramhash_dec{'_郵便番号'};
$team_pref = $paramhash_dec{'_都道府県名'};
$team_cities = $paramhash_dec{'_主な活動場所'};
$past_perform = $paramhash_dec{'過去戦績'};
$team_pr = $paramhash_dec{'チームＰＲ'};
$shimei1 = $paramhash_dec{'_代表者氏名'};
$shimei_kana1 = $paramhash_dec{'_代表者氏名（フリガナ）'};
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$tel1 = $paramhash_dec{'_代表者電話番号'};
$prefectural1 = $paramhash_dec{'_代表者都道府県名'};
$cities1 = $paramhash_dec{'_代表者住所'};
$shimei2 = $paramhash_dec{'_第2担当者氏名'};
$shimei_kana2 = $paramhash_dec{'_第2担当者氏名（フリガナ）'};
$tel2 = $paramhash_dec{'_第2担当者電話番号'};
$mailaddress2 = $paramhash_dec{'_チームメールアドレス'};
$team_hp = $paramhash_dec{'チームHPアドレス'};
$pwd = $paramhash_dec{'_パスワード'};
$mailmagazine = $paramhash_dec{'_メールマガジン配信の選択'};
$upfilename = $paramhash{'filename0'};
$lineid = $paramhash_dec{'LINEID'};
#チームメイト
foreach(0..29){
$teammember .= $paramhash_dec{"teammember_name$_"}.":".$paramhash_dec{"teammember_num$_"}.":".$paramhash_dec{"teammember_position$_"}."<>";
}	#foreach

#変更
$mailadr1 =~ s/\'/\'\'/gm;	#'
$mailadr2 =~ s/\'/\'\'/gm;	#'
$shimei1 =~ s/\'/\'\'/gm;	#'
$shimei_kana1 =~ s/\'/\'\'/gm;	#'
$mailaddress1 =~ s/\'/\'\'/gm;	#'
$tel1 =~ s/\'/\'\'/gm;	#'
$prefectural1 =~ s/\'/\'\'/gm;	#'
$cities1 =~ s/\'/\'\'/gm;	#'
$shimei2 =~ s/\'/\'\'/gm;	#'
$shimei_kana2 =~ s/\'/\'\'/gm;	#'
$tel2 =~ s/\'/\'\'/gm;	#'
$mailaddress2 =~ s/\'/\'\'/gm;	#'
$teamname =~ s/\'/\'\'/gm;	#'
$team_kana =~ s/\'/\'\'/gm;	#'
$team_abbr =~ s/\'/\'\'/gm;	#'
$team_year =~ s/\'/\'\'/gm;	#'
$team_hp =~ s/\'/\'\'/gm;	#'
$katsudou_week =~ s/\'/\'\'/gm;	#'
$average_age =~ s/\'/\'\'/gm;	#'
$team_zip =~ s/\'/\'\'/gm;	#'
$team_pref =~ s/\'/\'\'/gm;	#'
$team_cities =~ s/\'/\'\'/gm;	#'
$past_perform =~ s/\'/\'\'/gm;	#'
$team_pr =~ s/\'/\'\'/gm;	#'
$teammember =~ s/\'/\'\'/gm;	#'
$upfilename =~ s/\'/\'\'/gm;	#'
$lineid =~ s/\'/\'\'/gm;	#'

$str = "";
$str.="mailadr1 = '$mailadr1',";
$str.="mailadr2 = '$mailadr2',";
$str.="pwd = '$pwd',";
$str.="shimei1 = '$shimei1',";
$str.="shimei_kana1 = '$shimei_kana1',";
$str.="mailaddress1 = '$mailaddress1',";
$str.="tel1 = '$tel1',";
$str.="prefectural1 = '$prefectural1',";
$str.="cities1 = '$cities1',";
$str.="shimei2 = '$shimei2',";
$str.="shimei_kana2 = '$shimei_kana2',";
$str.="tel2 = '$tel2',";
$str.="mailaddress2 = '$mailaddress2',";
$str.="teamname = '$teamname',";
$str.="team_kana = '$team_kana',";
$str.="team_abbr = '$team_abbr',";
$str.="team_year = '$team_year',";
$str.="team_hp = '$team_hp',";
$str.="katsudou_week = '$katsudou_week',";
$str.="average_age = '$average_age',";
$str.="team_zip = '$team_zip',";
$str.="team_pref = '$team_pref',";
$str.="team_cities = '$team_cities',";
$str.="past_perform = '$past_perform',";
$str.="team_pr = '$team_pr',";
$str.="mailmagazine = '$mailmagazine',";
$str.="teammember = '$teammember',";
$str.="upfilename = '$upfilename',";
$str.="lineid = '$lineid',";

chop $str;
$sql_str = "UPDATE $member_tbl SET $str WHERE ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
###
$mes =<<"END_HTML";
<p align="center" style="color:red;font-weight:bold;font-size:20px;">修正登録完了</p>
<p align="center">
<input type="button" value="　　マイページへ戻る　　" onclick="location.href='system.cgi';" />
</p>
END_HTML
&mypagehtmldisp($mes);
exit;
}	#sub





# -----------------------------------------------------------------
# 順位／星取り表
# -----------------------------------------------------------------
sub ranking {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
if($taikainame =~ /不明/){
$mes =<<"END_HTML";
大会情報が取得できませんでした。
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if

&kachi;


########################
########################
$mes =<<"END_HTML";
<style>
#navigation2 li.menu3 a {
	background:url(img/menu2.jpg) no-repeat -492px -50px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>

<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">

<div id="pnl">
<div class="pnl">$areatag</div>
</div>

$arealist

</div>
END_HTML


&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# 試合予定報告：試合一覧
# -----------------------------------------------------------------
sub gameschedule {
($teamname,$teamserial) = &taikaiteamname_get2($loginuser);

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}

foreach $cate($sc .. $ec){
$taikainame = &taikainame_get($taikaicode, $cate);

if( $cate == 1 ){
#print "リーグ<br>";
##########################################################
# リーグ
##########################################################
#報告データをGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and linkadr = '$loginuser' and category = 1";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
%REPORTFLAG = ();
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
my $taikaicode = &paramsetsql('taikaicode',$REFHASH1);
#my $category = &paramsetsql('category',$REFHASH1);
my $area = &paramsetsql('area',$REFHASH1);
my $kumi = &paramsetsql('kumi',$REFHASH1);
my $setu = &paramsetsql('title',$REFHASH1);
my $text1 = &paramsetsql('text1',$REFHASH1);
my $teamnum = &paramsetsql('teamnum',$REFHASH1);
$REPORTFLAG{$taikaicode}{1}{$area}{$kumi}{$setu}{$text1} = $teamnum;	#
#print "teamnum=$teamnum<br>";
}	#for

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1<br>";
for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area2 = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area2);
if($areaname =~ /不明/){next;}
$kumi0 = $kumi2 = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi0);
if($kuminame =~ /不明/){next;}
#試合期限10日後は表示しない
$n = Date::Simple->new();
foreach(split(/<>/,$body)){
($setutemp,$nichiji1,$nichiji2) = split(/:/,$_);
#print "($setutemp,$nichiji1,$nichiji2)<br>\n";
$nichijistr = sprintf("%d年%d月%d日",split(/-/,$nichiji1))."～";
$nichijistr .= sprintf("%d年%d月%d日",split(/-/,$nichiji2))."まで";
$NISHIJISTR{$setutemp} = $nichijistr;
$n1 = Date::Simple->new($nichiji1);
$n2 = Date::Simple->new($nichiji2) +10;
if($n > $n2){
$DISPFLAG{$setutemp} = 0;	#非表示
$NISHIJISTR{$setutemp} .= "<hr><span style='color:red;'>（消去対象）$n2</span>";
}else{
$DISPFLAG{$setutemp} = 1;	#表示
}	#if
}	#foreach



# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu2,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu2,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($teamserial != $tss1 && $teamserial != $tss2){next;}
if($teamserial != $tss1){($tss1,$tss2)=($tss2,$tss1);}
($aiteteam,$aiteses) = &taikaiteamname_get3($tss2);
if($aiteteam eq ""){next;}	#相手チームがなければスルー
$aiteteam = "<a href='?code=mypage_team&ses=$aiteses'>$aiteteam</a>";
#$temp = "$taikaicode:$area:$kumi:$setu:$tss";
#期限チェック
if($DISPFLAG{$setu2} == 1){
### 両チームの報告の突き合わせ
#($tempname,$aitesession) = taikaiteamname_get3($tss2);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area2' and kumi = '$kumi2' and title = '$setu2' and text1 = '$num' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>\n";
$attention = "";
if($count2 == 2){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum2 = &paramsetsql('teamnum',$REFHASH2);
$n2 = &paramsetsql('nichiji1',$REFHASH2);
if($n1 ne $n2){$attention = "<br><span style='color:red;'>報告に相違があります。</span>";}
}else{
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnumtemp = &paramsetsql('teamnum',$REFHASH2);
if($teamserial != $teamnumtemp){$attention = "<br><span style='color:red;'>相手が未報告です。</span>";}
}	#if
}	#if count2 == 1



$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
if($REPORTFLAG{$taikaicode}{1}{$area2}{$kumi2}{$setu2}{$num} == $tss2){$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";}

#if($teamserial == $tss1 ){	#自分だけ処理する

$schedulelist1 .=<<"END_HTML";
<tr>
<th align="center" scope="row"><a href="?code=gamescheduleform&taikaicode=$taikaicode&category=1&area=$area2&kumi=$kumi2&kumi0=$kumi0&setu=$setu2&text1=$num&posi=0&aitess=$tss2"><img src="img/hensyuu.jpg" alt="編集" width="59" height="32" /></a></th>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$NISHIJISTR{$setu2}</th>
<th align="left" scope="row">地区名：$areaname<br>　組名：$kuminame</th>
<th align="center" scope="row">$aiteteam</th>
<th align="center" scope="row">$reportflag$attention</th>
</tr>
END_HTML
#}	#if teamserial

=pot
if( $teamserial == $tss2){	#自分だけ処理する
$aiteteam = &taikaiteamname_get($tss1);
$schedulelist1 .=<<"END_HTML";
<tr>
<th align="center" scope="row"><a href="?code=gamescheduleform&taikaicode=$taikaicode&category=1&area=$area2&kumi=$kumi&setu=$setu&text1=$num&posi=1&aitess=$tss1"><img src="img/hensyuu.jpg" alt="編集" width="59" height="32" /></a></th>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$NISHIJISTR{$setu}</th>
<th align="left" scope="row">地区名：$areaname<br>　組名：$kuminame</th>
<th align="center" scope="row">$aiteteam</th>
<th align="center" scope="row">$reportflag$attention</th>
</tr>
END_HTML
}	#if teamserial
=cut
}	#if DISPFLAG
}	#foreach vsdata

}	#if for
}	#if cate




##########################################################
# トーナメント
##########################################################
if( $cate == 2 ){
@CNT = (0,1,2,4,8,16,32,64,128);
$setu = "";
$kumi = "";
%REPORTFLAG =();
#報告データをGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and linkadr = '$loginuser' and taikaicode = $taikaicode and category = 2";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1<br>\n";
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
my $taikaicode = &paramsetsql('taikaicode',$REFHASH1);
#my $category = &paramsetsql('category',$REFHASH1);
my $area = &paramsetsql('area',$REFHASH1);
my $kumi = &paramsetsql('kumi',$REFHASH1);
my $setu = &paramsetsql('text1',$REFHASH1);
my $teamnum = &paramsetsql('teamnum',$REFHASH1);
my $linkadr = &paramsetsql('linkadr',$REFHASH1);
$REPORTFLAG{$taikaicode}{2}{$area}{$kumi}{$setu}{$teamnum} = 1;	#
#print "{$taikaicode}{2}{$area}{$kumi}{$setu}<br>\n";
}	#for

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode'  and category = '2' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1<br>\n";
for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area2 = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area2);
if($areaname =~ /不明/){next;}
$kumi0 = $kumi2 = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi0);
if($kuminame =~ /不明/){next;}
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";
$k+=2;
}	#foreach x
}	#foreach y

#最下段を求める
$gedan = 0;
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan";

#トーナメント○回戦
foreach $y(1..7){
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$dateover = "";
$d = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2) +10;
#試合期限後は表示しない
if( $d > $d2 ){$dateover .= "<hr><span style='color:red;'>（消去対象）$d2</span>";}

#報告範囲内
#if( $d1 <= $d && $d <= $d2){
#自分の場所を探す
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$posi = 0;
$aitess = "";
#print "y=$y<br>\n";
#左の枠
if($TEAMLIST{$y}{$x}{1} == $teamserial){
$posi = 1;
$aitess = $TEAMLIST{$y}{$x}{2};
$num = $y;
$kumi = $x;
last;
}	#if
#右の枠
if($TEAMLIST{$y}{$x}{2} == $teamserial){
$posi = 2;
$aitess = $TEAMLIST{$y}{$x}{1};
$num = $y;
$kumi = $x;
last;
}	#if
}	#foreach x
#posi確定
if($posi != 0){
($aiteteam,$aiteses) = &taikaiteamname_get3($aitess);
if($aiteteam eq ""){next;}	#相手チームがなければスルー
$aiteteam = "<a href='?code=mypage_team&ses=$aiteses'>$aiteteam</a>";

@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));


$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num +2)."回戦";
}	#num
$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
#print        "{$taikaicode}{2}{$area}{$kumi}{$num}<br>\n";
if($REPORTFLAG{$taikaicode}{2}{$area2}{$kumi}{$num}{$aitess} == 1){$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";}

$attention = "";
### 両チームの報告の突き合わせ
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area2' and kumi = '$kumi' and text1 = '$num' and ( (teamnum = '$teamserial' and teamnum = '$aitess' ) or (teamnum = '$aitess' and teamnum = '$teamserial' ) )";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>\n";
$attention = "";
if($count2 == 2){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum2 = &paramsetsql('teamnum',$REFHASH2);
$n2 = &paramsetsql('nichiji1',$REFHASH2);
if($n1 ne $n2){$attention = "<br><span style='color:red;'>報告に相違があります。</span>";}
}else{
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnumtemp = &paramsetsql('teamnum',$REFHASH2);
if($teamserial != $teamnumtemp){$attention = "<br><span style='color:red;'>相手が未報告です。</span>";}
}	#if
}	#if count2 == 2


if($dateover ne ""){next;}


#
$schedulelist2 .=<<"END_HTML";
<tr>
<th align="center" scope="row"><a href="?code=gamescheduleform&taikaicode=$taikaicode&category=2&area=$area2&kumi=$kumi&setu=$gedan&text1=$num&posi=$posi&aitess=$aitess"><img src="img/hensyuu.jpg" alt="編集" width="59" height="32" /></a></th>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$nichiji $dateover</th>
<th align="center" scope="row">$numstr</th>
<th align="center" scope="row">$aiteteam</th>
<th align="center" scope="row">$reportflag$attention</th>
</tr>
END_HTML
}	#if posi

#}	#if 日付が有効
}	#if nichiji
}	#foreach 1-7
}	#for
}	#if cate 2

}	#foreach cate
}	#for taikai

if($schedulelist1 ne ""){
$schedulelist1 =<<"END_HTML";
<table width="100%" cellspacing="0" class="stane">
<tr>
<th width="8%" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">&nbsp;</th>
<th width="19%" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">大会</th>
<th width="34%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合期日</th>
<th width="11%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="16%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
<th width="12%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">状態</th>
</tr>
$schedulelist1
</table>
END_HTML
}	#if 1

if($schedulelist2 ne ""){
$schedulelist2 =<<"END_HTML";
<table width="100%" cellspacing="0" class="stane">
<tr>
<th width="8%" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">&nbsp;</th>
<th width="19%" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">大会</th>
<th width="34%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合期日</th>
<th width="11%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="16%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
<th width="12%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">状態</th>
</tr>
$schedulelist2
</table>
END_HTML
}	#if 2


###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/geschti.jpg" alt="試合予定一覧" width="980" height="48" /> </div>
<div id="mainbox">
<h2 id="team" style="background-image:url(img/ter8.jpg)"><span>$teamname</span></h2>

<br>
<img src="img/riti.jpg" ALT="リーグ戦タイトル" />
$schedulelist1
<br>

<img src="img/toti.jpg" ALT="トーナメント戦タイトル" />
$schedulelist2

</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# 試合予定報告：試合予定報告フォーム
# -----------------------------------------------------------------
sub gamescheduleform {
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
$setu = $paramhash{'setu'};
$text1 = $paramhash{'text1'};
$posi = $paramhash{'posi'};
$aitess = $paramhash{'aitess'};
($aiteteam) = &taikaiteamname_get3($aitess);
$taikainame = &taikainame_get($taikaicode,$category);
$areaname = &taikaiareaname_get($area);
$kuminame = &taikaikuminame_get($kumi);
($teamname,$tss) = &taikaiteamname_get2($loginuser);

#
$nichiji1 = "<select name=syear id=syear>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect($year,$year+1);
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth id=smonth>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,12);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday id=sday>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,31);
$nichiji1 .= "</select>日　　\n";
$nichiji1 .= "<select name=shour id=shour>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(6,24,$shour);
$nichiji1 .= "</select>時\n";
$nichiji1 .= "<select name=smin id=smin>\n";
for($k=0;$k<60;$k+=5){
$nichiji1 .= "<option value='$k' >$k</option>\n";
}	#for
$nichiji1 .= "</select>分\n";

#############################
# リーグ
if($category == 1){
$areainfo =<<"HTML_END";
大会名：$taikainame<br>
地区名：$areaname<br>
　組名：$kuminame
HTML_END

#既存データがあればセット
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and linkadr = '$loginuser' and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$kumi' and title = '$setu' and teamnum = '$aitess' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1<br>\n";
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH1);
#$area = &paramsetsql('area',$REFHASH1);
#$kumi = &paramsetsql('kumi',$REFHASH1);
#$setu = &paramsetsql('title',$REFHASH1);
#$teamnum = &paramsetsql('teamnum',$REFHASH1);
$ss = &paramsetsql('serial',$REFHASH1);
$deletebtn =<<"HTML_END";
<br><br><br>
<input type=button value="この登録を削除する" onclick="urljump_kakunin2('?code=deleterecord_user&ss=$ss&returnurl=gameschedule')" />
HTML_END

$body = &paramsetsql('body',$REFHASH1);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH1));
($y,$m,$d) = split(/-/,$TEMP[0]);
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$MINFLAHG{$smin} = "selected";
$nichiji1 = "<select name=syear id=syear>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect($year+1,$year,$y);
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth id=smonth>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,12,$m);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday id=sday>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,31,$d);
$nichiji1 .= "</select>日　　\n";
$nichiji1 .= "<select name=shour id=shour>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(6,24,$shour);
$nichiji1 .= "</select>時\n";
$nichiji1 .= "<select name=smin id=smin>\n";
for($k=0;$k<60;$k+=5){
$nichiji1 .= "<option value='$k' $MINFLAHG{$k}>$k</option>\n";
}	#for
$nichiji1 .= "</select>分\n";

}	#if
#
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category'";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setutemp,$numtemp,$tss1) = split(/\./,$data1);	#1 1 1
($setutemp,$numtemp,$tss2) = split(/\./,$data2);	#1 1 8
if($tss == $tss1 && $setutemp == $setu && $numtemp == $text1){$aitetss = $tss2;}
if($tss == $tss2 && $setutemp == $setu && $numtemp == $text1){$aitetss = $tss1;}
}	#foreach vsdata

}	#if category

#############################
# トーナメント
#############################
if($category == 2){
$numstr = "";
if($text1 == 1){$numstr = "決勝戦";}
if($text1 == 2){$numstr = "準決勝";}
if($text1 == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($setu - $text1+2)."回戦";	#setu = gedan
}	#if
$areainfo =<<"HTML_END";
$taikainame<br>$numstr
HTML_END
#既存データがあればセット
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and linkadr = '$loginuser' and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and text1 = '$text1' and linkadrtitle = '$posi' and teamnum = '$aitess' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$ss = &paramsetsql('serial',$REFHASH1);
$deletebtn =<<"HTML_END";
<br><br><br>
<input type=button value="この登録を削除する" onclick="urljump_kakunin2('?code=deleterecord_user&ss=$ss&returnurl=gameschedule')" />
HTML_END
$body = &paramsetsql('body',$REFHASH1);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH1));
($y,$m,$d) = split(/-/,$TEMP[0]);
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$MINFLAHG{$smin} = "selected";
$nichiji1 = "<select name=syear id=syear>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect($year+1,$year,$y);
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth id=smonth>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,12,$m);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday id=sday>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(1,31,$d);
$nichiji1 .= "</select>日　　\n";
$nichiji1 .= "<select name=shour id=shour>\n";
$nichiji1 .= "<option>選択</option>\n";
$nichiji1 .= &makeselect(6,24,$shour);
$nichiji1 .= "</select>時\n";
$nichiji1 .= "<select name=smin id=smin>\n";
for($k=0;$k<60;$k+=5){
$nichiji1 .= "<option value='$k' $MINFLAHG{$k}>$k</option>\n";
}	#for
$nichiji1 .= "</select>分\n";
}	#if



}	#if category

###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/geschti2.jpg" alt="試合予定報告" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">試合予定報告フォーム</h2>
<div class="box">
チーム名：$teamname
<p>下記の必要事項を入力し、確認ボタンをクリックしてください。</p>
<script>
<!--
function kakunin(){

var i = document.getElementById('syear').selectedIndex;
if (i == 0) {
alert('日時が選択されていません。');
return(false);
}
var i = document.getElementById('smonth').selectedIndex;
if (i == 0) {
alert('日時が選択されていません。');
return(false);
}
var i = document.getElementById('sday').selectedIndex;
if (i == 0) {
alert('日時が選択されていません。');
return(false);
}

if (document.getElementById('body').value == "") {
alert('グランド情報が入力されていません。');
return(false);
}

if(window.confirm("この内容で登録します。\\nよろしければ「OK」を押して下さい。\\n修正する場合には「キャンセル」を押して下さい。")){
return true;
}

return false;
}


function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この操作は元に戻す事が出来ません。\\n本当に削除してもよろしいですか？\\n念のため、削除後に対戦相手にも情報を削除したことをご報告ください。")) {
	top.location.href=url;
}
}

-->
</script>
<form action="system.cgi" name="" method="POST" onSubmit="return kakunin()">
<input type="hidden" name="code" value="gamescheduleformadd" />
<input type="hidden" name="taikaicode" value="$taikaicode" />
<input type="hidden" name="category" value="$category" />
<input type="hidden" name="area" value="$area" />
<input type="hidden" name="kumi" value="$kumi" />
<input type="hidden" name="setu" value="$setu" />
<input type="hidden" name="text1" value="$text1" />
<input type="hidden" name="posi" value="$posi" />
<input type="hidden" name="aitess" value="$aitess" />

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">試合日時</font></td>
<td width="76%" bgcolor="#ffffff">$nichiji1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">名称</font></td>
<td bgcolor="#ffffff">
$areainfo
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">対戦チーム</font></td>
<td bgcolor="#ffffff">$aiteteam</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">グラウンド情報</td>
<td bgcolor="#ffffff"><input type="text" name="body" id="body" size="50" tabindex="7" value="$body" /></td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　報告する　　" />
</form>
$deletebtn
</div>
</div>
</div>
END_HTML
#
&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# 試合予定報告：試合予定報告フォーム：登録
# -----------------------------------------------------------------
sub gamescheduleformadd {
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
$setu = $paramhash{'setu'};
$text1 = $paramhash{'text1'};
$posi = $paramhash{'posi'};
$body = $paramhash2{'body'};
$aitess = $paramhash{'aitess'};
#日時チェック
$nichiji1 = sprintf("%04d-%02d-%02d",$paramhash{"syear"},$paramhash{"smonth"},$paramhash{"sday"});
$nichijistr = sprintf("%d年%d月%d日",$paramhash{"syear"},$paramhash{"smonth"},$paramhash{"sday"});
if(!Date::Simple->new($nichiji1)){
$mes =<<"END_HTML";
<p style="color:red;">日付にエラーがあります。</p>
<p>「$nichijistr」</p>
<p><input type=button onclick="javascript:history.back();" value="前に戻る" /></p>
END_HTML
&mypagehtmldisp($mes);
exit;
}		#if

=pot
#過去はだめ
if(Date::Simple->new($nichiji1) < Date::Simple->new()){
$n = sprintf("%d年%d月%d日",$year,$month,$mday);
$mes =<<"END_HTML";
<p style="color:red;">過去の日付では登録できません。</p>
<p>　本　日　：$n</p>
<p>登録予定日：$nichijistr</p>
<p><input type=button onclick="javascript:history.back();" value="前に戻る" /></p>
END_HTML
&mypagehtmldisp($mes);
exit;
}		#if
=cut

#時間をプラス
$nichiji1 .= " ".sprintf("%02d:%02d:%02d",$paramhash{"shour"},$paramhash{"smin"},0);

#重複チェック
$sql_str = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$text1' and linkadrtitle = '$posi' and linkadr = '$loginuser' and  teamnum = '$aitess' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
# 既に報告があれば、一応警告
$attention =<<"END_HTML";
<p style="color:red;">※この日の報告は既に受け付けておりますが、最新の情報に更新しました。</p>
END_HTML
#アップデート
$str = "body = '$body',";
$str.="nichiji1 = '$nichiji1',";
$str.="timestamp = '$nowdate',";
chop $str;
$sql_str = "UPDATE $dbname SET $str WHERE serial = $serial ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}else{
#DB
# 新規登録
$sql_str = qq{INSERT INTO $dbname(contents,koukaiflag,taikaicode,category,area,kumi,title,text1,linkadrtitle,body,nichiji1,linkadr,teamnum) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
34,
0,
$taikaicode,
$category,
$area,
$kumi,
$setu,
$text1,
$posi,
$body,
$nichiji1,
$loginuser,
$aitess,
);
}	#if
&sqlcheck($sql_str);

###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/geschti2.jpg" alt="試合予定報告" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">試合予定報告フォーム</h2>
<div class="box">
$attention
<p>報告完了</p>
<input type=button onClick="location.href='?code=gameschedule'" value="報告一覧ページに戻る" /><p>
<input type=button onClick="location.href='system.cgi'" value="マイページに戻る" />
</div>
</div>
</div>
END_HTML
#
&taikaihtmldisp($mes);
exit;
}	#sub









# -----------------------------------------------------------------
# 試合結果一覧
# -----------------------------------------------------------------
sub gameresult {
($teamname,$tss) = &taikaiteamname_get2($loginuser);

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}

foreach $cate($sc .. $ec){
$taikainame = &taikainame_get($taikaicode, $cate);

##########################################################
# リーグ
##########################################################
if( $cate == 1 ){
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
#print "sql_str1=$sql_str1<br>\n";
$count1 = $rs1->rows;	# Hit件数を確保
for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
$kumi0 = $kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi0);

$result0 = "";
$result1 = "";

#試合期日
$nowd = Date::Simple->new();
%DISPFLAG = ();
foreach(split(/<>/,$body)){
($setutemp,$nichiji1,$nichiji2) = split(/:/,$_);
if($nichiji1 eq "" || $nichiji2 eq "" || $nichiji1 eq "0000-00-00" || $nichiji2 eq "0000-00-00" ){next;}
$n1 = Date::Simple->new($nichiji1);
$n2 = Date::Simple->new($nichiji2) +90;
if($nowd > $n2){
$DISPFLAG{$setutemp} = 1;	#表示しない
$DISPFLAG2{$setutemp} = $n2;
}	#if
}	#foreach
#print "vsdata=$vsdata<br>\n";
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($tss != $tss1 && $tss != $tss2){next;}

if($tss != $tss1){($tss1,$tss2)=($tss2,$tss1);}

($aiteteam,$aiteses) = &taikaiteamname_get3($tss2);
$aiteteam = "<a href='?code=mypage_team&ses=$aiteses'>$aiteteam</a>";

$editflag = "";
$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
$tsstemp = "";
$attention = "";

#if($tss == $tss1 ){	#自分が左
#自分の試合結果報告をGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and category = 1 and kumi = '$kumi' and title = '$setu' and text1 = $num and linkadr = '$loginuser' and teamnum = '$tss2' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1<br>\n";
$ld1 = -1;
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH1);
$resultstr = &paramsetsql('resultstr',$REFHASH1);
$result0 = &paramsetsql('result0',$REFHASH1);
$result1 = &paramsetsql('result1',$REFHASH1);
if( &paramsetsql('linkadrtitle',$REFHASH1) == 1 ){($result0,$result1)=($result1,$result0);}
$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";
$editflag = " onClick='return editflag()' ";
#print "serial1=$s1<br>\n";
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH1));
$ld1 = Date::Simple->new($TEMP[0]);
}	#if 報告あり

### 両チームの報告の突き合わせ
#自分の報告書は上にあるので、相手チームの報告をGET
($tempname,$aitesession) = taikaiteamname_get3($tss2);
#print "()=($tempname,$aitesession)<br>\n";
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and category = 1 and kumi = '$kumi' and title = '$setu' and text1 = $num and teamnum = '$tss' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>\n";
$ld2 = -1;
if($count2 == 0 ){$attention = "<br>相手未報告";}	#if count2 == 0
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$aite_resultstr = &paramsetsql('resultstr',$REFHASH2);
$aite_result0 = &paramsetsql('result0',$REFHASH2);
$aite_result1 = &paramsetsql('result1',$REFHASH2);
if( &paramsetsql('linkadrtitle',$REFHASH2) == 1 ){($aite_result0,$aite_result1)=($aite_result1,$aite_result0);}
#print "serial2=$s2<br>\n";
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH2));
$ld2 = Date::Simple->new($TEMP[0]);
}	#if count2 == 1


#print "resultstr:$resultstr - aite_resultstr:$aite_resultstr<br>\n";

#$tsstemp = $tss2;

#print "count1=$count1 count2=$count2<br>\n";
$winlose = "";
$score222 = "";

if($count1 == 1 && $count2 == 1 ){

$score222 = $result0." - ".$result1;

if($resultstr == 1){$winlose = "○";}	#if win
if($resultstr == 2){$winlose = "×";}	#if win

#if($resultstr == 1 && $aite_resultstr != 2){next;}	#if
#if($resultstr == 2 && $aite_resultstr != 1){next;}	#if
#if($resultstr == 3 && $aite_resultstr != 3){next;}	#if
#if($resultstr == 4 && $aite_resultstr != 5){next;}	#if
#if($resultstr == 5 && $aite_resultstr != 4){next;}	#if

#引き分け
if($result0 == $result1){$winlose = "△";}	#if win
#不戦勝
if($resultstr == 4){$winlose = "○";$winlose = "不戦勝";}	#if
#不戦敗
if($resultstr == 5){$winlose = "×";$winlose = "不戦敗";}	#if
#自分が「勝ち」の場合、相手が「負け」以外は「相違！」
if($resultstr == 1 && $aite_resultstr != 2){
#$attention = "対戦相手との戦績登録に相違があります。1";
}	#if
#自分が「勝ち」の場合、相手が「負け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 1 && $aite_resultstr == 2 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
#$attention = "対戦相手との戦績登録に相違があります。1.1";
}	#if

#自分が「負け」の場合、相手が「勝ち」以外は「相違！」
if($resultstr == 2 && $aite_resultstr != 1 && $count2 == 1){
#$attention = "対戦相手との戦績登録に相違があります。2";
}	#if
#自分が「負け」の場合、相手が「勝ち」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 2 && $aite_resultstr == 1 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
#$attention = "対戦相手との戦績登録に相違があります。2.1";
}	#if

#自分が「不戦勝」の場合、相手が「不戦敗」以外は「相違！」
if($resultstr == 4 && $aite_resultstr != 5){
#$attention = "対戦相手との戦績登録に相違があります。3";
}	#if
#自分が「不戦敗」の場合、相手が「不戦勝」以外は「相違！」
if($resultstr == 5 && $aite_resultstr != 4){
#$attention = "対戦相手との戦績登録に相違があります。4";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外は「相違！」
if($resultstr == 3 && $aite_resultstr != 3){
#$attention = "対戦相手との戦績登録に相違があります。5";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 3 && $aite_resultstr == 3 and $result0 != $aite_result0 ){
#$attention = "対戦相手との戦績登録に相違があります。6";
}	#if
}	#if count1 count2

#}	#if tss
#注意があれば。
if($attention ne ""){
$attention = "<br><span style='color:red;font-size:12px;font-weight:normal;'>$attention</span>";
}	#if attention

=pot
### 反転
if($tss == $tss2 ){	#自分が右
#報告をGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' and title = '$setu' and linkadr = '$loginuser' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1<br>\n";
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH1);
$resultstr = &paramsetsql('resultstr',$REFHASH1);
$result0 = &paramsetsql('result0',$REFHASH1);
$result1 = &paramsetsql('result1',$REFHASH1);
$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";
$editflag = " onClick='return editflag()' ";
#print "serial1=$s1<br>\n";
}	#if 報告あり

### 両チームの報告の突き合わせ
#自分の報告書は上にあるので、相手チームの報告をGET
($tempname,$aitesession) = taikaiteamname_get3($tss1);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' and title = '$setu' and linkadr = '$aitesession' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>\n";
if($count2 == 0){
$attention = "<br>相手未報告";
}	#if count2 == 0
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$aite_resultstr = &paramsetsql('resultstr',$REFHASH2);
$aite_result0 = &paramsetsql('result0',$REFHASH2);
$aite_result1 = &paramsetsql('result1',$REFHASH2);
#print "serial2=$s2<br>\n";
}	#if count2 == 1

#print "resultstr:$resultstr - aite_resultstr:$aite_resultstr<br>\n";

$aiteteam = &taikaiteamname_get($tss1);
$tsstemp = $tss1;
$score = $result0." - ".$result1;
if($count1 != 0 && $count2 != 0){
if($resultstr == 2){$winlose = "×";}	#if win
if($resultstr == 1){$winlose = "○";}	#if win
#引き分け
if($result0 == $result1){$winlose = "△";}	#if win
#不戦勝
if($RESULTSTR{$loginuser} == 4){$winlose = "×";$score = "不戦敗";}	#if
#不戦敗
if($RESULTSTR{$loginuser} == 5){$winlose = "○";$score = "不戦勝";}	#if
#自分が「勝ち」の場合、相手が「負け」以外は「相違！」
if($resultstr == 1 && $aite_resultstr != 2){
$attention = "対戦相手との戦績登録に相違があります。1";
}	#if
#自分が「勝ち」、相手が「負け」、でもスコアが異なる場合は「相違！」
#print "$resultstr == 1 && $aite_resultstr == 2 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) <br>\n";
if($resultstr == 1 && $aite_resultstr == 2 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) ){
$attention = "対戦相手との戦績登録に相違があります。1.1";
}	#if

#自分が「負け」の場合、相手が「勝ち」以外は「相違！」
if($resultstr == 2 && $aite_resultstr != 1 && $count2 == 1){
$attention = "対戦相手との戦績登録に相違があります。2";
}	#if
#自分が「負け」の場合、相手が「勝ち」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 2 && $aite_resultstr == 1 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) ){
$attention = "対戦相手との戦績登録に相違があります。l 2.1";
}	#if

#自分が「不戦勝」の場合、相手が「不戦敗」以外は「相違！」
if($resultstr == 4 && $aite_resultstr != 5){
$attention = "対戦相手との戦績登録に相違があります。3";
}	#if
#自分が「不戦敗」の場合、相手が「不戦勝」以外は「相違！」
if($resultstr == 5 && $aite_resultstr != 4){
$attention = "対戦相手との戦績登録に相違があります。4";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外は「相違！」
if($resultstr == 3 && $aite_resultstr != 3){
$attention = "対戦相手との戦績登録に相違があります。5";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 3 && $aite_resultstr == 3 && $result0 != $aite_result0 ){
$attention = "対戦相手との戦績登録に相違があります。6";
}	#if

}	#if count1
}	#if tss
=cut

#注意があれば。
#if($attention ne ""){
#$attention = "<br><span style='color:red;font-size:12px;font-weight:normal;'>$attention</span>";
#}	#if attention

$ground = "";
$nichijireport = "";
#if($tsstemp ne ""){	#
#試合日と開催地をGET
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ORDER BY serial ASC LIMIT 1";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$count4<br>\n";
if($count4 != 0){
$REFHASH4 = $rs4->fetchrow_hashref;
$ground = &paramsetsql('body',$REFHASH4);
$n = &paramsetsql('nichiji1',$REFHASH4);
@TEMP = split(/ /,$n);
$nichijireport = sprintf("%d年<br>%d月%d日<br>%d時%02d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
}else{
next;
}	#if count


#自分が未報告の時は一切のエラーを隠す
if($reportflag =~ /未報告/){$attention = "";}	#if

#期限チェック
$dateover = "";
if($DISPFLAG{$setu} == 1){
$dateover = "<hr><span style='color:red;'>（90日消去対象）$DISPFLAG2{$setu}</span>";
}	#if DISPFLAG

if($dateover ne ""){next;}

#
$resultlist .=<<"END_HTML";
<tr>
<td align="center" ><a $editflag href="?code=gameresultform&taikaicode=$taikaicode&category=1&area=$area&kumi=$kumi&kumi0=$kumi0&setu=$setu&num=$num&aitess=$tss2"><img src="img/hensyuu.jpg" alt="編集" width="59" height="32" /></a>
</td>
<td align="center" >$taikainame</td>
<td align="center" >$nichijireport $dateover</td>
<td align="left" >地区名：$areaname<br>　組名：$kuminame</td>
<td align="left" >$aiteteam</td>
<td align="center" >$ground&nbsp;</td>
<td align="center" >&nbsp;$winlose&nbsp;</td>
<td align="center" >&nbsp;$score222&nbsp;</td>
<td align="center" >$reportflag$attention</td>
</tr>
END_HTML
#}	#if tsstemp
}	#foreach vsdata
}	#for
}	#if cate





#######################################################################################
# トーナメント
#######################################################################################
if( $cate == 2 ){
$aitess = "";
$aiteteam = "";
@CNT = (0,1,2,4,8,16,32,64,128);
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1." $sql_str1<br>\n";
for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi0 = $kumi2 = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi0);
if($kuminame =~ /不明/){next;}
#print "areaname=$areaname <br>\n";
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
%TEAMLIST = ();
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#if($taikaicode == 1282 && $area == 1570){print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";}
$k+=2;
}	#foreach x
}	#foreach y

#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan";

#トーナメント○回戦
foreach $y(1..7){
$DISPFLAG = 0;
$DISPFLAG2 = "";
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$nowd = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2) +90;
#print "y=$y $d1 - $d2<br>\n";
#報告範囲内
if( $nowd > $d2){
$DISPFLAG = 1;	#表示
$DISPFLAG2 = $d2;
}	#if

#自分の場所を探す
$cnt2 = $CNT[$y];
$posi = 0;
$aitess = "";
foreach $x(1..$cnt2){
#print "y=$y<br>\n";
#左の枠
if($TEAMLIST{$y}{$x}{1} == $tss){
#print "左<br>";
$posi = 1;
$aitess = $TEAMLIST{$y}{$x}{2};
$num = $y;
$kumi = $x;
last;
}	#if
#右の枠
if($TEAMLIST{$y}{$x}{2} == $tss){
#print "右<br>";
$posi = 2;
$aitess = $TEAMLIST{$y}{$x}{1};
$num = $y;
$kumi = $x;
last;
}	#if
}	#foreach x

if($aitess eq "" || $posi == 0){next;}
#print "$posi <br>";
($aiteteam,$aitesession) = &taikaiteamname_get3($aitess);
$aiteteam = "<a href='?code=mypage_team&ses=$aitesession'>$aiteteam</a>";

#posi確定
#if($posi != 0){
#$aiteteam = &taikaiteamname_get($aitess);
@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));
$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num +2)."回戦";
}	#num

#print "{$taikaicode}{2}{$area}{$kumi}{$num}<br>\n";
#if($REPORTFLAG{$taikaicode}{2}{$area}{$kumi}{$num} ne ""){$reportflag = "<span style='color:green;font-weight:bold;'>報告済<span>";}

$editflag = "";
$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
$tsstemp = "";
$result0 = "";
$result1 = "";
$score = "";
$winlose = "";
$attention = "";
#print "posi=$posi";

#if($posi == 1 ){	#自分が左
#自分の試合結果報告をGET
$sql_str5 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and text1 = $num and linkadr = '$loginuser' and teamnum = $aitess ";
$rs5 = $dbh->prepare($sql_str5);
$rs5->execute();
$count5 = $rs5->rows;	# Hit件数を確保
#print "count5=$count5<br>\n";
$ld1 = -1;
if($count5 == 1){
$REFHASH5 = $rs5->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH5);
#print "s1=$s1<br>\n";
$resultstr = &paramsetsql('resultstr',$REFHASH5);
$result0 = &paramsetsql('result0',$REFHASH5);
$result1 = &paramsetsql('result1',$REFHASH5);
$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";
$editflag = " onClick='return editflag()' ";
#$score = $result0." - ".$result1;
#if($resultstr == 1){$winlose = "○";}	#if win
#if($resultstr == 2){$winlose = "×";}	#if win
#print "serial1=$s1<br>\n";
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH1));
$ld1 = Date::Simple->new($TEMP[0]);
}	#if count1

### 両チームの報告の突き合わせ
#自分の報告書は上にあるので、相手チームの報告をGET
#($aiteteam,$aitesession) = &taikaiteamname_get3($aitess);
#$aiteteam = "<a href='?code=mypage_team&ses=$aitesession'>$aiteteam</a>";
#print "()=($tempname,$aitesession)<br>\n";
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and text1 = $num and teamnum = '$tss' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "sql_str2=$sql_str2<br>\n";
#print "count2=$count2<br>\n";
$ld2 = -1;
if($count2 == 0){
$attention = "相手未報告";
}	#if count2 == 0
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$aite_resultstr = &paramsetsql('resultstr',$REFHASH2);
$aite_result0 = &paramsetsql('result0',$REFHASH2);
$aite_result1 = &paramsetsql('result1',$REFHASH2);
#$score = $aite_result0." - ".$aite_result1;
#if($aite_resultstr == 1){$winlose = "○";}	#if win
#if($aite_resultstr == 2){$winlose = "×";}	#if win
#print "serial2=$s2<br>\n";
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH2));
$ld2 = Date::Simple->new($TEMP[0]);
}	#if count2 == 1

#print "resultstr:$resultstr - aite_resultstr:$aite_resultstr<br>\n";

if($count5 != 0 && $count2 != 0){

$score = $result0." - ".$result1;
if($resultstr == 1){$winlose = "○";}	#if win
if($resultstr == 2){$winlose = "×";}	#if win

#引き分け
if($result0 == $result1){$winlose = "△";}	#if win
#不戦勝
if($resultstr == 4){$winlose = "○";$winlose = "不戦勝";}	#if
#不戦敗
if($resultstr == 5){$winlose = "×";$winlose = "不戦敗";}	#if
#自分が「勝ち」の場合、相手が「負け」以外は「相違！」
if($resultstr == 1 && $aite_resultstr != 2){
#$attention = "対戦相手との戦績登録に相違があります。1";
}	#if
#自分が「勝ち」の場合、相手が「負け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 1 && $aite_resultstr == 2 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
#$attention = "対戦相手との戦績登録に相違があります。1.1";
}	#if

#自分が「負け」の場合、相手が「勝ち」以外は「相違！」
if($resultstr == 2 && $aite_resultstr != 1 && $count2 == 1){
#$attention = "対戦相手との戦績登録に相違があります。2";
}	#if
#自分が「負け」の場合、相手が「勝ち」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 2 && $aite_resultstr == 1 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
#$attention = "対戦相手との戦績登録に相違があります。2.1";
}	#if

#自分が「不戦勝」の場合、相手が「不戦敗」以外は「相違！」
if($resultstr == 4 && $aite_resultstr != 5){
#$attention = "対戦相手との戦績登録に相違があります。3";
}	#if
#自分が「不戦敗」の場合、相手が「不戦勝」以外は「相違！」
if($resultstr == 5 && $aite_resultstr != 4){
#$attention = "対戦相手との戦績登録に相違があります。4";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外は「相違！」
if($resultstr == 3 && $aite_resultstr != 3){
#$attention = "対戦相手との戦績登録に相違があります。5";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 3 && $aite_resultstr == 3 and $result0 != $aite_result0 ){
#$attention = "対戦相手との戦績登録に相違があります。6";
}	#if

}	#if count5 & count2


#注意があれば。
#if($attention ne ""){
#$attention = "<br><span style='color:red;font-size:12px;font-weight:normal;'>$attention</span>";
#}	#if attention



=pot
### 反転
if( $posi == 2 ){	#自分だけ処理する
#報告をGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and linkadr = '$loginuser' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1<br>\n";
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH1);
$resultstr = &paramsetsql('resultstr',$REFHASH1);
print "resultstr=$resultstr<br>\n";
$result0 = &paramsetsql('result0',$REFHASH1);
$result1 = &paramsetsql('result1',$REFHASH1);
$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";
$editflag = " onClick='return editflag()' ";
#print "serial1=$s1<br>\n";
}	#if 報告あり

### 両チームの報告の突き合わせ
#自分の報告書は上にあるので、相手チームの報告をGET
($tempname,$aitesession) = taikaiteamname_get3($aitess);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and linkadr = '$aitesession' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>\n";
if($count2 == 0){
$attention = "相手未報告";
}	#if count2 == 0
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$aite_resultstr = &paramsetsql('resultstr',$REFHASH2);
$aite_result0 = &paramsetsql('result1',$REFHASH2);
$aite_result1 = &paramsetsql('result0',$REFHASH2);
#print "serial2=$s2<br>\n";
}	#if count2 == 1

#print "resultstr:$resultstr - aite_resultstr:$aite_resultstr<br>\n";

$aiteteam = &taikaiteamname_get($aitess);
$tsstemp = $tss;
$score = $result0." - ".$result1;
if($count1 != 0){
#if($result0 > $result1){$winlose = "○";}	#if win
#if($result0 < $result1){$winlose = "×";}	#if win
if($resultstr == 1){$winlose = "○";}	#if win
if($resultstr == 2){$winlose = "×";}	#if win
#引き分け
if($result0 == $result1){$winlose = "△";}	#if win
#不戦勝
if($RESULTSTR{$loginuser} == 4){$winlose = "○";$score = "不戦勝";}	#if
#不戦敗
if($RESULTSTR{$loginuser} == 5){$winlose = "×";$score = "不戦敗";}	#if
#自分が「勝ち」の場合、相手が「負け」以外は「相違！」
if($resultstr == 1 && $aite_resultstr != 2){
$attention = "対戦相手との戦績登録に相違があります。1";
}	#if
#自分が「勝ち」の場合、相手が「負け」以外で、さらにスコアが異なる場合は「相違！」
#print "$resultstr == 1 && $aite_resultstr == 2 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) <br>\n";
if($resultstr == 1 && $aite_resultstr == 2 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) ){
$attention = "対戦相手との戦績登録に相違があります。1.1";
}	#if

#自分が「負け」の場合、相手が「勝ち」以外は「相違！」
if($resultstr == 2 && $aite_resultstr != 1 && $count2 == 1){
$attention = "対戦相手との戦績登録に相違があります。2";
}	#if
#自分が「負け」の場合、相手が「勝ち」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 2 && $aite_resultstr == 1 && ($result0 != $aite_result0 || $result1 != $aite_result1 ) ){
$attention = "対戦相手との戦績登録に相違があります。2.1.";
}	#if

#自分が「不戦勝」の場合、相手が「不戦敗」以外は「相違！」
if($resultstr == 4 && $aite_resultstr != 5){
$attention = "対戦相手との戦績登録に相違があります。3";
}	#if
#自分が「不戦敗」の場合、相手が「不戦勝」以外は「相違！」
if($resultstr == 5 && $aite_resultstr != 4){
$attention = "対戦相手との戦績登録に相違があります。4";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外は「相違！」
if($resultstr == 3 && $aite_resultstr != 3){
$attention = "対戦相手との戦績登録に相違があります。5";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 3 && $aite_resultstr == 3 && $result0 != $aite_result0 ){
$attention = "対戦相手との戦績登録に相違があります。6";
}	#if

}	#if count1
}	#if posi2
=cut

#注意があれば。
if($attention ne ""){
$attention = "<br><span style='color:red;font-size:12px;font-weight:normal;'>$attention</span>";
}	#if attention

$ground = "";
$nichijireport = "";
#if($tsstemp ne ""){	#
#試合日と開催地をGET
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = $kumi and title = $gedan and text1 = $num and (teamnum = $aitess or teamnum = $tss) and (linkadr = '$loginuser' or linkadr = '$aitesession' ) ORDER BY serial ASC ";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$count4 $sql_str4<br>\n";
if($count4 != 0){
$REFHASH4 = $rs4->fetchrow_hashref;
$ground .= &paramsetsql('body',$REFHASH4);
$n = &paramsetsql('nichiji1',$REFHASH4);
@TEMP = split(/ /,$n);
$nichijireport = sprintf("%d年<br>%d月%d日<br>%d時%02d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
}else{
next;
}	#if
#3ヶ月前のは表示しない
$dateover = "";
if( $DISPFLAG == 1  ){
$dateover = "<hr><span style='color:red;'>（90日消去対象）$DISPFLAG2</span>";
}

#自分が未報告の時は一切のエラーを隠す
if($reportflag =~ /未報告/){$attention = "";}	#if
##
if($dateover ne ""){next;}

#if($nichijireport ne ""){
$resultlist2 .=<<"END_HTML";
<tr>
<td align="center" ><a $editflag href="?code=gameresultform&taikaicode=$taikaicode&category=2&area=$area&kumi=$kumi&kumi0=$kumi0&numstr=$numstr&setu=$gedan&num=$num&aitess=$aitess"><img src="img/hensyuu.jpg" alt="編集" width="59" height="32" /></a>
</td>
<td align="center" >$taikainame</td>
<td align="center" >$nichijireport&nbsp;$dateover</td>
<td align="left" >$areaname<br>$kuminame<br>$numstr</td>
<td align="left" >$aiteteam</td>
<td align="center" >$ground&nbsp;</td>
<td align="center" >&nbsp;$winlose&nbsp;</td>
<td align="center" >&nbsp;$score&nbsp;</td>
<td align="center" >$reportflag$attention&nbsp;</td>
</tr>
END_HTML
#}	#if
#}	#tsstemp

#}	#if posi

}	#if nichiji

}	#foreach y

}	#for count

}	#if cate

}	#foreach cate

#############################
}	#for taikai
#####
$resultlist =<<"END_HTML";
<img src="img/riti.jpg" ALT="リーグ戦タイトル" />
<table width="100%" cellspacing="0" class="stane"  >
<tr>
<th width="75" align="center" class="underl" style="font-size: 14px; font-weight: bold;" >&nbsp;</th>
<th width="105" align="center" class="underl" style="font-size: 14px; font-weight: bold;" >大会</th>
<th width="85" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合日</th>
<th width="182" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="85" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
<th width="121" align="center" class="underl" style="font-size: 14px; font-weight: bold;">グラウンド</th>
<th width="67" align="center" class="underl" style="font-size: 14px; font-weight: bold;">勝敗</th>
<th width="67" align="center" class="underl" style="font-size: 14px; font-weight: bold;">スコア</th>
<th width="93" align="center" class="underl" style="font-size: 14px; font-weight: bold;">状態</th>
</tr>
$resultlist
</table>
END_HTML
###
$resultlist2 =<<"END_HTML";
<img src="img/toti.jpg" ALT="トーナメント戦タイトル" />
<table width="100%" cellspacing="0" class="stane">
<tr>
<th width="75" align="center" class="underl" style="font-size: 14px; font-weight: bold;" >&nbsp;</th>
<th width="105" align="center" class="underl" style="font-size: 14px; font-weight: bold;" >大会</th>
<th width="85" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合日</th>
<th width="182" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="85" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
<th width="121" align="center" class="underl" style="font-size: 14px; font-weight: bold;">グラウンド</th>
<th width="67" align="center" class="underl" style="font-size: 14px; font-weight: bold;">勝敗</th>
<th width="67" align="center" class="underl" style="font-size: 14px; font-weight: bold;">スコア</th>
<th width="93" align="center" class="underl" style="font-size: 14px; font-weight: bold;">状態</th>
</tr>
$resultlist2
</table>
END_HTML


###############
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gareti.jpg" alt="試合結果一覧" width="980" height="48" /> </div>
<div id="mainbox">
<h2 id="team" style="background-image:url(img/ter8.jpg)"><span>$teamname</span></h2>
<script>
function editflag(){
if(window.confirm("すでに報告がされています。\\n報告内容を更新する場合は「OK」を、\\n中止する場合には「キャンセル」を押して下さい。")){
return true;
}	//if
return false;
}	//func
</script>

$resultlist

$resultlist2

</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub








# -----------------------------------------------------------------
# 試合結果報告：試合結果報告フォーム
# -----------------------------------------------------------------
sub gameresultform {
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$areaname = &taikaiareaname_get($area);
$kumi = $paramhash{'kumi'};
$kumi0 = $paramhash{'kumi0'};
$numstr = $paramhash{'numstr'};
if($numstr ne ""){$numstr = "　$numstr";}
$kuminame = &taikaikuminame_get($kumi0);
$setu = $paramhash{'setu'};
$num = $paramhash{'num'};
#$posi = $paramhash{'posi'};
$aitess = $paramhash{'aitess'};
$aiteteam = &taikaiteamname_get($aitess);
$taikainame = &taikainame_get($taikaicode);
($teamname,$tss) = &taikaiteamname_get2($loginuser);
#「試合報告書」をGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ORDER BY serial ASC LIMIT 1";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1";
$REFHASH1 = $rs1->fetchrow_hashref;
$nichiji1 = &paramsetsql('nichiji1',$REFHASH1);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH1));
$nichiji1str = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
$ground = &paramsetsql('body',$REFHASH1);
#既存データがあればセット
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' and teamnum = '$aitess' and linkadr = '$loginuser' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$taikaicode = &paramsetsql('taikaicode',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$kumi = &paramsetsql('kumi',$REFHASH1);
$setu = &paramsetsql('title',$REFHASH1);
$teamnum = &paramsetsql('teamnum',$REFHASH1);
$RFLAG[&paramsetsql('resultstr',$REFHASH1)]="selected";
$RFLAG2[&paramsetsql('resultstr2',$REFHASH1)]="selected";
$result0 = &paramsetsql('result0',$REFHASH1);
$result1 = &paramsetsql('result1',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$text1 = &paramsetsql('text1',$REFHASH1);
$senpyo = &paramsetsql('senpyo',$REFHASH1);
$linkadrtitle = &paramsetsql('linkadrtitle',$REFHASH1);
$comment = &paramsetsql('comment',$REFHASH1);
$upfilename = &paramsetsql('upfilename',$REFHASH1);
@CAP = split(/<>/,&paramsetsql('caption',$REFHASH1));
#画像
@IMGTEMPS = split(/:/,$upfilename);
foreach $i(0..2){
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=system/file/$TEMP[0]pda.jpg>$sfn<br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach

#
}	#if 修正


# 対戦組み合わせデータGET
##################################
# リーグ
if($category == 1){
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setutemp,$numtemp,$tss1) = split(/\./,$data1);	#1 1 1
($setutemp,$numtemp,$tss2) = split(/\./,$data2);	#1 1 8
if($tss == $tss2 && $setutemp == $setu && $numtemp == $num){$rflag = 1;}
#if($tss == $tss2 && $setutemp == $setu && $numtemp == $num){$rflag = 0;}
}	#foreach vsdata
}	#if category
##################################
# トーナメント
if($category == 2){
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1."<br>\n";
if($count1 != 0){
$REFHASH1 = $rs1->fetchrow_hashref;
#$area = &paramsetsql('area',$REFHASH1);
#$kumi = &paramsetsql('kumi',$REFHASH1);
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
if($tss == $TEAMLISTTEMP[$k+1]){$rflag = 1;last;}
$k+=2;
}	#foreach x
}	#foreach y
}
#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#自分
($teamname,$teamnumber) = &taikaiteamname_get2($loginuser);
#相手チーム
($tempname,$aitesession) = taikaiteamname_get3($aitess);



#「試合報告書」をGET
#$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = $kumi and title = $gedan and text1 = $num and (teamnum = $aitess or teamnum = $teamnumber) ORDER BY serial ASC LIMIT 1";
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and text1 = '$num' and (teamnum = $aitess or teamnum = $teamnumber) and (linkadr = '$loginuser' or linkadr = '$aitesession') ORDER BY serial ASC LIMIT 1";
#print $sql_str1;
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1";
$REFHASH1 = $rs1->fetchrow_hashref;
$nichiji1 = &paramsetsql('nichiji1',$REFHASH1);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH1));
$nichiji1str = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
$ground = &paramsetsql('body',$REFHASH1);
#
}	#if category 2

##################################
#同じデータでも自分と相手で処理を変える
$posi = 0;
$changeflag =<<"END_HTML";
var r1 = document.getElementById('result0').value;
var r2 = document.getElementById('result1').value;
END_HTML
$husenvalue = "var h1 = 4,h2 = 0;";
$siai =<<"END_HTML";
$teamname <input type="text" name="result0" id="result0" size="2" tabindex="7" value="$result0" style="ime-mode: disabled;" /> - <input type="text" name="result1" id="result1" size="2" tabindex="7" value="$result1" style="ime-mode: disabled;" /> $aiteteam
END_HTML
if($rflag == 1 ){	#反転
$posi = 1;
$changeflag =<<"END_HTML";
r1 = document.getElementById('result1').value;
r2 = document.getElementById('result0').value;
END_HTML
$husenvalue = "var h1 = 0,h2 = 4;";
$siai =<<"END_HTML";
$teamname <input type="text" name="result1" id="result1" size="2" tabindex="7" value="$result1" style="ime-mode: disabled;" /> - <input type="text" name="result0" id="result0" size="2" tabindex="7" value="$result0" style="ime-mode: disabled;" /> $aiteteam
END_HTML
}	#if rflag


###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gareti2.jpg" alt="試合結果報告" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">試合結果報告フォーム</h2>
<div class="box">
チーム名：$teamname
<p>※マークは入力必須項目です。下記の必要事項を入力し、確認ボタンをクリックしてください。</p>
<script>
<!--
function kakunin(){


var re = document.getElementById('resultstr').selectedIndex;
var re2 = document.getElementById('resultstr2').selectedIndex;
if (re == 0 && re2 != 1) {
alert('試合結果が選択されていません。');
return(false);
}

$changeflag



// 不戦勝、不戦敗、中止、以外
if(re < 4 && re2 != 1){
if (r1 == "") {
alert('結果が入力されていません。');
return(false);
}
if (r2 == "") {
alert('結果が入力されていません。');
return(false);
}

/* 半角数字チェック */
if( r1.match( /[^0-9]+/ ) ) {
	alert("結果は半角数字のみで入力して下さい。");
	return(false);
}
/* 半角数字チェック */
if( r2.match( /[^0-9]+/ ) ) {
	alert("結果は半角数字のみで入力して下さい。");
	return(false);
}

r1 -=0;
r2 -=0;
/* 勝敗チェック */
// セレクトで「勝ち」を選んでいるのに、数字が不当な場合
if( re == 1 ){
	if( r1 < r2 ){
		alert("正しい結果を入力して下さい。勝敗チェック1 re="+re+",r1="+r1+",r2="+r2);
		return(false);
	}	//if
}	//if

/* 勝敗チェック */
// セレクトで「負け」を選んでいるのに、数字が不当な場合
if( re == 2 ){
	if(r1 > r2 || r1 == r2 ){
		alert("正しい結果を入力して下さい。勝敗チェック2 re="+re+",r1="+r1+",r2="+r2);
		return(false);
	}	//if
}	//if

/* 勝敗チェック */
// セレクトで「引き分け」を選んでいるのに、数字が不当な場合
if( re == 3 ){
	if(r1 != r2 ){
		alert("正しい結果を入力して下さい。勝敗チェック3 re="+re+",r1="+r1+",r2="+r2);
		return(false);
	}	//if
}	//if

/* セレクトチェック */
// 上：勝ち、下：負け
if( re == 1 && re2 == 2 ){alert("正しい結果を入力して下さい。13");return(false);}
// 上：勝ち、下：負け
if( re == 1 && re2 == 4 ){alert("正しい結果を入力して下さい。15");return(false);}
// 上：勝ち、下：負け
if( re == 1 && re2 == 6 ){alert("正しい結果を入力して下さい。17");return(false);}

/* セレクトチェック */
// 上：負け、下：中止
if( re == 2 && re2 == 1 ){alert("正しい結果を入力して下さい。22");return(false);}
// 上：負け、下：勝ち
if( re == 2 && re2 == 3 ){alert("正しい結果を入力して下さい。24");return(false);}
// 上：負け、下：勝ち
if( re == 2 && re2 == 5 ){alert("正しい結果を入力して下さい。26");return(false);}
// 上：負け、下：勝ち
if( re == 2 && re2 == 7 ){alert("正しい結果を入力して下さい。28");return(false);}


}else{
//if (r1 != "") {
//alert('結果が正しく入力されていません。');
//return(false);
//}

//if (r2 != "") {
//alert('結果が正しく入力されていません。');
//return(false);
//}


}	// 不戦勝、不戦敗、中止、以外







if (document.getElementById('comment').value == "") {
alert('相手チームへのコメントが入力されていません。');
return(false);
}


if(window.confirm("この内容で登録します。\\nよろしければ「OK」を押して下さい。\\n修正する場合には「キャンセル」を押して下さい。")){
return true;
}

return false;
}
-->
</script>
<form action="system.cgi" name="form1" method="post" enctype="multipart/form-data" accept-charset="UTF-8" onSubmit="return kakunin()">
<input type="hidden" name="code" value="gameresultformadd" />
<input type="hidden" name="taikaicode" value="$taikaicode" />
<input type="hidden" name="category" value="$category" />
<input type="hidden" name="area" value="$area" />
<input type="hidden" name="kumi" value="$kumi" />
<input type="hidden" name="setu" value="$setu" />
<input type="hidden" name="num" value="$num" />
<input type="hidden" name="posi" value="$posi" />
<input type="hidden" name="aitess" value="$aitess" />

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">試合日時</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" bgcolor="#ffffff">$nichiji1str</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">名称</font></td>
<td bgcolor="#ffffff">地区名：$areaname<br>　$kuminame$numstr</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">対戦チーム</font></td>
<td bgcolor="#ffffff">$aiteteam</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">グラウンド情報</td>
<td bgcolor="#ffffff">$ground&nbsp;</td>
</tr>


<tr>
<td align="center" bgcolor="#F2F2F2">試合結果<font class="type1" color="#ff0000">*</font></td>
<td bgcolor="#ffffff">
<select name="resultstr" id="resultstr" onChange="resel()">
<option value="" $RFLAG[0]>選択</option>
<option value="1" $RFLAG[1]>勝ち</option>
<option value="2" $RFLAG[2]>負け</option>
<option value="3" $RFLAG[3]>引き分け</option>
<option value="4" $RFLAG[4]>不戦勝</option>
<option value="5" $RFLAG[5]>不戦敗</option>
</select>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">試合結果2</td>
<td bgcolor="#ffffff">
<select name="resultstr2" id="resultstr2">
<option value="" $RFLAG[5]>選択</option>
<option value="7" $RFLAG[7]>コールド勝ち</option>
<option value="8" $RFLAG[8]>コールド負け</option>
<option value="9" $RFLAG[9]>延長勝ち</option>
<option value="10" $RFLAG[10]>延長負け</option>
<option value="11" $RFLAG[11]>サヨナラ勝ち</option>
<option value="12" $RFLAG[12]>サヨナラ負け</option>
</select>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">結果　<font class="type1" color="#ff0000">※半角数字</font></td>
<td bgcolor="#ffffff">

$siai

</td>
</tr>

<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">戦評</font></td>
<td bgcolor="#ffffff"><textarea rows="10" cols="60" name="senpyo" id="senpyo" tabindex="29">$senpyo</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">相手チームへのコメント</font><font class="type1" color="#ff0000">*</font></td>
<td bgcolor="#ffffff"><textarea rows="10" cols="60" name="comment" id="comment" tabindex="29">$comment</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像1</font></td>
<td bgcolor="#ffffff"><input type="file" name="file0" id="file0" />
$IMGSRC[0]$FILENAME[0]$FILEDELETE[0]<br>
<font class="type1" color="#ff0000">※「2MB以下までの画像をお入れください」もしくは「2000px　×　2000px以内」</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像1の説明</font></td>
<td bgcolor="#ffffff">
<input type="text" size="60" maxlength="50" name="caption0" id="caption0" value="$CAP[0]" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像2</font></td>
<td bgcolor="#ffffff"><input type="file" name="file1" id="file1" />
$IMGSRC[1]$FILENAME[1]$FILEDELETE[1]<br>
<font class="type1" color="#ff0000">※「2MB以下までの画像をお入れください」もしくは「2000px　×　2000px以内」</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像2の説明</font></td>
<td bgcolor="#ffffff">
<input type="text" size="60" maxlength="50" name="caption1" id="caption1" value="$CAP[1]" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像3</font></td>
<td bgcolor="#ffffff"><input type="file" name="file2" id="file2" />
$IMGSRC[2]$FILENAME[2]$FILEDELETE[2]<br>
<font class="type1" color="#ff0000">※「2MB以下までの画像をお入れください」もしくは「2000px　×　2000px以内」</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">画像3の説明</font></td>
<td bgcolor="#ffffff">
<input type="text" size="60" maxlength="50" name="caption2" id="caption2" value="$CAP[2]" />
</td>
</tr>
</tbody>
</table>

<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　報告する　　" />
</div>
</form>
</div>
</div>
<script>
var abort = 0;
function aborttag(){
if(abort == 0){
document.getElementById('resultstr').disabled = true;
document.getElementById('resultstr2').disabled = true;
document.getElementById('result0').disabled = true;
document.getElementById('result1').disabled = true;
abort = 1;
}else{
document.getElementById('resultstr').disabled = false;
document.getElementById('resultstr2').disabled = false;
document.getElementById('result0').disabled = false;
document.getElementById('result1').disabled = false;
abort = 0;
}	//if
}	//func

function resel(){
$husenvalue
document.getElementById('result0').disabled = false;
document.getElementById('result1').disabled = false;
var i = document.getElementById('resultstr').selectedIndex;
if(i == 3){
document.getElementById('resultstr2').disabled = true;
}else{
document.getElementById('resultstr2').disabled = false;
}	//if
if(i == 4){
document.getElementById('result0').value = h1;
document.getElementById('result1').value = h2;
document.getElementById('result0').disabled = true;
document.getElementById('result1').disabled = true;
}	//if
if(i == 5){
document.getElementById('result0').value = h2;
document.getElementById('result1').value = h1;
document.getElementById('result0').disabled = true;
document.getElementById('result1').disabled = true;
}	//if

}	//func
</script>
END_HTML
#
&taikaihtmldisp($mes);
exit;
}	#sub

# -----------------------------------------------------------------
# 試合結果報告：試合結果報告フォーム：登録
# -----------------------------------------------------------------
sub gameresultformadd {
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
$setu = $paramhash{'setu'};
$num = $paramhash{'num'};
$posi = $paramhash{'posi'};
$body = $paramhash2{'body'};
$aitess = $paramhash{'aitess'};
$resultstr = $paramhash2{'resultstr'};
$resultstr2 = $paramhash2{'resultstr2'};
$result0 = $paramhash2{'result0'};
$result1 = $paramhash2{'result1'};
$senpyo = $paramhash2{'senpyo'};
$comment = $paramhash2{'comment'};
if($resultstr == 4){
$result0 = 4;
$result1 = 0;
}	#if
if($resultstr == 5){
$result0 = 0;
$result1 = 4;
}	#if

# --------------------------
# 添付ファイルの登録処理
$upfilename = "";
$caption = "";
foreach $i(0..2){
if($paramhash{"file$i"} ne ""){$file = &fileup("file$i",$contents,"system/");}else{$file = $paramhash2{"filename$i"};}
if($paramhash{"filedelete$i"} == 1){$file = "";}
$upfilename .= $file.":";
#キャプション
$caption .= $paramhash2{"caption$i"}."<>";
}	#foreach


#重複チェック
$sql_str = "SELECT * FROM $dbname WHERE contents = 35 and linkadr = '$loginuser' and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' and linkadrtitle = '$posi' and linkadr = '$loginuser' and  teamnum = '$aitess' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};

#アップデート
$str ="body = '$body',";
$str.="nichiji1 = '$nichiji1',";
$str.="resultstr = '$resultstr',";
$str.="resultstr2 = '$resultstr2',";
$str.="result0 = '$result0',";
$str.="result1 = '$result1',";
$str.="senpyo = '$senpyo',";
$str.="comment = '$comment',";
$str.="upfilename = '$upfilename',";
$str.="caption = '$caption',";
chop $str;
$sql_str = "UPDATE $dbname SET $str WHERE serial = $serial ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
# 既に報告があれば、一応警告
$attention =<<"END_HTML";
<p style="color:red;">※この日の報告は既に受け付けておりますが、最新の情報に更新しました。</p>
END_HTML

}else{
#DB
# 新規登録
$sql_str = qq{INSERT INTO $dbname(contents,koukaiflag,taikaicode,category,area,kumi,title,text1,linkadrtitle,body,nichiji1,linkadr,teamnum,resultstr,resultstr2,result0,result1,senpyo,comment,upfilename,caption) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
35,
0,
$taikaicode,
$category,
$area,
$kumi,
$setu,
$num,
$posi,
$body,
$nichiji1,
$loginuser,
$aitess,
$resultstr,
$resultstr2,
$result0,
$result1,
$senpyo,
$comment,
$upfilename,
$caption,
);
}	#if
&sqlcheck($sql_str);

###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gareti2.jpg" alt="試合結果報告" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">試合結果報告フォーム</h2>
<div class="box">
$attention
<p>報告完了</p>
<input type=button onClick="location.href='?code=gameresult'" value="試合結果一覧ページに戻る" /><p>
<input type=button onClick="location.href='system.cgi'" value="マイページに戻る" />
</div>
</div>
</div>
END_HTML
#
&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# マイページ：チーム情報
# -----------------------------------------------------------------
sub mypage_team {
$ses = $paramhash{'ses'};
if($ses eq ""){
$ses = $loginuser;
}	#if
if($ses eq ""){
$mes =<<"END_HTML";
チームが未指定です。
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if

$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
#$mes =<<"END_HTML";
#END_HTML
&mypagehtmldisp("指定のチームが見つかりません。");
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
#$ssid = &paramsetsql('ssid');
$teamserial = &paramsetsql('serial');
$teamname = &paramsetsql('teamname');
#print "$teamserial,$teamname<br>\n";
$team_kana = &paramsetsql('team_kana');
$shimei1 = &paramsetsql('shimei1');
$shimei_kana2 = &paramsetsql('shimei_kana2');
$team_abbr = &paramsetsql('team_abbr');
$team_year = &paramsetsql('team_year');
$team_hp = &paramsetsql('team_hp');
if($team_hp ne ""){$team_hp = "<a href='$team_hp' target='_blank'>$team_hp</a>";}
$katsudou_week = &paramsetsql('katsudou_week');
$average_age = &paramsetsql('average_age');
$team_pref = &paramsetsql('team_pref');
$team_cities = &paramsetsql('team_cities');
$past_perform = &paramsetsql('past_perform');
$team_pr = &paramsetsql('team_pr');
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
#画像
$i = 0;
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=system/file/$TEMP[0]myteam.jpg>";}
}	#if 存在
#チームメンバー
$n = 0;
foreach $line(split(/<>/,&paramsetsql('teammember'))){
($TMNAME[$n],$TMNUM[$n],$TMPOSITION[$n]) = split(/:/,$line);
if($TMNAME[$n] ne ""){
$memberlist .=<<"END_HTML";
<li>$TMNAME[$n] / $TMNUM[$n] / $TMPOSITION[$n]</li>
END_HTML
$n++;
}	#if
}	#foreach
#お知らせ
$whatnew = "";
$sql_str = "SELECT * FROM othercontents WHERE contents = 100 and koukaiflag = 0 and ( ( TO_DAYS(nichiji_from) <= TO_DAYS(NOW()) and TO_DAYS(NOW()) <= TO_DAYS(nichiji_to) ) or (TO_DAYS(nichiji_from) = TO_DAYS(nichiji_to) )) ORDER BY nichiji DESC";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck;	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i=0;$i<$count;$i++){
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql2('title');
$body = &paramsetsql('body');
if($body ne ""){
$title = "<a href='$body'>$title</a>";
}	#if
$nichiji = &paramsetsql('nichiji');
$nichiji =~ s/-/\//g;
$whatnew .=<<"END_HTML";
<dt>$nichiji</dt>
<dd>$title</dd>
END_HTML
}	#for


#($teamname,$tss) = &taikaiteamname_get2($ses);
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}

foreach $cate($sc .. $ec){

####################################
# 試合予定：リーグ
####################################
if( $cate == 1 ){
$taikainame = &taikainame_get($taikaicode, $cate);
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag != 9 and taikaicode = '$taikaicode' and category = 1 ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1<br>";
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}
#print "$vsdata<br>\n";
#試合期日
$n = Date::Simple->new();
foreach(split(/<>/,$body)){
($setutemp,$nichiji1,$nichiji2) = split(/:/,$_);
$nichijistr = sprintf("%d年%d月%d日",split(/-/,$nichiji1))."〜<br>";
$nichijistr .= sprintf("%d年%d月%d日",split(/-/,$nichiji2))."まで";
$NISHIJISTR{$setutemp} = $nichijistr;
if($nichiji1 eq "" || $nichiji2 eq "" || $nichiji1 eq "0000-00-00" || $nichiji2 eq "0000-00-00"){next;}
#print "($setutemp,$nichiji1,$nichiji2)<br>\n";
$n1 = Date::Simple->new($nichiji1);
$n2 = Date::Simple->new($nichiji2);
#print "$nichiji1,$nichiji2<br>\n";
if($n > $n2){
$DISPFLAG{$setutemp} = 0;	#非表示
$DISPFLAG2{$setutemp} = $n2;
}else{
$DISPFLAG{$setutemp} = 1;	#表示
}	#if
}	#foreach

# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($tss1 eq "" || $tss2 eq ""){next;}
if($teamserial != $tss1 && $teamserial != $tss2){next;}

if($teamserial != $tss1){($tss1,$tss2)=($tss2,$tss1);}
$aiteteam = &taikaiteamname_get($tss2);

#$temp = "$taikaicode:$area:$kumi:$setu:$tss";
#if($nichiji1 ne ""){
#期限チェック
#if($DISPFLAG{$setu} == 1){
### 両チームの報告の突き合わせ
#($tempname,$aitesession) = taikaiteamname_get3($tss2);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ORDER BY serial ASC LIMIT 1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>\n";
$attention = "";
if($count2 > 0){
$REFHASH2 = $rs2->fetchrow_hashref;
#$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
#$n1 = &paramsetsql('nichiji1',$REFHASH2);
#$REFHASH2 = $rs2->fetchrow_hashref;
#$teamnum2 = &paramsetsql('teamnum',$REFHASH2);
#$n2 = &paramsetsql('nichiji1',$REFHASH2);
#if($n1 ne $n2){$attention = "<br><span style='color:red;'>報告に相違があります。</span>";}else{$attention = "";}
#}	#if count2 == 2
#if($count2 == 1){
#$REFHASH2 = $rs2->fetchrow_hashref;
#$teamnumtemp = &paramsetsql('teamnum',$REFHASH2);
#if($tss == $teamnumtemp){$attention = "<br><span style='color:red;'></span>";}else{$attention = "<br><span style='color:red;'>相手が未報告です。</span>";}
#}	#if

#$flag = 0;
#相手の報告データをGET
#$sql_str1 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = '$setu' and teamnum = '$tss2' ";
#$rs1 = $dbh->prepare($sql_str1);
#$rs1->execute();
#$count1 = $rs1->rows;	# Hit件数を確保
#if($count1 != 0){
#$REFHASH1 = $rs1->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH1);
#$area = &paramsetsql('area',$REFHASH1);
#$kumi = &paramsetsql('kumi',$REFHASH1);
#$setu = &paramsetsql('title',$REFHASH1);
#$nichiji1 = &paramsetsql('nichiji1',$REFHASH1);
#$flag++;
#}	#if count
#相手の報告データをGET
#$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = '$setu' and teamnum = '$teamserial' ";
#$rs2 = $dbh->prepare($sql_str2);
#$rs2->execute();
#$count2 = $rs2->rows;	# Hit件数を確保
#if($count2 > 0){
#$REFHASH2 = $rs2->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH2);
#$area = &paramsetsql('area',$REFHASH2);
#$kumi = &paramsetsql('kumi',$REFHASH2);
#$setu = &paramsetsql('title',$REFHASH2);
$nichiji1 = &paramsetsql('nichiji1',$REFHASH2);
#$flag++;
#}	#if count
#print "count1=$count1 count2=$count2<br>\n";

#if($nichiji1 ne $nichiji2 || $flag != 2){
#print "($nichiji1 ne $nichiji2)<br>";
#next;}	#if

@TEMP = split(/ /,$nichiji1);
#print "$nichiji1<br>\n";
#if($TEMP[0] eq "0000-00-00" || $TEMP[0] eq ""){next;}
#if($aiteteam ne "" && Date::Simple->new($TEMP[0]) > Date::Simple->new() ){
#print "a+";
$nichijitemp = sprintf("%d年%d月%d日<br>%d時%02d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));

#試合期限後は表示しない
if($DISPFLAG{$setu} == 0){
$dateover = "<hr><span style='color:red;'>（消去対象）試合の対戦期限$DISPFLAG2{$setu}</span>";}else{$dateover = "";
}

if($dateover ne ""){next;}


#if($teamserial == $tss1 ){	#自分だけ処理する
#$aiteteam = &taikaiteamname_get($tss2);
$schedulelist .=<<"END_HTML";
<tr>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row" nowrap>$nichijitemp$dateover</th>
<th align="left" scope="row" nowrap>$areaname<br>$kuminame</th>
<th align="center" scope="row">$aiteteam</th>
</tr>
END_HTML
#}	#if tss
#if( $teamserial == $tss2){	#自分だけ処理する
#$aiteteam = &taikaiteamname_get($tss1);
#$schedulelist .=<<"END_HTML";
#<tr>
#<th align="center" scope="row">$taikainame</th>
#<th align="center" scope="row" nowrap>$nichijitemp</th>
#<th align="left" scope="row" nowrap>$areaname<br>$kuminame</th>
#<th align="center" scope="row">$aiteteam</th>
#</tr>
#END_HTML
#}	#if tss
}	#if count

#}	#if DISPFLAG
}	#foreach vsdata
}	#for k
}	#if cate
}	#for cate
}	#for count




####################################
# 試合予定：トーナメント
####################################
@CNT = (0,1,2,4,8,16,32,64,128);

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
#print "taikaicode=$taikaicode<br>\n";
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}
foreach $cate($sc .. $ec){
if( $cate == 2 ){
$taikainame = &taikainame_get($taikaicode, $cate);
$setu = "";
$kumi = "";
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and category = 2 and taikaicode = '$taikaicode' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#if($taikaicode == 1382){print " $count1 sql_str1=$sql_str1<br>";}
for($jj = 0;$jj < $count1;$jj++){
#if($taikaicode == 1382){print "jj=$jj<hr>";}
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$kumi = &paramsetsql('kumi',$REFHASH1);
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
#print &paramsetsql('body',$REFHASH1)."<p>";
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
%TEAMLIST = ();
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
$k+=2;
}	#foreach x
}	#foreach y
#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print $gedan."<br>";
#トーナメント○回戦
foreach $y(1..7){
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
$dateover = "";
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#試合期限後は表示しない
$n = Date::Simple->new();
$n2 = Date::Simple->new($n2);
if( $n > $n2 ){
$dateover = "<hr><span style='color:red;'>（消去対象）試合の対戦期限$n2</span>";
}
}


$cnt2 = $CNT[$y];
$num = $y;
$aitess = "";
foreach $x(1..$cnt2){
#if($TEAMLIST{$y}{$x}{1} eq "" || $TEAMLIST{$y}{$x}{2} eq ""){next;}
$tss    = $TEAMLIST{$y}{$x}{1};
$aitess = $TEAMLIST{$y}{$x}{2};
if($tss eq "" || $aitess eq ""){next;}
if($tss != $teamserial && $aitess != $teamserial ){next;}

($temp,$aitesestemp1) = &taikaiteamname_get3($tss);
($temp,$aitesestemp2) = &taikaiteamname_get3($aitess);
@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));
$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){$numstr = "".($gedan - $num+2)."回戦";}	#num

$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = $x and text1 = $y and ( (teamnum = $tss and linkadr = '$aitesestemp2') or (teamnum = $aitess and linkadr = '$aitesestemp1') ) ORDER BY serial ASC LIMIT 1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
&sqlcheck($sql_str2);
$count2 = $rs2->rows;	# Hit件数を確保
#if($taikaicode == 1382){print "$TEAMLIST{$y}{$x}{1} || $TEAMLIST{$y}{$x}{2} $count2 $sql_str2<br>";}
#if($count2 != 0){print "$count2 sql_str2=$sql_str2<br>";}
#for($h=0;$h<$count2;$h++){
if($count2 == 0){next;}
#print "$count2 <br>";
$REFHASH2 = $rs2->fetchrow_hashref;
$sss = &paramsetsql('serial',$REFHASH2);
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
$linkadr = &paramsetsql('linkadr',$REFHASH2);
#報告相手のシリアルが自分で、登録者のsesが一致しない場合はスルー
if($teamnum1 == $teamserial){
	if($linkadr ne $aitesestemp1 && $linkadr ne $aitesestemp2){next;}
}
#報告者が自分で、登録相手のssが一致しない場合はスルー
if($ses eq $linkadr){
	if($tss != $teamnum1 && $aitess != $teamnum1){next;}
}

$n1 = &paramsetsql('nichiji1',$REFHASH2);
$area2 = &paramsetsql('area',$REFHASH2);
$areaname = &taikaiareaname_get($area2);
if($areaname =~ "不明"){next;}

if($teamnum1 == $teamserial ){
($aiteteam,$teamnum1) = &taikaiteamname_get2($linkadr);
}else{
$aiteteam = &taikaiteamname_get($teamnum1);
}	#If
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$area2 = &paramsetsql('area',$REFHASH2);
$areaname = &taikaiareaname_get($area2);
if($areaname =~ "不明"){next;}


#対戦日時のGET
@TEMP = split(/ /,$n1);
($yy,$mm,$d) = split(/-/,$TEMP[0]);
$mm -=0;
$d -=0;
$nichijitemp  = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
$nichijitemp .= "<br>".sprintf("%d時%02d分",split(/:/,$TEMP[1]));
$ground = $ground1;

if($dateover ne ""){next;}
##
$schedulelist .=<<"END_HTML";
<tr>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row" nowrap>$nichijitemp$dateover</th>
<th align="left" scope="row" nowrap>$areaname<br>$numstr</th>
<th align="center" scope="row">$aiteteam</th>
</tr>
END_HTML
#}	#for h
}	#for x
#}	#if nichiji
}	#foreach y
}	#for k
}	#if cate
}	#foreach cate
}	#for i






########################################################################
# 最新の試合結果：リーグ
########################################################################
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$taikainame = &taikainame_get($taikaicode,1,1);	#大会名GET

#print "taikaicode=$taikaicode<br>\n";

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1  ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 sql_str1=$sql_str1<br>\n";
for($k=0;$k<$count;$k++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}

# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($tss1 eq "" || $tss2 eq ""){next;}
if($teamserial != $tss1 && $teamserial != $tss2){next;}

if($teamserial != $tss1){($tss1,$tss2)=($tss2,$tss1);}
$aiteteamname = &taikaiteamname_get($tss2);

#print "ok<br>";

$teamnum1="";
$syouhai1="";
$result10="";
$result11="";
$result20="";
$result21="";
$score="";

#試合結果をGET（自分）
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = $setu and text1 = $num and teamnum = $tss2 ";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4 =$count4 sql_str4=$sql_str4<br>\n";
$ld1 = -1;
if($count4 != 1 ){next;}
$REFHASH4 = $rs4->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH4);
$syouhai1 = &paramsetsql('resultstr',$REFHASH4);
#$SYOUHAI{$teamnum1} = $syouhai1;
$result10 = &paramsetsql('result0',$REFHASH4);
$result11 = &paramsetsql('result1',$REFHASH4);
if( &paramsetsql('linkadrtitle',$REFHASH4) && ($syouhai1 != 4 && $syouhai1 != 5) ){($result10,$result11)=($result11,$result10);}
$date1 = &paramsetsql('timestamp',$REFHASH4);
@TEMP1 = split(/ /,$date1);
$dates1 = sprintf("%04d%02d%02d%02d%02d%02d",split(/-/,$TEMP1[0]),split(/:/,$TEMP1[1]));
$dates11 = Date::Simple->new($TEMP1[0]);
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH4));
$ld1 = Date::Simple->new($TEMP[0]);

#試合結果をGET（相手のチーム）
$sql_str5 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = $setu and text1 = $num and teamnum = $tss1 ";
$rs5 = $dbh->prepare($sql_str5);
$rs5->execute();
&sqlcheck($sql_str5);
$count5 = $rs5->rows;	# Hit件数を確保
#print "count5 =$count5 sql_str5=$sql_str5<br>\n";
$ld2 = -1;
if($count5 != 1 ){next;}
$REFHASH5 = $rs5->fetchrow_hashref;
$teamnum2 = &paramsetsql('teamnum',$REFHASH5);
$syouhai2 = &paramsetsql('resultstr',$REFHASH5);
#$SYOUHAI{$teamnum2} = $syouhai2;
$result20 = &paramsetsql('result0',$REFHASH5);
$result21 = &paramsetsql('result1',$REFHASH5);
if( &paramsetsql('linkadrtitle',$REFHASH5) && ($syouhai2 != 4 && $syouhai2 != 5)){($result20,$result21)=($result21,$result20);}
$date2 = &paramsetsql('timestamp',$REFHASH5);
@TEMP2 = split(/ /,$date2);
$dates2 = sprintf("%04d%02d%02d%02d%02d%02d",split(/-/,$TEMP2[0]),split(/:/,$TEMP2[1]));
$dates22 = Date::Simple->new($TEMP2[0]);
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH5));
$ld2 = Date::Simple->new($TEMP[0]);

#print "($count4 != 1 && $count5 != 1)<br>\n";
#print "($syouhai1 == 1 && $syouhai2 != 2)<br>\n";

if($syouhai1 == 1 && $syouhai2 != 2){next;}	#if
if($syouhai1 == 2 && $syouhai2 != 1){next;}	#if
if($syouhai1 == 3 && $syouhai2 != 3){next;}	#if
if($syouhai1 == 4 && $syouhai2 != 5){next;}	#if
if($syouhai1 == 5 && $syouhai2 != 4){next;}	#if

#相違がある場合
if( $result10 != $result21 || $result11 != $result20 ){next;}

$nichijireport = "";
#print "OK";
#各チームの報告から「試合日時」と「場所」をGET
$sql_str6 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$kumi' and title = '$setu'  and text1 = '$num' ORDER BY serial ASC LIMIT 1";
$rs6 = $dbh->prepare($sql_str6);
$rs6->execute();
$count6 = $rs6->rows;	# Hit件数を確保
#print "count1=$count1 sql_str1=$sql_str1<br>\n";
#print "count=".$count1."<br>"; 
=pot
if($count6 == 2){
#チーム１
$REFHASH6 = $rs6->fetchrow_hashref;
$taikaicode = &paramsetsql('taikaicode',$REFHASH6);
$ground1 = &paramsetsql('body',$REFHASH6);
$n1 = &paramsetsql('nichiji1',$REFHASH6);
@TEMP = split(/ /,$n1);
$nichijireport = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
#$teamnum1 = &paramsetsql('teamnum',$REFHASH1);
#チーム２
$REFHASH6 = $rs1->fetchrow_hashref;
$ground2 = &paramsetsql('body',$REFHASH6);
$n2 = &paramsetsql('nichiji1',$REFHASH6);
#$teamnum2 = &paramsetsql('teamnum',$REFHASH1);
#入力チェック
#print "$n1 ne $n2<br>";
#if($n1 eq $n2){
#if($ground1 ne $ground2){
#$ground1 .= "（$ground2）";
#$ground2 ="";
#}	#if
#}	#if n1 n2
}	#if count1 = 2
=cut
$nichijireport ="";
if($count6 == 1){
$REFHASH6 = $rs6->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH6);
#$ground1 = &paramsetsql('body',$REFHASH6);
$n1 = &paramsetsql('nichiji1',$REFHASH6);
@TEMP = split(/ /,$n1);
$nichijireport = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
}	#if count1 = 1

#print "ok"; 

=pot
#3ヶ月前のは表示しない
$n1 = Date::Simple->new();
if($n ne ""){
$n2 = Date::Simple->new($TEMP[0]);
}else{
if($ld1 > $ld2 ){$ld1 = $ld2;}
$n2 = $ld1;
}	#if
if( ($n1 - $n2) > 30){$dateover = "<hr><span style='color:red;'>（30日消去対象）$n2</span>";}else{$dateover = "";}
=cut


#if($dates11 > $dates22){	#新しい方の報告日
#$date0 = $dates1;
#$date00 = $dates11;
#}else{
#$date0 = $dates2;
#$date00 = $dates22;
#}	#if

#print "($teamnum2 == $tss)<br>"; 

#自分のチームの結果報告
#if($tss2 == $teamserial){
if($result10 eq "" && $result11 eq ""){$winlose="";}else{$winlose="△";}
$score = $result10." - ".$result11;

if($syouhai1 == 1 ){
$winlose="○";
#if($score0 < $score1){$score = $score0." - ".$score1;}
#if($score0 > $score1){$score = $score1." - ".$score0;}
}	#if syousai
if($syouhai1 == 2 ){
$winlose="×";
$score = $result10." - ".$result11;
#if($score0 < $score1){$score = $score1." - ".$score0;}
#if($score0 > $score1){$score = $score0." - ".$score1;}
}	#if syousai
if($syouhai1 == 4){
$winlose="○";
$score = "不戦勝";
#if($score0 < $score1){$score = $score1." - ".$score0;}
#if($score0 > $score1){$score = $score0." - ".$score1;}
}	#if syousai
if($syouhai1 == 5){
$winlose="×";
$score = "不戦敗";
#if($score0 < $score1){$score = $score1." - ".$score0;}
#if($score0 > $score1){$score = $score0." - ".$score1;}
}	#if syousai


$resultlist .=<<"END_HTML";
<tr>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$nichijireport</th>
<th align="left" scope="row">$areaname<br>$kuminame</th>
<th align="left" scope="row">$aiteteamname</th>
<th align="center" scope="row" nowrap>&nbsp;$winlose&nbsp;</th>
<th align="center" scope="row" nowrap>&nbsp;$score&nbsp;</th>
</tr>
END_HTML
#}	#if teamnum2

=pot
#自分のチームの報告のみ（VS左）
if($tss1 == $teamserial){
$winlose="△";
$score = $result20." - ".$result21;
if($syouhai2 == 1 || $syouhai2 == 4){
$winlose="×.";
#if($score0 < $score1){$score = $score0." - ".$score1;}
#if($score0 > $score1){$score = $score1." - ".$score0;}
}
if($syouhai2 == 2 || $syouhai2 == 5){
$winlose="○.";
#if($score0 < $score1){$score = $score1." - ".$score0;}
#if($score0 > $score1){$score = $score0." - ".$score1;}
}
$resultlist .=<<"END_HTML";
<tr>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$n1</th>
<th align="left" scope="row">$areaname<br>$kuminame</th>
<th align="left" scope="row">$teamnum2name</th>
<th align="center" scope="row">&nbsp;$winlose</th>
<th align="center" scope="row" nowrap>&nbsp;$score</th>
</tr>
END_HTML
}	#if teamnum1
=cut


}	#foreach vsdata
}	#for k
}	#for i





########################################################################
# 最新の試合結果：トーナメント
########################################################################
@CNT = (0,1,2,4,8,16,32,64,128);
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}

foreach $cate($sc .. $ec){
$taikainame = &taikainame_get($taikaicode, $cate,1);

if( $cate == 2 ){

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1."<br>\n";
for($jj=0;$jj<$count1;$jj++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";
$k+=2;
}	#foreach x
}	#foreach y
$gedan = 0;
#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan<br>";

#トーナメント○回戦
foreach $y(1..7){
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
#print "($n1,$n2)<br>";
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$d = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2);
#報告範囲内
#if( $d1 <= $d && $d <= $d2){
#自分の場所を探す
$aitess = "";
$posi = 0;
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
#print "y=$y<br>\n";
#左の枠
if($TEAMLIST{$y}{$x}{1} == $teamserial){
#print "左<br>";
$posi = 1;
$aitess = $TEAMLIST{$y}{$x}{2};
$num = $y;
$kumi = $x;
last;
}	#if
#右の枠
if($TEAMLIST{$y}{$x}{2} == $teamserial){
#print "右<br>";
$posi = 2;
$aitess = $TEAMLIST{$y}{$x}{1};
$num = $y;
$kumi = $x;
last;
}	#if
}	#foreach x

if($aitess eq "" || $posi == 0){next;}
#print "$posi <br>";

@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));
$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num +2)."回戦";
}	#num




$editflag = "";
$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
$tsstemp = "";
$result0 = "";
$result1 = "";
$score = "";
$winlose = "";
$attention = "";

#if($posi == 1 ){	#自分が左
#自分の試合結果報告をGET
$sql_str5 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and text1 = '$num' and linkadr = '$ses' and teamnum = $aitess ";
$rs5 = $dbh->prepare($sql_str5);
$rs5->execute();
$count5 = $rs5->rows;	# Hit件数を確保
#print "count5=$count5<br>\n";
$ld1 = -1;
if($count5 != 1){next;}
$REFHASH5 = $rs5->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH5);
$resultstr = &paramsetsql('resultstr',$REFHASH5);
$result0 = &paramsetsql('result0',$REFHASH5);
$result1 = &paramsetsql('result1',$REFHASH5);
$reportflag = "<span style='color:green;font-weight:bold;'>報告済</span>";
$editflag = " onClick='return editflag()' ";
#print "serial1=$s1<br>\n";
$score = $result0." - ".$result1;
if($resultstr == 1){$winlose = "○";}	#if win
if($resultstr == 2){$winlose = "×";}	#if win
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH5));
$ld1 = Date::Simple->new($TEMP[0]);


### 両チームの報告の突き合わせ
#自分の報告書は上にあるので、相手チームの報告をGET
($aiteteam,$aitesession) = taikaiteamname_get3($aitess);
#print "()=($tempname,$aitesession)<br>\n";
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and text1 = '$num' and title = '$gedan' and teamnum = '$teamserial' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>\n";
$ld2 = -1;
if($count2 != 1){next;}
#print "sql_str2=$sql_str2<br>\n";
if($count2 == 0){
$attention = "相手未報告";
}	#if count2 == 0
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$aite_resultstr = &paramsetsql('resultstr',$REFHASH2);
$aite_result0 = &paramsetsql('result0',$REFHASH2);
$aite_result1 = &paramsetsql('result1',$REFHASH2);
#print "serial2=$s2<br>\n";
@TEMP = split(/ /,&paramsetsql('timestamp',$REFHASH2));
$ld2 = Date::Simple->new($TEMP[0]);
}	#if count2 == 1

#print "resultstr:$resultstr - aite_resultstr:$aite_resultstr<br>\n";

if($count5 != 0 && $count2 != 0){

#相違がある場合
if($result0 != $aite_result1 || $result1 != $aite_result0 ){next;}



#引き分け
if($result0 == $result1){$winlose = "△";}	#if win
#不戦勝
if($resultstr == 4){$winlose = "○";$score = "不戦勝";}	#if
#不戦敗
if($resultstr == 5){$winlose = "×";$score = "不戦敗";}	#if
#自分が「勝ち」の場合、相手が「負け」以外は「相違！」
if($resultstr == 1 && $aite_resultstr != 2){
$attention = "対戦相手との戦績登録に相違があります。1";
}	#if
#自分が「勝ち」の場合、相手が「負け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 1 && $aite_resultstr == 2 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
$attention = "対戦相手との戦績登録に相違があります。1.1";
}	#if

#自分が「負け」の場合、相手が「勝ち」以外は「相違！」
if($resultstr == 2 && $aite_resultstr != 1 && $count2 == 1){
$attention = "対戦相手との戦績登録に相違があります。2";
}	#if
#自分が「負け」の場合、相手が「勝ち」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 2 && $aite_resultstr == 1 and ($result0 != $aite_result1 || $result1 != $aite_result0 ) ){
$attention = "対戦相手との戦績登録に相違があります。2.1 | ";
}	#if

#自分が「不戦勝」の場合、相手が「不戦敗」以外は「相違！」
if($resultstr == 4 && $aite_resultstr != 5){
$attention = "対戦相手との戦績登録に相違があります。3";
}	#if
#自分が「不戦敗」の場合、相手が「不戦勝」以外は「相違！」
if($resultstr == 5 && $aite_resultstr != 4){
$attention = "対戦相手との戦績登録に相違があります。4";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外は「相違！」
if($resultstr == 3 && $aite_resultstr != 3){
$attention = "対戦相手との戦績登録に相違があります。5";
}	#if
#自分が「引き分け」の場合、相手が「引き分け」以外で、さらにスコアが異なる場合は「相違！」
if($resultstr == 3 && $aite_resultstr == 3 and $result0 != $aite_result0 ){
$attention = "対戦相手との戦績登録に相違があります。6";
}	#if

#}	#if count1
#}	#if posi1


#注意があれば。
if($attention ne ""){
$attention = "<br><span style='color:red;font-size:12px;font-weight:normal;'>$attention</span>";
}	#if attention

$ground = "";
$nichijireport = "";
#試合日と開催地をGET
#$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and text1 = '$num'";
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = $kumi and title = $gedan and text1 = $num and (teamnum = $aitess or teamnum = $teamserial) and (linkadr = '$loginuser' or linkadr = '$aitesession' ) ORDER BY serial ASC LIMIT 1";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$sql_str4<br>\n";
if($count4 != 0){
$REFHASH4 = $rs4->fetchrow_hashref;
$ground .= &paramsetsql('body',$REFHASH4);
$n = &paramsetsql('nichiji1',$REFHASH4);
@TEMP = split(/ /,$n);
$nichijireport = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
}	#if
=pot
#3ヶ月前のは表示しない
$n1 = Date::Simple->new();
if($n ne ""){
$n2 = Date::Simple->new($TEMP[0]);
}else{
if($ld1 > $ld2 ){$ld1 = $ld2;}
$n2 = $ld1;
}	#if
if( ($n1 - $n2) > 30){$dateover = "<hr><span style='color:red;'>（30日消去対象）$n2</span>";}else{$dateover = "";}
=cut

##
$resultlist .=<<"END_HTML";
<tr>
<th align="center" scope="row">$taikainame</th>
<th align="center" scope="row">$nichijireport</th>
<th align="left" scope="row">$areaname<br>$numstr</th>
<th align="left" scope="row">$aiteteam</th>
<th align="center" scope="row" nowrap>&nbsp;$winlose&nbsp;</th>
<th align="center" scope="row" nowrap>&nbsp;$score&nbsp;</th>
</tr>
END_HTML
}	#if 双方
}	#if nichiji
#}	#if count = 2
#}	#foreach x
}	#foreach y
}	#if count1
}	#if cate
}	#foreach cate
}	#for count



# 問い合わせバナー
if($loginuser ne "" ){
#ログインの確認
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' and contents = 21 and koukaiflag = 0 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1 && $ses ne ""){
#相手チームの情報をGET
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' and contents = 21 and koukaiflag = 0 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$email = &paramsetsql('mailaddress2');
$shimei1 = &paramsetsql('shimei1');
$teamname1 = &paramsetsql('teamname');
$lineid = &paramsetsql('lineid');
=pot
$subject = "「$teamname1」チームへ問い合わせ　｜$sitetitle";
$subject = Unicode::Japanese->new($subject)->sjis;
#utf8::encode($subject);
$subject =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$subject =~ tr/ /+/;
#utf8::decode($subject);
$body =<<"END_HTML";
チーム名：$teamname1
代表者　：$shimei1 様

END_HTML
$body = Unicode::Japanese->new($body)->sjis;
$body =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$body =~ tr/ /+/;
utf8::decode($body);
#IEのみ便利機能
if($ENV{"HTTP_USER_AGENT"} =~ /MSIE/){
$toiawasebanner =<<"END_HTML";
<div class="center"><a href="mailto:$email?subject=$subject&amp;body=$body"><img src="img/te3.jpg" width="268" height="42" /></a></div>
END_HTML
}else{
=cut
=pot
($m1,$m2) = split(/@/,$email);
$emailtemp = $email;
$emailtemp =~ s/@/☆/;
$toiawasebanner =<<"END_HTML";
<div class="center"><a href="javascript:mail_to()"><img src="img/te3.jpg" width="268" height="42" /></a></div>
<table align=center style="border:none;">
<tr>
<td nowrap style="border:none;">
<noscript>
<p style="color:red;font-size:12px;line-height:150%;" align=left>※メーラを立ち上げるにはJavaScriptをONにしてください。</p></noscript>
<p style="color:red;font-size:12px;line-height:150%;" align=left>※クリックしてもメーラーが立ち上がらない場合は、<br>　お手数ですが上記チームアドレスをコピーして、<br>　お使いのメーラーよりご連絡ください。<br>
　ご使用の際は、☆を\@に変更してご使用下さい。</p>
</td>
</tr>
</table>
<script>
function mail_to(){
var m1 = "$m1";
var m2 = "$m2";
location.href = "mai"+"lto:"+m1+"\@"+m2;
}	//func
</script>
END_HTML
$toiawasebanner2 =<<"END_HTML";
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold">チームアドレス</td>
<td>$emailtemp&nbsp;</td>
</tr>
END_HTML
=cut

$toiawasebanner =<<"END_HTML";
<link rel='stylesheet' type='text/css' href='./css/colorbox.css'>
<script type='text/javascript' src='./js/jquery.min.js'></script>
<script type='text/javascript' src='./js/jquery.colorbox-min.js'></script>

<div class='center'><a href='#teamaddrbox' id='teamabox' ><img src='img/te3.jpg' width='268' height='42' /></a></div>
<script>
\$(document).ready(function(){
	\$("#teamabox").colorbox({inline:true, href:"#teamaddrbox"});
});
</script>
<div style='display:none;'>
<div id='teamaddrbox' style='padding:10px 10px 0px 10px;' >
<table width=400 style="margin-bottom:0;">
<tr>
<th nowrap >メールアドレス</th><td nowrap >$email</td>
</tr>
<tr>
<th nowrap >LINE ID</th><td >$lineid<br>
</td>
</tr>
</table>
<font class="type1" color="#ff0000">
※パソコンメールアドレスかメールアプリLINE（ライン）を、<br>
チーム間の連絡用としてお使いいただけます。
</font>
</div>
</div>
END_HTML


}	#if count
}	#if count
}	#if


###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/reti.jpg" alt="登録チーム一覧" width="980" height="48" /> </div>
<div id="mainbox">
<h2 id="team"><span>$teamname</span></h2>
<div class="teaml" style="width:533px;">$IMGSRC[0]</div>
<div class="teamr" style="width:341px;">
<div><img src="img/te2.jpg" width="341" height="38" /></div>
<table width="100%" cellspacing="0" class="stane">
<tr>
<td width="117" align="center" bgcolor="#F2F2F2" style="font-weight: bold"> チーム正式名称</td>
<td width="222">$teamname（$team_kana）</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> チーム略称</td>
<td>$team_abbr&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" style="font-weight: bold"> 代表者</td>
<td>$shimei1&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> チーム結成年</td>
<td>$team_year&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> 主な活動曜日</td>
<td>$katsudou_week&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" style="font-weight: bold"> 主な活動場所</td>
<td>$team_pref&nbsp;$team_cities</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> 過去戦績</td>
<td>$past_perform&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> チームPR</td>
<td>$team_pr&nbsp;</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2" class="odd" style="font-weight: bold"> チームホームページ</td>
<td>$team_hp&nbsp;</td>
</tr>
$toiawasebanner2
</table>
$toiawasebanner
</div>
<hr class="clear" />
<div class="teaml">
<h2 class="subti" style="background-image:url(img/te4.jpg)">新着情報</h2>
<dl id="news2">
$whatnew
</dl>

<h2 class="subti" style="background-image:url(img/te4.jpg)">最新の試合予定</h2>
<table width="633" cellspacing="0" class="stane">
<tr>
<th width="331" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">大会</th>
<th width="69" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合日</th>
<th width="76" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="147" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
</tr>
$schedulelist
</table>

<h2 class="subti" style="background-image:url(img/te4.jpg)">最新の試合結果</h2>
<table width="633" cellspacing="0" class="stane">
<tr>
<th width="239" align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">大会</th>
<th width="63" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合日</th>
<th width="78" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
<th width="143" align="center" class="underl" style="font-size: 14px; font-weight: bold;">対戦チーム</th>
<th width="36" align="center" class="underl" style="font-size: 14px; font-weight: bold;">勝敗</th>
<th width="60" align="center" class="underl" style="font-size: 14px; font-weight: bold;">スコア</th>
</tr>
$resultlist
</table>

</div>
<div class="teamr">
<h2 class="subti" style="background-image:url(img/te4.jpg)">登録選手</h2>
<ul>
$memberlist
</ul>
</div>
<hr class="clear" />
</div>
END_HTML
#
&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# チーム一覧
# -----------------------------------------------------------------
sub resistration {
$p = $paramhash_dec{'p'};
$w = $paramhash_dec{'w'};
$PREFFLAG{$p} = "selected";
if($p ne ""){push(@TEMP,"team_pref like '%$p%' ");}	#if
if($w ne ""){push(@TEMP,"teamname like '%$w%' ");}	#if
$temp = join(" or ",@TEMP);
if($temp ne ""){$str = "and ($temp)";}
#検索
$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 0 $str ORDER BY createdate ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ssid = $REFHASH->{'ssid'};
$teamname = &paramsetsql('teamname');
$team_pref = &paramsetsql('team_pref');
$team_pr = &paramsetsql('team_pr');
if(length($team_pr) > 30){$team_pr = substr($team_pr,0,30)."...";}
$team_pr = &crlfreset2($team_pr);

#
$searchlist .=<<"END_HTML";
<tr>
<td align="center" scope="row">&nbsp;$teamname</td>
<td align="center" scope="row">&nbsp;$team_pref</td>
<td align="left" scope="row" style='word-break: break-all;'>&nbsp;$team_pr</td>
<td align="left" scope="row"><a href='system.cgi?code=mypage_team&ses=$ssid'><img src="img/syousai.jpg" width="59" height="32" /></a></td>
</tr>
END_HTML
}	#for

###
$mes =<<"END_HTML";
<form action='registration.html' method='GET' name='form1' id='form1' >
<input type='hidden' name='code' value='resistration' />
<div id='search'>
<div id='search1'>
<select name=p id=p>
<option value='' >選択</option>
<option value=北海道 $PREFFLAG{'北海道'}>北海道</option>
<option value=青森県 $PREFFLAG{'青森県'}>青森県</option>
<option value=岩手県 $PREFFLAG{'岩手県'}>岩手県</option>
<option value=宮城県 $PREFFLAG{'宮城県'}>宮城県</option>
<option value=秋田県 $PREFFLAG{'秋田県'}>秋田県</option>
<option value=山形県 $PREFFLAG{'山形県'}>山形県</option>
<option value=福島県 $PREFFLAG{'福島県'}>福島県</option>
<option value=茨城県 $PREFFLAG{'茨城県'}>茨城県</option>
<option value=栃木県 $PREFFLAG{'栃木県'}>栃木県</option>
<option value=群馬県 $PREFFLAG{'群馬県'}>群馬県</option>
<option value=埼玉県 $PREFFLAG{'埼玉県'}>埼玉県</option>
<option value=千葉県 $PREFFLAG{'千葉県'}>千葉県</option>
<option value=東京都 $PREFFLAG{'東京都'}>東京都</option>
<option value=神奈川県 $PREFFLAG{'神奈川県'}>神奈川県</option>
<option value=新潟県 $PREFFLAG{'新潟県'}>新潟県</option>
<option value=富山県 $PREFFLAG{'富山県'}>富山県</option>
<option value=石川県 $PREFFLAG{'石川県'}>石川県</option>
<option value=福井県 $PREFFLAG{'福井県'}>福井県</option>
<option value=山梨県 $PREFFLAG{'山梨県'}>山梨県</option>
<option value=長野県 $PREFFLAG{'長野県'}>長野県</option>
<option value=岐阜県 $PREFFLAG{'岐阜県'}>岐阜県</option>
<option value=静岡県 $PREFFLAG{'静岡県'}>静岡県</option>
<option value=愛知県 $PREFFLAG{'愛知県'}>愛知県</option>
<option value=三重県 $PREFFLAG{'三重県'}>三重県</option>
<option value=滋賀県 $PREFFLAG{'滋賀県'}>滋賀県</option>
<option value=京都府 $PREFFLAG{'京都府'}>京都府</option>
<option value=大阪府 $PREFFLAG{'大阪府'}>大阪府</option>
<option value=兵庫県 $PREFFLAG{'兵庫県'}>兵庫県</option>
<option value=奈良県 $PREFFLAG{'奈良県'}>奈良県</option>
<option value=和歌山県 $PREFFLAG{'和歌山県'}>和歌山県</option>
<option value=鳥取県 $PREFFLAG{'鳥取県'}>鳥取県</option>
<option value=島根県 $PREFFLAG{'島根県'}>島根県</option>
<option value=岡山県 $PREFFLAG{'岡山県'}>岡山県</option>
<option value=広島県 $PREFFLAG{'広島県'}>広島県</option>
<option value=山口県 $PREFFLAG{'山口県'}>山口県</option>
<option value=徳島県 $PREFFLAG{'徳島県'}>徳島県</option>
<option value=香川県 $PREFFLAG{'香川県'}>香川県</option>
<option value=愛媛県 $PREFFLAG{'愛媛県'}>愛媛県</option>
<option value=高知県 $PREFFLAG{'高知県'}>高知県</option>
<option value=福岡県 $PREFFLAG{'福岡県'}>福岡県</option>
<option value=佐賀県 $PREFFLAG{'佐賀県'}>佐賀県</option>
<option value=長崎県 $PREFFLAG{'長崎県'}>長崎県</option>
<option value=熊本県 $PREFFLAG{'熊本県'}>熊本県</option>
<option value=大分県 $PREFFLAG{'大分県'}>大分県</option>
<option value=宮崎県 $PREFFLAG{'宮崎県'}>宮崎県</option>
<option value=鹿児島県 $PREFFLAG{'鹿児島県'}>鹿児島県</option>
<option value=沖縄県 $PREFFLAG{'沖縄県'}>沖縄県</option>
</select>
</div>
<div id='search2'>
<input name='w' id='w' type='text' value='$w' />
</div>
<div id='search3'><img src='img/re3.jpg' width='91' height='41' onClick='document.form1.submit();' /></div>
</div>
</form>

<div class='box'>
<table width='100%' cellspacing='0' class='stane'>
<tr>
<th width="22%" align='center' class='underl' style='font-size: 14px; font-weight: bold;' scope='row'>チーム名</th>
<th width="13%" align='center' class='underl' style='font-size: 14px; font-weight: bold;'>活動拠点</th>
<th width="61%" align='center' class='underl' style='font-size: 14px; font-weight: bold;'>チームPR</th>
<th width="4%" align='center' class='underl' style='font-size: 14px; font-weight: bold;'>詳細</th>
</tr>
$searchlist
</table>
</div>
END_HTML
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub



# -----------------------------------------------------------------
# TOP大会バナー
# -----------------------------------------------------------------
sub taikaibanner {
# バナーカテゴリ
$sql_str = "SELECT * FROM $dbname WHERE contents = 44 and koukaiflag = 0 ORDER BY sortnum DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = $REFHASH->{'serial'};
$title = &paramsetsql('title');
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[0]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){
	$mes .= "<div><a href='system.cgi?code=bannercategory&taikaicode=$taikaicode&bannercategory=$ss'><img src='system/file/$TEMP[0]taikaiimage2.jpg' ALT='$title' width='265' height='69' border=0 /></a></div>";
}	#if
}else{
	$mes .="<div><img src='system/systemimages/dat.gif' ALT='$title' width='265' height='69' border=0 /></div>";
}	#if 存在
}	#for
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub



# -----------------------------------------------------------------
# TOP大会バナー2
# -----------------------------------------------------------------
sub taikaibanner2 {
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$taikainame = &paramsetsql('title');
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[1]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$mes .= "<div class='taikai'><a href='system.cgi?code=convention&taikaicode=$taikaicode'><img src='system/file/$TEMP[0].jpg' ALT='$taikainame' width='440' height='114' /></a></div>";}
}	#if 存在
}	#for
# width='265' height='69' 　小さい方
# width='440' height='114'　大きい方
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub




# -----------------------------------------------------------------
# 大会詳細
# -----------------------------------------------------------------
sub convention {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
#大会情報をGET
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 and serial = '$taikaicode' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<br>
<br>
<br>
<p align=center>ご指定の大会情報は登録されておりません。</p>
<br>
<br>
<br>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[0]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$imgsrc .= "<img src='system/file/$TEMP[0]taikaiimage.jpg' ALT='$taikainame' />";}
}	#if 存在

#大会イメージ記事をGET
$sql_str = "SELECT * FROM $dbname WHERE contents = 36 and koukaiflag = 0 and taikaicode = '$taikaicode' ORDER BY sortnum DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql2('title');
$body = &paramsetsql2('body');
$text1 = &paramsetsql2('text1');
$comment = &paramsetsql2('comment');
#画像2:width="790" height="391"
@IMGSRC2 = ();
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
foreach(0..2){
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[$_]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC2[$_] = "<img src='system/file/$TEMP[0]convention.jpg' ALT='$taikainame' /><br>";}
}	#if 存在
}	#foreach
#画像があるかないか
$temp = @IMGSRC2;
$imgtemp = "";
if($temp != 0){
$imgtemp =<<"END_HTML";
<div class="boxg">
$IMGSRC2[0]
$IMGSRC2[1]
$IMGSRC2[2]
</div>
END_HTML
}	#if
#
$taikaiimagekiji .=<<"END_HTML";
<h2 class="subti">$title</h2>
<div class="box">
<p>$body</p>
$imgtemp
</div>
END_HTML
}	#for


###
$mes =<<"END_HTML";
<style type="text/css">
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
#navigation2 li.menu0 a {
	background:url(img/menu2.jpg) no-repeat -0px -50px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>

<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">
<div style="margin-bottom:30px;">$imgsrc</div>
$taikaiimagekiji
</div>

END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# 大会概要
# -----------------------------------------------------------------
sub outline {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);

#概要
$sql_str = "SELECT * FROM $dbname WHERE contents = 45 and koukaiflag = 0 and taikaicode = '$taikaicode' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$gaiyou = &paramsetsql('title');
}	#if

=pot
#大会イメージ記事をGET
$sql_str = "SELECT * FROM $dbname WHERE contents = 36 and koukaiflag = 0 and taikaicode = '$taikaicode' ORDER BY sortnum DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
#$title = &paramsetsql2('title');
#$body = &paramsetsql2('body');
$text1 = &paramsetsql2('text1');
$comment = &paramsetsql2('comment');
#
$taikaiimagekiji .=<<"END_HTML";
<div class="boxg" style="margin-bottom:30px;">
<div><img src="img/tai2.jpg" width="479" height="34" /></div>
<p>$text1</p>
<div><img src="img/tai3.jpg" width="479" height="34" /></div>
<p>$comment</p>
<hr class="clear" />
</div>
END_HTML
}	#for
=cut

###
$mes =<<"END_HTML";
<style>
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
#navigation2 li.menu1 a {
	background:url(img/menu2.jpg) no-repeat -164px -50px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>
<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">

$gaiyou

</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# 大会結果
# -----------------------------------------------------------------
sub result {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
$tdata = "";

#トーナメント画像をGET
$category = 1;
$sql_str = "SELECT * FROM $dbname WHERE contents = 42 and koukaiflag = 0 and taikaicode = '$taikaicode' ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$title = &paramsetsql('title');
$tagjump .=<<"END_HTML";
<a href="#$ss"><span>$title</span></a> 
END_HTML
$title = "<h2 class='subti' id='$ss'>".$title."</h2>";
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[0]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$imgsrc = "<img src='system/file/$TEMP[0].jpg' ALT='' />";}
}	#if 存在
$tdata .=<<"END_HTML";
$title
<div class="box">
<div class="center">$imgsrc</div>
</div>
<br>
END_HTML
}	#for


&kachi;


if($arealist2 ne ""){
$arealist2 =<<"END_HTML";
<img src="img/toti.jpg" ALT="トーナメント戦タイトル" />
<div id="pnl">
<div class="pnl">$areatag2</div>
</div>

$arealist2
END_HTML
}



###
$mes =<<"END_HTML";
<style>
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
#navigation2 li.menu2 a {
	background:url(img/menu2.jpg) no-repeat -328px -50px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>
<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">

$tdata

$arealist2

</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#sub



# -----------------------------------------------------------------
# 大会内：試合予定一覧
# -----------------------------------------------------------------
sub schedule {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
if($taikainame =~ /不明/){
$mes =<<"END_HTML";
大会情報が取得できませんでした。
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if

$jimukyoku = "";
#事務局
$sql_str = "SELECT * FROM $dbname WHERE contents = 43 and taikaicode = '$taikaicode' and category = 1 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql3('title');
$text1 = &paramsetsql3('text1');
$body = &paramsetsql3('body');
@RESULTSTR = split(/<>/,&paramsetsql2('resultstr'));
@RESULTSTR2 = split(/<>/,&paramsetsql2('resultstr2'));
@RESULT0 = split(/<>/,&paramsetsql2('result0'));
@RESULT1 = split(/<>/,&paramsetsql2('result1'));
@SENPYO = split(/<>/,&paramsetsql2('senpyo'));
$list = "";
foreach $i(0..19){
if($RESULTSTR[$i] eq "" && $RESULTSTR2[$i] eq ""){next;}
$list .=<<"END_HTML";
<tr>
<td align="center">$RESULTSTR[$i]　　vs　　$RESULTSTR2[$i]</td>
<td align="center">$RESULT0[$i]&nbsp;</td>
<td>$RESULT1[$i]&nbsp;</td>
<td>$SENPYO[$i]&nbsp;</td>
</tr>
END_HTML
}	#foreach
##
$jimukyoku .=<<"END_HTML";
<h2 class="subti" id="1" style="margin-bottom:-20px;">$title</h2>
<div class="box">
<h3>$text1</h3>
<div class="subti3">$body</div>
<table width="840" cellspacing="0" class="table_02" summary="ブロック分け">
<tr>
<th width="366" bgcolor="#F2F2F2">内　　容</th>
<th width="127" bgcolor="#F2F2F2">日　　程</th>
<th width="181" bgcolor="#F2F2F2">場　　所</th>
<th width="156" bgcolor="#F2F2F2">試合時間</th>
</tr>
$list
</table>
</div>
END_HTML
}	#for

########################################################################
#リーグ戦
########################################################################
$list = "";
#エリア一覧
$sql_str0 = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 ORDER BY sortnum ASC, serial DESC ";
$rs0 = $dbh->prepare($sql_str0);
$rs0->execute();
&sqlcheck($sql_str0);	#SQLエラーチェック
$count0 = $rs0->rows;	# Hit件数を確保
#print "count0=$count0";
for($k = 0;$k < $count0;$k++){	# データベース１件ずつ
$REFHASH0 = $rs0->fetchrow_hashref;
$area = &paramsetsql('serial',$REFHASH0);
$areaname = &paramsetsql('title',$REFHASH0);
if($areaname =~ /不明/){next;}

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = $area ORDER BY sortnum ASC, serial DESC";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);	#SQLエラーチェック
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1";
for($i=0;$i<$count1;$i++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}

if($areaname !~ /不明/ && $kuminame !~ /不明/){
#試合期日
$n = Date::Simple->new();
foreach(split(/<>/,$body)){
($setutemp,$nichiji1,$nichiji2) = split(/:/,$_);
$nichijistr = sprintf("%d年%d月%d日",split(/-/,$nichiji1))."〜";
$nichijistr .= sprintf("%d年%d月%d日",split(/-/,$nichiji2))."まで";
$NISHIJISTR{$setutemp} = $nichijistr;
$n1 = Date::Simple->new($nichiji1);
$n2 = Date::Simple->new($nichiji2);
%DISPFLAG = ();
if($n > $n2){
$DISPFLAG{$setutemp} = 0;	#表示
}else{
$DISPFLAG{$setutemp} = 1;	#非表示
}	#if
}	#foreach

# vsチームを分解
%SETUCNT=();
%AUTOLIST = ();
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($tss1 eq "" || $tss2 eq ""){next;}

($tss1name,$tss1ses) = &taikaiteamname_get3($tss1);
($tss2name,$tss2ses) = &taikaiteamname_get3($tss2);

$SETUCNT{$setu}=1;
#左チームの報告から「試合日時」と「場所」をGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category= 1 and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ORDER BY serial ASC LIMIT 1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>";
#$nichijistr = "";
#$nichijistr2 = "";
$nichijistr10 = "";
$nichijistr11 = "";
$ground1 = "";
if($count2 != 0){
$REFHASH2 = $rs2->fetchrow_hashref;
$ground1 = &paramsetsql('body',$REFHASH2);
$n = &paramsetsql('nichiji1',$REFHASH2);
@TEMP = split(/ /,$n);
if($TEMP[0] ne "0000-00-00" && $TEMP[0] ne ""){
($y,$m,$d) = split(/-/,$TEMP[0]);
$nichijistr10 = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$nichijistr11 = sprintf("%d時%02d分",split(/:/,$TEMP[1]));
}	#if
}	#if count2 != 0
=pot
#右チームの報告から「試合日時」と「場所」をGET
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = '$taikaicode' and category= 1 and area = '$area' and kumi = '$kumi' and title = '$setu' and linkadr = '$tss2ses' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
$count3 = $rs3->rows;	# Hit件数を確保
#print "count3=$count3<br>";
$nichijistr20 = "";
$nichijistr21 = "";
$ground2 = "";
if($count3 != 0){
$REFHASH3 = $rs3->fetchrow_hashref;
$ground2 = &paramsetsql('body',$REFHASH3);
$n = &paramsetsql('nichiji1',$REFHASH3);
@TEMP = split(/ /,$n);
if($TEMP[0] ne "0000-00-00" && $TEMP[0] ne ""){
($y,$m,$d) = split(/-/,$TEMP[0]);
$nichijistr20 = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$nichijistr21 = sprintf("%d時%02d分",split(/:/,$TEMP[1]));
}	#if
}	#if count2 != 0
$nichijistr = $nichijistr10;
$nichijistr2 = $nichijistr11;
$ground = $ground1;
#両方報告がないと詳細は隠す
if($count2 == 0 || $count3 == 0){
$nichijistr = "";
$nichijistr2 = "";
$ground = "";
}	#if
=cut

#
#if($tss1name ne "" && $tss2name ne "" ){
$AUTOLIST{$setu} .=<<"END_HTML";
<tr>
<td align="center">$tss1name　　vs　　$tss2name&nbsp;</td>
<td align="center">$nichijistr10&nbsp;</td>
<td align="center">$ground1&nbsp;</td>
<td align="center">$nichijistr11&nbsp;</td>
</tr>
END_HTML
#}
}	#foreach vsdata


###
$list .=<<"END_HTML";
<h2 class="subti" id="1" style="margin-bottom:-20px;">$areaname</h2>
<div class="box">
<h3>$kuminame</h3>
END_HTML

foreach $setu(sort keys  %SETUCNT){
$autolist = "";
if($AUTOLIST{$setu} ne ""){
$autolist .=<<"END_HTML";
<table width="840" cellspacing="0" class="table_02" summary="ブロック分け">
<tr>
<th width="366" bgcolor="#F2F2F2" align="center">内　　容</th>
<th width="127" bgcolor="#F2F2F2" align="center">日　　程</th>
<th width="181" bgcolor="#F2F2F2" align="center">場　　所</th>
<th width="156" bgcolor="#F2F2F2" align="center">試合時間</th>
</tr>
$AUTOLIST{$setu}
</table>
END_HTML
}	#if
if($autolist ne ""){
$list .=<<"END_HTML";
<h4 style="font-weight:bold;font-size:16px;">第${setu}節</h4>
$autolist
END_HTML
}	#if
}	#foreach setu
$list .=<<"END_HTML";
</div>
END_HTML
}	#if 不明
}	#for
if($list ne ""){
$siailist =<<"END_HTML";
<img src="img/riti.jpg" ALT="リーグ戦タイトル" />
$list
END_HTML
}	#if

}	#for area

########################################################################
# トーナメント戦
########################################################################
@KUMINUM = ();
@CNT = (0,1,2,4,8,16,32,64,128);
$list2 = "";

# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode'  and category = 2 ORDER BY area ASC,kumi ASC";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1."<br>\n";
for($i=0;$i<$count1;$i++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";
$k+=2;
}	#foreach x
}	#foreach y

#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan";

#トーナメント○回戦
foreach $y(1..7){
$list2 = "";
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
#print "($n1,$n2)<br>\n";
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$d = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2);
#報告範囲内
#if( $d1 <= $d && $d <= $d2){
#
$cnt2 = $CNT[$y];
$num = $y;
foreach $x(1..$cnt2){
$tss1 = $TEAMLIST{$y}{$x}{1};	#左のチームnum
$tss2 = $TEAMLIST{$y}{$x}{2};	#右のチームnum
#print "y=$y,x=$x($tss1,$tss2)<br>\n";
if($tss1 eq "" || $tss2 eq ""){next;}
($tss1name,$tss1ses) = &taikaiteamname_get3($tss1);
($tss2name,$tss2ses) = &taikaiteamname_get3($tss2);

$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num+2)."回戦";
}	#num
#報告データをGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = $x and text1 = $y and ((teamnum = $tss1 and linkadr = '$tss2ses') or (teamnum = $tss2 and linkadr = '$tss1ses') ) ORDER BY serial ASC ";

$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>";
$ground = "";
$nichijistr = "";
$nichijistr2 = "";
#if($count2 != 0){
#試合日と開催地をGET
#チーム１
$REFHASH2 = $rs2->fetchrow_hashref;
$ground = &paramsetsql('body',$REFHASH2);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
#チーム２
#$REFHASH2 = $rs2->fetchrow_hashref;
#$ground2 = &paramsetsql('body',$REFHASH2);
#$n2 = &paramsetsql('nichiji1',$REFHASH2);
#入力チェック
#print "$n1 ne $n2<br>";
#if($ground ne $ground2){$ground .= "（$ground2）";}
#$n = &paramsetsql('nichiji1',$REFHASH2);
if($n1 ne ""){
@TEMP = split(/ /,$n1);
$nichijistr = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$nichijistr2 = sprintf("%d時%02d分",split(/:/,$TEMP[1]));
}	#if


###
$list2 .=<<"END_HTML";
<tr>
<td align="center">$tss1name　　vs　　$tss2name&nbsp;</td>
<td align="center">$nichijistr&nbsp;</td>
<td align="center">$ground&nbsp;</td>
<td align="center">$nichijistr2&nbsp;</td>
</tr>
END_HTML
#}	#if count
}	#foreach x
}	#if 日付が有効

if($list2 ne ""){
$list3 .=<<"END_HTML";
<h4 style="font-weight:bold;font-size:16px;">$numstr</h4>
<table width="840" cellspacing="0" class="table_02" summary="ブロック分け">
<tr>
<th width="366" bgcolor="#F2F2F2" align="center">内　　容</th>
<th width="127" bgcolor="#F2F2F2" align="center">日　　程</th>
<th width="181" bgcolor="#F2F2F2" align="center">場　　所</th>
<th width="156" bgcolor="#F2F2F2" align="center">試合時間</th>
</tr>
$list2
</table>
END_HTML
}	#if
}	#foreach y 1-7
if($list3 ne ""){
$siailist2 .=<<"END_HTML";
<h2 class="subti" id="1" style="margin-bottom:-20px;">$areaname</h2>
<div class="box">
<h3>$kuminame</h3>
$list3
</div>
END_HTML
}	#if
$list3 = "";

}	#for i


if($siailist2 ne ""){
$siailist2 =<<"END_HTML";
<img src="img/toti.jpg" ALT="トーナメント戦タイトル" />
$siailist2
END_HTML
}	#if





####################################
$mes =<<"END_HTML";
<style type="text/css">
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
#navigation2 li.menu5 a {
	background:url(img/menu2.jpg) no-repeat -820px -50px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>
<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">
$jimukyoku

$siailist


$siailist2


</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub

# -----------------------------------------------------------------
# 大会記事
# -----------------------------------------------------------------
sub report {
$ofslimit = 10;
$taikaicode = $paramhash{'taikaicode'};
$tyear = $paramhash{'y'};
$tmonth = $paramhash{'m'};
if($tyear eq "" || $tmonth eq ""){
$tyear = $year;
$tmonth = $month;
}	#if
$byear = $nyear = $tyear;
$bmonth = $nmonth = $tmonth;
#前月
$bmonth--;
if($bmonth < 1 ){$byear--;$bmonth+=12;}
#次月
$nmonth++;
if($nmonth > 12 ){$nyear++;$nmonth-=12;}
#
$ofs = $paramhash{'ofs'} -0;
$nn = sprintf("%04d-%02d-",$tyear,$tmonth);
$taikainame = &taikainame_get($taikaicode);	#大会名GET
#記事ALL GET
$sql_str = "SELECT * FROM $dbname WHERE contents = 7 and koukaiflag = 0 and taikaicode = '$taikaicode' and nichiji1 like '$nn%' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$countall = $rs->rows;	# Hit件数を確保
#記事GET
$sql_str = "SELECT * FROM $dbname WHERE contents = 7 and koukaiflag = 0 and taikaicode = '$taikaicode' and nichiji1 like '$nn%' ORDER BY nichiji1 DESC,serial DESC LIMIT $ofs,$ofslimit";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保

#NEXTBACKを作る
$max = int( ($countall-1) / $ofslimit);
#リンクバーを作る
$linkadr = "";
if($max >= 1){
for($i=0;$i<=$max;$i++){
$cnt = $i * $ofslimit;
$kk = $i + 1;
if($cnt == $ofs){$linkadr .= "<font color=red>$kk</font> ";}else{$linkadr .= "<a href='?code=report&taikaicode=$taikaicode&y=$tyear&m=$tmonth&ofs=$cnt' >$kk</a> ";}	#if
$cnt++;
}	#for max
$ofs2 = $ofs - $ofslimit;
$ofs3 = $ofs + $ofslimit;
if( $ofs > 1){$linkadrback = "<a href='?code=report&taikaicode=$taikaicode&y=$tyear&m=$tmonth&ofs=$ofs2' >≪前へ</a>";}else{$linkadrback = "≪前へ";}
if( $ofs3 < $countall ){$linkadrnext = "<a href='?code=report&taikaicode=$taikaicode&y=$tyear&m=$tmonth&ofs=$ofs3' >次へ≫</a>";}	#if
}	#if max > 1
$linkadr = $linkadrback.$linkadr.$linkadrnext;

#
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$text1 = &paramsetsql2('text1');
$nichijistr = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji1')));
$title = &paramsetsql2('title');
$body = &paramsetsql2('body');
@CAPTION = split(/<>/,&paramsetsql2('caption'));
$resultstr = &paramsetsql2('resultstr');
$resultstr2 = &paramsetsql2('resultstr2');
$result0 = &paramsetsql2('result0');
$result1 = &paramsetsql2('result1');
#画像
@IMGSRC = ();
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn) = split(/<>/,$IMGTEMPS[0]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){
$IMGSRC[0] = "<img src='system/file/$TEMP[0]taikaikiji1.jpg' ALT='$CAPTION[0]' />";
$IMGSRC[1] = "<img src='system/file/$TEMP[0]taikaikiji2.jpg' ALT='$CAPTION[0]' />";
}	#if
}	#if 存在
##記事ループ
if($i == 0){
#最初の記事
$body = &paramsetsql2('body');	#
$kiji .=<<"END_HTML";
<div class="subti4"><span>$text1</span></div>
<h2 class="subti" id="1">$title<span class="subdate">$nichijistr</span></h2>
<div class="box">
<div class="na">
<table width="760" border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td width="48" align="center">&nbsp;</td>
<td width="249" align="center" bgcolor="#F2EEE6">$resultstr</td>
<td width="53" align="center">$result0</td>
<td width="53" align="center">―</td>
<td width="53" align="center">$result1</td>
<td width="249" align="center" bgcolor="#F2EEE6">$resultstr2</td>
<td width="55" align="center">&nbsp;</td>
</tr>
</table>
</div>
<div class="repo">
<div class="repopho">
<div>$IMGSRC[0]</div>
<p>$CAPTION[0]</p>
</div>
<div class="reptex" style='word-break: break-all;'>$body</div>
<hr class="clear" />
</div>
END_HTML
}else{
#２番目以降
$body = &paramsetsql2('body');	#素のテキストデータ
$body =<<"END_HTML";
<span id="stag$ss" class="tagspan" onClick="tagopen($ss)">≫詳細を見る</span><span id="tag$ss" style="display:none;">$body<span class="tagspan" onClick="tagclose($ss)"><br>≪閉じる</span>
</span>
END_HTML
$kiji .=<<"END_HTML";
<div class="repo2">
<div class="repopho2">
<div>$IMGSRC[1]</div>
<p>$CAPTION[0]</p>
</div>
<div class="reptex2">
<div class="subti4"><span>$text1</span></div>
<h3>$title</h3>
<span class="subtis"><span class="subdate">$nichijistr</span></span>
<div class="na4">
<table border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td>&nbsp;</td>
<td bgcolor="#F2EEE6">$resultstr</td>
<td>$result0</td>
<td>―</td>
<td>$result1</td>
<td bgcolor="#F2EEE6">$resultstr2</td>
<td>&nbsp;</td>
</tr>
</table>
</div>
<p>$body</p>
</div>
<hr class="clear" />
</div>
END_HTML
}	#if
#
}	#for
#################################
$mes =<<"END_HTML";
<style type="text/css">
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
#navigation2 li.menu4 a {
	background:url(img/menu2.jpg) no-repeat -656px -50px;
}

.tagspan {
	color:orange;
	text-decoration:underline;
}
.tagspan:hover {
	cursor: pointer;
}

</style>
<script>
function tagopen(n){
document.getElementById("tag"+n).style.display = "block";
document.getElementById("stag"+n).style.display = "none";
}	//func
function tagclose(n){
document.getElementById("tag"+n).style.display = "none";
document.getElementById("stag"+n).style.display = "block";
}	//func
</script>
<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>
<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">

<div id="mon">
<div class="mon1"><a href="?code=report&taikaicode=$taikaicode&y=$byear&m=$bmonth"><img src="img/mon1.jpg" width="114" height="33" /></a></div>
<div class="mon2">${tyear}年<span class="moj1">$tmonth</span><span class="moj2">月</span></div>
<div class="mon3"><a href="?code=report&taikaicode=$taikaicode&y=$nyear&m=$nmonth"><img src="img/mon2.jpg" width="114" height="33" /></a></div>
</div>

$kiji
$nextbackstr

<div class="next">$linkadr</div>
</div>
<div></div>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#sub






# -----------------------------------------------------------------
# 大会エントリー
# -----------------------------------------------------------------
sub gameentry {
#ログインチェック
if($loginuser eq ""){
$mes =<<"END_HTML";
ログインして下さい。<br>
<br>
<input type="button" value="　TOPへ　" onclick="location.href='$sitefulladr'" />
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if
#セッション作成
$session = sprintf("%02d%02d%02d",$sec,$min,$hour);
for (1..15) { $session .= ((0..9,a..z,A..Z)[int rand 62])};
$session .= sprintf("%02d%02d%02d",$mday,$month,$year-2000);
#チーム情報をGET
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div align=center>
<br>
<p style="color:red;">チーム情報が見つかりません。</p>
<p>もう一度ログインをお願いします。</p>
<br>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$shimei1 = &paramsetsql('shimei1');
$mailaddress1 = &paramsetsql('mailaddress1');
$tel1 = &paramsetsql('tel1');
$shimei2 = &paramsetsql('shimei2');
$tel2 = &paramsetsql('tel2');
$mailaddress2 = &paramsetsql('mailaddress2');
$teamname = &paramsetsql('teamname');
$team_pref = &paramsetsql('team_pref');
$team_cities = &paramsetsql('team_cities');

#修正の場合
$pr = $paramhash_dec{'pr'};
$PFLAG{$paramhash_dec{'pref'}} = "selected";
my %TAIKAIFLAG = ();
foreach(split(/<>/,$paramhash{'taikainum'})){
$TAIKAIFLAG{$_} = "checked=checked";
}	#foreach
foreach(split(/:/,$paramhash{'weeklist'})){
$WEEKFLAG{$_} = "checked=checked";
}	#foreach

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
#$genre1 = $REFHASH->{'genre1'};
#$genre2 = $REFHASH->{'genre2'};
$title = &paramsetsql('title');
$maninonrei1 = &paramsetsql('maninonrei1');
$maninprice1flag = "";
$price1attention = "";
if(&paramsetsql('maninonrei1') == 1 && $TAIKAIFLAG{"$taikaicode:1"} eq ""){$maninprice1flag = "disabled";$price1attention_bak = "<span style='color:red;'>　※募集を終了しました。</span>";}
$maninprice2flag = "";
$price2attention = "";
$maninonrei2 = &paramsetsql('maninonrei2');
if(&paramsetsql('maninonrei2') == 1 && $TAIKAIFLAG{"$taikaicode:2"} eq ""){$maninprice2flag = "disabled";$price2attention_bak = "<span style='color:red;'>　※募集を終了しました。</span>";}
$price1 = &ketakanma(&paramsetsql('price1'));
$price2 = &ketakanma(&paramsetsql('price2'));
$price3 = &ketakanma(&paramsetsql('price3'));
$nichiji1 = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji1')));
#エントリー状況
$sql_str1 = "SELECT * FROM entrylist WHERE taikaicode = $taikaicode and teamsession = '$loginuser' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);	#SQLエラーチェック
$count1 = $rs1->rows;	# Hit件数を確保
%DFLAG =();
%DFLAGMES = ();
for($h = 0;$h < $count1;$h++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$cate = &paramsetsql('category',$REFHASH1);
$DFLAG{$cate} = "disabled";
$DFLAGMES{$cate} = "（エントリー済み）";
}	#for
$catestr = "";

if($category == 1 ){	#リーグ
$catestr .=<<"END_HTML";
<input $DFLAG{1} type="checkbox" name="taikainum" value="$taikaicode:1" $TAIKAIFLAG{"$taikaicode:1"} $maninprice1flag >$GENRENAME{1}　${price1}円<span style="color:red;">$DFLAGMES{1}</span>$price1attention<br>
END_HTML
}	#if c=1

if($category == 2){	#トーナメント
$catestr .=<<"END_HTML";
<input $DFLAG{2} type="checkbox" name="taikainum" value="$taikaicode:2" $TAIKAIFLAG{"$taikaicode:2"} $maninprice2flag >$GENRENAME{2}　${price2}円<span style="color:red;">$DFLAGMES{2}</span>$price2attention<br>
END_HTML
}	#if c=1

$attention = "";
if($category == 3){
$attention = "※同時参加で ${price3}円";
$catestr .=<<"END_HTML";
<input $DFLAG{1} type="checkbox" name="taikainum" value="$taikaicode:1" $TAIKAIFLAG{"$taikaicode:1"} $maninprice1flag >$GENRENAME{1}　${price1}円<span style="color:red;">$DFLAGMES{1}</span>$price1attention<br>
END_HTML
$catestr .=<<"END_HTML";
<input $DFLAG{2} type="checkbox" name="taikainum" value="$taikaicode:2" $TAIKAIFLAG{"$taikaicode:2"} $maninprice2flag >$GENRENAME{2}　${price2}円<span style="color:red;">$DFLAGMES{2}</span>$price2attention<br>
END_HTML
}	#if c=3
###
$taikailist .=<<"END_HTML";
<tr>
<td >
$title<br>
</td>
<td align=left nowrap>$catestr$attention</td>
</tr>
END_HTML
}	#for

#####
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gaenti.jpg" alt="大会エントリー" width="980" height="48" /> </div>

<div id="mainbox">
<h2 class="subti" id="1">大会エントリーフォーム</h2>
<div class="box">
<p>大会エントリーに必要な項目を入力してください<br>
大会エントリー前には必ず参加を希望される大会の大会概要をご確認ください。</p>

<script>
function kakunin(){
var cnt = document.form1.taikainum.length;
var flag = 0;
if(cnt > 1){
for(i=0;i<cnt;i++){
if(document.form1.taikainum[i].checked == true){flag++;}
}
}else{
if(document.form1.taikainum.checked == true){flag++;}
}

if(flag == 0){
alert("大会が選択されておりません。");
return false;
}

if(document.getElementById('pref').selectedIndex == 0){
alert("大会参加希望都道府県が選択されておりません。");
return false;
}

flag = 0;
if(document.getElementById('week0').checked == true){flag=1;}
if(document.getElementById('week1').checked == true){flag=1;}
if(document.getElementById('week2').checked == true){flag=1;}
if(document.getElementById('week3').checked == true){flag=1;}
if(document.getElementById('week4').checked == true){flag=1;}
if(flag == 0){
alert("大会参加希望曜日が選択されておりません。");
return false;
}

return true;
}
</script>

<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onSubmit="return kakunin()" >
<input type=hidden name="code" value="gameentry_check" />
<input type=hidden name="ses" value="$session" />

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">参加大会</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td width="76%" bgcolor="#ffffff">

<table width="100%" cellspacing="0" class="stan2">
$taikailist
</table>

</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望都道府県</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">
<select name="pref" id="pref" >
<option value="" >選択して下さい
<option value="北海道" $PFLAG{'北海道'}>北海道
<option value="青森県" $PFLAG{'青森県'}>青森県
<option value="岩手県" $PFLAG{'岩手県'}>岩手県
<option value="宮城県" $PFLAG{'宮城県'}>宮城県
<option value="秋田県" $PFLAG{'秋田県'}>秋田県
<option value="山形県" $PFLAG{'山形県'}>山形県
<option value="福島県" $PFLAG{'福島県'}>福島県
<option value="茨城県" $PFLAG{'茨城県'}>茨城県
<option value="栃木県" $PFLAG{'栃木県'}>栃木県
<option value="群馬県" $PFLAG{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG{'千葉県'}>千葉県
<option value="東京都" $PFLAG{'東京都'}>東京都
<option value="神奈川県" $PFLAG{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG{'新潟県'}>新潟県
<option value="富山県" $PFLAG{'富山県'}>富山県
<option value="石川県" $PFLAG{'石川県'}>石川県
<option value="福井県" $PFLAG{'福井県'}>福井県
<option value="山梨県" $PFLAG{'山梨県'}>山梨県
<option value="長野県" $PFLAG{'長野県'}>長野県
<option value="岐阜県" $PFLAG{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG{'静岡県'}>静岡県
<option value="愛知県" $PFLAG{'愛知県'}>愛知県
<option value="三重県" $PFLAG{'三重県'}>三重県
<option value="滋賀県" $PFLAG{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG{'京都府'}>京都府
<option value="大阪府" $PFLAG{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG{'島根県'}>島根県
<option value="岡山県" $PFLAG{'岡山県'}>岡山県
<option value="広島県" $PFLAG{'広島県'}>広島県
<option value="山口県" $PFLAG{'山口県'}>山口県
<option value="徳島県" $PFLAG{'徳島県'}>徳島県
<option value="香川県" $PFLAG{'香川県'}>香川県
<option value="愛媛県" $PFLAG{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG{'高知県'}>高知県
<option value="福岡県" $PFLAG{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG{'長崎県'}>長崎県
<option value="熊本県" $PFLAG{'熊本県'}>熊本県
<option value="大分県" $PFLAG{'大分県'}>大分県
<option value="宮崎県" $PFLAG{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG{'沖縄県'}>沖縄県
</select>
<br />
※居住等は問いません。参加希望の都道府県でご参加頂けます。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">活動拠点／主に利用する<br />
グラウンドののある市町村名</td>
<td bgcolor="#ffffff">$team_pref $team_cities</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第一担当者名</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$shimei1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム代表者PCメールアドレス</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$mailaddress1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者携帯番号</font></td>
<td bgcolor="#ffffff">$tel1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者名</font></td>
<td bgcolor="#ffffff">$shimei2
<br />
※事務局から第一担当者と連絡がつかなかった場合は、第二担当者に電話連絡を行います。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者携帯番号</font></td>
<td bgcolor="#ffffff">$tel2
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望曜日</font></td>
<td bgcolor="#ffffff">
<input tabindex="21" type="checkbox" name="week" id="week0" value="土日祝" $WEEKFLAG{'土日祝'} />
<font class="type3">土日祝　</font>
<input tabindex="22" type="checkbox" name="week" id="week1" value="土日" $WEEKFLAG{'土日'} />
<font class="type3">土日　</font>
<input tabindex="25" type="checkbox" name="week" id="week4" value="土曜日" $WEEKFLAG{'土曜日'} />
<font class="type3">土曜日　</font>
<input tabindex="23" type="checkbox" name="week" id="week2" value="日曜日" $WEEKFLAG{'日曜日'} />
<font class="type3">日曜日　</font>
<input tabindex="24" type="checkbox" name="week" id="week3" value="日祝" $WEEKFLAG{'日祝'} />
<font class="type3">日祝　</font>
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信確認画面へ　　" />
</div>
</form>

</div>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# 大会エントリー：確認
# -----------------------------------------------------------------
sub gameentry_check {
#ログインチェック
if($loginuser eq ""){
$mes =<<"END_HTML";
ログインして下さい。<br>
<br>
<input type="button" value="　TOPへ　" onclick="location.href='$sitefulladr'" />
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if
#チーム情報をGET
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div align=center>
<br>
<p style="color:red;">チーム情報が見つかりません。</p>
<p>もう一度ログインをお願いします。</p>
<br>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$shimei1 = &paramsetsql('shimei1');
$mailaddress1 = &paramsetsql('mailaddress1');
$tel1 = &paramsetsql('tel1');
$shimei2 = &paramsetsql('shimei2');
$tel2 = &paramsetsql('tel2');
$mailaddress2 = &paramsetsql('mailaddress2');
$teamname = &paramsetsql('teamname');
$team_pref = &paramsetsql('team_pref');
$team_cities = &paramsetsql('team_cities');
###
for my $p ($query->param) {
	if($p eq ""){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
	$paramhash{$p} = $v;
$list .="$p : $v<br>\n";
}	#for
#大会選択
@TAIKAI = $query->param('taikainum');
$temp ="";
foreach(@TAIKAI){
($tc,$tg) = split(/:/,$_);
$temp .= "「".&taikainame_get($tc,$tg)."」\n";
}	#foreach
$taikailist = &crlfreset2($temp);
$taikai = join("<>",@TAIKAI);

#県
$pref = $paramhash{'pref'};
#曜日選択
@WEEK = $query->param('week');
foreach(@WEEK){utf8::decode($_);$weeklist.=$_."、";}
chop($weeklist);
$w = join(":",@WEEK);

#項目セット
$rewritestr =<<"END_HTML";
<input type="hidden" name="taikainum" value="$taikai" />
<input type="hidden" name="weeklist" value="$w" />
<input type="hidden" name="pref" value="$paramhash_enc{'pref'}" />
<input type="hidden" name="ses" value="$paramhash_enc{'ses'}" />
END_HTML

#####
#重複登録チェック
($teamname,$teamnum) = &taikaiteamname_get2($loginuser);
foreach (split(/<>/,$taikai)){
($taikaicode,$category) = split(/:/,$_);
$sql_str = "SELECT * FROM entrylist WHERE taikaicode = $taikaicode and category = $category and teamnum = $teamnum and teamsession = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$mes =<<"END_HTML";
<div align=center>
<br>
<p style="color:red;font-weight:bold;font-size:20px;">重複登録がされました。</p>
<p>処理を中止します。</p>
<br>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if 重複
}	#foreach


#####
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gaenti.jpg" alt="大会エントリー" width="980" height="48" /> </div>

<div id="mainbox">
<h2 class="subti" id="1">大会エントリーフォーム</h2>
<div class="box">
<p>以下の情報で登録します。よろしければ「エントリーする」ボタンを押してください。</p>

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">参加大会</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td width="76%" bgcolor="#ffffff">
$taikailist
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望都道府県</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">
$pref
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">活動拠点／主に利用する<br />
グラウンドののある市町村名</td>
<td bgcolor="#ffffff">$team_pref $team_cities</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第一担当者名</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$shimei1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム代表者PCメールアドレス</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$mailaddress1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者携帯番号</font></td>
<td bgcolor="#ffffff">$tel1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者名</font></td>
<td bgcolor="#ffffff">$shimei2
<br />
※事務局から第一担当者と連絡がつかなかった場合は、第二担当者に電話連絡を行います。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者携帯番号</font></td>
<td bgcolor="#ffffff">$tel2
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望曜日</font></td>
<td bgcolor="#ffffff">
$weeklist
</td>
</tr>
</tbody>
</table>

<br />

<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type=hidden name="code" value="gameentry" />
$rewritestr
<input type="submit" value="修正する" />
</form>

<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type=hidden name="code" value="gameentry_add" />
$rewritestr
<input type="submit" value="エントリーする" />
</form>

</div>
</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub





# -----------------------------------------------------------------
# 大会エントリー：確認
# -----------------------------------------------------------------
sub gameentry_add {
#ログインチェック
if($loginuser eq ""){
$mes =<<"END_HTML";
ログインして下さい。<br>
<br>
<input type="button" value="　TOPへ　" onclick="location.href='$sitefulladr'" />
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if

#チーム情報をGET
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div align=center>
<br>
<p style="color:red;">チーム情報が見つかりません。</p>
<p>もう一度ログインをお願いします。</p>
<br>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$shimei1 = &paramsetsql('shimei1');
$mailaddress1 = &paramsetsql('mailaddress1');
$tel1 = &paramsetsql('tel1');
$shimei2 = &paramsetsql('shimei2');
$tel2 = &paramsetsql('tel2');
$mailaddress2 = &paramsetsql('mailaddress2');
$teamname = &paramsetsql('teamname');
$team_pref = &paramsetsql('team_pref');
$team_cities = &paramsetsql('team_cities');
###
for my $p ($query->param) {
	if($p eq ""){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
	$paramhash{$p} = $v;
$list .="$p : $v<br>\n";
}	#for

#大会
$taikainum = $paramhash{'taikainum'};
foreach(split(/<>/,$taikainum)){
($tc,$category) = split(/:/,$_);
$temp .= "「".&taikainame_get($tc,$category)."」\n";
$taikailisttemp .= "・".&taikainame_get($tc,$category)."\n";
}	#foreach
$taikailist = &crlfreset2($temp);

#県
$pref = $paramhash_dec{'pref'};
#実績
$pr = $paramhash_dec{'pr'};
#曜日
$weeklist = $paramhash{'weeklist'};
foreach(split(/:/,$weeklist)){
$week .= "$_、";
}	#foreach
chop($week);



#########################
# データベースへ登録
#大会別に登録
$cnt = 0;
($teamname,$teamnum) = &taikaiteamname_get2($loginuser);
foreach (split(/<>/,$taikainum)){
($taikaicode,$category) = split(/:/,$_);
#重複登録チェック
$sql_str = "SELECT * FROM entrylist WHERE taikaicode = $taikaicode and category = $category and teamnum = $teamnum and teamsession = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$mes =<<"END_HTML";
<div align=center>
<br>
<p style="color:red;font-weight:bold;font-size:20px;">重複登録がされました。</p>
<p>処理を中止します。</p>
<br>
</div>
END_HTML
&taikaihtmldisp($mes);
exit;
}	#if 重複
#
$sql_str = qq{INSERT INTO entrylist(taikaicode,category,teamnum,teamsession,pref,pr,weeklist,payment,createdate) VALUES (?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$taikaicode,
$category,
$teamnum,
$loginuser,
$pref,
$pr,
$weeklist,
0,
$nowdate,
);
&sqlcheck($sql_str);
#金額
$COSTBOX{$taikaicode}++;
$CATEBOX{$taikaicode}{$category}=1;
}	#foreach

#金額計算
$list = "";
foreach $taikaicode(keys %COSTBOX){
$cnt = $COSTBOX{$taikaicode};
# 大会情報
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 and serial = $taikaicode ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){die "taikai info error! $count $sql_str";}
$REFHASH = $rs->fetchrow_hashref;
$taikainame = &paramsetsql('title');
$price1 = &paramsetsql('price1');
$price2 = &paramsetsql('price2');
$price3 = &paramsetsql('price3');
if($cnt == 1 && $CATEBOX{$taikaicode}{1} == 1){$cost = $price1;$entryinfo = "リーグのみ参加";}
if($cnt == 1 && $CATEBOX{$taikaicode}{2} == 1){$cost = $price2;$entryinfo = "トーナメントのみ参加";}
if($cnt == 2){$cost = $price3;$entryinfo = "リーグおよびトーナメント参加";}
$totalcost += $cost;
$coststr = &ketakanma($cost);
$list .=<<"HTML_END";
大会名：$taikainame（$entryinfo）
費　用：${coststr}円
-------------------------------------------------------
HTML_END
}	#foreach
$totalcost = &ketakanma($totalcost);

###
# 控えメール送付
###メール：ユーザー宛
$mailbody =<<"HTML_END";
大会へのエントリーありがとうございます。

以下の情報でエントリーを受け付けました。
ご入金お手続きいただきました後、正式エントリーとなります。
お手数ですが、下記指定口座へご入金または、
オンライン決済のお支払いも可能です。

【エントリー詳細】
-------------------------------------------------------
$list
【ご入金金額合計】
${totalcost}円

【ネット決済について】
http://pridejapan.shop13.makeshop.jp/

【振込先口座番号について】
・GMOあおぞらネット銀行　法人第二営業部　
・普通預金口座　1545251
・ビーエスオー（カ

お振込みの際は必ず「チーム名＋代表者氏名」名義でお振込み下さい。
（例）チーム名　アストロズ　　代表者氏名　山田太郎　の場合
　　「振込み名義」アストロズヤマダタロウ

※恐れ入りますが振込み手数料はご負担下さい。
※本メール受信日を含む７日以内にご入金下さい（７日以内にご入金がない場合
は一旦、仮エントリーを取り消しといたします。予めご了承下さい。）
※入金確認後、受付完了メールを送信いたしますのでご確認下さい。
（入金確認には３日～５日程度の時間がかかる場合があります）


=======================================================
エントリー内容控え
【参加大会】
$taikailisttemp
【大会参加希望都道府県】
$pref

【大会参加希望曜日】
$week

=======================================================
PRIDE JAPAN運営事務局
HTML_END
#
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
$subject = Unicode::Japanese->new("大会にエントリー頂きありがとうございます｜PRIDE JAPAN",'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"HTML_END";
From: info\@$domain
To: $mailaddress1
Cc:info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Type: text/plain; charset="ISO-2022-JP" 
HTML_END
#メーラーOPEN
open(MAIL, "| $sendmail");
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

#####
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/gaenti.jpg" alt="大会エントリー" width="980" height="48" /> </div>

<div id="mainbox">
<h2 class="subti" id="1">大会エントリーフォーム</h2>
<div class="box">
<p>以下の情報でエントリーを受け付けました。<br>
自動返信メールを送信しますので、詳細をご確認下さい。</p>

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">参加大会</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td width="76%" bgcolor="#ffffff">
$taikailist
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望都道府県</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">
$pref
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2">活動拠点／主に利用する<br />
グラウンドののある市町村名</td>
<td bgcolor="#ffffff">$team_pref $team_cities</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第一担当者名</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$shimei1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム代表者PCメールアドレス</font><font class="type1" color="#ff0000">&nbsp;</font></td>
<td bgcolor="#ffffff">$mailaddress1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者携帯番号</font></td>
<td bgcolor="#ffffff">$tel1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者名</font></td>
<td bgcolor="#ffffff">$shimei2
<br />
※事務局から第一担当者と連絡がつかなかった場合は、第二担当者に電話連絡を行います。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第二担当者携帯番号</font></td>
<td bgcolor="#ffffff">$tel2
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">大会参加希望曜日</font></td>
<td bgcolor="#ffffff">
$week
</td>
</tr>
</tbody>
</table>

<p align=center><a href="$sitefulladr/system.cgi"><img src="img/mypage.jpg" ALT="マイページへ戻る" /><br>マイページへ戻る</a></p>

</div>
</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub





# -----------------------------------------------------------------
# 大会エントリー：入金確認
# -----------------------------------------------------------------
sub ajaxsave_payment {
$ss = $paramhash{'s'};
#$category = $paramhash{'c'};
#$teamnum = $paramhash{'tn'};
#履歴保存
$sql_str9 = qq{INSERT INTO entrylist_rireki(ss,refara,remoteaddr,host,cgi,querystring) VALUES (?,?,?,?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$ss,
$ENV{'HTTP_REFERER'},
$ENV{'REMOTE_ADDR'},
$ENV{'HTTP_HOST'},
"system.cgi",
$ENV{'QUERY_STRING'},
);

#リファラ無しは弾く
if($ENV{'HTTP_REFERER'} eq ""){
#履歴保存
$sql_str9 = qq{INSERT INTO entrylist_rireki(ss,refara,remoteaddr,host,cgi,querystring,mes) VALUES (?,?,?,?,?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$ss,
$ENV{'HTTP_REFERER'},
$ENV{'REMOTE_ADDR'},
$ENV{'HTTP_HOST'},
"system.cgi",
$ENV{'QUERY_STRING'},
"リファラなし",
);
exit;
}	#if

#要素調査
$sql_str = "SELECT * FROM entrylist WHERE serial = '$ss' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
#履歴保存
$sql_str9 = qq{INSERT INTO entrylist_rireki(ss,refara,remoteaddr,host,cgi,querystring,mes) VALUES (?,?,?,?,?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$ss,
$ENV{'HTTP_REFERER'},
$ENV{'REMOTE_ADDR'},
$ENV{'HTTP_HOST'},
"system.cgi",
$ENV{'QUERY_STRING'},
"エラーss=$ss,cnt=$count",
);
print "9<>$ss<>".sprintf("%d年%d月%d日 %d時%d分",$year,$month,$mday,$hour,$min)."<>エラーss=$ss,cnt=$count";
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$payment = 9;
if(&paramsetsql('payment',$REFHASH) == 0){$payment = 1;}
if(&paramsetsql('payment',$REFHASH) == 1){$payment = 0;}
#アップデート
$sql_str = "UPDATE entrylist SET payment = $payment , paymentdate = '$nowdate' WHERE serial = '$ss' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);



#返す
print "$payment<>$ss<>".sprintf("%d年%d月%d日 %d時%d分",$year,$month,$mday,$hour,$min)."<>$count";
exit;
}	#sub




# -----------------------------------------------------------------
# 大会通信
# -----------------------------------------------------------------
sub taikaireport {
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$taikainame = &paramsetsql('title');
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[1]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$mes .= "<div class='taikai'><a href='system.cgi?code=report&taikaicode=$taikaicode'><img src='system/file/$TEMP[0].jpg' ALT='$taikainame' width='440' height='114' /></a></div>";}
}	#if 存在
}	#for 
# width='265' height='69' 　小さい方
# width='440' height='114'　大きい方
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub


# -----------------------------------------------------------------
# 試合結果
# -----------------------------------------------------------------
sub taikairesult {
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$taikainame = &paramsetsql('title');
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[1]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$mes .= "<div class='taikai'><a href='system.cgi?code=result&taikaicode=$taikaicode'><img src='system/file/$TEMP[0].jpg' ALT='$taikainame' width='440' height='114' /></a></div>";}
}	#if 存在
}	#for 　http://pridejapan.net/system.cgi?code=result&taikaicode=3
# width='265' height='69' 　小さい方
# width='440' height='114'　大きい方
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub





# -----------------------------------------------------------------
# 大会内：試合予定一覧
# -----------------------------------------------------------------
sub scheduleall {
$tyear = $paramhash{'y'};
$tmonth = $paramhash{'m'};
if($tyear eq "" || $tmonth eq ""){
$tyear = $year;
$tmonth = $month;
}	#if
$byear = $nyear = $tyear;
$bmonth = $nmonth = $tmonth;
#前月
$bmonth--;
if($bmonth < 1 ){$byear--;$bmonth+=12;}
#次月
$nmonth++;
if($nmonth > 12 ){$nyear++;$nmonth-=12;}
#
$nn = sprintf("%04d-%02d-",$tyear,$tmonth);


# 大会リスト
$sql_str9 = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute();
$count9 = $rs9->rows;	# Hit件数を確保
for($p = 0;$p < $count9;$p++){	# データベース１件ずつ
$REFHASH9 = $rs9->fetchrow_hashref;
$taikaicode = &paramsetsql('serial',$REFHASH9);

################################################################################
# リーグ
################################################################################
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
for($k=0;$k<$count1;$k++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}

$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}

$taikainame = &taikainame_get($taikaicode,1);	#大会名GET

# vsチームを分解
#print "vsdata=".$vsdata."<br>"; 
foreach $temp2(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp2);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
#print "tss1=$tss1 , tss2=$tss2<br>\n";
if($tss1 eq "" || $tss2 eq ""){next;}
($tss1name,$tss1ses) = &taikaiteamname_get3($tss1);
($tss2name,$tss2ses) = &taikaiteamname_get3($tss2);
#各チームの報告から「試合日時」と「場所」をGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = $setu and text1 = $num and nichiji1 like '$nn%' ORDER BY serial ASC LIMIT 1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>"; 
if($count2 == 0){next;}
#両チーム報告
if($count2 == 2){
#チーム
$REFHASH2 = $rs2->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH2);
$ground1 = &paramsetsql('body',$REFHASH2);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
#if($tss1 != $teamnum1){
#もう一方のチーム
#$REFHASH2 = $rs2->fetchrow_hashref;
#$ground = &paramsetsql('body',$REFHASH2);
#$n1 = &paramsetsql('nichiji1',$REFHASH2);
#$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
#}	#if
#入力チェック
#print "$n1 ne $n2<br>";
#if($n1 eq $n2){
#if($ground1 ne $ground2){
#$ground1 .= "（$ground2）";
#$ground2 ="";
#}	#if
}else{
#片方のチームが報告
$REFHASH2 = $rs2->fetchrow_hashref;
#$taikaicode = &paramsetsql('taikaicode',$REFHASH2);
$ground1 = &paramsetsql('body',$REFHASH2);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
}	#if 両チーム


@TEMP = split(/ /,$n1);
($yy,$mm,$d) = split(/-/,$TEMP[0]);
if(!Date::Simple->new(sprintf("%04d-%02d-%02d",$yy,$mm,$d))){next;}
$date = Date::Simple->new(sprintf("%04d-%02d-%02d",$yy,$mm,$d));
$mm -=0;
$d -=0;
$nichijistr = sprintf("%d年%d月%d日",split(/-/,$TEMP[0]));
($shour,$smin,$sc) = split(/:/,$TEMP[1]);
$nichijistr2 = sprintf("%d：%02d〜",split(/:/,$TEMP[1]));
$week = $date->day_of_week;
$weekstr = $WEEKNAME[$week];
if($week == 0){$weekstr = "<font class='type3' color='#ff0000'>日</font>";}
if($week == 6){$weekstr = "<font class='type3' color='#0000ff'>土</font>";}
#
$DD{$yy}{$mm}{$d} .=<<"END_HTML";
<tr>
%checkday%
%checkweek%
<th align="center" scope="row" nowrap >$nichijistr2&nbsp;</th>
<th width="212" align="right" scope="row">$tss1name&nbsp;</th>
<th width="31" align="center" scope="row">VS</th>
<th width="213" align="left" scope="row">$tss2name&nbsp;</th>
<th align="left" scope="row">$ground1&nbsp;</th>
<th align="left" scope="row"><b>$taikainame</b><br>$areaname/$kuminame/第${setu}節</th>
</tr>
END_HTML
$CC{$yy}{$mm}{$d}++;
#}	#if	n1 n2
#}	#if count
}	#foreach
}	#for k



################################################################################
# トーナメント
################################################################################
@CNT = (0,1,2,4,8,16,32,64,128);
$setu = "";
$kumi = "";
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '2' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1." $sql_str1<br>\n";
for($jj=0;$jj<$count1;$jj++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}

$kumi = &paramsetsql('kumi',$REFHASH1);
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
%TEAMLIST = ();
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";
$k+=2;
}	#foreach x
}	#foreach y

#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan";

#トーナメント○回戦
foreach $y(1..7){
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$d = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2);
#報告範囲内
#if( $d1 <= $d && $d <= $d2){
$cnt2 = $CNT[$y];
$num = $y;
foreach $x(1..$cnt2){
if($TEAMLIST{$y}{$x}{1} eq "" || $TEAMLIST{$y}{$x}{2} eq ""){next;}

$tss    = $TEAMLIST{$y}{$x}{1};
$aitess = $TEAMLIST{$y}{$x}{2};
$tss1name = &taikaiteamname_get($tss);
$tss2name = &taikaiteamname_get($aitess);
#print "tss=$tss、aitess=$aitess<br>\n";

$aiteteam = &taikaiteamname_get($aitess);
@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));
$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num+2)."回戦";
}	#num

$flag = 0;
$flag1 = 0;
$flag2 = 0;
### 両チームの予定報告
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 34 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 and area = $area and kumi = '$x' and text1 = '$y' and (teamnum = $tss or teamnum = $aitess) and nichiji1 like '$nn%' ORDER BY serial ASC LIMIT 1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#for($h=0;$h<$count2;$h++){
#print "$count2 $sql_str2<br>";
=pot
#今までのやりかた
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
$tss1name = &taikaiteamname_get($teamnum1);
$linkadr = &paramsetsql('linkadr',$REFHASH2);
($tss2name,$teamserial) = &taikaiteamname_get2($linkadr);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$ground1 = &paramsetsql('body',$REFHASH2);
$area = &paramsetsql('area',$REFHASH2);
$areaname = &taikaiareaname_get($area);
=cut

if($count2 == 0){next;}

#print "count2=$count2 $sql_str2<br>\n";
#for($h=0;$h<$count2;$h++){
=pot
#両報告の場合
if($count2 == 2){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
#両チームで、報告が左チームからの場合
if($tss == $teamnum1){
$tss1name = &taikaiteamname_get($teamnum1);
$linkadr = &paramsetsql('linkadr',$REFHASH2);
($tss2name,$teamserial) = &taikaiteamname_get2($linkadr);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$ground1 = &paramsetsql('body',$REFHASH2);
$area2 = &paramsetsql('area',$REFHASH2);
$areaname = &taikaiareaname_get($area2);
#もう一方の報告は捨てる？
$REFHASH2 = $rs2->fetchrow_hashref;
}	#if
}	#if 両報告の場合
=cut

#片報告の場合
#if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH2);
$tss1name = &taikaiteamname_get($teamnum1);
$linkadr = &paramsetsql('linkadr',$REFHASH2);
($tss2name,$teamserial) = &taikaiteamname_get2($linkadr);
$n1 = &paramsetsql('nichiji1',$REFHASH2);
$ground1 = &paramsetsql('body',$REFHASH2);
$area2 = &paramsetsql('area',$REFHASH2);
$areaname = &taikaiareaname_get($area2);
#}	#

#対戦日時のGET
@TEMP = split(/ /,$n1);
($yy,$mm,$d) = split(/-/,$TEMP[0]);
if(!Date::Simple->new(sprintf("%04d-%02d-%02d",$yy,$mm,$d))){next;}
$mm -=0;
$d -=0;
$nichijistr2 = sprintf("%d：%02d〜",split(/:/,$TEMP[1]));
#$ground = $ground1;
#if($ground1 ne $ground2){$ground = "$ground1（$ground2）";}
#print "{$yy}{$mm}{$d}<br>\n";
##
$taikainame = &taikainame_get($taikaicode,2);	#大会名GET

#重複チェック
#if($tss1name eq "高槻市役所" || $tss1name eq "大阪ブルーソックス" ){
#$debug .=<<"END_HTML";
#$tss1name taikaicode=$taikaicode area=$area y=$y x=$x <br>
#END_HTML
#}


if($teamnum1 < $teamserial){$temp = "$teamnum1:$teamserial"}else{$temp = "$teamserial:$teamnum1"}

if($DPCHECK{$taikaicode}{$area}{$y}{$x}{$temp} == 1){next;}
$DPCHECK{$taikaicode}{$area}{$y}{$x}{$temp} = 1;

#
$DD{$yy}{$mm}{$d} .=<<"END_HTML";
<tr>
%checkday%
%checkweek%
<th align="center" scope="row" nowrap >$nichijistr2&nbsp;</th>
<th width="212" align="right" scope="row">$tss1name&nbsp;</th>
<th width="31" align="center" scope="row">VS</th>
<th width="213" align="left" scope="row">$tss2name&nbsp;</th>
<th align="left" scope="row">$ground1&nbsp;</th>
<th align="left" scope="row"><b>$taikainame</b><br>$areaname/$numstr</th>
</tr>
END_HTML
$CC{$yy}{$mm}{$d}+=1;
#print "{$yy}{$mm}{$d} $CC{$yy}{$mm}{$d}<br>\n";
#}	#foreach h count2
}	#foreach x
}	#if nichiji
}	#foreach 1-7
}	#for jj
########################################
}	#大会ループ

#日付まとめ
$lastday = &urudays($tyear,$tmonth);
$date = Date::Simple->new(sprintf("%04d-%02d-%02d",$tyear,$tmonth,1));
$week = $date->day_of_week;
foreach $k(1..$lastday){
$weekstr = $WEEKNAME[$week];
if($week > 6){$week = 0;}
if($week == 0){$weekstr = "<font class='type3' color='#ff0000'>日</font>";}
if($week == 6){$weekstr = "<font class='type3' color='#0000ff'>土</font>";}
$week++;
#print "{$tyear}{$tmonth}{$k} $CC{$tyear}{$tmonth}{$k}<br>\n";
if($CC{$tyear}{$tmonth}{$k} == 0){
$DD{$tyear}{$tmonth}{$k} =<<"END_HTML";
<tr>
<th align='center' scope='row' nowrap >$k</th>
<th align="center" scope="row">$weekstr&nbsp;</th>
<th align="center" scope="row" nowrap >&nbsp;</th>
<th width="162" align="right" scope="row">&nbsp;</th>
<th width="31" align="center" scope="row">&nbsp;</th>
<th width="162" align="left" scope="row">&nbsp;</th>
<th align="left" scope="row">&nbsp;</th>
<th align="left" scope="row">&nbsp;</th>
</tr>
END_HTML
}	#if
if($CC{$tyear}{$tmonth}{$k} == 1){
$temp = "<th align='center' scope='row' nowrap >$k</th>";
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkday\%/$temp/;
$temp = "<th align='center' scope='row'>$weekstr</th>";
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkweek\%/$temp/;
}	#if
if($CC{$tyear}{$tmonth}{$k} > 1){
$temp = "<th align='center' scope='row' rowspan='$CC{$tyear}{$tmonth}{$k}' nowrap  >$k</th>";
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkday\%/$temp/;
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkday\%//g;
$temp = "<th align='center' scope='row' rowspan='$CC{$tyear}{$tmonth}{$k}' >$weekstr</th>";
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkweek\%/$temp/;
$DD{$tyear}{$tmonth}{$k} =~ s/\%checkweek\%//g;
}	#if

}	#foreach






####
$date = Date::Simple->new(sprintf("%04d-%02d-%02d",$tyear,$tmonth,1));
$week = $date->day_of_week;
foreach $d(1..$lastday){
$list .= $DD{$tyear}{$tmonth}{$d};
}	#foreach


####

#########
$mes =<<"END_HTML";
<style type="text/css">
#navigation li.menu5 a {
	background:url(img/menu.jpg) no-repeat -664px -47px;
}
</style>

<div id="mainbox">
<div id="mon">
<div class="mon1"><a href="?y=$byear&m=$bmonth"><img src="img/mon1.jpg" width="114" height="33" /></a></div>
<div class="mon2">${tyear}年<span class="moj1">$tmonth</span><span class="moj2">月</span></div>
<div class="mon3"><a href="?y=$nyear&m=$nmonth"><img src="img/mon2.jpg" width="114" height="33" /></a></div>
</div>

<table width="100%" cellspacing="0" class="stane">
<tr>
<th  align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row">日</th>
<th   align="center" class="underl" style="font-size: 14px; font-weight: bold;" scope="row" nowrap>曜日</th>
<th  align="center" class="underl" style="font-size: 14px; font-weight: bold;" nowrap>時間</th>
<th colspan="3" align="center" class="underl" style="font-size: 14px; font-weight: bold;">試合</th>
<th width="20%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">場所</th>
<th width="25%" align="center" class="underl" style="font-size: 14px; font-weight: bold;">名称</th>
</tr>
$list
</table>

</div>
END_HTML
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub



# -----------------------------------------------------------------
# 大会内：エントリー状況
# -----------------------------------------------------------------
sub entrysituation {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
$areacnt = 0;
###################################
# リーグ
$entrylist = "";
#エリア
$sql_str9 = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  ";
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute();
$count9 = $rs9->rows;	# Hit件数を確保
#print "count9=$count9 $sql_str9<br>\n";
for($i = 0;$i < $count9;$i++){	# データベース１件ずつ
$REFHASH9 = $rs9->fetchrow_hashref;
$area = &paramsetsql('serial',$REFHASH9);
$areaserial = &paramsetsql('serial',$REFHASH9);
$areaname = &taikaiareaname_get($area);

### エントリー一覧
#対戦チーム一覧
$teamlist = "";
$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1,sql_str1  = $sql_str1 <br>\n";
%TSS =();
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$tss = &paramsetsql('teamnum',$REFHASH1);
#print "tss  = $tss <br>\n";
$TSS{$tss} = 1;
}	#for
#入金確認
foreach $tss(keys %TSS){
$teamname = &taikaiteamname_get($tss);
$sql_str = "SELECT * FROM entrylist WHERE taikaicode = '$taikaicode' and category = 1 and teamnum = $tss and payment = 1 ORDER BY lastupdated DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$PAY{$tss} = 1;
$areacnt++;
}	#if
}	#foreach
$entrylist .=<<"END_HTML";
<div class="enteam">
<table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr>
<td width="50%" align="center" bgcolor="#FFFFCC">$areaname</td>
<td width="50%" align="center">${areacnt}チーム</td>
</tr>
</table>
</div>
END_HTML
$areacnt = 0;
}	#for
if($entrylist ne ""){
$entrylist =<<"END_HTML";
<h2 class="subti" id="$areaserial">リーグ</h2>
$entrylist
END_HTML
}	#if

###################################
# トーナメント
$entrylist2 = "";
#エリア
$sql_str9 = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2  ";
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute();
$count9 = $rs9->rows;	# Hit件数を確保
#print "count9=$count9<br>\n";
for($i = 0;$i < $count9;$i++){	# データベース１件ずつ
$REFHASH9 = $rs9->fetchrow_hashref;
$area = &paramsetsql('serial',$REFHASH9);
$areaserial = &paramsetsql('serial',$REFHASH9);
$areaname = &taikaiareaname_get($area);

### エントリー一覧
#対戦チーム一覧
%TSS = ();
$teamlist = "";
$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area'  ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1,sql_str1  = $sql_str1 <br>\n";
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$tss = &paramsetsql('teamnum',$REFHASH1);
#print "tss  = $tss <br>\n";
$TSS{$tss} = 1;
}	#for
#入金確認
%PAY = ();
$areacnt = 0;
foreach $tss(keys %TSS){
$teamname = &taikaiteamname_get($tss);
$sql_str = "SELECT * FROM entrylist WHERE taikaicode = '$taikaicode' and category = 2 and teamnum = $tss and payment = 1 ORDER BY lastupdated DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$PAY{$tss} = 1;
$areacnt++;
}	#if
}	#foreach
$entrylist2 .=<<"END_HTML";
<div class="enteam">
<table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr>
<td width="50%" align="center" bgcolor="#FFFFCC">$areaname</td>
<td width="50%" align="center">${areacnt}チーム</td>
</tr>
</table>
</div>
END_HTML
x}	#for
if($entrylist2 ne ""){
$entrylist2 =<<"END_HTML";
<h2 class="subti" id="$areaserial">トーナメント</h2>
$entrylist2
END_HTML
}	#if


###################################
$mes =<<"END_HTML";
<style type="text/css">
#navigation li.menu2 a {
	background:url(img/menu.jpg) no-repeat -196px -47px;
}
</style>

<div id="mtop">
<div id="mtop1"><img src="img/taiti2.jpg" alt="大会メニュー" width="183" height="48" /></div>
<div id="mtop2">$taikainame</div>
<div id="mtop3"><a href="system.cgi?code=entrysituation&taikaicode=$taikaicode"><img src="img/taien.jpg" alt="大会メニュー" width="223" height="32" /></a></div>
</div>

<div id="navigation2">
<ul>
<li class="menu0"><a href="?code=convention&taikaicode=$taikaicode">大会イメージ</a></li>
<li class="menu1"><a href="?code=outline&taikaicode=$taikaicode">大会概要／規定</a></li>
<li class="menu2"><a href="?code=result&taikaicode=$taikaicode">大会結果</a></li>
<li class="menu3"><a href="?code=ranking&taikaicode=$taikaicode">順位／星取表</a></li>
<li class="menu4"><a href="?code=report&taikaicode=$taikaicode">大会記事</a></li>
<li class="menu5"><a href="?code=schedule&taikaicode=$taikaicode">試合予定一覧</a></li>
</ul>
</div>

<div id="mainbox">

$entrylist


$entrylist2

<div class="clear"></div>
</div>
END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# TOP：新規チーム紹介
# -----------------------------------------------------------------
sub newteamlist {
$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 0 ORDER BY createdate DESC LIMIT 10";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$ses = &paramsetsql('ssid');
$teamname = &paramsetsql('teamname');
$team_pr = &paramsetsql('team_pr');
$team_pref = &paramsetsql('team_pref');
$createdate = &paramsetsql('createdate');
if($createdate ne ""){
$n1 = Date::Simple->new();
@TEMP = split(/ /,$createdate);
$n2 = Date::Simple->new($TEMP[0]);
if( ($n1 - $n2) < 7){$newicon = " <img src='img/new.gif' ALT='' />";}else{$newicon ="";}
}	#if
$team_pr_short = "";
if(length($team_pr) > 20){
$team_pr_short = substr($team_pr,0,20)."...<a href='javascript:tagopen($ss)'>続きをみる≫</a>";
}	#if
$team_pr =<<"END_HTML";
<div id="nttag1_$ss">
$team_pr_short
</div>
<div id="nttag2_$ss" style='display:none;'>
$team_pr
<a href='javascript:tagopen($ss)'> ≪閉じる</a>
</div>
END_HTML
#画像
=pot
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[0]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$imgsrc .= "<img src='system/file/$TEMP[0]s.jpg' ALT='$teamname' />";}
}	#if 存在
=cut
#
$mes .=<<"END_HTML";
<div class="ball2"><a href='system.cgi?code=mypage_team&ses=$ses'>$newicon$teamname($team_pref)</a></div>
<div class="baph1">$imgsrc</div>
<div class="baph2">
<div class="baph3"><a href='system.cgi?code=mypage_team&ses=$ses'><img src='img/syou.jpg' width="58" height="19" /></a></div>
</div>
END_HTML
}	#for
###
$mes =<<"END_HTML";
<script>
function tagopen(ss){
if(document.getElementById('nttag2_'+ss).style.display == 'none'){
document.getElementById('nttag1_'+ss).style.display = 'none';
document.getElementById('nttag2_'+ss).style.display = 'block';
}else{
document.getElementById('nttag1_'+ss).style.display = 'block';
document.getElementById('nttag2_'+ss).style.display = 'none';
}
}
</script>
$mes
END_HTML
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub







# -----------------------------------------------------------------
# TOP：試合結果速報
# -----------------------------------------------------------------
sub sokuhou {
#セッション作成
$session = sprintf("%02d%02d%02d",$sec,$min,$hour);
for (1..15) { $session .= ((0..9,a..z,A..Z)[int rand 62])};
$session .= sprintf("%02d%02d%02d",$mday,$month,$year-2000);

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$category = $REFHASH->{'category'};
if($category == 1){$sc = 1;$ec = 1;}
if($category == 2){$sc = 2;$ec = 2;}
if($category == 3){$sc = 1;$ec = 2;}

foreach $cate($sc .. $ec){
$taikainame = &taikainame_get($taikaicode, $cate);

##########################################################
# リーグ
##########################################################
if($cate == 1){
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode'  ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
#print "sql_str1=$sql_str1<br>\n";
$count1 = $rs1->rows;	# Hit件数を確保
for($k=0;$k<$count1;$k++){
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
$body = &paramsetsql('body',$REFHASH1);
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);

# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
if($tss1 eq "" || $tss2 eq ""){next;}
#試合結果をGET
#$sql_str4 = "SELECT * FROM $dbname WHERE contents = 35 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ";

$sql_str4 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = $setu and text1 = $num and teamnum = $tss2 ";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$count4<br>\n";
if($count4 == 1){
$REFHASH4 = $rs4->fetchrow_hashref;
$teamnum1 = &paramsetsql('teamnum',$REFHASH4);
$syouhai1 = &paramsetsql('resultstr',$REFHASH4);
$result10 = &paramsetsql('result0',$REFHASH4);
$result11 = &paramsetsql('result1',$REFHASH4);
$posi1 = &paramsetsql('linkadrtitle',$REFHASH4);
$date1 = &paramsetsql('timestamp',$REFHASH4);
@TEMP1 = split(/ /,$date1);
$dates1 = sprintf("%04d%02d%02d%02d%02d%02d",split(/-/,$TEMP1[0]),split(/:/,$TEMP1[1]));
$dates11 = Date::Simple->new($TEMP1[0]);
}	#if

$sql_str5 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = $taikaicode and category = 1 and area = $area and kumi = $kumi and title = $setu and text1 = $num and teamnum = $tss1 ";
$rs5 = $dbh->prepare($sql_str5);
$rs5->execute();
&sqlcheck($sql_str5);
$count5 = $rs5->rows;	# Hit件数を確保
#print "count5=$count5<br>\n";
if($count5 == 1){
$REFHASH5 = $rs5->fetchrow_hashref;
$teamnum2 = &paramsetsql('teamnum',$REFHASH5);
$syouhai2 = &paramsetsql('resultstr',$REFHASH5);
$result20 = &paramsetsql('result0',$REFHASH5);
$result21 = &paramsetsql('result1',$REFHASH5);
$posi2 = &paramsetsql('linkadrtitle',$REFHASH5);
$date2 = &paramsetsql('timestamp',$REFHASH5);
@TEMP2 = split(/ /,$date2);
$dates2 = sprintf("%04d%02d%02d%02d%02d%02d",split(/-/,$TEMP2[0]),split(/:/,$TEMP2[1]));
$dates22 = Date::Simple->new($TEMP2[0]);
}	#if

if($posi1 == 0){($result10,$result11)=($result11,$result10);}
if($posi2 == 0){($result20,$result21)=($result21,$result20);}


if($count4 == 1 && $count5 == 1){

if($syouhai1 == 1 && $syouhai2 != 2){next;}	#if
if($syouhai1 == 2 && $syouhai2 != 1){next;}	#if
if($syouhai1 == 3 && $syouhai2 != 3){next;}	#if
if($syouhai1 == 4 && $syouhai2 != 5){next;}	#if
if($syouhai1 == 5 && $syouhai2 != 4){next;}	#if

#相違がある場合
#print "\n$result10 != $result21 || $result11 != $result20<br>\n";
if( ($result10 != $result21 || $result11 != $result20 ) && ($syouhai1 == 1 || $syouhai1 == 2 || $syouhai1 == 3) ){
#print "$sql_str4<br>\n";
#print "$sql_str5<br>\n";

next;}

if($posi1 == 0){($result10,$result11)=($result11,$result10);}
if($posi2 == 0){($result20,$result21)=($result21,$result20);}
#

#報告オッケー！
$teamnum1name = &taikaiteamname_get($tss1);
$teamnum2name = &taikaiteamname_get($tss2);
$score = $result10." - ".$result11;
if($dates11 > $dates22){	#新しい方の報告日
$date0 = $dates1;
}else{
$date0 = $dates2;
}	#if
#不戦勝
if($syouhai1 == 4){$winlose = "○";$score = "不戦勝 - 不戦敗";}	#if
#不戦敗
if($syouhai1 == 5){$winlose = "×";$score = "不戦敗 - 不戦勝";}	#if

#
$list =<<"END_HTML";
<div class=ball2>$taikainame</div><div class=game> $teamnum1name vs $teamnum2name <span><br>$score</span> </div>
END_HTML
#DBに入れる
$sql_str9 = qq{INSERT INTO sokuhosort(ses,date,list) VALUES (?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$session,
$date0,
$list,
);
}	#報告がそろったものだけ
}	#foreach vsdata
}	#for k
}	#if cate

##########################################################
# トーナメント
##########################################################
if($cate == 2){

@CNT = (0,1,2,4,8,16,32,64,128);
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = $taikaicode and category = 2 ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1." $sql_str1<br>\n";
for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
$kumi2 = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi2);
@NICHIJITEMP = split(/<>/,&paramsetsql('nichiji1',$REFHASH1));
unshift(@NICHIJITEMP,"");
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REFHASH1));
$yusyo = shift(@TEAMLISTTEMP);
#チーム分け
$k=0;
%TEAMLIST = ();
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$TEAMLIST{$y}{$x}{1} = $TEAMLISTTEMP[$k+0];	#左のチームnum
$TEAMLIST{$y}{$x}{2} = $TEAMLISTTEMP[$k+1];	#右のチームnum
#print "$TEAMLIST{$y}{$x}{1} vs $TEAMLIST{$y}{$x}{2}<br>\n";
$k+=2;
}	#foreach x
}	#foreach y

#最下段を求める
foreach(1..7){
if($NICHIJITEMP[$_] !~ /0000/){$gedan = $_ -1;}
}	#foreach
#print "gedan=$gedan";

#トーナメント○回戦
foreach $y(1..7){
$n = $NICHIJITEMP[$y];
($n1,$n2) = split(/:/,$n);
if($n1 ne "0000-00-00" && $n2 ne "0000-00-00"){
#日付が有効
$d = Date::Simple->new();
$d1 = Date::Simple->new($n1);
$d2 = Date::Simple->new($n2);
#報告範囲内
#if( $d1 <= $d && $d <= $d2){

@TEMP = split(/:/,$NICHIJITEMP[$num]);
$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));
$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($gedan - $num+2)."回戦";
}	#num

$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){

$editflag = "";
$reportflag = "<span style='color:red;font-weight:bold;'>未報告</span>";
$tsstemp = "";
$resultstr1 = "";
$resultstr2 = "";
$result10 = "";
$result11 = "";
$result20 = "";
$result21 = "";
$score = "";
$winlose = "";
$attention = "";

$tss1 = $TEAMLIST{$y}{$x}{1};
$tss2 = $TEAMLIST{$y}{$x}{2};
if($tss1 eq "" || $tss2 eq ""){next;}

$teamnum1name = &taikaiteamname_get($tss1);
$teamnum2name = &taikaiteamname_get($tss2);
$date0 = "";
#自分の試合結果報告をGET
$sql_str5 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = '$tss2' ";
$rs5 = $dbh->prepare($sql_str5);
$rs5->execute();
$count5 = $rs5->rows;	# Hit件数を確保
if($count5 == 1){
$REFHASH5 = $rs5->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH5);
$resultstr1 = &paramsetsql('resultstr',$REFHASH5);
$result10 = &paramsetsql('result0',$REFHASH5);
$result11 = &paramsetsql('result1',$REFHASH5);
$date1 = &paramsetsql('timestamp',$REFHASH5);
@TEMP1 = split(/ /,$date1);
$date0 = sprintf("%04d%02d%02d%02d%02d%02d",split(/-/,$TEMP1[0]),split(/:/,$TEMP1[1]));
}	#if count5 == 1
#自分の報告書は上にあるので、相手チームの報告をGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = '$tss1' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$resultstr2 = &paramsetsql('resultstr',$REFHASH2);
$result20 = &paramsetsql('result0',$REFHASH2);
$result21 = &paramsetsql('result1',$REFHASH2);
}	#if count2 == 1

#print "$resultstr1 || $resultstr2<br>";
###
if($resultstr1 eq "" || $resultstr2 eq "" ){next;}

#相違がある場合
#print "$result10 != $result21 || $result11 != $result20<br>";
if($result10 != $result21 || $result11 != $result20 ){next;}


$winlose = "△";
$score = $result10." - ".$result11;
if($resultstr1 == 1){$winlose = "○";}	#if win
if($resultstr1 == 2){$winlose = "×";}	#if win

#不戦勝
if($resultstr1 == 4){$winlose = "○";$score = "不戦勝 - 不戦敗";}	#if
#不戦敗
if($resultstr1 == 5){$winlose = "×";$score = "不戦敗 - 不戦勝";}	#if

#####
$list =<<"END_HTML";
<div class=ball2>$taikainame</div><div class=game> $teamnum1name vs $teamnum2name <span><br>$score</span> </div>
END_HTML
#DBに入れる
$sql_str9 = qq{INSERT INTO sokuhosort(ses,date,list) VALUES (?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$session,
$date0,
$list,
);
}	#foreach x
}	#if nichiji
}	#foreach y
}	#for count
}	#if cate
##########################################################
}	#foreach cate
}	#for i
##########################################################

###
$mes = "";
$sql_str = "SELECT * FROM sokuhosort WHERE ses = '$session' ORDER BY date DESC LIMIT 5";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck;	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i=0;$i<$count;$i++){
$REFHASH = $rs->fetchrow_hashref;
$mes .= &paramsetsql('list');
}	#for

#
$sql_str1 = "DELETE FROM sokuhosort WHERE ses = '$session' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);


###
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub






# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub membercontact_form {
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
print <<"END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<p align=center>
ログインしてからご利用下さい。
</p>
</body>
</html>
END_HTML
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$mailaddress1 = &paramsetsql('mailaddress1',$REFHASH);
###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
<script>
function kakunin(){

if (document.getElementById('namae').value == "") {
alert('「氏名」が入力されていません。');
return(false);
}

if (document.getElementById('yomi').value == "") {
alert('「フリガナ」が入力されていません。');
return(false);
}

return true;
}	//func
</script>
</head>

<body>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="membercontact_check" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
<input type="text" name="_氏名" id="namae" size="50" tabindex="7" value="$paramhash_dec{'_氏名'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_フリガナ" id="yomi" size="50" tabindex="7" value="$paramhash_dec{'_フリガナ'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$teamname
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$team_kana
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$mailaddress1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
<textarea rows="20" cols="60" name="お問い合わせ" tabindex="29">
$paramhash_dec{'お問い合わせ'}</textarea>
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信確認画面へ　　" />
</div>
</form>
</body>
</html>
END_HTML
###
print $mes;
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub membercontact_check {
my $errormes = "";
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
print <<"END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<p align=center>
ログインしてからご利用下さい。
</p>
</body>
</html>
END_HTML
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$mailaddress1 = &paramsetsql('mailaddress1',$REFHASH);
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#エラーチェック
if($errormes ne ""){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="membercontact_form" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</body>
</html>
END_HTML
exit;
}	#if

###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>

<body>
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
$paramhash_dec{'_氏名'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_フリガナ'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$teamname
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$team_kana
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$mailaddress1
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'お問い合わせ'}
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="membercontact_form" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="membercontact_ok" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>

</body>
</html>
END_HTML
###
print $mes;
exit;
}	#sub


# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub membercontact_ok {
my $errormes = "";
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
print <<"END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<p align=center>
ログインしてからご利用下さい。
</p>
</body>
</html>
END_HTML
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$email = &paramsetsql('mailaddress1',$REFHASH);
#$email = $paramhash_dec{'_メールアドレス'};

#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	$p =~ s/\_//;
#文字のURLデコード
	utf8::encode($v);
	$v =~ tr/+/ /;
	$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	utf8::decode($v);
if($p =~ /\*/){next;}
##
$list .= "$p：$v\n";
}	#for



#控えメール
$subject = "お問い合わせ【控え】｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $email
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
お問い合せ頂きありがとうございます。
以下の内容は控えとなります。

$list

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

#クライアントへメール
$subject = "問い合わせフォームより｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: $email
To: info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
以下のチームより問い合わせが来ております。

チーム名：$teamname（$team_kana）
$list

--------------------------------------
From
全国草野球大会サイト PRIDE JAPAN
マイページ内「問い合わせフォーム」
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

# 新規登録
$sql_str = qq{INSERT INTO othercontents_toiawase(namae,yomi,teamname,teamyomi,email,body) VALUES (?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$paramhash_dec{'_氏名'},
$paramhash_dec{'_フリガナ'},
$paramhash_dec{'_チーム正式名称'},
$paramhash_dec{'_チーム正式名称（フリガナ）'},
$paramhash_dec{'_メールアドレス'},
$paramhash_dec{'お問い合わせ'},
);
###
print <<"END_HTML";
<!DOCTYPE>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title></title>
</head>
<body>
<div id="iframe">
お問い合せありがとうございます。<br>
折り返し弊社より連絡をさせて頂きます。<br>
<br>
また控えのメールを送らせて頂きましたのでご確認下さい。<br>
</div>

</body>
</html>
END_HTML
}	#sub


sub membercontact_form_noframe {
$loginuser = $paramhash{'ses'};
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p align=center>
ログインしてからご利用下さい。
</p>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$mailaddress1 = &paramsetsql('mailaddress1',$REFHASH);
###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">
<span style="color: #F00">*は必須項目です。 </span>

<script>
function kakunin(){

if (document.getElementById('namae').value == "") {
alert('「氏名」が入力されていません。');
return(false);
}

if (document.getElementById('yomi').value == "") {
alert('「フリガナ」が入力されていません。');
return(false);
}

return true;
}	//func
</script>

<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="membercontact_check_noframe" />
<input type="hidden" name="ses" value="$loginuser" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
<input type="text" name="_氏名" id="namae" size="50" tabindex="7" value="$paramhash_dec{'_氏名'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_フリガナ" id="yomi" size="50" tabindex="7" value="$paramhash_dec{'_フリガナ'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$teamname
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$team_kana
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$mailaddress1</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
<textarea rows="20" cols="60" name="お問い合わせ" tabindex="29">
$paramhash_dec{'お問い合わせ'}</textarea>
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信確認画面へ　　" />
</div>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub membercontact_check_noframe {
$loginuser = $paramhash{'ses'};
my $errormes = "";
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p align=center>
ログインしてからご利用下さい。
</p>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$mailaddress1 = &paramsetsql('mailaddress1',$REFHASH);
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	if($p eq "ses"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="membercontact_form_noframe" />
<input type="hidden" name="ses" value="$loginuser" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#if

###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
$paramhash_dec{'_氏名'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_フリガナ'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$teamname
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$team_kana
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$mailaddress1
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'お問い合わせ'}
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="membercontact_form_noframe" />
<input type="hidden" name="ses" value="$loginuser" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="membercontact_ok_noframe" />
<input type="hidden" name="ses" value="$loginuser" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>

</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub membercontact_ok_noframe {
$loginuser = $paramhash{'ses'};
my $errormes = "";
#チーム情報
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$loginuser' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 1){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p align=center>
ログインしてからご利用下さい。
</p>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH);
$teamname = &paramsetsql('teamname',$REFHASH);
$team_kana = &paramsetsql('team_kana',$REFHASH);
$email = &paramsetsql('mailaddress1',$REFHASH);
#$email = $paramhash_dec{'_メールアドレス'};

#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	if($p eq "ses"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	$p =~ s/\_//;
#文字のURLデコード
	utf8::encode($v);
	$v =~ tr/+/ /;
	$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	utf8::decode($v);
if($p =~ /\*/){next;}
##
$list .= "$p：$v\n";
}	#for



#控えメール
$subject = "お問い合わせ【控え】｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $email
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
お問い合せ頂きありがとうございます。
以下の内容は控えとなります。

$list

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

#クライアントへメール
$subject = "問い合わせフォームより｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: $email
To: info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
以下のチームより問い合わせが来ております。

チーム名：$teamname（$team_kana）
$list

--------------------------------------
From
全国草野球大会サイト PRIDE JAPAN
マイページ内「問い合わせフォーム」
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

# 新規登録
$sql_str = qq{INSERT INTO othercontents_toiawase(namae,yomi,teamname,teamyomi,email,body) VALUES (?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$paramhash_dec{'_氏名'},
$paramhash_dec{'_フリガナ'},
$paramhash_dec{'_チーム正式名称'},
$paramhash_dec{'_チーム正式名称（フリガナ）'},
$paramhash_dec{'_メールアドレス'},
$paramhash_dec{'お問い合わせ'},
);
###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">

お問い合せありがとうございます。<br>
折り返し弊社より連絡をさせて頂きます。<br>
<br>
また控えのメールを送らせて頂きましたのでご確認下さい。<br>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub






# -----------------------------------------------------------------
# whatnew
# -----------------------------------------------------------------
sub whatnew {
$sql_str = "SELECT * FROM othercontents WHERE contents = 100 and koukaiflag = 0 and ( ( TO_DAYS(nichiji_from) <= TO_DAYS(NOW()) and TO_DAYS(NOW()) <= TO_DAYS(nichiji_to) ) or (TO_DAYS(nichiji_from) = TO_DAYS(nichiji_to) ) )ORDER BY sortnum DESC,nichiji DESC";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck;	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i=0;$i<$count;$i++){
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql2('title');
$body = &paramsetsql('body');
if($body ne ""){
$title = "<a href='$body'>$title</a>";
}	#if
$nichiji = &paramsetsql('nichiji');
$nichiji =~ s/-/\//g;
$createdate = &paramsetsql('createdate');
if($createdate ne ""){
$n1 = Date::Simple->new();
@TEMP = split(/ /,$createdate);
$n2 = Date::Simple->new($TEMP[0]);
if( ($n1 - $n2) < 7){$title .= " <img src='img/new.gif' ALT='' />";}
}	#if
##
$whatnew .=<<"END_HTML";
<dt>$nichiji</dt>
<dd>$title</dd>
END_HTML
}	#for
if($whatnew eq ""){
$whatnew .=<<"END_HTML";
お知らせはありません。
END_HTML
}	#if
$mes =<<"END_HTML";
<dl>
$whatnew
</dl>
END_HTML
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub


# -----------------------------------------------------------------
# Link
# -----------------------------------------------------------------
sub link {
my @LINKLIST = ();
#ジャンル順にリンクリストを作成
$sql_str = "SELECT * FROM othercontents WHERE contents = 101 and koukaiflag = 0 ORDER BY sortnum DESC";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck;	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
$temp =<<"END_HTML";
END_HTML
for($i=0;$i<$count;$i++){
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql2('title');
$body = &paramsetsql('body');
$genre = &paramsetsql('genre');
$body = "<a href='$body' target=_blank>$body</a>";
$LINKLIST[$genre] .=<<"END_HTML";
<tr>
<th width="32%" align="left" scope="row">$title</th>
<td width="68%">$body</td>
</tr>
END_HTML
}	#for
###
$mes =<<"END_HTML";
<h2 class="subti" id="1">$LINKGENRENAME[1]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[1]
</table>
</div>
<h2 class="subti" id="2">$LINKGENRENAME[2]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[2]
</table>
</div>
<h2 class="subti" id="3">$LINKGENRENAME[3]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[3]
</table>
</div>
<h2 class="subti" id="4">$LINKGENRENAME[4]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[4]
</table>
</div>
<h2 class="subti" id="5">$LINKGENRENAME[5]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[5]
</table>
</div>
<h2 class="subti" id="9">$LINKGENRENAME[9]</h2>
<div class="box">
<table width="100%" cellspacing="0" class="stan">
$LINKLIST[9]
</table>
</div>
END_HTML
#差し込み表示
$mes =~ s/\"//g;	#"削除
$mes = &crlfreset0($mes);
print "document.write(\"$mes\");\n";
exit;
}	#sub



# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_form {

print <<"END_HTML";
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
<script>
function kakunin(){

if (document.getElementById('namae').value == "") {
alert('「氏名」が入力されていません。');
return(false);
}

if (document.getElementById('yomi').value == "") {
alert('「フリガナ」が入力されていません。');
return(false);
}

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('teamyomi').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('teamemail').value == "") {
alert('「メールアドレス」が入力されていません。');
return(false);
}
var str = document.getElementById("teamemail").value;
if( !str.match(/[@]/) ){
alert("「メールアドレス」が不正です。");
return false;
}	//if
var str = document.getElementById("teamemail").value;
if( str.match(/[@]{2,}/) ){
alert("「メールアドレス」が不正です2。");
return false;
}	//if
var str = document.getElementById("teamemail").value;
if( str.match(/[ ]/) ){
alert("「メールアドレス」が不正です3。");
return false;
}	//if

if (document.getElementById('teamemail2').value == "") {
alert('「メールアドレス（確認用）」が入力されていません。');
return(false);
}

if (document.getElementById('teamemail').value != document.getElementById('teamemail2').value) {
alert('「メールアドレス」が一致しません。');
return(false);
}

return true;
}	//func
</script>
</head>

<body>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="contact_check" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
<input type="text" name="_氏名" id="namae" size="50" value="$paramhash_dec{'_氏名'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_フリガナ" id="yomi" size="50" value="$paramhash_dec{'_フリガナ'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_チーム正式名称" id="teamname" size="50" value="$paramhash_dec{'_チーム正式名称'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_チーム正式名称（フリガナ）" id="teamyomi" size="50" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_メールアドレス" id="teamemail" size="50" value="$paramhash_dec{'_メールアドレス'}" style="ime-mode: disabled;" />
<br />
※PC、携帯どちらのアドレスでも構いません。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス確認</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_*メールアドレス" id="teamemail2" size="50" value="$paramhash_dec{'_*メールアドレス'}" style="ime-mode: disabled;" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
<textarea rows="20" cols="60" name="お問い合わせ">
$paramhash_dec{'お問い合わせ'}</textarea>
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信確認画面へ　　" />
</div>
</form>
</body>
</html>
END_HTML
###
print $mes;
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_check {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#エラーチェック
if($errormes ne ""){
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="contact_form" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</body>
</html>
END_HTML
exit;
}	#if

###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>

<body>
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
$paramhash_dec{'_氏名'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_フリガナ'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_チーム正式名称'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_チーム正式名称（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_メールアドレス'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'お問い合わせ'}
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="contact_form" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="contact_ok" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>

</body>
</html>
END_HTML
###
print $mes;
exit;
}	#sub


# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_ok {
$email = $paramhash_dec{'_メールアドレス'};
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	$p =~ s/\_//;
#文字のURLデコード
	utf8::encode($v);
	$v =~ tr/+/ /;
	$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	utf8::decode($v);
if($p =~ /\*/){next;}
##
$list .= "$p：$v\n";
}	#for



#控えメール
$subject = "お問い合わせ【控え】｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $email
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
お問い合せ頂きありがとうございます。
以下の内容は控えとなります。

$list

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

#クライアントへメール
$subject = "問い合わせフォームより｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: $email
To: info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
以下の問い合わせが来ております。

$list

--------------------------------------
From:
全国草野球大会サイト PRIDE JAPAN
問い合わせフォーム
https://pridejapan-net.ssl-xserver.jp/system.cgi?code=contact_form_noframe
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

# 新規登録
$sql_str = qq{INSERT INTO othercontents_toiawase(namae,yomi,teamname,teamyomi,email,body) VALUES (?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$paramhash_dec{'_氏名'},
$paramhash_dec{'_フリガナ'},
$paramhash_dec{'_チーム正式名称'},
$paramhash_dec{'_チーム正式名称（フリガナ）'},
$paramhash_dec{'_メールアドレス'},
$paramhash_dec{'お問い合わせ'},
);
###
print <<"END_HTML";
<!DOCTYPE>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title></title>
</head>
<body>
<div id="iframe">
お問い合せありがとうございます。<br>
折り返し弊社より連絡をさせて頂きます。<br>
<br>
また控えのメールを送らせて頂きましたのでご確認下さい。<br>
</div>

</body>
</html>
END_HTML
}	#sub





# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_form_noframe {

$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">
<p>チーム登録をしているチームは必ず「マイページ」からお問合わせください。<br />
<span style="color: #F00">*は必須項目です。 </span></p>
<script>
function kakunin(){

if (document.getElementById('namae').value == "") {
alert('「氏名」が入力されていません。');
return(false);
}

if (document.getElementById('yomi').value == "") {
alert('「フリガナ」が入力されていません。');
return(false);
}

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('teamyomi').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}


var str = document.getElementById("teamemail").value;
if (str == "") {
alert('「メールアドレス」が入力されていません。');
return(false);
}
if( str.match(/[^0-9a-zA-Z_\\-\\.@]/) ){
alert("「メールアドレス」に使用できない文字があります。");
return false;
}	//if
if( !str.match(/[0-9a-zA-Z_-]{1,}@[0-9a-zA-Z_-]{1,}\\.[0-9a-zA-Z_-]{1,}/) ){
alert("「メールアドレス」が不正です6。");
return false;
}	//if
if( !str.match(/[@]/) ){
alert("「メールアドレス」が不正です1。");
return false;
}	//if
if( str.match(/[@]{2,}/) ){
alert("「メールアドレス」が不正です2。");
return false;
}	//if
if( str.match(/[ 　]/) ){
alert("「メールアドレス」が不正です3。");
return false;
}	//if
if( !str.match(/[\\.]/) ){
alert("「メールアドレス」が不正です4。");
return false;
}	//if
if( str.match(/\\.@/) ){
alert("「メールアドレス」が不正です5。");
return false;
}	//if
if( str.match(/\\.\$/) ){
alert("「メールアドレス」が不正です7。");
return false;
}	//if
if( str.match(/\\.\\./) ){
alert("「メールアドレス」が不正です8。");
return false;
}	//if
if( str.match(/^\\./) ){
alert("「メールアドレス」が不正です9。");
return false;
}	//if



if (document.getElementById('teamemail2').value == "") {
alert('「メールアドレス（確認用）」が入力されていません。');
return(false);
}

if (document.getElementById('teamemail').value != document.getElementById('teamemail2').value) {
alert('「メールアドレス」が一致しません。');
return(false);
}

return true;
}	//func
</script>

<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="contact_check_noframe" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
<input type="text" name="_氏名" id="namae" size="50" value="$paramhash_dec{'_氏名'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_フリガナ" id="yomi" size="50" value="$paramhash_dec{'_フリガナ'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_チーム正式名称" id="teamname" size="50" value="$paramhash_dec{'_チーム正式名称'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_チーム正式名称（フリガナ）" id="teamyomi" size="50" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_メールアドレス" id="teamemail" size="50" value="$paramhash_dec{'_メールアドレス'}" style="ime-mode: disabled;" />
<br />
※PC、携帯どちらのアドレスでも構いません。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス確認</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_*メールアドレス" id="teamemail2" size="50" value="$paramhash_dec{'_*メールアドレス'}" style="ime-mode: disabled;" />
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
<textarea rows="20" cols="60" name="お問い合わせ">
$paramhash_dec{'お問い合わせ'}</textarea>
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信確認画面へ　　" />
</div>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_check_noframe {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">
<p>チーム登録をしているチームは必ず「マイページ」からお問合わせください。<br />

以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="contact_form_noframe_noframe" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#if

###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">
<p>チーム登録をしているチームは必ず「マイページ」からお問合わせください。<br />

<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
$paramhash_dec{'_氏名'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_フリガナ'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_チーム正式名称'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_チーム正式名称（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_メールアドレス'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">お問い合わせ</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'お問い合わせ'}
</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="contact_form_noframe" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="contact_ok_noframe" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub contact_ok_noframe {
$email = $paramhash_dec{'_メールアドレス'};
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	$p =~ s/\_//;
#文字のURLデコード
	utf8::encode($v);
	$v =~ tr/+/ /;
	$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	utf8::decode($v);
if($p =~ /\*/){next;}
##
$list .= "$p：$v\n";
}	#for



#控えメール
$subject = "お問い合わせ【控え】｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $email
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
お問い合せ頂きありがとうございます。
以下の内容は控えとなります。

$list

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

#クライアントへメール
$subject = "問い合わせフォームより｜全国草野球大会サイト PRIDE JAPAN";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: $email
To: info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
以下の問い合わせが来ております。

$list

--------------------------------------
From:
全国草野球大会サイト PRIDE JAPAN
問い合わせフォーム
https://pridejapan-net.ssl-xserver.jp/system.cgi?code=contact_form_noframe
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

# 新規登録
$sql_str = qq{INSERT INTO othercontents_toiawase(namae,yomi,teamname,teamyomi,email,body) VALUES (?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$paramhash_dec{'_氏名'},
$paramhash_dec{'_フリガナ'},
$paramhash_dec{'_チーム正式名称'},
$paramhash_dec{'_チーム正式名称（フリガナ）'},
$paramhash_dec{'_メールアドレス'},
$paramhash_dec{'お問い合わせ'},
);
###
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">お問い合わせフォーム</h2>
<div class="box" id="contact_top">
<p align=center>
お問い合せありがとうございます。<br>
折り返し弊社より連絡をさせて頂きます。<br>
<br>
また控えのメールを送らせて頂きましたのでご確認下さい。<br>
</p>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
}	#sub





# -----------------------------------------------------------------
# 問い合わせ：パスワード
# -----------------------------------------------------------------
sub forgetpassword_form {

print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
<script>
function kakunin(){

var str = document.getElementById("email").value;
if (str == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}
if( str.match(/[ 　]/) ){
alert("「チームメールアドレス」が不正です1。");
return false;
}	//if
if( str.match(/[^0-9a-zA-Z_\\-\\.@]/) ){
alert("「チームメールアドレス」に使用できない文字があります。");
return false;
}	//if
if( !str.match(/[\\.]/) ){
alert("「チームメールアドレス」が不正です2。");
return false;
}	//if
if( !str.match(/[\@]/) ){
alert("「チームメールアドレス」が不正です3。");
return false;
}	//if
if( !str.match(/[0-9a-zA-Z_\\-]@[0-9a-zA-Z_\\-\\.]\\.[0-9a-zA-Z_\\-]\$/) ){
alert("「チームメールアドレス」が不正です4。");
return false;
}	//if

return true;
}	//func

</script>
</head>

<body>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="forgetpassword_check" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_メールアドレス" id="email" size="50" tabindex="7" value="$paramhash_dec{'_メールアドレス'}" />
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　確認画面へ　　" />
</div>
</form>
</body>
</html>
END_HTML
###
print $mes;
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub forgetpassword_check {
my $errormes = "";

#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#
($mailadr1,$mailadr2) = split(/\@/,$paramhash{'_メールアドレス'});
$tel = $paramhash{'_電話番号'};
$team_year = $paramhash{'_チーム設立年'};

#エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
<p style="color:red;">以下の必須項目が入力されておりません。</p>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="forgetpassword_form" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
END_HTML
}else{
#整合性チェック
$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailadr1 = '$mailadr1' and mailadr2 = '$mailadr2' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
#一致
$REFHASH = $rs->fetchrow_hashref;
$pwd = &paramsetsql('pwd');
$mes =<<"END_HTML";
<p style="color:red;">登録の確認が出来ました。</p>
<p>ご指定のメールアドレス宛にパスワードを送付しましたのでご確認下さい。</p>
END_HTML
#メール送信
$subject = "パスワード問い合わせフォームより｜$sitetitle";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $mailadr1\@$mailadr2
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
このメールはパスワード問い合わせフォームを利用して送信されています。
利用の覚えがない場合は事務局までお問い合わせ下さい。

パスワード：$pwd

ログインは以下よりお願いします。
$sitefulladr

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;





}else{
#不一致
$mes =<<"END_HTML";
<p style="color:red;">登録された情報から確認出来ません。</p>
<p>お手数ですがもう一度お問い合わせ下さい。</p>
<p>※どうしても確認されない場合は、お手数ですが<a target=_top href="https://pridejapan-net.ssl-xserver.jp/system.cgi?code=contact_form_noframe">こちらから</a>事務局までお問い合わせ下さい。</p>
END_HTML
}	#if 整合性
}	#if エラーチェック

###
print <<"END_HTML";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
	margin:0px;
	padding:0px;
	text-align:center;
	font-size: 82%;
	line-height: 200%;
}
table {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: solid;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	font-size: 12px;
	line-height: 150%;
	margin-bottom: 30px;
}
td {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding: 8px;
}
th {
	border-top-width: 1px;
	border-right-width: 1px;
	border-bottom-width: 1px;
	border-left-width: 1px;
	border-top-style: none;
	border-right-style: solid;
	border-bottom-style: solid;
	border-left-style: none;
	border-top-color: #999;
	border-right-color: #999;
	border-bottom-color: #999;
	border-left-color: #999;
	padding-right: 8px;
	padding-left: 8px;
	padding-top: 8px;
	padding-bottom: 8px;
}
.stan {
	border-right-style: none;
	border-bottom-style: solid;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	border-top-style: none;
	border-left-style: none;
}
.stan td {
	border-top-style: solid;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
}
.stan th {
	border-top-style: solid;
	border-right-style: dotted;
	border-bottom-style: none;
	border-left-style: none;
	border-top-color: #000;
	border-right-color: #000;
	border-bottom-color: #000;
	border-left-color: #000;
	font-weight: normal;
}
.center {
	text-align: center;
}
</style>
</head>

<body>
<hr>
$mes
</body>
</html>
END_HTML
###
exit;
}	#sub



# -----------------------------------------------------------------
# 問い合わせ：パスワード
# -----------------------------------------------------------------
sub forgetpassword_form_noframe {
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">パスワード問い合わせフォーム</h2>
<div class="box" id="contact_top">
<p>下記入力欄に、登録時のメールアドレスを記入し、送信してください。<br />
こちらからメールを送信致します。<br>
</p>
<script>
function kakunin(){

var str = document.getElementById("email").value;
if (str == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}
if( str.match(/[ 　]/) ){
alert("「チームメールアドレス」が不正です1。");
return false;
}	//if
if( str.match(/[^0-9a-zA-Z_\\-\\.@]/) ){
alert("「チームメールアドレス」に使用できない文字があります。");
return false;
}	//if
if( !str.match(/[\\.]/) ){
alert("「チームメールアドレス」が不正です2。");
return false;
}	//if
if( !str.match(/[\@]/) ){
alert("「チームメールアドレス」が不正です3。");
return false;
}	//if
if( !str.match(/[0-9a-zA-Z_-]{1,}@[0-9a-zA-Z_-]{1,}\\.[0-9a-zA-Z_-]{1,}/) ){
alert("「チームメールアドレス」が不正です4。");
return false;
}	//if

return true;
}	//func

</script>

<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="forgetpassword_check_noframe" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールアドレス</font> <font class="type1" color="#ff0000">*必須</font></td>
<td align="left" bgcolor="#ffffff">
<input type="text" name="_メールアドレス" id="email" size="50" tabindex="7" value="$paramhash_dec{'_メールアドレス'}" />
</td>
</tr>
</tbody>
</table>
<div class="center">内容をご確認の上、よろしければ下記ボタンをクリックして下さい。<br />
<input type="submit" value="　　送信　　" />
</div>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}	#sub




# -----------------------------------------------------------------
# 問い合わせ
# -----------------------------------------------------------------
sub forgetpassword_check_noframe {
my $errormes = "";

#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#
($mailadr1,$mailadr2) = split(/\@/,$paramhash{'_メールアドレス'});
$tel = $paramhash{'_電話番号'};
$team_year = $paramhash{'_チーム設立年'};

#エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">パスワード問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p style="color:red;">以下の必須項目が入力されておりません。</p>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="forgetpassword_form_noframe" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
</div>
</div>
END_HTML
###
&taikaihtmldisp($mes);
exit;
}else{
#整合性チェック
$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailadr1 = '$mailadr1' and mailadr2 = '$mailadr2' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
#一致
$REFHASH = $rs->fetchrow_hashref;
$pwd = &paramsetsql('pwd');
#メール送信
$subject = "パスワード問い合わせフォームより｜$sitetitle";
$subject = Unicode::Japanese->new($subject,'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@pridejapan.net
To: $mailadr1\@$mailadr2
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
このメールはパスワード問い合わせフォームを利用して送信されています。
利用の覚えがない場合は事務局までお問い合わせ下さい。

パスワード：$pwd

ログインは以下よりお願いします。
$sitefulladr

--------------------------------------
PRIDE JAPAN運営事務局
END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">パスワード問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p style="color:red;">登録の確認が出来ました。</p>
<p>ご指定のメールアドレス宛にパスワードを送付しましたのでご確認下さい。</p>
</div>
</div>
END_HTML

}else{
#不一致
$mes =<<"END_HTML";
<div id="mtop"> <img src="img/conti.jpg" alt="お問い合わせ" width="980" height="48" /> </div>
<div id="mainbox">
<h2 class="subti" id="1">パスワード問い合わせフォーム</h2>
<div class="box" id="contact_top">

<p style="color:red;">登録された情報から確認出来ません。</p>
<p>お手数ですがもう一度お問い合わせ下さい。</p>
<p>※どうしても確認されない場合は、お手数ですが<a target=_top href="https://pridejapan-net.ssl-xserver.jp/system.cgi?code=contact_form_noframe">こちらから</a>事務局までお問い合わせ下さい。</p>
</div>
</div>
END_HTML
}	#if 整合性
}	#if エラーチェック

###
&taikaihtmldisp($mes);
exit;

}	#sub






# -----------------------------------------------------------------
# バナーカテゴリ
# -----------------------------------------------------------------
sub bannercategory {
$bannercategory = $paramhash{'bannercategory'};
# バナーカテゴリ
$sql_str = "SELECT * FROM $dbname WHERE serial = '$bannercategory' and koukaiflag = 0  ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql('title');
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 and bannercategory = '$bannercategory' ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLエラーチェック
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$taikaicode = $REFHASH->{'serial'};
$taikainame = &paramsetsql('title');
#画像
$imgsrc = "";
@IMGTEMPS = split(/:/,&paramsetsql('upfilename'));
($sfn,$fn,$mime) = split(/<>/,$IMGTEMPS[1]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$mes .= "<div class='taikai'><a href='system.cgi?code=convention&taikaicode=$taikaicode'><img src='system/file/$TEMP[0].jpg' ALT='$taikainame' width='440' height='114' /></a></div>";}
}	#if 存在
}	#for
# width='265' height='69' 　小さい方
# width='440' height='114'　大きい方
$mes =<<"END_HTML";
<div id="mainbox">
<h2 class="subti" style="margin-bottom:14px;">$title</h2>
<div id="taikai">
$mes
<div class="clear"></div>
</div>
</div>

END_HTML

&taikaihtmldisp($mes);
exit;
}	#sub






# -----------------------------------------------------------------
# チーム：新規登録
# -----------------------------------------------------------------
sub member_new_noframe {
#セッション作成
$session = sprintf("%02d%02d%02d",$sec,$min,$hour);
for (1..15) { $session .= ((0..9,a..z,A..Z)[int rand 62])};
$session .= sprintf("%02d%02d%02d",$mday,$month,$year-2000);

#
if($paramhash_dec{'_都道府県名'} ne ""){$PFLAG{$paramhash_dec{'_都道府県名'}} = "selected";}
if($paramhash_dec{'_代表者都道府県名'} ne ""){$PFLAG2{$paramhash_dec{'_代表者都道府県名'}} = "selected";}
if($paramhash_dec{'_メールマガジン配信の選択'} ne ""){
$MAILMAGAZINEFLAG{$paramhash_dec{'_メールマガジン配信の選択'}}="checked=checked";
}else{
$MAILMAGAZINEFLAG{1}="checked=checked";
}	#if
###
$mes =<< "END_HTML";
<script>
function kakunin(){

if (document.getElementById('teamname').value == "") {
alert('「チーム正式名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_kana').value == "") {
alert('「チーム正式名称（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('team_abbr').value == "") {
alert('「チーム省略名称」が入力されていません。');
return(false);
}

if (document.getElementById('team_year').value == "") {
alert('「チーム結成年」が入力されていません。');
return(false);
}
var str = document.getElementById("team_year").value;
if( str.match(/[^0-9]/) ){
alert("「チーム結成年」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('team_year').value < 1800) {
alert('「チーム結成年」にエラーがあります。');
return(false);
}


if (document.getElementById('katsudou_week').value == "") {
alert('「主な活動曜日」が入力されていません。');
return(false);
}

if (document.getElementById('average_age').value == "") {
alert('「平均年齢」が入力されていません。');
return(false);
}
var str = document.getElementById("average_age").value;
if( str.match(/[^0-9]/) ){
alert("「平均年齢」に半角数字以外が入力されております。");
return false;
}	//if
if (document.getElementById('average_age').value < 5) {
alert('「平均年齢」にエラーがあります。');
return(false);
}


if (document.getElementById('pref').selectedIndex == 0) {
alert('「主な活動場所（都道府県）」が選択されていません。');
return(false);
}

if (document.getElementById('team_cities').value == "") {
alert('「主な活動場所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei1').value == "") {
alert('「代表者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana1').value == "") {
alert('「代表者氏名（フリガナ）」が入力されていません。');
return(false);
}

var str = document.getElementById("mailadr1").value;
if (str == "") {
alert('「代表者メールアドレス」が入力されていません。');
return(false);
}
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス」が不正です。");
return false;
}	//if
if( str.match(/[^0-9a-zA-Z_\\.\\-]/) ){
alert("「代表者メールアドレス」に使用できない文字があります。");
return false;
}	//if
if( str.match(/\\.\$/) ){
alert("「代表者メールアドレス」が不正です3。");
return false;
}	//if
if( str.match(/\\.\\./) ){
alert("「代表者メールアドレス」が不正です4。");
return false;
}	//if
if( str.match(/^\\./) ){
alert("「代表者メールアドレス」が不正です5。");
return false;
}	//if


var str = document.getElementById("mailadr2").value;
if (str == "") {
alert('「代表者メールアドレス（ドメイン）」が入力されていません。');
return(false);
}
if( str.match(/[^0-9a-zA-Z_\\-\\.]/) ){
alert("「代表者メールアドレス（ドメイン）」に使用できない文字があります。");
return false;
}	//if
if( str.match(/[ @　]/) ){
alert("「代表者メールアドレス（ドメイン）」が不正です1。");
return false;
}	//if
if( !str.match(/[\\.]/) ){
alert("「代表者メールアドレス（ドメイン）」が不正です2。");
return false;
}	//if
if( str.match(/\\.\$/) ){
alert("「代表者メールアドレス（ドメイン）」が不正です3。");
return false;
}	//if
if( str.match(/\\.\\./) ){
alert("「代表者メールアドレス（ドメイン）」が不正です4。");
return false;
}	//if
if( str.match(/^\\./) ){
alert("「代表者メールアドレス（ドメイン）」が不正です5。");
return false;
}	//if


if (document.getElementById('tel1').value == "") {
alert('「代表者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel1").value;
if( str.match(/[^0-9-]/) ){
alert("代表者電話番号に半角数字以外が入力されております。");
return false;
}	//if


if (document.getElementById('zip').value == "") {
alert('「代表者住所（郵便番号）」が入力されていません。');
return(false);
}

if (document.getElementById('pref2').value == "") {
alert('「代表者住所（都道府県）」が入力されていません。');
return(false);
}

if (document.getElementById('cities1').value == "") {
alert('「代表者住所（市区町村）」が入力されていません。');
return(false);
}

if (document.getElementById('shimei2').value == "") {
alert('「第2担当者氏名」が入力されていません。');
return(false);
}

if (document.getElementById('shimei_kana2').value == "") {
alert('「第2担当者氏名（フリガナ）」が入力されていません。');
return(false);
}

if (document.getElementById('tel3').value == "") {
alert('「第2担当者電話番号」が入力されていません。');
return(false);
}
var str = document.getElementById("tel3").value;
if( str.match(/[^0-9-]/) ){
alert("第2担当者電話番号に半角数字以外が入力されております。");
return false;
}	//if


var str = document.getElementById("mailaddress2").value;
if (str == "") {
alert('「チームメールアドレス」が入力されていません。');
return(false);
}
if( str.match(/[^0-9a-zA-Z_\\-\\.@]/) ){
alert("「チームメールアドレス」に使用できない文字があります。");
return false;
}	//if
if( !str.match(/[@]/) ){
alert("「チームメールアドレス」が不正です1。");
return false;
}	//if
if( str.match(/[@]{2,}/) ){
alert("「チームメールアドレス」が不正です2。");
return false;
}	//if
if( str.match(/[ 　]/) ){
alert("「チームメールアドレス」が不正です3。");
return false;
}	//if
if( !str.match(/[\\.]/) ){
alert("「チームメールアドレス」が不正です4。");
return false;
}	//if
if( str.match(/\\.@/) ){
alert("「チームメールアドレス」が不正です5。");
return false;
}	//if
if( !str.match(/[0-9a-zA-Z_-]{1,}@[0-9a-zA-Z_-]{1,}\\.[0-9a-zA-Z_-]{1,}/) ){
alert("「チームメールアドレス」が不正です6。");
return false;
}	//if
if( str.match(/\\.\$/) ){
alert("「チームメールアドレス」が不正です7。");
return false;
}	//if
if( str.match(/\\.\\./) ){
alert("「チームメールアドレス」が不正です8。");
return false;
}	//if







if (document.getElementById('pwd').value == "") {
alert('「パスワード」が入力されていません。');
return(false);
}
if (document.getElementById('pwd').value.length < 4) {
alert('「パスワード」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd2').value == "") {
alert('「パスワード（確認用）」が入力されていません。');
return(false);
}
if (document.getElementById('pwd2').value.length < 4) {
alert('「パスワード（確認用）」が短すぎます。');
return(false);
}
var str = document.getElementById("pwd2").value;
if( str.match(/[^0-9a-zA-Z]/) ){
alert("「パスワード（確認用）」に半角英数字以外が入力されております。");
return false;
}	//if

if (document.getElementById('pwd').value != document.getElementById('pwd2').value) {
alert('パスワードが一致していません。');
return(false);
}

return true;
}	//func

</script>
<span style="color: #F00">*は必須項目です。</span>
<noscript>
<p style="color:red;font-size:16px;">（！）Javascriptを有効にしてください。</p>
</noscript>
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" onsubmit="return kakunin()" />
<input type="hidden" name="code" value="member_check_noframe" />
<input type="hidden" name="ses" value="$session" />
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff"><input name="_チーム正式名称" type="text" id="teamname" value="$paramhash_dec{'_チーム正式名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム正式名称（フリガナ）" type="text" id="team_kana" value="$paramhash_dec{'_チーム正式名称（フリガナ）'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム省略名称" type="text" id="team_abbr" value="$paramhash_dec{'_チーム省略名称'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_チーム結成年" maxlength=4 type="text" id="team_year" value="$paramhash_dec{'_チーム結成年'}" size="4" style="ime-mode: disabled;" />
<font class="type3">年　<font class="type1" color="#ff0000">※半角数字のみ</font><br />
※西暦（例：2012）にてご入力下さい。
</font>

</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_主な活動曜日" type="text" id="katsudou_week" value="$paramhash_dec{'_主な活動曜日'}" size="60" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_平均年齢" type="text" id="average_age" value="$paramhash_dec{'_平均年齢'}" size="4" style="ime-mode: disabled;" />
才　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
都道府県 <select name="_都道府県名" id="pref">
<option value="" >選択して下さい
<option value="北海道" $PFLAG{'北海道'}>北海道
<option value="青森県" $PFLAG{'青森県'}>青森県
<option value="岩手県" $PFLAG{'岩手県'}>岩手県
<option value="宮城県" $PFLAG{'宮城県'}>宮城県
<option value="秋田県" $PFLAG{'秋田県'}>秋田県
<option value="山形県" $PFLAG{'山形県'}>山形県
<option value="福島県" $PFLAG{'福島県'}>福島県
<option value="茨城県" $PFLAG{'茨城県'}>茨城県
<option value="栃木県" $PFLAG{'栃木県'}>栃木県
<option value="群馬県" $PFLAG{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG{'千葉県'}>千葉県
<option value="東京都" $PFLAG{'東京都'}>東京都
<option value="神奈川県" $PFLAG{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG{'新潟県'}>新潟県
<option value="富山県" $PFLAG{'富山県'}>富山県
<option value="石川県" $PFLAG{'石川県'}>石川県
<option value="福井県" $PFLAG{'福井県'}>福井県
<option value="山梨県" $PFLAG{'山梨県'}>山梨県
<option value="長野県" $PFLAG{'長野県'}>長野県
<option value="岐阜県" $PFLAG{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG{'静岡県'}>静岡県
<option value="愛知県" $PFLAG{'愛知県'}>愛知県
<option value="三重県" $PFLAG{'三重県'}>三重県
<option value="滋賀県" $PFLAG{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG{'京都府'}>京都府
<option value="大阪府" $PFLAG{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG{'島根県'}>島根県
<option value="岡山県" $PFLAG{'岡山県'}>岡山県
<option value="広島県" $PFLAG{'広島県'}>広島県
<option value="山口県" $PFLAG{'山口県'}>山口県
<option value="徳島県" $PFLAG{'徳島県'}>徳島県
<option value="香川県" $PFLAG{'香川県'}>香川県
<option value="愛媛県" $PFLAG{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG{'高知県'}>高知県
<option value="福岡県" $PFLAG{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG{'長崎県'}>長崎県
<option value="熊本県" $PFLAG{'熊本県'}>熊本県
<option value="大分県" $PFLAG{'大分県'}>大分県
<option value="宮崎県" $PFLAG{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG{'沖縄県'}>沖縄県
</select> 
　市区町村
<input name="_主な活動場所" type="text" id="team_cities" value="$paramhash_dec{'_主な活動場所'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="過去戦績" cols="60" rows="5" id="past_perform">$paramhash_dec{'過去戦績'}</textarea>
<br />
過去に参加された大会の実績等を具体的にご記入ください。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff"><textarea name="チームＰＲ" cols="60" rows="5" id="team_pr">$paramhash_dec{'チームＰＲ'}</textarea></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名" type="text" id="shimei1" value="$paramhash_dec{'_代表者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者氏名（フリガナ）" type="text" id="shimei_kana1" value="$paramhash_dec{'_代表者氏名（フリガナ）'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font>
<br>
<font class="type1" color="#ff0000">（ログインID）</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_代表者メールアドレス" type="text" id="mailadr1" value="$paramhash_dec{'_代表者メールアドレス'}" size="20" style="ime-mode: disabled;" />
＠
<input name="_代表者メールアドレス（ドメイン）" type="text" id="mailadr2" value="$paramhash_dec{'_代表者メールアドレス（ドメイン）'}" size="20" style="ime-mode: disabled;" />
<br />
※ログインIDには、PCアドレスを推奨いたします。<br>
<font class="type1" color="#ff0000">※携帯アドレスで登録される方は本登録用のメールがブロックされ届かない場合がありますので、<br>
　その場合はお手数ですがＴＯＰページのお問い合わせから事務局までご連絡下さい。<br>
※迷惑メール防止のための受信設定をしている場合は、あらかじめ設定 を解除、あるいはドメイン指定設定<br>
（「pridejapan.net」を指定）　などを行って下さい。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者電話番号" type="text" id="tel1" value="$paramhash_dec{'_代表者電話番号'}" size="20" style="ime-mode: disabled;" />　（例：0000-00-0000）　<font class="type1" color="#ff0000">※半角数字のみ</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
郵便番号<input name="_郵便番号" type="text" maxlength=8 id="zip" value="$paramhash_dec{'_郵便番号'}" size="10" />　
都道府県 <select name="_代表者都道府県名" id="pref2">
<option value="" >選択して下さい
<option value="北海道" $PFLAG2{'北海道'}>北海道
<option value="青森県" $PFLAG2{'青森県'}>青森県
<option value="岩手県" $PFLAG2{'岩手県'}>岩手県
<option value="宮城県" $PFLAG2{'宮城県'}>宮城県
<option value="秋田県" $PFLAG2{'秋田県'}>秋田県
<option value="山形県" $PFLAG2{'山形県'}>山形県
<option value="福島県" $PFLAG2{'福島県'}>福島県
<option value="茨城県" $PFLAG2{'茨城県'}>茨城県
<option value="栃木県" $PFLAG2{'栃木県'}>栃木県
<option value="群馬県" $PFLAG2{'群馬県'}>群馬県
<option value="埼玉県" $PFLAG2{'埼玉県'}>埼玉県
<option value="千葉県" $PFLAG2{'千葉県'}>千葉県
<option value="東京都" $PFLAG2{'東京都'}>東京都
<option value="神奈川県" $PFLAG2{'神奈川県'}>神奈川県
<option value="新潟県" $PFLAG2{'新潟県'}>新潟県
<option value="富山県" $PFLAG2{'富山県'}>富山県
<option value="石川県" $PFLAG2{'石川県'}>石川県
<option value="福井県" $PFLAG2{'福井県'}>福井県
<option value="山梨県" $PFLAG2{'山梨県'}>山梨県
<option value="長野県" $PFLAG2{'長野県'}>長野県
<option value="岐阜県" $PFLAG2{'岐阜県'}>岐阜県
<option value="静岡県" $PFLAG2{'静岡県'}>静岡県
<option value="愛知県" $PFLAG2{'愛知県'}>愛知県
<option value="三重県" $PFLAG2{'三重県'}>三重県
<option value="滋賀県" $PFLAG2{'滋賀県'}>滋賀県
<option value="京都府" $PFLAG2{'京都府'}>京都府
<option value="大阪府" $PFLAG2{'大阪府'}>大阪府
<option value="兵庫県" $PFLAG2{'兵庫県'}>兵庫県
<option value="奈良県" $PFLAG2{'奈良県'}>奈良県
<option value="和歌山県" $PFLAG2{'和歌山県'}>和歌山県
<option value="鳥取県" $PFLAG2{'鳥取県'}>鳥取県
<option value="島根県" $PFLAG2{'島根県'}>島根県
<option value="岡山県" $PFLAG2{'岡山県'}>岡山県
<option value="広島県" $PFLAG2{'広島県'}>広島県
<option value="山口県" $PFLAG2{'山口県'}>山口県
<option value="徳島県" $PFLAG2{'徳島県'}>徳島県
<option value="香川県" $PFLAG2{'香川県'}>香川県
<option value="愛媛県" $PFLAG2{'愛媛県'}>愛媛県
<option value="高知県" $PFLAG2{'高知県'}>高知県
<option value="福岡県" $PFLAG2{'福岡県'}>福岡県
<option value="佐賀県" $PFLAG2{'佐賀県'}>佐賀県
<option value="長崎県" $PFLAG2{'長崎県'}>長崎県
<option value="熊本県" $PFLAG2{'熊本県'}>熊本県
<option value="大分県" $PFLAG2{'大分県'}>大分県
<option value="宮崎県" $PFLAG2{'宮崎県'}>宮崎県
<option value="鹿児島県" $PFLAG2{'鹿児島県'}>鹿児島県
<option value="沖縄県" $PFLAG2{'沖縄県'}>沖縄県
</select> 
<br>市区町村
<input name="_代表者住所" type="text" id="cities1" value="$paramhash_dec{'_代表者住所'}" size="60" /><br>
<font class="type1" color="#ff0000">※賞品をお送りすることがございます。マンション名、部屋番号まで正確にご記入ください。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名" type="text" id="shimei2" value="$paramhash_dec{'_第2担当者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名（フリガナ）" type="text" id="shimei_kana2" value="$paramhash_dec{'_第2担当者氏名（フリガナ）'}" size="20" />
<br />
　代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。 </td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者電話番号" type="text" id="tel3" value="$paramhash_dec{'_第2担当者電話番号'}" size="20" style="ime-mode: disabled;" />　（例：0000-00-0000）　<font class="type1" color="#ff0000">※半角数字のみ</font>
<br />
※代表者様にご連絡がつかない場合、こちらにご連絡を差し上げます。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font>
</td>
<td align="left" bgcolor="#ffffff"><input name="_チームメールアドレス" type="text" id="mailaddress2" value="$paramhash_dec{'_チームメールアドレス'}" size="40" style="ime-mode: disabled;" />
<br />
　チームメールアドレスはPCもしくは携帯電話のアドレスがお使い頂けます。<br />
<font class="type1" color="#ff0000">※このアドレスは、登録をした全てのチームに表示されます。</font>
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff"><input name="チームHPアドレス" type="text" id="team_hp" value="$paramhash_dec{'チームHPアドレス'}" size="60" style="ime-mode: disabled;" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード" type="text" id="pwd" value="$paramhash_dec{'_パスワード'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード（確認用）</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_パスワード*" type="text" id="pwd2" value="$paramhash_dec{'_パスワード*'}" size="20" style="ime-mode: disabled;" />
<br />
※4桁以上の英数字</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input type="radio" name="_メールマガジン配信の選択" value="1" $MAILMAGAZINEFLAG{1} />
<font class="type3">希望する</font>　
<input type="radio" name="_メールマガジン配信の選択" value="0" $MAILMAGAZINEFLAG{0} />
<font class="type3">希望しない</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">LINE ID</font></td>
<td align="left" bgcolor="#ffffff"><input name="LINEID" type="text" id="lineid" value="$paramhash_dec{'LINEID'}" size="20" style="ime-mode: disabled;" />
<br>
<font class="type1" color="#ff0000">※メールアプリLINE（ライン）をお使いの方は、LINEのIDをチーム間の連絡用としてチームページに表示させることができます。<br>
※このIDは、プライドジャパンにログインしている全てのチームが閲覧可能になります。</font>
</td>
</tr>
</tbody>
</table>
<p align=center><input type="submit" id="submit" value="　　確認画面へ　　" disabled /></p>
</form>

<script>
//Javascriptが有効ならDisabledを外す
document.getElementById('submit').disabled = false;
</script>
END_HTML
###
&teamentryhtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：確認
# -----------------------------------------------------------------
sub member_check_noframe {
my $errormes = "";
#データ取得
for my $p ($query->param) {
	if($p eq ""){next;}
	if($p eq "code"){next;}
	my $v = $query->param($p);
#	utf8::decode($p);
#	utf8::decode($v);
$p = Encode::decode('utf8',$p);
$v = Encode::decode('utf8',$v);
#必須チェック
if($p =~ /^_/ && $v eq ""){
$p2 = $p;
$p2 =~ s/^_//;
$p2 =~ s/\*/確認/;
$errormes .=<<"END_HTML";
・$p2<br>
END_HTML
}	#if
#相互確認
if($p =~ /\*/){
$v2 = $paramhash{$p};
$p1 = $p;
$p1 =~ s/\*//;
$v1 = $paramhash{$p1};
if($v1 ne $v2){
$p1 =~ s/_//;
$errormes .=<<"END_HTML";
・$p1\が異なります。<br>
END_HTML
}	#if
}	#if
##
$v = $paramhash_enc{$p};
$rewritestr .=<<"END_HTML";
<input type="hidden" name="$p" value="$v" />
END_HTML
}	#for

#メールアドレス重複チェック
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$pwd = $paramhash_dec{'_パスワード'};
if($mailaddress1 ne "" && $pwd ne ""){
$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailaddress1 = '$mailaddress1' and pwd = '$pwd' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$errormes .=<<"END_HTML";
・既に登録されているメールアドレスです。<br>
END_HTML
}	#if 
}	#if 

############
# エラーチェック
if($errormes ne ""){
$mes =<<"END_HTML";
以下の必須項目が入力されておりません。<br>
$errormes
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" >
<input type="hidden" name="code" value="member_new_noframe" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" /></p>
</form>
END_HTML
###
&teamentryhtmldisp($mes);
exit;
}	#if

###
$mes =<< "END_HTML";
<table width="100%" cellspacing="0" class="stan">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム正式名称</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム正式名称（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム省略名称</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム省略名称'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム結成年</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チーム結成年'}
<font class="type3">年</font></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動曜日</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_主な活動曜日'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">平均年齢</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_平均年齢'}才</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">主な活動場所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_都道府県名'} $paramhash_dec{'_主な活動場所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">過去戦績</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'過去戦績'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームＰＲ</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームＰＲ'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者氏名（フリガナ）'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者メールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">（ログインID）</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者メールアドレス'}＠$paramhash_dec{'_代表者メールアドレス（ドメイン）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_代表者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
$paramhash_dec{'_郵便番号'} 
$paramhash_dec{'_代表者都道府県名'} 
$paramhash_dec{'_代表者住所'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者氏名（フリガナ）'}
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_第2担当者電話番号'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメールアドレス</font><font class="type1" color="#ff0000">*</font><br>
<font class="type1" color="#ff0000">※対戦相手との連絡用になりますので、お間違いのないようお願いします</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'_チームメールアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームHPアドレス</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'チームHPアドレス'}</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">パスワード</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">*****</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">メールマガジン配信の選択</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
<font class="type3">$MAILMAGAZINENAME{$paramhash_dec{'_メールマガジン配信の選択'}}</font>　
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">LINE ID</font></td>
<td align="left" bgcolor="#ffffff">$paramhash_dec{'LINEID'}</td>
</tr>
</tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="system.cgi" name="form2" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_new_noframe" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="system.cgi" name="form1" method="POST" enctype="multipart/form-data" accept-charset="UTF-8" />
<input type="hidden" name="code" value="member_add_noframe" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>
END_HTML
###
&teamentryhtmldisp($mes);
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：登録
# -----------------------------------------------------------------
sub member_add_noframe {

$teamname = $paramhash_dec{'_チーム正式名称'};
$team_kana = $paramhash_dec{'_チーム正式名称（フリガナ）'};
$team_abbr = $paramhash_dec{'_チーム省略名称'};
$team_year = $paramhash_dec{'_チーム結成年'};
$katsudou_week = $paramhash_dec{'_主な活動曜日'};
$average_age = $paramhash_dec{'_平均年齢'};
$team_zip = $paramhash_dec{'_郵便番号'};
$team_pref = $paramhash_dec{'_都道府県名'};
$team_cities = $paramhash_dec{'_主な活動場所'};
$past_perform = $paramhash_dec{'過去戦績'};
$team_pr = $paramhash_dec{'チームＰＲ'};
$shimei1 = $paramhash_dec{'_代表者氏名'};
$shimei_kana1 = $paramhash_dec{'_代表者氏名（フリガナ）'};
$mailadr1 = $paramhash_dec{'_代表者メールアドレス'};
$mailadr2 = $paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$mailaddress1 = $mailadr1."@".$mailadr2;
$tel1 = $paramhash_dec{'_代表者電話番号'};
$prefectural1 = $paramhash_dec{'_代表者都道府県名'};
$cities1 = $paramhash_dec{'_代表者住所'};
$shimei2 = $paramhash_dec{'_第2担当者氏名'};
$shimei_kana2 = $paramhash_dec{'_第2担当者氏名（フリガナ）'};
$tel2 = $paramhash_dec{'_第2担当者電話番号'};
$mailaddress2 = $paramhash_dec{'_チームメールアドレス'};
$team_hp = $paramhash_dec{'チームHPアドレス'};
$pwd = $paramhash_dec{'_パスワード'};
$mailmagazine = $paramhash_dec{'_メールマガジン配信の選択'};
$ses = $paramhash_dec{'ses'};
$lineid = $paramhash_dec{'LINEID'};

#セッションによる重複登録チェック
$sql_str = "SELECT * FROM $member_tbl WHERE ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count != 0){
$mes =<<"END_HTML";
<p style="color:red;font-weight:bold;font-size:20px;">重複登録がされました。</p>
<p>画面をリロードしないようご注意ください。</p>
END_HTML
###
&teamentryhtmldisp($mes);
exit;
}	#if 重複


# 新規登録
$sql_str = qq{INSERT INTO $member_tbl(ssid,contents,koukaiflag,mailadr1,mailadr2,pwd,shimei1,shimei_kana1,mailaddress1,tel1,prefectural1,cities1,shimei2,shimei_kana2,tel2,mailaddress2,teamname,team_kana,team_abbr,team_year,team_hp,katsudou_week,average_age,team_zip,team_pref,team_cities,past_perform,team_pr,mailmagazine,lineid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$ses,
21,
2,
$mailadr1,
$mailadr2,
$pwd,
$shimei1,
$shimei_kana1,
$mailaddress1,
$tel1,
$prefectural1,
$cities1,
$shimei2,
$shimei_kana2,
$tel2,
$mailaddress2,
$teamname,
$team_kana,
$team_abbr,
$team_year,
$team_hp,
$katsudou_week,
$average_age,
$team_zip,
$team_pref,
$team_cities,
$past_perform,
$team_pr,
$mailmagazine,
$lineid,
);
&sqlcheck($sql_str);
###
$subject = Unicode::Japanese->new("チーム情報 確認メール",'utf8')->jis;		#JISとして処理
$subject = jcode($subject)->mime_encode;
$mailheader =<<"END_HTML";
From: info\@$domain
To:$mailaddress1
Cc:info\@$domain
Subject: $subject
MIME-Version: 1.0
Content-Type: text/plain; charset="ISO-2022-JP"
Content-Transfer-Encoding: 7bit
END_HTML
$mailbody =<<"END_HTML";
PRIDE JAPANにご登録いただきありがとうございます。

以下のURLをクリックして登録手続きを完了してください。
$sitefulladr/systemmessage.html?code=member_ok&ses=$ses

また以下の情報はログインする際に必要となりますので大切に保管して下さい。
登録ID（メールアドレス）：$mailaddress1
パスワードについてはメールに記載しておりません。
各自でお控えください。

--------------------------------------
PRIDE JAPAN運営事務局

END_HTML
$mailbody = Unicode::Japanese->new($mailbody,'utf8')->jis;		#JISとして処理
open(MAIL, "| $sendmail") or die "sendmail open error.";
print MAIL "$mailheader\n$mailbody";	#送信
close MAIL;

###
$mes =<<"END_HTML";
<center>
<p style="color:red;font-weight:bold;font-size:20px;">現在はまだ「仮登録」です。</p>
<p>フォームに登録されたメールアドレスに、info\@pridejapan.netよりメールを送信しました。</p>
<p>パソコン等の迷惑メールフォルダに入ってしまわないよう設定を変更してください。</p>
<p>メール内に記載された注意事項に従って本登録をお願いします。</p>
<p>24時間以内に返信メールがない際は、お手数ですがお問い合わせフォームから、</p>
<p>またはinfo\@pridejapan.net宛てにお問い合わせください。</p>
</center>
END_HTML
###
&teamentryhtmldisp($mes);
exit;
}	#sub





# -----------------------------------------------------------------
# チーム登録用表示
# -----------------------------------------------------------------
sub teamentryhtmldisp {
my ($data)=(@_);
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"template_teamentry.html" or die "template_teamentry open error";
my @TEMPLATE = <IN>;
close IN;
#
utf8::decode($data);
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%data\%/$data/;
$str .= $line;
}	#foreach
print $str;
exit;
}	#sub




# -----------------------------------------------------------------
# マイページ用表示
# -----------------------------------------------------------------
sub mypagehtmldisp {
my ($data,$flag)=(@_);
if($flag ne ""){print "Content-type: text/html;\n\n";}
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"indextemplate.html" or die "indextemplate open error";
my @TEMPLATE = <IN>;
close IN;
#
utf8::decode($data);
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%data\%/$data/;
$str .= $line;
}	#foreach
print $str;
exit;
}	#sub


# -----------------------------------------------------------------
# ユーザーによるレコードの削除処理
# -----------------------------------------------------------------
sub deleterecord_user {
$ss = $paramhash{'ss'};
$ss =~ s/'/''/g;	#'
$returnurl = $paramhash{'returnurl'};
$returnurl =~ s/'/''/g;	#'
if($ss eq ""){	# serialがないとエラー
print "serial error.";
exit;
}	#if
#
$sql_str = "UPDATE $dbname SET koukaiflag = 9 WHERE serial = $ss";
$rs = $dbh->prepare($sql_str);
$rs->execute();
#
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="0;URL=?code=$returnurl">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
</body>
</html>
END_HTML
}


