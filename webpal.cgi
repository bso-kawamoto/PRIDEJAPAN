#!/usr/bin/perl

use utf8;
use CGI::Carp qw(fatalsToBrowser);

$cgifile = "webpal.cgi";
$cgifile2 = "webpal.cgi";

require 'common.cgi';


#履歴保存
$sql_str9 = qq{INSERT INTO entrylist_rireki(refara,remoteaddr,host,cgi,querystring) VALUES (?,?,?,?,?);};
$rs9 = $dbh->prepare($sql_str9);
$rs9->execute(
$ENV{'HTTP_REFERER'},
$ENV{'REMOTE_ADDR'},
$ENV{'HTTP_HOST'},
"webpal.cgi",
$ENV{'QUERY_STRING'},
);


if( $code eq "webpallogout"){&webpallogout;}
#
#　サイトコンテンツ管理CGI
#
$loginuser = "";

$webpalheader = << "HTML_VIEW";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle$webpalname</title>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td width=150><a href=$cgifile><img src=$sitefulladr/system/systemimages/webpallogo.jpg valign=middle border="0"></a></td>
<td align=center>$webpalname<p>
<font size="4"><b>$sitetitle 様</b></font>
</td>
<td width=150>　</td>
</tr>
<tr>
<td colspan=3>
<hr>
<center>
HTML_VIEW

$webpalfooter = << "HTML_VIEW";
</center>
</td></tr></table>
$webrightbar
</body>
</html>
HTML_VIEW
# -----------------------------------------------------------------
# ログイン管理
# -----------------------------------------------------------------
$id = $query->param('id');
@mailadr = split(/\@/,$query->param('id'));
$pw = $query->param('pw');
$code = $query->param('code');

$loginuser = &getcook('ssid');		# クッキーから値を取得する
$logincook = &getcook($cookiename);

# 権限エラーを優先
if( $code eq "kengenerror"){&kengen_error("権限がありません。");}
# 新規登録時はDBもクッキーも無いので、ここで処理分岐
if( $code eq "newentry"  ){&newentry;exit;}

$glevel = 0;
$flag = 0;
#事務局権限でクッキーがある場合
foreach  $key(keys %ID){
if($logincook eq $key && $key ne "" ){$glevel = 1;$flag = 1;last;}
}
if( $flag == 1 ){
if($code eq ""){$bookmark =1;}
goto loginok;
}	#if
#
#ユーザ権限でクッキーがある場合
if( $loginuser ne "" && $id eq "" && $pw eq "" ){
	#クッキーのSSIDの値で、DBを検索する
	$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and ssid = '$loginuser'  ";
	$rs = $dbh->prepare($sql_str);
	$rs->execute();
	&sqlcheck;	#SQLチェック
	$count = $rs->rows;	# Hit件数を確保
	if( $count == 1 ){
	$REFHASH = $rs->fetchrow_hashref;
	$glevel = $REFHASH->{'glevel'};
	$serial = $REFHASH->{'serial'};
	$teamname = &paramsetsql('teamname');
	$contents = &paramsetsql('contents');
	#&updateSSID($mailadr[0], $mailadr[1], $loginuser);
	#print "Content-type: text/html;\n\n";
	$OK_flg = 1;
	if($code eq ""){$bookmark =1;}
	goto loginok;
	}	#if $count == 1
}	#if
#
#メンバーパスワードチェック（クッキーが無い通常ルート）
if($mailadr[1] ne "" && $id ne "" && $pw ne ""){
	$sql_str = "SELECT * FROM member_tbl WHERE koukaiflag = 0 and mailadr1 = '$mailadr[0]' and mailadr2 = '$mailadr[1]'  ";
	$rs = $dbh->prepare($sql_str);
	$rs->execute();
	&sqlcheck;	#SQLチェック
	$count = $rs->rows;	# Hit件数を確保
	if( $count == 1 ){
	$REFHASH = $rs->fetchrow_hashref;
	$pwd_db = &paramsetsql('pwd');
	if($pw eq $pwd_db){
	$glevel = $REFHASH->{'glevel'};
	$serial = $REFHASH->{'serial'};
	$teamname = &paramsetsql('teamname');
	$contents = &paramsetsql('contents');
$OK_flg = 1;
goto logincheck2;
	}	#if
	}	#if count == 1
	#チェックしきれない場合はログイン画面へ
	print "Set-Cookie: value=; expires=Thu, 1-Jan-1970 00:00:00 GMT;\n";	#不正なクッキーの削除
	$OK_flg = 0;
	$loginuser = "";
	goto logincheck;
}	#if

#

if( $flag == 0 && $code eq "" && $id eq "" ){goto logincheck;}
if( $flag == 0 && $code ne "" && $id ne "" ){goto logincheck2;}

if($loginuser eq "" && $code eq ""){
# ログイン処理
logincheck:
print "Content-type: text/html;\n\n";
print <<"HTML_VIEW";
$webpalheader
<a href=$cgifile><font size=+1><b>$cgititle</b></font></a>
<center>
<form name="login" method="post" action="$cgifile" enctype="multipart/form-data">
<input name=code value="login" type=hidden>
<table border=0 bgcolor="#c0e2c4" width=200>
<tr bgcolor="#59e156"><td colspan=2>ログインをお願いします</td></tr>
<tr><td>ID</td><td><input name=id type=text size=24></td></tr>
<tr><td>Password</td><td><input name=pw type=password size=24></td></tr>
<tr><td colspan=2 align=center><input type=submit value=ログイン style="width:100px"></td></tr>
</table>
$footer
HTML_VIEW
exit;
}

logincheck2:
# 事務局権限 or ユーザ権限、でクッキーが無い場合
if( ($ID{$id} eq $pw || $OK_flg eq 1) && $id ne "" && $pw ne ""){
$loginuser = &setcook($cookiename,$id);
if($ID{$id} eq $pw){$glevel = 1;}
if($OK_flg eq 1){&updateSSID($mailadr[0], $mailadr[1], $loginuser);}
if($code eq ""){$bookmark =1;}

}else{
#IDエラー
print "Content-type: text/html;\n\n";
print <<"HTML_VIEW";
$webpalheader
ログイン出来ません。<p>
ID・パスワードをお確かめの上、ログインして下さい。
<p>
<a href=$cgifile>再ログイン</a>
HTML_VIEW
$footer;
exit;
}

# -----------------------------------------------------------------
# クッキーにログインがあれば飛んでくる
loginok:

if($glevel ne 1){
$sitetitle = $teamname;		#個別の名前を入れるようにする
}

$webpalimg = << "END_HTML";
<table width="100%" border="0" cellspacing="0" cellpadding="0" class="text-12" align=center>
<tr>
<td width=75%>
<table width=100% border="0" cellspacing="0" cellpadding="0" class="text-12">
<tr>
<td width=1><a href=$cgifile><img src=systemimages/webpallogo.jpg hspace=0 border="0" valign=middle></a></td>
<td align=center>$webpalname<p>
<font size="4"><b>$sitetitle 様</b></font>
</td>
</tr>
</table>
</td>
<td width=25% valign=top>
<table border="0" cellspacing="0" cellpadding="0" class="text-10" align=right>
<tr>
<td nowrap>■<a href="$sitefulladr" target=_blank>サイトへ</a></td>
<td nowrap>　</td>
<td nowrap>■<a href="$cgifile?code=webpallogout">ログアウト</a></td>
</tr>
</table>
</td>
</tr>
</table>
<hr width=100%>
END_HTML


# -----------------------------------------------------------------
# 分岐

#リファラ無しは弾く
if($ENV{'HTTP_REFERER'} eq "" && $bookmark eq "" &&  $code eq ""){
$mes =<<"END_HTML";
申し訳ありません。アクセスされたページはブックマークからのアクセスを禁止しております。<br>
<br>
お手数ですがTOPより順にお進み下さい。
<br>
<br>
<input type=button value="管理画面TOPへ" onclick="location.href='https://pridejapan.net/system/webpal.cgi' " />
<br>
END_HTML
&error($mes,1);
exit;

}	#if



# -----------------------------------------------------------------
# 分岐
# -----------------------------------------------------------------
if( $code eq "download"){&download;}
if( $code eq "csvdownload"){&csvdownload;exit;}

binmode STDOUT, ':utf8';
print "Content-type: text/html;\n\n";


if( $code eq "help"){&helpdisp;}

#フォーマット部更新
if( $code eq "newform"  ){&newform;exit;}
if( $code eq "editlist"  ){&editlist;exit;}
if( $code eq "editform"){&editform;exit;}
if( $code eq "formadd"){&formadd;exit;}
if( $code eq "deleterecord"){&deleterecord;exit;}
if( $code eq "deleteset"){&deleteset;exit;}


if( $code eq "member_editform"){&member_editform;exit;}
if( $code eq "member_formadd"){&member_formadd;exit;}
if( $code eq "member_editlist"){&member_editlist;exit;}

if( $code eq "entrylist"){&entrylist;exit;}
if( $code eq "entrydelete"){&entrydelete;exit;}

if( $code eq "othercontents_newform"  ){&othercontents_newform;exit;}
if( $code eq "othercontents_editlist"  ){&othercontents_editlist;exit;}
if( $code eq "othercontents_editform"){&othercontents_editform;exit;}
if( $code eq "othercontents_formadd"){&othercontents_formadd;exit;}
if( $code eq "othercontents_deleterecord"){&othercontents_deleterecord;exit;}
if( $code eq "othercontents_deleteset"){&othercontents_deleteset;exit;}
if( $code eq "passedconvention"){&passedconvention;exit;}

if( $code eq "teamlist"){&teamlist;exit;}
if( $code eq "team_edit"){&team_edit;exit;}
if( $code eq "team_check"){&team_check;exit;}
if( $code eq "team_add"){&team_add;exit;}
if( $code eq "team_delete"){&team_delete;exit;}

if( $code eq "nonteamlist"){&nonteamlist;exit;}
if( $code eq "ranking2"){&ranking2;exit;}

main();
exit;
# -----------------------------------------------------------------
# HTML処理開始
# -----------------------------------------------------------------
sub main {
print <<"HTML_VIEW";
$header
<table width="90%" border="0" cellpadding="2" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<br>
HTML_VIEW
#バナーカテゴリ
$bannercategory = &paramsetsql('bannercategory');
$temp = "";
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 44 and koukaiflag = 0 ORDER BY sortnum DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
for($i = 0;$i < $count1;$i++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$sstemp = &paramsetsql('serial',$REFHASH1);
$titletemp = &paramsetsql('title',$REFHASH1);
$BANNERCATENAME{$sstemp} = $titletemp;
}	#for
$BANNERCATENAME{0} = "未選択";

# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$koukaiflag = &paramsetsql('koukaiflag');
$title = &paramsetsql('title');
if($koukaiflag == 1){$title .= "<span class='hikoukaicolor'>【非公開】</span>";}
$category0 = &paramsetsql('category');
$genre1 = &paramsetsql('genre1');
$genrename1 = $GENRENAME{$genre1};
$genre2 = &paramsetsql('genre2');
$genrename2 = $GENRENAME{$genre2};
#if($genre1 == 1){$category = 1;}
#if($genre2 == 2){$category = 2;}

$price1 = &ketakanma(&paramsetsql('price1'));
$price2 = &ketakanma(&paramsetsql('price2'));
$price3 = &ketakanma(&paramsetsql('price3'));
$bannercategory = &paramsetsql('bannercategory')-0;

$nichiji1 = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji1')));
#画像
@IMGTEMPS = split(/:/,$REFHASH->{'upfilename'});
foreach $j(0..$gazoulimitnum){
utf8::decode($IMGTEMPS[$j]);
($sfn,$fn) = split(/<>/,$IMGTEMPS[$j]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
$IMGSRC[$j] = "<img src=img/dat.gif><br>";
if( $TEMP[1] eq "jpg"){$IMGSRC[$j] = "<img src=file/$TEMP[0]top.$TEMP[1]><br>";}
if( $TEMP[1] eq "pdf"){$IMGSRC[$j] = "<img src=img/pdf.gif><br>";}
if( $TEMP[1] eq "doc"){$IMGSRC[$j] = "<img src=img/doc.gif><br>";}
if( $TEMP[1] eq "xls"){$IMGSRC[$j] = "<img src=img/xls.gif><br>";}
if( $TEMP[1] eq "dat"){$IMGSRC[$j] = "<img src=img/dat.gif><br>";}
$FILENAME[$j] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$j] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
#エリア一覧
%AREALIST = ();
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag != 9 and taikaicode = $serial ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$ss = &paramsetsql('serial',$REFHASH1);
$category2 = &paramsetsql('category',$REFHASH1);
$area = &paramsetsql('serial',$REFHASH1);
$areaname = &paramsetsql('title',$REFHASH1);
$genre1 = &paramsetsql('genre1',$REFHASH1);
$genre2 = &paramsetsql('genre2',$REFHASH1);
$AREALIST{$category2} .=<<"END_HTML";
<tr>
<td>
<input type=button onClick="urljump(\'$cgifile?code=editlist&area=$area&contents=31&taikaicode=$serial&category=$category2\')" value="「${areaname}」に属する「組」の操作" style="width:200px;" />
</td><td>
<input type=button onClick="urljump(\'$cgifile?code=editform&serial=$area&contents=30&taikaicode=$serial&category=$category2\')" value="「${areaname}」の修正"  style="width:150px;" />
</td>
</tr>
<tr>
<td colspan=2>
<!--
<pre>
<span style='color:red;'>※現在修正中です。この部分には触れないで下さい。</span>
category2 = $category2
area = $area
areaname = $areaname
genre1 = $genre1
genre2 = $genre2
</pre>
-->
</td>
</tr>
END_HTML
}	#for

if($category0 == 1){$cflag1 = "";$cflag2 = "disabled";}
if($category0 == 2){$cflag1 = "disabled";$cflag2 = "";}
if($category0 == 3){$cflag1 = "";$cflag2 = "";}
$AREALIST{1} .=<<"END_HTML";
<tr>
<td colspan=2>
<hr>
<input type=button value="エリア登録" onClick="urljump(\'$cgifile?code=newform&taikaicode=$serial&category=1&contents=30\')" $cflag1>
</td>
</tr>
END_HTML

$AREALIST{2} .=<<"END_HTML";
<tr>
<td colspan=2>
<hr>
<input type=button value="エリア登録" onClick="urljump(\'$cgifile?code=newform&taikaicode=$serial&category=2&contents=30\')" $cflag2>
</td>
</tr>
END_HTML

### 表示
$TAIKAILIST{$koukaiflag} .=<<"END_HTML";
<table width="100%" border="0" align="center" cellpadding="1" cellspacing="1" class="text-12" bgcolor="#cccccc">
<tr class="s2" bgcolor="$BGCOLOR{$koukaiflag}">
<td align=center >大会画像</td>
<td align=center nowrap  width=80%>概要</td>
<td align=center nowrap >第１枠（リーグ）　：エリア操作</td>
<td align=center nowrap >第２枠（トーナメント）　：エリア操作</td>
</tr>
<tr bgcolor="white">
<td class="tdpad" valign=top align=center>$IMGSRC[$j] </td>
<td class="tdpad" valign=top nowrap >
大会名：<strong>$title</strong><br>
登録日：$nichiji1<br>
バナーカテゴリ名：$BANNERCATENAME{$bannercategory}<br>
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=0\')">
<!--
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=0\')">
<span style='color:red;'>※現在修正中です。この部分には触れないで下さい。</span>
-->

<table border="0" cellpadding="0" cellspacing="0" align="left" class="text-12">
<tr><td bgcolor="#dd8680" align=center></td></tr>
<tr><td>
</td></tr>
</table>

</td>

<td nowrap valign=top >
<table border="0" cellpadding="0" cellspacing="0" align="left" class="text-12">
$AREALIST{1}
</table>
</td>

<td nowrap valign=top >
<table border="0" cellpadding="0" cellspacing="0" align="left" class="text-12">
$AREALIST{2}
</table>
</td>

</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left class="tdpad2">大会イメージ</td>
<td bgcolor="white" colspan=3>

<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=newform&contents=36&taikaicode=$serial")' >
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=36&taikaicode=$serial")' >
</td></tr>
</table>

</td>
</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left nowrap class="tdpad2"> - 勝ち点について</td>
<td bgcolor="white" colspan=3>

<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editform&contents=40&taikaicode=$serial")'>
</td></tr>
</table>

</td>
</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left class="tdpad2"> - 大会概要</td>
<td bgcolor="white" colspan=3>
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editform&contents=45&taikaicode=$serial")' >
</td></tr>
</table>
</td>
</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left class="tdpad2"> - トーナメント画像</td>
<td bgcolor="white" colspan=3>
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=newform&contents=42&taikaicode=$serial")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=42&taikaicode=$serial")'>
</td></tr>
</table>
</td>
</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left class="tdpad2"> - $CONTENTSNAME[7]</td>
<td bgcolor="white" colspan=3>
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=newform&contents=7&taikaicode=$serial")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=7&taikaicode=$serial")'>
</td></tr>
</table>
</td>
</tr>

<tr class="s2" bgcolor="#73d783">
<td align=left class="tdpad2" nowrap > - エントリーチーム一覧</td>
<td bgcolor="white" colspan=3>
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=entrylist&taikaicode=$serial")'>
</td></tr>
</table>
</td>
</tr>



</table>

<p>
END_HTML
}	#for

# 管理画面 ==========================================
if($glevel == 1){
print <<"HTML_VIEW";
<table width="100%" border="0" align="center" cellpadding="1" cellspacing="1" class="text-12" bgcolor="#cccccc">

<tr valign="top">
<td  bgcolor="#dd8680" class="tdpad"  colspan=2>
<span style="font-size:14px;font-weight:bold;color:#FFFFFF;">TOPページ</span>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[0]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<!--
<span style='color:red;'>※現在修正中です。この部分には触れないで下さい。</span>
-->
<table width="365" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=newform&contents=0")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=0")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="過去の大会一覧" style="width:150px" onClick='urljump("$cgifile?code=passedconvention")'>
</td></tr>
</table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$OTHERCONTENTSNAME[100]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="315" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=othercontents_newform&contents=100")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=othercontents_editlist&contents=100")'>
</td></tr>
</table>
</td>
</tr>
<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$OTHERCONTENTSNAME[101]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="315" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=othercontents_newform&contents=101")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=othercontents_editlist&contents=101")'>
</td><td align="left">
</td></tr>
</table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
登録チーム一覧
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=teamlist")'>
</td><td align="left">
</td></tr>
</table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[44]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="新規" style="width:100px" onClick='urljump("$cgifile?code=newform&contents=44")'>
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=44")'>
</td></tr>
</table>
</td>
</tr>


<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
メールマガジン登録チーム
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
<input name="contents" type="button" id="contents" value="CSVダウンロード" style="width:150px" onClick='urljump("$cgifile?code=csvdownload")'>
</td><td align="left"></td>
</tr>
</table>
</td>
</tr>


<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
仮登録チーム一覧
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left">
<tr><td align="left" width="105">
</td><td align="left">
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=nonteamlist")'>
</td><td align="left">
</td></tr>
</table>
</td>
</tr>

</table>

<table width=100% cellpadding=4 cellspacing=0 border=0 >
<tr>
<td bgcolor="#98fb98" align=center onclick="panelchg(1)" ><span style="font-weight:bold;color:#008000;">【公開中】</span>の大会</td>
<td bgcolor="#ffc0cb" align=center onclick="panelchg(2)" ><span style="font-weight:bold;color:#ff1493;">【非公開】</span>の大会</td>
</tr>
</table>
<div id="panel1" >
$TAIKAILIST{0}
</div>
<div id="panel2" style="display:none;">
$TAIKAILIST{1}
</div>

<script>
function panelchg(n){
document.getElementById('panel1').style.display = "none";
document.getElementById('panel2').style.display = "none";
document.getElementById('panel'+n).style.display = "block";
}	//func
</script>

HTML_VIEW

}else{	#if $glevel
# メンバー画面 ==========================================
print <<"HTML_VIEW";
<table width="80%" border="0" align="center" cellpadding="1" cellspacing="1" class="text-12" bgcolor="#cccccc">

<tr valign="top">
<td  bgcolor="#dd8680" class="tdpad"  colspan=2>
<span style="font-size:14px;font-weight:bold;color:#FFFFFF;">TOPページ（メンバー）</span>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[21]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left"><tr><td align="left">
<input name="contents" type="button" id="contents" value="登録／編集" style="width:100px" onClick='urljump("$cgifile?code=member_editform&serial=$serial&contents=21")'>
</td></tr></table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[22]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left"><tr><td align="left">
<input name="contents" type="button" id="contents" value="新規エントリー" style="width:100px" onClick='urljump("$cgifile?code=member_editform&serial=$serial&contents=22")'>
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=member_editlist&serial=$serial&contents=22")'>
</td></tr></table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#dd8680" class="tdpad"  colspan=2>
<span style="font-size:14px;font-weight:bold;color:#FFFFFF;">試合予定／結果　管理</span>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[23]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left"><tr><td align="left">
<input name="contents" type="button" id="contents" value="新規報告" style="width:100px" onClick='urljump("$cgifile?code=newform&serial=$serial&contents=23")'>
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=23")'>
</td></tr></table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[24]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left"><tr><td align="left">
<input name="contents" type="button" id="contents" value="新規報告" style="width:100px" onClick='urljump("$cgifile?code=newform&serial=$serial&contents=24")'>
<input name="contents" type="button" id="contents" value="編集/更新" style="width:100px" onClick='urljump("$cgifile?code=editlist&contents=24")'>
</td></tr></table>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#dd8680" class="tdpad"  colspan=2>
<span style="font-size:14px;font-weight:bold;color:#FFFFFF;">コンタクト</span>
</td>
</tr>

<tr valign="top">
<td  bgcolor="#ffffff" nowrap class="tdpad" width="200" >
$CONTENTSNAME[25]
</td>
<td bgcolor="#ffffff" class="tdpad" align="left">
<table width="210" border="0" cellpadding="0" cellspacing="0" align="left"><tr><td align="left">
<input name="contents" type="button" id="contents" value="問合せ" style="width:100px" onClick='urljump("$cgifile?code=newform&serial=$serial&contents=25")'>
</td></tr></table>
</td>
</tr>

</td>
</tr>
</table>
HTML_VIEW
}	#if $glevel

print <<"HTML_VIEW";
$footer
HTML_VIEW
exit;
}	#sub

# -----------------------------------------------------------------
# ログアウト処理
# -----------------------------------------------------------------
sub webpallogout {
print "Set-Cookie: value=; expires=Thu, 1-Jan-1970 00:00:00 GMT;\n";
print "Content-type: text/html;\n\n";
print <<"END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$webpalname</title>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td width=150><a href=$cgifile><img src=systemimages/webpallogo.jpg valign=middle border="0"></a></td>
<td align=center><a href=$cgifile><font color="#666666">$webpalname</font></a></td>
<td width=150>　</td>
</tr>
<tr>
<td colspan=3>
<hr>
<center>
ログアウトしました。<p>
<br>
<a href=$cgifile>再ログイン</a>
</td></tr></table>
</body>
</html>
END_HTML
exit;
}


# -----------------------------------------------------------------
# ヘルプ
# -----------------------------------------------------------------
sub helpdisp {
print <<"END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<p>■Webpalシステムにおける、制限や注意事項など</p>

□写真のアップロード<br>
<table>
<tr><td>・画像の種類制限</td><td>：jpeg,pjpeg</td></tr>
<tr><td>・画像のサイズ制限</td><td>：縦サイズもしくは横サイズが $psize ピクセル以下</td></tr>
<tr><td>・ファイルサイズ制限</td><td>：$maxfilesize Mまで（サーバーの負荷により、この制限より小さいサイズでもエラーが出る場合がございます。）</td></tr>
</table>

<p>不明な点がございましたら以下の【技術サポート窓口】より問い合わせください。<p/>

</td>
</tr>
</table>
$footer
END_HTML
exit;
}





