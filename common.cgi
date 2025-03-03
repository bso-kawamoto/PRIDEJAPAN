use utf8;
use lib './system/lib','./lib';
use File::Basename;
use File::Copy;
use Jcode;
use Unicode::Japanese;	#文字コード
use Date::Simple (':all');
use Unicode::Normalize;
use Digest::SHA1 qw(sha1_hex);

#-------------------------------------#
# サイト固有データ
#-------------------------------------#
#本サイト用
$sitetitle = "Pride Japan";
$domain = 'pridejapan.net';
$sitefulladr = "http://pridejapan.net";
$sitefulladr_ssl = "https://pridejapan-net.ssl-xserver.jp";
$dbhostname ="mysql64.xserver.jp";
$database = "bso_pridejapan";
$dbuser = "bso_pridejapan";
$dbpassword = "bso7344";

#テストサイト用
if($ENV{'SERVER_NAME'} eq 'screation.net'){
$sitetitle = "Pride Japan";
$domain = 'screation.net';
$sitefulladr = "https://$domain/pridejapan";
$sitefulladr_ssl = "https://$domain/pridejapan";
$dbhostname ="mysql412.db.sakura.ne.jp";
$database = "yureru_bso";
$dbuser = "yureru";
$dbpassword = "cryasc0212";
}	#if

#-------------------------------------#
# /サイト固有データ
#-------------------------------------#



$dbname = 'pridejapan';		#tablename
$member_tbl = 'member_tbl';
$cookiename = "bso_pridejapan";
%ID = (
	"pridebso" => "uzbu7ppi",
);
%IDNAME = (
	"pridejapan" => "$sitetitle",
);
$webpalname = "- WebPal -ウェブパル　[サイトコンテンツ管理]";
$sendmail = '/usr/sbin/sendmail -t ';

$ofslimit = 4;

#コンテンツ名
@CONTENTSNAME = ();
$CONTENTSNAME[0] = "大会登録";
$CONTENTSNAME[1] = "お知らせ記事";
$CONTENTSNAME[2] = "リンク集登録";
$CONTENTSNAME[3] = "対戦チーム登録";
$CONTENTSNAME[4] = "対戦予定日・グラウンド登録";
$CONTENTSNAME[5] = "試合結果入力";
$CONTENTSNAME[6] = "星取り表入力";
$CONTENTSNAME[7] = "大会記事";
$CONTENTSNAME[8] = "入金確認チェック";
$CONTENTSNAME[9] = "チーム情報参照・変更";
$CONTENTSNAME[21] = "チーム情報";
$CONTENTSNAME[22] = "大会エントリー";
$CONTENTSNAME[23] = "予定試合一覧／報告";
$CONTENTSNAME[24] = "試合結果一覧／報告";
$CONTENTSNAME[25] = "事務局問合せ";
$CONTENTSNAME[30] = "地区名";
$CONTENTSNAME[31] = "組";
$CONTENTSNAME[32] = "エントリーチーム";
$CONTENTSNAME[33] = "対戦組み合わせ";
$CONTENTSNAME[34] = "試合予定報告";
$CONTENTSNAME[35] = "試合結果報告";
$CONTENTSNAME[36] = "大会イメージ";
$CONTENTSNAME[37] = "ブロック分け";
$CONTENTSNAME[38] = "募集対象";
$CONTENTSNAME[39] = "大会の流れ";
$CONTENTSNAME[40] = "勝ち点";
$CONTENTSNAME[41] = "大会ルール";
$CONTENTSNAME[42] = "トーナメント画像";
$CONTENTSNAME[43] = "試合予定一覧";
$CONTENTSNAME[44] = "バナーカテゴリ";
$CONTENTSNAME[45] = "大会概要／規定";

#フォームファイル名
@FORMFILE = ();
$FORMFILE[0] = "form_taikai.html";
$FORMFILE[1] = "form_holiday.html";
$FORMFILE[2] = "form_holiday.html";
$FORMFILE[3] = "form_holiday.html";
$FORMFILE[4] = "form_holiday.html";
$FORMFILE[5] = "form_holiday.html";
$FORMFILE[6] = "form_holiday.html";
$FORMFILE[7] = "form_taikaikiji.html";
$FORMFILE[8] = "form_holiday.html";
$FORMFILE[9] = "form_holiday.html";
$FORMFILE[21] = "form_member.html";
$FORMFILE[22] = "form_taikai_entry.html";
$FORMFILE[23] = "form_holiday.html";
$FORMFILE[24] = "form_holiday.html";
$FORMFILE[25] = "form_holiday.html";
$FORMFILE[30] = "form_area.html";
$FORMFILE[31] = "form_kumi.html";
$FORMFILE[32] = "form_team.html";
$FORMFILE[33] = "form_vs.html";
$FORMFILE[34] = "form_yoteireport.html";
$FORMFILE[35] = "form_resultreport.html";
$FORMFILE[36] = "form_taikaiimage.html";
$FORMFILE[37] = "form_block.html";
$FORMFILE[38] = "form_bosyu.html";
$FORMFILE[39] = "form_nagare.html";
$FORMFILE[40] = "form_kachiten.html";
$FORMFILE[41] = "form_rule.html";
$FORMFILE[42] = "form_result.html";
$FORMFILE[43] = "form_yoteiichiran.html";
$FORMFILE[44] = "form_bannercategory.html";
$FORMFILE[45] = "form_gaiyou.html";

@WEEKNAME = ("日","月","火","水","木","金","土",);

@KOUKAIFLAG = ("公開","非公開");
$KATSUDOUNAME{0} = "活動中";
$KATSUDOUNAME{1} = "凍結中";
$KATSUDOUNAME{9} = "削除";



%MAILMAGAZINENAME = ();
$MAILMAGAZINENAME{'1'} = "希望する";
$MAILMAGAZINENAME{'0'} = "希望しない";


#画像（書類）の最大数：０〜なので、実際はこの数値＋１個
$gazoulimitnum = 19;

#休日の枠数
$holidaycount = 19;	#0〜　なので＋１個になる

#勝ち点
$KACHITENNAME[1] = "勝ち";
$KACHITENNAME[2] = "負け";
$KACHITENNAME[3] = "引き分け";
$KACHITENNAME[4] = "不戦勝";
$KACHITENNAME[5] = "不戦敗";
#$KACHITENNAME[6] = "中止";
$KACHITENNAME[7] = "コールド勝ち";
$KACHITENNAME[8] = "コールド負け";
$KACHITENNAME[9] = "延長勝ち";
$KACHITENNAME[10] = "延長負け";
$KACHITENNAME[11] = "サヨナラ勝ち";
$KACHITENNAME[12] = "サヨナラ負け";


$othercontents_dbname = 'othercontents';

$OTHERCONTENTSNAME[100] = "お知らせ";
$OTHERCONTENTSNAME[101] = "リンク集";

$OTHERCONTENTS_FORMFILE[100] = "othercontents_osirase.html";
$OTHERCONTENTS_FORMFILE[101] = "othercontents_link.html";

$LINKGENRENAME[1] = "草野球情報・コミュニティ";
$LINKGENRENAME[2] = "野球用品販売店・施設";
$LINKGENRENAME[3] = "団体・連盟等";
$LINKGENRENAME[4] = "野球用品メーカー";
$LINKGENRENAME[5] = "野球関連企業";
$LINKGENRENAME[9] = "その他";

$GENRENAME{1} = "リーグ";
$GENRENAME{2} = "トーナメント";

$BGCOLOR{0} = "#73d783";
$BGCOLOR{1} = "#ffb6c1";

# -----------------------------------------------------------------
#データベースオープン
# -----------------------------------------------------------------
use DBI;
$sqldsn="DBI:mysql:$database:$dbhostname";
$dbh = DBI->connect($sqldsn,$dbuser,$dbpassword);
$dbh->do("set names utf8");
# ----------------------------------
sub sqlcheck {
my ($sql_str)=(@_);
my $s1 = $dbh->err;
my $s2 = $dbh->errstr;
if($s1 ne ""){
print "$sql_str<br>\n";
print "$s1:$s2<br>\n";
exit;
}	#if
}	#sub

#-------------------------------------#
# アクセス履歴
#-------------------------------------#
&accesslog;


# -----------------------------------------------------------------
# 初期設定
# -----------------------------------------------------------------
use CGI;
$query = new CGI;
$query->charset('utf-8');
$id = $query->param('id');
$pw = $query->param('pw');
$code = $query->param('code');
$maxfilesize = 2;	#単位：MB
# 最大許容サイズ（KByte）
$maxsize = 1024*$maxfilesize;
$CGI::POST_MAX = 1024 * 1024*$maxfilesize;
# 最大ピクセルサイズ
$psize = 2000;
# アップロードを許可するファイルの種類（MIMEと拡張子）
%hash_mime = (
	'application/xls' => 'xls', # EXCELファイル
	'application/vnd.ms-excel' => 'xls', # EXCELファイル
	'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' => 'xlsx', # EXCELファイル
	'application/octet-stream' => 'xls', # EXCELファイル
	
	'application/msword' => 'doc', # WORDファイル
	'application/msworddoc' => 'doc', # WORDファイル
	'application/vnd.openxmlformats-officedocument.wordprocessingml.document' => 'docx', # WORDファイル
	
	'application/pdf' => 'pdf', # PDFファイル
	'application/x-pdf' => 'pdf', # PDFファイル
	
	'image/jpg' => 'jpg', # Jpegファイル
	'image/pjpg' => 'jpg', # Jpegファイル
	'image/jpeg' => 'jpg', # Jpegファイル
	'image/pjpeg' => 'jpg', # Jpegファイル
  );
# -----------------------------------------------------------------
# CGI.pm 文字化け対策（サーバーのバージョンで動作）
for my $p ($query->param) {
	if($p eq ""){next;}
	my $v = $query->param($p);
	utf8::decode($p);
	utf8::decode($v);
	$paramhash{$p} = $v;
	my $v2 = $v;
	$v2 =~ s/'/''/gm;	#'
	$paramhash2{$p} = $v2;
#文字のURLエンコード
	$s = $v;
	utf8::encode($s);
	$s =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
	$s =~ tr/ /+/;
	utf8::decode($s);
	$paramhash_enc{$p} = $s;
#文字のURLデコード
	$s = $v;
	utf8::encode($s);
	$s =~ tr/+/ /;
	$s =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	utf8::decode($s);
	$paramhash_dec{$p} = $s;
#
if($p =~ /^file\d+/){next;}
#文字のURLデコード
$paramhash_sjis2utf8{$p} = Unicode::Japanese->new($v,'sjis')->get;
utf8::decode($paramhash_sjis2utf8{$p});
#文字のURLエンコード
$s = $paramhash_sjis2utf8{$p};
utf8::encode($s);
$s =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$s =~ tr/ /+/;
utf8::decode($s);
$paramhash_sjis2utf8enc{$p} = $s;
}	#for# -----------------------------------------------------------------
$imgmaxlength = 62;	#画像の数
$attach_dir = "file";

use Image::Size;
require 'GetPicSize.pl';
use ImgResize;
# 初期化
$ImgResize = new ImgResize( 6 );
GD::Image->trueColor(1);	#GDをフルカラーに対応させる
# -----------------------------------------------------------------

($sec,$min,$hour,$mday,$month,$year,$wno) = localtime(time);
$month++;
$year += 1900;

@GETUMATU = (0,31,28,31,30,31,30,31,31,30,31,30,31);
# 閏年計算
# 入力年がうるう年の場合は $flag に 1 をセットする
if ($year % 400 == 0) {			# ← 400の倍数年の場合
  $flag = 1;
} elsif ($year % 100 == 0) {	# ← 100の倍数年の場合
  $flag = 0;
} elsif ($year % 4 == 0) {		# ← 4の倍数年の場合
  $flag = 1;
} else {						# ← その他の場合
  $flag = 0;
}
if($flag == 1){$GETUMATU[2] = 29;}
$nowdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year,$month,$mday,$hour,$min,$sec);

# -----------------------------------------------------------------
$webrightbar = << "HTML_VIEW";
<br>
<br>
<br>
<div align=center style="font-size: 10px;">
<hr width=600>
<a target="_blank" href="http://www.net-friends.co.jp/webpal/support/form/form.cgi?c=$sitetitle">【技術サポート窓口】</a><br>
&copy;2012 NET FRIENDS INC. All Rights Reserved.
</div>
HTML_VIEW

#---------------------------
$loginuser = &getcook($cookiename);

$header = <<"END_HTML";
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>$sitetitle $webpalname</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に削除してもよろしいですか")) {
	top.location.href=url;
}
}
function windowopen(url,w,h){
if( url != ""){
if(w <600 ){w=600;}
if(h <600 ){h=600;}
w = window.open(url, "workspace", "width="+w+",height="+h+",directories=no,location=no,menubar=no,resizable=yes,scrollbars=yes,status=no,toolbar=no");
}
}
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
END_HTML

$footer = <<"END_HTML";
$webrightbar
</body>
</html>
END_HTML



$webpalimg = << "HTML_VIEW";
<table width="90%" border="0" cellspacing="0" cellpadding="0" class="text-12" align=center>
<tr>
<td width=75%>
<table width=100% border="0" cellspacing="0" cellpadding="0" class="text-12">
<tr>
<td width=1><a href=webpal.cgi><img src=$sitefulladr/system/systemimages/webpallogo.jpg hspace=0 border="0" valign=middle></a></td>
<td align=center>$webpalname<p>
<font size="4"><b>$sitetitle 様</b></font>
</td>
</tr>
</table>
</td>
<td width=25%>
<table border="0" cellspacing="0" cellpadding="0" class="text-10" align=right>
<tr>
<td colspan=3>
<table border="0" cellspacing="0" cellpadding="0" class="text-10" width=100%>
<tr>
<td nowrap>■<a href="$sitefulladr" target="_blank">サイトへ</a></td>
<td nowrap>■<a href="webpal.cgi?code=logout">ログアウト</a></td>
</tr>
</table>
</td>
</tr>
<tr>
<td nowrap colspan=2>□ログインユーザー</td><td nowrap>：[$IDNAME{$loginuser}]</td>
</tr>
</table>
</td>
</tr>
</table><hr width=90%>
HTML_VIEW

# -----------------------------------------------------------------
# 閏年計算
# -----------------------------------------------------------------
sub urudays {
my ($year,$mm)=(@_);
my $flag;
my @GETUMATU = (0,31,28,31,30,31,30,31,31,30,31,30,31);
# 閏年計算
# 入力年がうるう年の場合は $flag に 1 をセットする
if ($year % 400 == 0) {			# ← 400の倍数年の場合
  $flag = 1;
} elsif ($year % 100 == 0) {	# ← 100の倍数年の場合
  $flag = 0;
} elsif ($year % 4 == 0) {		# ← 4の倍数年の場合
  $flag = 1;
} else {						# ← その他の場合
  $flag = 0;
}
if($flag == 1){$GETUMATU[2] = 29;}
return $GETUMATU[$mm];
}	#sub

# -----------------------------------------------------------------
# 年月日のselectタグを作成
# -----------------------------------------------------------------
sub makeselect{
my ($st,$ed,$ec) = (@_);
my $data = "";
if( $ed >= $st ){
for(my $i=$st;$i<=$ed;$i++){
if($i == $ec){
	$data .= "<option value=\"$i\" selected>$i</option>\n";
}else{
	$data .= "<option value=\"$i\">$i</option>\n";
}	#if
}	#for
}else{
#リバースモード
for(my $i=$st;$i>=$ed;$i--){
if($i == $ec){
	$data .= "<option value=\"$i\" selected>$i</option>\n";
}else{
	$data .= "<option value=\"$i\">$i</option>\n";
}	#if
}	#for
}	#if

return $data;
}	#sub

# -----------------------------------------------------------------
# 都道府県のselectタグを作成
# -----------------------------------------------------------------
sub makeselect_pref{
my ($ec) = (@_);
my $data = "";
my @PREF = ("","北海道","青森県","秋田県","岩手県","山形県","宮城県","福島県","茨城県","栃木県","群馬県","埼玉県","神奈川県","千葉県","東京都","山梨県","長野県","新潟県","富山県","石川県","福井県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県");

for(my $i=0;$i<=47;$i++){
if($PREF[$i] eq $ec){
	$data .= "<option value=\"$PREF[$i]\" selected>$PREF[$i]</option>\n";
}else{
	$data .= "<option value=\"$PREF[$i]\">$PREF[$i]</option>\n";
}	#if
}	#for

return $data;
}	#sub
# -----------------------------------------------------------------
# 現在のセッションIDをデータベースに格納する
# -----------------------------------------------------------------
sub updateSSID{
my ($mailadr1,$mailadr2, $loginuser) = @_;
# データベースに格納されているセッションIDを持ってくる
$sql_str = "SELECT * FROM member_tbl WHERE mailadr1 = '$mailadr1' AND mailadr2 = '$mailadr2'  ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck;	#SQLエラーチェック
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$ssid_db = &paramsetsql('ssid');
# 一致するか？
if($loginuser eq $ssid_db){
return true;
}else{
#データベースにセッションIDを格納する
	if($loginuser ne ""){
	$sql_str = "UPDATE member_tbl SET ssid = '$loginuser' WHERE serial = $serial ";
	$rs = $dbh->prepare($sql_str);
	$rs->execute();
	&sqlcheck;	#SQLエラーチェック
	}
}	#if
}
# -----------------------------------------------------------------
# ユニークなIDを生成する
# -----------------------------------------------------------------
sub genUniqID{
  my $seed = shift || 'seed-string';
  my $id = join(''
          , $ENV{'REMOTE_ADDR'}
          , $ENV{'HTTP_USER_AGENT'}
          , time
          , $$
          , rand(9999)
          , $seed
      );

  return(sha1_hex($id));
}
# -----------------------------------------------------------------
# セットクッキー　６時間有効
# -----------------------------------------------------------------
sub setcook {
my ($fn,$cook) = @_;
utf8::encode($cook);
$cook =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$cook =~ tr/ /+/;
utf8::decode($cook);
my($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+30*24*60*60);
$wday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[$wday];
$mon = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec)[$mon];
$expire = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$wday,$mday,$mon,$year+1900,$hour,$min,$sec);
$ssid = &genUniqID;
print "Set-Cookie: value=$fn&$cook&$ssid; expires=$expire;\n";
return($ssid);
}
# -----------------------------------------------------------------
# ゲットクッキー
# -----------------------------------------------------------------
sub getcook {
my ($fn) = @_;
my($n,$val,$val1,$val2,$val3,@pair);
@pair = split(/;\s*/,$ENV{'HTTP_COOKIE'});
foreach (@pair) {
($n,$val) = split(/=/);
utf8::encode($val);
$val =~ tr/+/ /;
$val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
utf8::decode($val);
($val1,$val2,$val3) = split(/&/, $val);
	if($fn eq $val1){return $val2;}
	if($fn eq "ssid"){return $val3;}
}
return "";
}

# -----------------------------------------------------------------
# セットクッキー　３０日有効
# -----------------------------------------------------------------
sub setcook2 {
my ($fn,$cook) = @_;
utf8::encode($cook);
$cook =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$cook =~ tr/ /+/;
utf8::decode($cook);
my($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+30*24*60*60);
$wday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[$wday];
$mon = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec)[$mon];
$expire = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$wday,$mday,$mon,$year+1900,$hour,$min,$sec);
print "Set-Cookie: $fn=$cook; expires=$expire;\n";
}
# -----------------------------------------------------------------
# ゲットクッキー
# -----------------------------------------------------------------
sub getcook2 {
my ($fn) = @_;
my @pair = split(/;/,$ENV{'HTTP_COOKIE'});
foreach (@pair) {
my ($n,$val) = split(/=/);
$n =~ s/ //g;
if($fn eq $n){
utf8::encode($val);
$val =~ tr/+/ /;
$val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
utf8::decode($val);
return $val;
}
}
return "";
}

# -----------------------------------------------------------------
# 改行対策
# -----------------------------------------------------------------
sub crlfreset {		#改行を\nに統一
my ($ss)=(@_);
$ss =~ s/\x0D\x0A/\n/g;
$ss =~ s/\t//g;
##$ss =~ s/"/&quot;/g;	#"
#$ss =~ s/\<br>/\n/g;
#$ss =~ s/\<br \/>/\n/g;
#$ss =~ s/\<BR>/\n/g;
#$ss =~ s/\<BR \/>/\n/g;
#$ss =~ s/\<Br>/\n/g;
#$ss =~ s/\<Br \/>/\n/g;
#$ss =~ s/\<bR>/\n/g;
#$ss =~ s/\<bR \/>/\n/g;
return $ss;
}
sub crlfreset2 {		#改行を<br>に統一
my ($ss)=(@_);
$ss =~ s/\x0D\x0A/<br>/g;
$ss =~ s/\t//g;
$ss =~ s/\n/<br \/>/g;
return $ss;
}
sub crlfreset0 {		#改行を削除
my ($ss)=(@_);
$ss =~ s/\x0D\x0A//g;
$ss =~ tr/\x0D\x0A//;
$ss =~ s/\t//g;
$ss =~ s/\n//g;
return $ss;
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramset {
my ($str) = (@_);
my $temp = &crlfreset($paramhash{$str});
utf8::decode($temp);
return ($temp);
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramset2 {
my ($str) = (@_);
my $temp = &crlfreset2($paramhash{$str});
utf8::decode($temp);
return ($temp);
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramsetsql {
my ($str,$REF) = (@_);
my $temp;
if($REF ne ""){
$temp = &crlfreset($REF->{$str});
}else{
$temp = &crlfreset($REFHASH->{$str});
}	#if
utf8::decode($temp);
return ($temp);
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramsetsql0 {
my ($str,$REF) = (@_);
my $temp;
if($REF ne ""){
$temp = &crlfreset0($REF->{$str});
}else{
$temp = &crlfreset0($REFHASH->{$str});
}	#if
utf8::decode($temp);
return ($temp);
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramsetsql2 {
my ($str,$REF) = (@_);
my $temp;
if($REF ne ""){
$temp = &crlfreset2($REF->{$str});
}else{
$temp = &crlfreset2($REFHASH->{$str});
}	#if
utf8::decode($temp);
return ($temp);
}
# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット
# -----------------------------------------------------------------
sub paramsetsql3 {
my $temp;
my ($str,$REF) = (@_);
if($REF ne ""){
$temp = $REF->{$str};
}else{
$temp = $REFHASH->{$str};
}	#if
$temp = &urllink($temp);
utf8::decode($temp);
&crlfreset2($temp);
return ($temp);
}

#----------------------------------------------#
#■数字を三桁ずつカンマで区切る
#----------------------------------------------#
sub ketakanma{
my ($num) = (@_);
while($num =~ s/(.*\d)(\d\d\d)/$1,$2/){} ;
return($num);
}	#sub

# -----------------------------------------------------------------
# パラメータの取得及びutfフラグセット及びエンコード
# -----------------------------------------------------------------
sub paramsetsqlenc {
my ($str,$REF) = (@_);
my $temp;
if($REF ne ""){
$temp = &crlfreset($REF->{$str});
}else{
$temp = &crlfreset($REFHASH->{$str});
}	#if
$temp =~ s/([^￥w])/'%'.unpack("H2", $1)/ego;
$temp =~ tr/ /+/;
utf8::decode($temp);
return ($temp);
}

# -----------------------------------------------------------------
# 文中のアドレスにリンクを貼る
# -----------------------------------------------------------------
sub urllink {
my ($str) = (@_);
$str =~ s/<br>/\n/g;
$str =~ s/</&lt;/g;
$str =~ s/>/&gt;/g;

# $str の中の URI(URL) にリンクを張った $result を作る
# $tag_regex と $tag_regex_ は別途参照
# $http_URL_regex と $ftp_URL_regex および $mail_regex は別途参照

$tag_regex_ = q{[^"'<>]*(?:"[^"]*"[^"'<>]*|'[^']*'[^"'<>]*)*(?:>|(?=<)|$(?!\n))}; #'}}}}
$text_regex = q{[^<]*};

$http_URL_regex =
q{\b(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f} .
q{][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)} .
q{*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.} .
q{[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]} .
q{[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-} .
q{Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f} .
q{])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)} .
q{*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])} .
q{*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*} .
q{)?};

$ftp_URL_regex =
q{\bftp://(?:(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*} .
q{(?::(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?} .
q{:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z](?:[-a-zA-} .
q{Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)?} .
q{(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?} .
q{:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(?:;type=[} .
q{AIDaid])?)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9} .
q{A-Fa-f])*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A} .
q{-Fa-f])*)?};

$mail_regex =
q{(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\} .
q{\[\]\000-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][} .
q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x} .
q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff])|"[^\\\\\x80-} .
q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(} .
q{\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0} .
q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*} .
q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,} .
q{;:".\\\\\[\]\000-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[} .
q{^\x80-\xff])*\]))*};

$result = '';  $skip = 0;
while ($str =~ /($text_regex)($tag_regex)?/gso) {
  last if $1 eq '' and $2 eq '';
  $text_tmp = $1;
  $tag_tmp = $2;
  if ($skip) {
    $result .= $text_tmp . $tag_tmp;
    $skip = 0 if $tag_tmp =~ /^<\/[aA](?![0-9A-Za-z])/;
  } else {
    $text_tmp =~ s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
      {my($org, $mail) = ($1, $2);
       (my $tmp = $org) =~ s/"/&quot;/g;	#"
       '<A target=_blank HREF="' . ($mail ne '' ? 'mailto:' : '') . "$tmp\">$org</A>"}ego;		#"
    $result .= $text_tmp . $tag_tmp;
    $skip = 1 if $tag_tmp =~ /^<[aA](?![0-9A-Za-z])/;
    if ($tag_tmp =~ /^<(XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z])/i) {
      $str =~ /(.*?(?:<\/$1(?![0-9A-Za-z])$tag_regex_|$))/gsi;
      $result .= $1;
    }
  }
}

$result =~ s/\x0D\x0A/<BR>/g;
$result =~ s/\x0D/<BR>/g;
$result =~ s/\x0A/<BR>/g;

$result =~ s/&lt;/</g;
$result =~ s/&gt;/>/g;

return $result;
}	#sub

# -----------------------------------------------------------------
# 権限エラーの表示
# -----------------------------------------------------------------
sub kengen_error {
my ($str,$flag) = (@_);
if($flag ne ""){
print "Content-type: text/html;\n\n";
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="0;URL=/mema/system/$cgifile?code=kengenerror">
<title>$sitetitle</title>
<link href="style.css" rel="stylesheet" type="text/css">
<style type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
</body>
</html>
END_HTML
exit;
}	#if
#
print "Set-Cookie: ".$cookiename."=; expires=Thu, 1-Jan-1970 00:00:00 GMT;\n";
print "Content-type: text/html;\n\n";
$loginuser = &getcook($cookiename);
$fcsession = &getcook($cookiename_session);
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle システムエラー</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p><font color=red><b>$str</b></font></p>
<p>再度ログインして下さい。<p>
<form name="login" method="post" action="$cgifile" >
<input name=code value="login" type=hidden>
<table border=0 bgcolor="#c0e2c4" width=200>
<tr bgcolor="#59e156"><td colspan=2>ログインをお願いします</td></tr>
<tr><td>ID</td><td><input name="id" type="text" size="16"></td></tr>
<tr><td>Password</td><td><input name="psw" type="password" size="16"></td></tr>
<tr><td colspan=2 align=center><input type=submit value=ログイン style="width:70px"></td></tr>
</table>
</fotm>

</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
exit;
}	#sub




# -----------------------------------------------------------------
# 新規フォーム
# -----------------------------------------------------------------
sub newform {
$code = $paramhash{'code'};
$contents = $paramhash{'contents'};
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
if(3 <= $contents && $contents <= 43 ){
$taikainamestr = "■大会名：$taikainame";
}
$category = $paramhash{'category'};
if($category ne ""){$sql_category = " and category = '$category'";}
$area = $paramhash{'area'};
if($area ne ""){$sql_area = " and area = '$area'";}
$kumi = $paramhash{'kumi'};
if($kumi ne ""){$sql_kumi = " and kumi = '$kumi'";}
#
$sql_str = "SELECT MAX(sortnum) as sortnum FROM $dbname WHERE contents = '$contents' and koukaiflag != 9 and taikaicode = '$taikaicode' $sql_category $sql_area $sql_kumi";
#print "$sql_str";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
$REFHASH = $rs->fetchrow_hashref;
$sortnum = $REFHASH->{'sortnum'} + 1;
#
$year_pass = $year - 1;
$year_future = $year + 1;
$nichiji1 = "<select name=syear>\n";
$nichiji1 .= "<option value=$year_pass>$year_pass</option>\n";
$nichiji1 .= "<option value=$year selected>$year</option>\n";
$nichiji1 .= "<option value=$year_future>$year_future</option>\n";
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth>\n";
$nichiji1 .= &makeselect(1,12,$month);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday>\n";
$nichiji1 .= &makeselect(1,31,$mday);
$nichiji1 .= "</select>日\n";

#日付from
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_from'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_from = "<select name=fyear>\n";
$nichiji_from .= &makeselect($y-1,$year+1,$y);
$nichiji_from .= "</select>年\n";
$nichiji_from .= "<select name=fmonth>\n";
$nichiji_from .= &makeselect(1,12,$m);
$nichiji_from .= "</select>月\n";
$nichiji_from .= "<select name=fday>\n";
$nichiji_from .= &makeselect(1,31,$d);
$nichiji_from .= "</select>日\n";

#日付to
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_to'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_to = "<select name=eyear>\n";
$nichiji_to .= &makeselect($y-1,$year+1,$y);
$nichiji_to .= "</select>年\n";
$nichiji_to .= "<select name=emonth>\n";
$nichiji_to .= &makeselect(1,12,$m);
$nichiji_to .= "</select>月\n";
$nichiji_to .= "<select name=eday>\n";
$nichiji_to .= &makeselect(1,31,$d);
$nichiji_to .= "</select>日\n";


#大会名のGET
if($contents == 30 || $contents == 31 || $contents == 32){
=pot
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 and serial = '$taikaicode' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$taikainame = &paramsetsql('title');
}else{
$taikainame = "（大会名：取得エラー）";
}	#if
=cut
}	#if c=30

#エリア名のGET
if($contents == 30 || $contents == 31 || $contents == 32){
$sql_str = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag != 9 and serial = '$area' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$areaname = &paramsetsql('title');
}else{
$areaname = "（地区名：取得エラー）";
}	#if
}	#if c=30

#組名のGET
if($contents == 30 || $contents == 31 || $contents == 32){
$sql_str = "SELECT * FROM $dbname WHERE contents = 31 and koukaiflag != 9 and serial = '$kumi' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$kuminame = &paramsetsql('title');
}else{
$kuminame = "（組名：取得エラー）";
}	#if
}	#if c=30


$data = &vsdataset($taikaicode,$category,$area,$kumi,$REFHASH);

# エントリーしていて、なおかつ入金済みのチームのみ列挙
if($contents == 32 ){
#チームリストの作成
%KITEAM = ();
#http://pridejapan.net/system/webpal.cgi?code=newform&contents=32&taikaicode=1&category=1&area=22&kumi=25
#既登録チームの一覧GET：他の組も合わせて
$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area'  ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count22 = $rs1->rows;	# Hit件数を確保
for($k = 0;$k < $count22;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$KITEAM{&paramsetsql('teamnum',$REFHASH1)} = "disabled";
}	#for
#http://pridejapan.net/system/webpal.cgi?code=newform&contents=32&taikaicode=1&category=1&area=22&kumi=25
#既登録チームの一覧GET
$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count2 = $rs1->rows;	# Hit件数を確保
#print "count2=$count2";
for($k = 0;$k < $count2;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$KITEAM{&paramsetsql('teamnum',$REFHASH1)} = "disabled";
}	#for

$teamlist =<<"END_HTML";
<select name="teamnum" id="teamnum">
<option value=''>選択してください</option>
END_HTML
$sql_str1 = "SELECT * FROM entrylist WHERE taikaicode = '$taikaicode' and category = '$category' and payment = 1 ORDER BY lastupdated DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
for($i = 0;$i < $count1;$i++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$teamserial = &paramsetsql('teamnum',$REFHASH1);
($teamname,$teamsession) = &taikaiteamname_get3($teamserial);
if($teamname eq ""){next;}
#if( $TSS{$teamserial} == 1){$flag = "disabled";}else{$flag = "";}
$teamlist .=<<"END_HTML";
<option value='$teamserial' $KITEAM{$teamserial} >$teamname</option>
END_HTML
}	#for
$teamlist .=<<"END_HTML";
</select>
END_HTML
}	#if

#試合予定一覧の枠
@RESULTSTR = split(/<>/,&paramsetsql('resultstr'));
@RESULTSTR2 = split(/<>/,&paramsetsql('resultstr2'));
@RESULT0 = split(/<>/,&paramsetsql('result0'));
@RESULT1 = split(/<>/,&paramsetsql('result1'));
@SENPYO = split(/<>/,&paramsetsql('senpyo'));
foreach $i(0..19){
$n = $i+1;
$wakulist .=<<"END_HTML";
<tr>
<td align="center" bgcolor="#FFFFFF">$n</td>
<td align="center" bgcolor="#FFFFFF"><input name="resultstr_$i" type="text" id="resultstr_$i" value="$RESULTSTR[$i]" size="20" />
vs
<input name="resultstr2_$i" type="text" id="resultstr2_$i" value="$RESULTSTR2[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="result0_$i" type="text" id="result0_$i" value="$RESULT0[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="result1_$i" type="text" id="result1_$i" value="$RESULT1[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="senpyo$i" type="text" id="senpyo$i" value="$SENPYO[$i]" size="20" /></td>
</tr>
END_HTML
}	#foreach

#
if($contents eq ""){print "contents error by newform.";exit;}
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"template/$FORMFILE[$contents]";
@TEMPLATE = <IN>;
close IN;
#
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%code\%/formadd/;
$line =~ s/\%contents\%/$contents/;
$line =~ s/\%koukaiflag0\%/checked/;
$line =~ s/\%sortnum\%/$sortnum/;
$line =~ s/\%taikaicode\%/$taikaicode/;
$line =~ s/\%title\%/$title/;
$line =~ s/\%text1\%/$text1/;
$line =~ s/\%nichiji\%/$nichiji1/;
$line =~ s/\%body\%/$body/;
$line =~ s/\%linkadrtitle\%/$linkadrtitle/;
$line =~ s/\%linkadr\%/$linkadr/;
$line =~ s/\%filename0\%/$filename0/;
$line =~ s/\%price\%/$price/;
$line =~ s/\%taikainame\%/$taikainame/;
$line =~ s/\%category\%/$category/;
$line =~ s/\%area\%/$area/;
$line =~ s/\%areaname\%/$areaname/;
$line =~ s/\%kumi\%/$kumi/;
$line =~ s/\%kuminame\%/$kuminame/;
$line =~ s/\%teamlist\%/$teamlist/;
$line =~ s/\%data\%/$data/;
$line =~ s/\%nichiji_from\%/$nichiji_from/;
$line =~ s/\%nichiji_to\%/$nichiji_to/;
$line =~ s/\%wakulist\%/$wakulist/;


#残り全て空白に
$line =~ s/\%(.*)\%//g;
$str .= $line;
}
#チーム数限度：８
if($count2 >= 8){
$str =<<"END_HTML";
<p style="color:red;">
既に8チームが登録されております。
</p>
<input type=button onclick="javascript:history.back();" value="戻る" />
END_HTML
}	#if
###
print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
■【$CONTENTSNAME[$contents]】 登録フォーム<br>
$taikainamestr
$str
</td>
</tr>
</table>
$footer
END_HTML

}


# -----------------------------------------------------------------
# フォーム登録
# -----------------------------------------------------------------
sub formadd {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
$koukaiflag = $paramhash{'koukaiflag'};
$sortnum = $paramhash{'sortnum'};
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$genre1 = $paramhash{'genre1'};
$genre2 = $paramhash{'genre2'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
$teamnum = $paramhash{'teamnum'};
$title = $paramhash{'title'};
$text1 = $paramhash{'text1'};
$body = $paramhash{'body'};
$linkadrtitle = $paramhash{'linkadrtitle'};
$linkadr = $paramhash{'linkadr'};
$price1 = $paramhash{'price1'};
$price2 = $paramhash{'price2'};
$price3 = $paramhash{'price3'};
$comment = $paramhash{'comment'};
$nichiji1 = $paramhash{'nichiji1'};
$resultstr = $paramhash{'resultstr'};
$resultstr2 = $paramhash{'resultstr2'};
$result0 = $paramhash{'result0'};
$result1 = $paramhash{'result1'};
$maninonrei1 = $paramhash{'maninonrei1'} -0;
$maninonrei2 = $paramhash{'maninonrei2'} -0;
$bannercategory = $paramhash{'bannercategory'};

if($contents == 40){
$resultstr = "";
foreach $n(0..4){
$resultstr .= $paramhash{'result'.$n}.":";
}	#foreach
}	#if


if($contents == 0 || $contents == 7){
$nichiji1 = sprintf("%04d-%02d-%02d",$paramhash{'syear'},$paramhash{'smonth'},$paramhash{'sday'});
	if(!Date::Simple->new($nichiji1)){
		&error("日付にエラーがあります。「$nichiji1」");
	}		#if
}		#if



#######################
# VS登録の重複チェック
if($contents == 33 && $serial eq ""){
$sql_str = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
if($count !=0 ){&error("VS登録の重複があります。");}	#if
}	#if

#######################
#対戦組み合わせ：リーグ
if($contents == 33 && $category == 1){
$count1 = $paramhash{'count'};
$temp = int($count1 / 2);
foreach $setu(1..7){
foreach $num(1..4){
$title .= "team1:$setu.$num.".&paramset("team1:$setu.$num")."|";
$title .= "team2:$setu.$num.".&paramset("team2:$setu.$num")."<>";
}	#foreach num
#日時チェック
$nichiji1 = sprintf("%04d-%02d-%02d",$paramhash{"syear:$setu"},$paramhash{"smonth:$setu"},$paramhash{"sday:$setu"});
$nichiji2 = sprintf("%04d-%02d-%02d",$paramhash{"eyear:$setu"},$paramhash{"emonth:$setu"},$paramhash{"eday:$setu"});
if(!Date::Simple->new($nichiji1)){&error("日付にエラーがあります。「第${setu}節　$nichiji1」");}	#if
if(!Date::Simple->new($nichiji2)){&error("日付にエラーがあります。「第${setu}節　$nichiji2」");}	#if
$body .= "$setu:$nichiji1:$nichiji2<>";
}	#foreach setu
}	#if 33

#######################
#対戦組み合わせ：トーナメント
if($contents == 33 && $category == 2){
$body = $paramhash{"teamnum0:1"}.":";
$text1 = "";
$nichiji1 = "";
$cnt = 2;
$scorenum = 0;
@SCORETEMP = $query->param('score');
foreach $y(1..7){
#日時チェック
$n1 = sprintf("%04d-%02d-%02d",$paramhash{"syear:$y"},$paramhash{"smonth:$y"},$paramhash{"sday:$y"});
if($n1 ne "0000-00-00"){
if(!Date::Simple->new($n1)){
	&error("日付にエラーがあります。「NO${y}　$n1」");
}		#if
}		#if
$n2 = sprintf("%04d-%02d-%02d",$paramhash{"eyear:$y"},$paramhash{"emonth:$y"},$paramhash{"eday:$y"});
if($n1 ne "0000-00-00"){
if(!Date::Simple->new($n2)){
	&error("日付にエラーがあります。「NO${y}　$n2」");
}		#if
}		#if
$nichiji1 .= "$n1:$n2<>";

foreach $x(1 .. $cnt){
#チーム
$body .= $paramhash{"teamnum$y:$x"}.":";
#スコア
$text1 .= $SCORETEMP[$scorenum++].":";
}	#foreach x
$cnt *= 2;
}	#foreach y
}	#if cc33



if($contents == 43){
$resultstr = "";
$resultstr2 = "";
$result0 = "";
$result1 = "";
$senpyo = "";
foreach $n(0..19){
$resultstr .= $paramhash{'resultstr_'.$n}."<>";
$resultstr2 .= $paramhash{'resultstr2_'.$n}."<>";
$result0 .= $paramhash{'result0_'.$n}."<>";
$result1 .= $paramhash{'result1_'.$n}."<>";
$senpyo .= $paramhash{'senpyo'.$n}."<>";
}	#foreach
}	#if



# --------------------------
# 添付ファイルの登録処理
$upfilename = "";
$caption = "";
foreach $i(0..$gazoulimitnum){
if($paramhash{"file$i"} ne ""){$file = &fileup("file$i",$contents);}else{$file = $paramhash{"filename$i"};}
if($paramhash{"filedelete$i"} == 1){$file = "";}
$upfilename .= $file.":";
#キャプション
$caption .= $paramhash{"caption$i"}."<>";
}	#foreach


#DB
if($serial eq ""){
# 新規登録
$sql_str = qq{INSERT INTO $dbname(contents,koukaiflag,sortnum,taikaicode,title,text1,nichiji1,body,linkadrtitle,linkadr,upfilename,price1,price2,price3,area,kumi,teamnum,nichiji_from,nichiji_to,comment,resultstr,resultstr2,result0,result1,caption,senpyo,category,genre1,genre2,bannercategory,maninonrei1,maninonrei2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$contents,
$koukaiflag,
$sortnum,
$taikaicode,
$title,
$text1,
$nichiji1,
$body,
$linkadrtitle,
$linkadr,
$upfilename,
$price1,
$price2,
$price3,
$area,
$kumi,
$teamnum,
$nichiji1,
$nichiji2,
$comment,
$resultstr,
$resultstr2,
$result0,
$result1,
$caption,
$senpyo,
$category,
$genre1,
$genre2,
$bannercategory,
$maninonrei1,
$maninonrei2,
);
}else{
#変更
$title =~ s/\'/\'\'/gm;	#'
$text1 =~ s/\'/\'\'/gm;	#'
$nichiji1 =~ s/\'/\'\'/gm;	#'
$body =~ s/\'/\'\'/gm;	#'
$linkadrtitle =~ s/\'/\'\'/gm;	#'
$linkadr =~ s/\'/\'\'/gm;	#'
$upfilename =~ s/\'/\'\'/gm;	#'
$price1 =~ s/\'/\'\'/gm;	#'
$price2 =~ s/\'/\'\'/gm;	#'
$price3 =~ s/\'/\'\'/gm;	#'
$comment =~ s/\'/\'\'/gm;	#'
$resultstr =~ s/\'/\'\'/gm;	#'
$resultstr2 =~ s/\'/\'\'/gm;	#'
$result0 =~ s/\'/\'\'/gm;	#'
$result1 =~ s/\'/\'\'/gm;	#'
$caption =~ s/\'/\'\'/gm;	#'
$senpyo =~ s/\'/\'\'/gm;	#'


$str = "";
$str.="sortnum = '$sortnum',";
$str.="taikaicode = '$taikaicode',";
$str.="category = '$category',";
$str.="title = '$title',";
$str.="text1 = '$text1',";
if($nichiji1 ne""){$str.="nichiji1 = '$nichiji1',";}
$str.="body = '$body',";
$str.="linkadrtitle = '$linkadrtitle',";
$str.="linkadr = '$linkadr',";
$str.="upfilename = '$upfilename',";
$str.="price1 = '$price1',";
$str.="price2 = '$price2',";
$str.="price3 = '$price3',";
$str.="area = '$area',";
$str.="kumi = '$kumi',";
$str.="teamnum = '$teamnum',";
$str.="nichiji_from = '$nichiji1',";
$str.="nichiji_to = '$nichiji2',";
$str.="comment = '$comment',";
$str.="resultstr = '$resultstr',";
$str.="resultstr2 = '$resultstr2',";
$str.="result0 = '$result0',";
$str.="result1 = '$result1',";
$str.="caption = '$caption',";
$str.="senpyo = '$senpyo',";
$str.="genre1 = '$genre1',";
$str.="genre2 = '$genre2',";
$str.="bannercategory = '$bannercategory',";
$str.="maninonrei1 = '$maninonrei1',";
$str.="maninonrei2 = '$maninonrei2',";
chop $str;
#
$sql_str = "UPDATE $dbname SET koukaiflag = \'$koukaiflag\',contents = \'$contents\',$str WHERE serial = $serial";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}	#if
&sqlcheck($sql_str);


#コンテンツ別戻り先


if($contents == 32){$contents = 31;}
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button  onClick="urljump('webpal.cgi?code=editlist&contents=$contents&taikaicode=$taikaicode&category=$category&area=$area&kumi=$kumi')">一覧に戻る</button></td>
<td><button onClick="urljump('webpal.cgi')">トップに戻る</button></td>
</tr>
</table>
END_HTML
#
if($contents == 0 || $contents == 30 || $contents == 38 || $contents == 39 || $contents == 40 || $contents == 43 ){
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('webpal.cgi')">トップに戻る</button></td>
</tr>
</table>
END_HTML
}	#if
#
if($contents == 33 ){
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('?code=editlist&contents=31&taikaicode=$taikaicode&category=$category&area=$area')">一覧に戻る</button></td>
</tr>
</table>
END_HTML
}	#if
#
if($contents == 45 || $contents == 31){
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('webpal.cgi')">トップに戻る</button></td>
</tr>
</table>
END_HTML
}	#if

if($contents == 37 || $contents == 43){
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td>
<button onClick="urljump('?code=editlist&contents=$contents&taikaicode=$taikaicode&category=$category')">　一覧に戻る　</button>
<button onClick="urljump('?code=newform&contents=$contents&taikaicode=$taikaicode&category=$category')">続けて登録する</button></td>
</tr>
<tr>
<td align=center><button onClick="urljump('webpal.cgi')">トップに戻る</button></td>
</tr>
</table>
END_HTML
}	#if




###
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
<!--
function urljump(url){
top.location.href=url;
}
-->
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" class="text-12">
<tr><td>
<center>
<p>登録が完了致しました。</p>
<br>
$backmes
</center>
</td>
</tr>
</table>
</td>
</tr>
</table>
$footer
END_HTML
}

# -----------------------------------------------------------------
# 編集リスト
# -----------------------------------------------------------------
sub editlist {
$contents = $paramhash{'contents'};
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
#
$taikainame = &taikainame_get($taikaicode,$category);
$taikainamestr = "■大会名：$taikainame<hr>";
if($contents == 0){$taikainamestr = "";}



###
print << "END_HTML";
$header
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に削除してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
function delete_allset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = true;
}	//for
}	// func
function delete_allreset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = false;
}	//for
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg
END_HTML
# -----------------------------------------------------------------
$allstr = <<"END_HTML";
<a href="javascript:void(0);" onclick="delete_allset()">□全部を選択</a>　
<a href="javascript:void(0);" onclick="delete_allreset()">□全部の選択を解除</a>　
<input type=submit value="変更/登録">　<font color=red size=-1>※一括削除と表示順位設定は一度に処理されます。</font>
END_HTML
#
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY nichiji1 DESC, sortnum DESC LIMIT 100";
#
if($contents == 0){	#大会登録
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap >登録年月日</td>
<td align=center nowrap >大会名</td>
<td align=center width=90% >大会イメージ画像（縮小版）</td>
</tr>
END_HTML
}	#if
if($contents == 7){	#大会記事作成
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY nichiji1 DESC, serial DESC LIMIT 10";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>一括削除</td>
<td align=center nowrap>公開</td>
<td align=center nowrap >公開年月日</td>
<td align=center nowrap >大会情報</td>
<td align=center width=90% >タイトル</td>
</tr>
END_HTML
}	#if
if($contents == 22){	#大会エントリー
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>一括削除</td>
<td align=center nowrap>公開</td>
<td align=center nowrap >登録年月日</td>
<td align=center nowrap >どの予選の何節目か</td>
<td align=center width=90% >エントリーした大会</td>
</tr>
END_HTML
}	#if
if($contents == 30){	#大会：エリア一覧
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY sortnum ASC, sortnum DESC ";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap width=90%>地区名</td>
<td align=center nowrap>「組」操作</td>
</tr>
END_HTML
}	#if

if($contents == 31 ){	#大会：チーム一覧
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and koukaiflag != 9 and taikaicode = '$taikaicode' and area = '$area' ORDER BY sortnum ASC, sortnum DESC ";
$taikainamestr .= "<br>地区名：".&taikaiareaname_get($area);
$taikainamestr .=<< "END_HTML";
<br>
<input type=button value="「組」の新規登録" onClick="urljump(\'$cgifile?code=newform&contents=31&area=$area&taikaicode=$taikaicode&category=$category\')">
<br>
<font color=red size=-1>※チームが登録されている場合は「組」の削除は行えません。</font>
<br>
<br>
END_HTML
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap width=90%>「組」名称</td>
<td align=center nowrap>「チーム」操作</td>
<td align=center nowrap>「対戦組み合わせ」操作</td>
</tr>
END_HTML
}	#if

if($contents == 36){	#大会イメージ
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum DESC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap width=90%>タイトル</td>
</tr>
END_HTML
}	#if

if($contents == 37){	#大会：ブロック
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>ブロック名</td>
<td align=center nowrap>内容</td>
</tr>
END_HTML
}	#if

if($contents == 40){	#大会：ブロック
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>名称</td>
<td align=center nowrap>内容</td>
</tr>
END_HTML
}	#if

if($contents == 41){	#大会：勝ち点
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>名称</td>
<td align=center nowrap>内容</td>
</tr>
END_HTML
}	#if

if($contents == 42){	#大会：トーナメント画像
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>タイトル</td>
<td align=center nowrap>画像</td>
</tr>
END_HTML
}	#if

if($contents == 43){	#
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and taikaicode = $taikaicode and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>タイトル</td>
<td align=center nowrap>節</td>
<td align=center nowrap>組</td>
</tr>
END_HTML
}	#if

if($contents == 44){	#
$sql_str = "SELECT * FROM $dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY sortnum ASC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>タイトル</td>
</tr>
END_HTML
}	#if



#
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
#
print << "END_HTML";
<form action="webpal.cgi" method="post" enctype="multipart/form-data" name="form1" id="form1" onSubmit="return delete_kakunin()" >
<input name="code" type="hidden" id="code" value="deleteset" />
<input name="contents" type="hidden" id="contents" value="$contents" />
<input name="taikaicode" type="hidden" id="taikaicode" value="$taikaicode" />
<input name="category" type="hidden" id="contents" value="$category" />
<input name="area" type="hidden" id="area" value="$area" />
<input name="kumi" type="hidden" id="kumi" value="$kumi" />
■【$CONTENTSNAME[$contents]】  編集<br>
$taikainamestr
$allstr
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>
<table  border="0" cellpadding="1" cellspacing="1" class="text-12" width=100%>
$disp
END_HTML
#
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$koukaiflag = $REFHASH->{'koukaiflag'};
$contents = $REFHASH->{'contents'};
$sortnum = $REFHASH->{'sortnum'};
$title = &paramsetsql('title');
$body = &paramsetsql('body');
$text1 = &paramsetsql('text1');
$price = &ketakanma(&paramsetsql('price'));
$kumi = &paramsetsql('kumi');
$resultstr = &paramsetsql('resultstr');

#日時
$nichiji1 = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji1')));
#画像
@IMGSRC = ();
@IMGTEMPS = split(/:/,$REFHASH->{'upfilename'});
foreach $j(0..$gazoulimitnum){
utf8::decode($IMGTEMPS[$j]);
($sfn,$fn) = split(/<>/,$IMGTEMPS[$j]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
#$IMGSRC[$j] = "<img src=img/dat.gif><br>";
if( $TEMP[1] eq "jpg"){$IMGSRC[$j] = "<img src=file/$TEMP[0]top.$TEMP[1]><br>";}
if( $TEMP[1] eq "pdf"){$IMGSRC[$j] = "<img src=img/pdf.gif><br>";}
if( $TEMP[1] eq "doc"){$IMGSRC[$j] = "<img src=img/doc.gif><br>";}
if( $TEMP[1] eq "xls"){$IMGSRC[$j] = "<img src=img/xls.gif><br>";}
if( $TEMP[1] eq "dat"){$IMGSRC[$j] = "<img src=img/dat.gif><br>";}
$FILENAME[$j] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$j] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach


#
if($contents == 0){	#大会登録
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents\')">
</td>
<td class="tdpad" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$nichiji1 </td>
<td class="tdpad" nowrap >$title </td>
<td class="tdpad" nowrap >$IMGSRC[$j] </td>
</tr>
END_HTML
}	#if
if($contents == 7){	#大会記事作成
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents\')">
</td>
<td align=center ><input type=checkbox name="deleteset" id="deleteset" value="$serial"></td>
<td class="tdpad" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad" nowrap >$nichiji1 </td>
<td class="tdpad" nowrap >$text1 </td>
<td class="tdpad" nowrap >$title </td>
</tr>
END_HTML
}	#if

if($contents == 30){	#大会：エリア
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
</tr>
END_HTML
}	#if



##############################
# 【組】 編集
if($contents == 31){	#大会：組
#リーグかトーナメントか
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 and serial = '$taikaicode' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
$REFHASH1 = $rs1->fetchrow_hashref;

#
if($category == 1){	#リーグ
#「チーム」一覧
$teamlist = "";
$sql_str1 = "SELECT p.serial as serial,m.teamname as teamname FROM pridejapan as p,member_tbl as m WHERE p.contents = 32 and p.koukaiflag != 9 and p.taikaicode = '$taikaicode' and p.category = 1 and p.area = '$area' and kumi = '$serial' and p.teamnum = m.serial ORDER BY p.sortnum ASC, p.serial DESC ";
#$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag != 9 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$serial' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
&sqlcheck($sql_str);
$teamlist = "";
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH1);
$teamname = &paramsetsql('teamname',$REFHASH1);
$teamlist .=<<"END_HTML";
<tr>
<td style="border-bottom:solid #aaaaaa 1px;" nowrap>$teamname</td>
<td style="border-bottom:solid #aaaaaa 1px;"><input type=button onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&contents=32&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial&serial=$tss\')" value="登録の解除" /></td>
</tr>
END_HTML
}	#for
#
$deldisabled = "";
# 組に登録されたチームをGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$serial' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
if($count1 != 0){$deldisabled = "disabled";}
@TSS = ();
%TNAME = ();
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH1);
push(@TSS,$teamnum );
$TNAME{$teamnum} = &taikaiteamname_get($teamnum);
}	#for
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1 and area = '$area' and kumi = '$serial' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
$REFHASH1 = $rs1->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH1);
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.2|team2:1.1.2<>.....
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.2  team2:1.2.2
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.2
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.2
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 2
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 2
$RDATA1{$setu}{$num} = $tss1;
$RDATA2{$setu}{$num} = $tss2;
}	#foreach
$ndata = &paramsetsql('body',$REFHASH1);
foreach $n(split(/<>/,$ndata)){	#setu:n1:n2
($st,$n1,$n2) = split(/:/,$n);
if($n1 ne "0000-00-00"){$NN{$st} = 1;}
}	#foreach
$teamcount = @TSS;
# >>試合結果
$vslist = "";
foreach $setu(1..7){
if($NN{$setu} != 1){next;}
$vslist .=<<"END_HTML";
<style>
.tdline {
	border:solid #aaaaaa 1px;
	}
</style>
<strong>【第${setu}節】</strong>
END_HTML
#得点表
$half = int($teamcount/2);
foreach $num(1..4){
$tname1 = $TNAME{$RDATA1{$setu}{$num}};
if($tname1 eq ""){$tname1 = "<span style='color:red;'>（未定）</span>";}
$tname2 = $TNAME{$RDATA2{$setu}{$num}};
if($tname2 eq ""){$tname2 = "<span style='color:red;'>（未定）</span>";}
$tokuten1 = $TOKUTEN1{$setu}{$num}{$RDATA1{$setu}{$num}};
$tokuten2 = $TOKUTEN2{$setu}{$num}{$RDATA2{$setu}{$num}};
if($tokuten1 == $tokuten2){$marubatu1 = "-";$marubatu2 = "-";}
if($tokuten1 > $tokuten2){$marubatu1 = "○";$marubatu2 = "×";}
if($tokuten1 < $tokuten2){$marubatu1 = "×";$marubatu2 = "○";}
$vslist .=<<"END_HTML";
<table class="text-12 tdline"  >
<tr><td nowrap width=50%>$tname1</td><td nowrap> <strong>vs</strong> </td><td nowrap width=50% >$tname2</td></tr>
</table>
END_HTML
}	#foreach 
$vslist .=<<"END_HTML";
END_HTML
}	#foreach setu
#
if($serial != $kumi_keep && $i != 0 ){print $disp;$kumi_keep = $serial;}
#
print << "END_HTML";
<tr bgcolor="white">
<td nowrap class="tdpad2">
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode&category=$category&area=$area\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode&area=$area&category=$category\')" $deldisabled >
</td>
<td class="tdpad2" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad2"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad2" nowrap >$title </td>
<td nowrap valign=top >
<table class="text-12">
$teamlist
</table>
<hr>
<input type=button value="「チーム」の登録" onClick="urljump(\'$cgifile?code=newform&contents=32&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial\')"><br>
</td>
<td class="tdpad2" valign=top align=center>
$vslist
<hr>
<input type=button value="vs登録/編集" onClick="urljump(\'$cgifile?code=editform&contents=33&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial&sortnum=$sortnum\')"><br>
</td>
</tr>
END_HTML
}	#リーグ
############### トーナメント
if($category == 2){	#トーナメント
#「チーム」一覧
$teamlist = "";
$sql_str1 = "SELECT p.serial as serial,m.teamname as teamname FROM pridejapan as p,member_tbl as m WHERE p.contents = 32 and p.koukaiflag != 9 and p.taikaicode = '$taikaicode' and p.category = '$category' and p.area = '$area' and kumi = '$serial' and p.teamnum = m.serial ORDER BY p.sortnum ASC, p.serial DESC ";
#$sql_str1 = "SELECT * FROM pridejapan WHERE contents = 32 and koukaiflag != 9 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$serial' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
&sqlcheck($sql_str);
$teamlist = "";
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$tss = &paramsetsql('serial',$REFHASH1);
$teamname = &paramsetsql('teamname',$REFHASH1);
$teamlist .=<<"END_HTML";
<tr>
<td style="border-bottom:solid #aaaaaa 1px;" nowrap>$teamname</td>
<td style="border-bottom:solid #aaaaaa 1px;"><input type=button onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&contents=32&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial&serial=$tss\')" value="登録の解除" /></td>
</tr>
END_HTML
}	#for
#
# 組に登録されたチームをGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$serial' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
for($k = 0;$k < $count1;$k++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH1);
push(@TSS,$teamnum );
$TNAME{$teamnum} = &taikaiteamname_get($teamnum);
}	#for
if($serial != $kumi_keep && $i != 0 ){print $disp;$kumi_keep = $serial;}
#
print << "END_HTML";
<tr bgcolor="white">
<td nowrap class="tdpad2">
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode&category=$category&area=$area\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode&area=$area&category=$category\')">
</td>
<td class="tdpad2" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad2"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad2" nowrap >$title </td>
<td nowrap valign=top >
<table class="text-12">
$teamlist
</table>
<hr>
<input type=button value="「チーム」の登録" onClick="urljump(\'$cgifile?code=newform&contents=32&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial\')"><br>
</td>
<td class="tdpad2" valign=top align=center>
<input type=button value="vs登録/編集" onClick="urljump(\'$cgifile?code=editform&contents=33&taikaicode=$taikaicode&category=$category&area=$area&kumi=$serial\')"><br>
<input type=button value="vs結果ページ" onClick="urljump('?code=ranking2&taikaicode=$taikaicode&area=$area&kumi=$serial&categorey=$category')"><br>
</td>
</tr>
END_HTML
}	#トーナメント
}	#if





##############################
if($contents == 36){	#大会イメージ
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
</tr>
END_HTML
}	#if

if($contents == 37){	#大会：ブロック
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad" nowrap >$KOUKAIFLAG[$koukaiflag] </td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
<td class="tdpad" width=90% >$body </td>
</tr>
END_HTML
}	#if

if($contents == 40){	#大会：勝ち点
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
<td class="tdpad" width=90% >${resultstr}点 </td>
</tr>
END_HTML
}	#if

if($contents == 41){	#大会：ルール
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
<td class="tdpad" width=90% >$body </td>
</tr>
END_HTML
}	#if

if($contents == 42){	#大会：トーナメント画像
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$title </td>
<td class="tdpad" width=90% >$IMGSRC[0] </td>
</tr>
END_HTML
}	#if

if($contents == 43){	#
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" width=90% >$title </td>
<td class="tdpad" nowrap >$text1 </td>
<td class="tdpad" nowrap >$body </td>
</tr>
END_HTML
}	#if

if($contents == 44){	#
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=$contents&taikaicode=$taikaicode\')">
</td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" width=90% >$title </td>
</tr>
END_HTML
}	#if






}	#for loop
print << "END_HTML";
</table>
</td>
</tr>
</table>
</form>

END_HTML
print $footer;
}


# -----------------------------------------------------------------
# 編集フォーム
# -----------------------------------------------------------------
sub editform {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$taikainame = &taikainame_get($taikaicode,$category);
$taikainamestr = "<br>■大会名：$taikainame";
if($contents == 0){$taikainamestr = "";}
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
$sortnum = $paramhash{'sortnum'};
if($serial eq ""){
$sql_str = "SELECT * FROM $dbname WHERE contents = $contents and taikaicode = '$taikaicode'";
}else{
$sql_str = "SELECT * FROM $dbname WHERE serial = $serial ";
}	#if
#
if($contents == 33){
$sql_str = "SELECT * FROM $dbname WHERE contents = 33 and taikaicode = '$taikaicode' and category = '$category' and area = '$area' and kumi = '$kumi' ";
}	#if

#
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#if($count != 1){print "error.";exit;}
$REFHASH = $rs->fetchrow_hashref;
$title = &paramsetsql('title');
$serial = $REFHASH->{'serial'};
$KFLAG[$REFHASH->{'koukaiflag'}-0] = " checked ";
if($sortnum eq ""){$sortnum = &paramsetsql('sortnum');}
if($taikaicode eq ""){$taikaicode = &paramsetsql('taikaicode');}
$text1 = &paramsetsql('text1');
$body = &paramsetsql('body');
$linkadrtitle = &paramsetsql('linkadrtitle');
$linkadr = &paramsetsql('linkadr');
if($category eq ""){$category = &paramsetsql('category');}
$CATEFLAG{$category} = "checked=checked";
if($category == 3){$CATEFLAG{1}=$CATEFLAG{2}="disabled";}
$genre1 = &paramsetsql('genre1');
$genre2 = &paramsetsql('genre2');
$GENRE1FLAG{$genre1} = "checked=checked";
$GENRE2FLAG{$genre2} = "checked=checked";
$price1 = &paramsetsql('price1');
$price2 = &paramsetsql('price2');
$price3 = &paramsetsql('price3');
if($area eq ""){$area = &paramsetsql('area');}
$comment = &paramsetsql('comment');
#$taikainame = &taikainame_get($taikaicode);
$areaname = &taikaiareaname_get($area);
$resultstr = &paramsetsql('resultstr');
$resultstr2 = &paramsetsql('resultstr2');
$result0 = &paramsetsql('result0');
$result1 = &paramsetsql('result1');
if(&paramsetsql('maninonrei1') == 1){$maninonrei1flag = "checked=checked";}
if(&paramsetsql('maninonrei2') == 1){$maninonrei2flag = "checked=checked";}
@CAPTION = split(/<>/,&paramsetsql('caption'));

#勝ち点リスト
@TEMP = split(/:/,$resultstr);
for($k=0;$k<5;$k++){
$temp ="";
for($n=10;$n>=-5;$n--){
if($n == $TEMP[$k]){$flag="selected";}else{$flag="";}
$temp .="<option value='$n' $flag>$n</option>\n";
}	#for
$KACHITENLIST[$k] =<<"END_HTML";
<select name="result$k" id="result$k">
$temp
</select>
END_HTML
}	#foreach

#画像
@IMGSRC = ();
@IMGTEMPS = split(/:/,$REFHASH->{'upfilename'});
foreach $i(0..$gazoulimitnum){
utf8::decode($IMGTEMPS[$i]);
($sfn,$fn) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
#$IMGSRC[$i] = "<img src=img/dat.gif><br>";
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=file/$TEMP[0]pda.$TEMP[1]><br>";}
if( $TEMP[1] eq "pdf"){$IMGSRC[$i] = "<img src=img/pdf.gif><br>";}
if( $TEMP[1] eq "doc"){$IMGSRC[$i] = "<img src=img/doc.gif><br>";}
if( $TEMP[1] eq "xls"){$IMGSRC[$i] = "<img src=img/xls.gif><br>";}
if( $TEMP[1] eq "dat"){$IMGSRC[$i] = "<img src=img/dat.gif><br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
#
#日付
($y,$m,$d) = split(/-/,&paramsetsql('nichiji1'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji1 = "<select name=syear>\n";
$nichiji1 .= &makeselect($y-1,$year+1,$y);
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth>\n";
$nichiji1 .= &makeselect(1,12,$m);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday>\n";
$nichiji1 .= &makeselect(1,31,$d);
$nichiji1 .= "</select>日\n";

#日付from
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_from'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_from = "<select name=fyear>\n";
$nichiji_from .= &makeselect($y-1,$year+1,$y);
$nichiji_from .= "</select>年\n";
$nichiji_from .= "<select name=fmonth>\n";
$nichiji_from .= &makeselect(1,12,$m);
$nichiji_from .= "</select>月\n";
$nichiji_from .= "<select name=fday>\n";
$nichiji_from .= &makeselect(1,31,$d);
$nichiji_from .= "</select>日\n";

#日付to
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_to'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_to = "<select name=eyear>\n";
$nichiji_to .= &makeselect($y-1,$year+1,$y);
$nichiji_to .= "</select>年\n";
$nichiji_to .= "<select name=emonth>\n";
$nichiji_to .= &makeselect(1,12,$m);
$nichiji_to .= "</select>月\n";
$nichiji_to .= "<select name=eday>\n";
$nichiji_to .= &makeselect(1,31,$d);
$nichiji_to .= "</select>日\n";

#リーグ戦VS表
$data = &vsdataset($taikaicode,$category,$area,$kumi,$title,$REFHASH);



#チームリストの作成
if($contents == 32 ){
$teamlist =<<"END_HTML";
<select name="teamnum" id="teamnum">
<option value=''>選択してください</option>
END_HTML
$sql_str1 = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 ORDER BY serial ASC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
for($i = 0;$i < $count1;$i++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$teamserial = &paramsetsql('serial',$REFHASH1);
$teamname = &paramsetsql('teamname',$REFHASH1);
if( $TSS{$teamserial} == 1){$flag = "disabled";}else{$flag = "";}
$teamlist .=<<"END_HTML";
<option value='$teamserial' $flag>$teamname</option>
END_HTML
}	#for
$teamlist .=<<"END_HTML";
</select>
END_HTML
}	#if

#試合予定一覧の枠
@RESULTSTR = split(/<>/,&paramsetsql('resultstr'));
@RESULTSTR2 = split(/<>/,&paramsetsql('resultstr2'));
@RESULT0 = split(/<>/,&paramsetsql('result0'));
@RESULT1 = split(/<>/,&paramsetsql('result1'));
@SENPYO = split(/<>/,&paramsetsql('senpyo'));
foreach $i(0..19){
$n = $i+1;
$wakulist .=<<"END_HTML";
<tr>
<td align="center" bgcolor="#FFFFFF">$n</td>
<td align="center" bgcolor="#FFFFFF"><input name="resultstr_$i" type="text" id="resultstr_$i" value="$RESULTSTR[$i]" size="20" />
vs
<input name="resultstr2_$i" type="text" id="resultstr2_$i" value="$RESULTSTR2[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="result0_$i" type="text" id="result0_$i" value="$RESULT0[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="result1_$i" type="text" id="result1_$i" value="$RESULT1[$i]" size="20" /></td>
<td align="center" bgcolor="#FFFFFF"><input name="senpyo$i" type="text" id="senpyo$i" value="$SENPYO[$i]" size="20" /></td>
</tr>
END_HTML
}	#foreach

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
if($bannercategory == $sstemp){$flag = "selected";}else{$flag="";}
$temp .=<<"END_HTML";
<option value='$sstemp' $flag>$titletemp</option>
END_HTML
}	#for
$bannercategory =<<"HTML_END";
<select name="bannercategory">
<option value='0' >未選択</option>
$temp
</select>
HTML_END
#
if($contents == 33){
$kuminame = &taikaikuminame_get($kumi);
$taikaiinfo = "<br>「".$taikainame."」<br>「".$areaname."」<br>「".$kuminame."」";
}	#if
#
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"template/$FORMFILE[$contents]" or die "open error";
@TEMPLATE = <IN>;
close IN;
#
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%serial\%/$serial/;
$line =~ s/\%code\%/formadd/;
$line =~ s/\%koukaiflag0\%/$KFLAG[0]/;
$line =~ s/\%koukaiflag1\%/$KFLAG[1]/;
$line =~ s/\%contents\%/$contents/;
$line =~ s/\%sortnum\%/$sortnum/;
$line =~ s/\%taikaicode\%/$taikaicode/;
$line =~ s/\%taikainame\%/$taikainame/;
$line =~ s/\%category\%/$category/;
$line =~ s/\%category1flag\%/$CATEFLAG{1}/;
$line =~ s/\%category2flag\%/$CATEFLAG{2}/;
$line =~ s/\%category3flag\%/$CATEFLAG{3}/;
$line =~ s/\%genre11flag\%/$GENRE1FLAG{1}/;
$line =~ s/\%genre12flag\%/$GENRE1FLAG{2}/;
$line =~ s/\%genre21flag\%/$GENRE2FLAG{1}/;
$line =~ s/\%genre22flag\%/$GENRE2FLAG{2}/;
$line =~ s/\%area\%/$area/;
$line =~ s/\%areaname\%/$areaname/;
$line =~ s/\%title\%/$title/;
$line =~ s/\%text1\%/$text1/;
$line =~ s/\%nichiji\%/$nichiji1/;
$line =~ s/\%body\%/$body/;
$line =~ s/\%linkadrtitle\%/$linkadrtitle/;
$line =~ s/\%linkadr\%/$linkadr/;
$line =~ s/\%price1\%/$price1/;
$line =~ s/\%price2\%/$price2/;
$line =~ s/\%price3\%/$price3/;
$line =~ s/\%data\%/$data/;
$line =~ s/\%kumi\%/$kumi/;
$line =~ s/\%nichiji_from\%/$nichiji_from/;
$line =~ s/\%nichiji_to\%/$nichiji_to/;
$line =~ s/\%comment\%/$comment/;
$line =~ s/\%kachitenlist\%/$kachitenlist/;
$line =~ s/\%resultstr\%/$resultstr/;
$line =~ s/\%resultstr2\%/$resultstr2/;
$line =~ s/\%result0\%/$result0/;
$line =~ s/\%result1\%/$result1/;
$line =~ s/\%wakulist\%/$wakulist/;
$line =~ s/\%bannercategory\%/$bannercategory/;
$line =~ s/\%maninonrei1flag\%/$maninonrei1flag/;
$line =~ s/\%maninonrei2flag\%/$maninonrei2flag/;

foreach $i(0..11){
$line =~ s/\%katitenlist$i\%/$KACHITENLIST[$i]/;
}

foreach $i(0..$gazoulimitnum){
$line =~ s/\%imgsrc$i\%/$IMGSRC[$i]/;
$line =~ s/\%filename$i\%/$FILENAME[$i]/;
$line =~ s/\%filedelete$i\%/$FILEDELETE[$i]/;
$line =~ s/\%caption$i\%/$CAPTION[$i]/;
}


#残り全て空白に
$line =~ s/\%(.*)\%//g;
$str .= $line;
}

print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
■【$CONTENTSNAME[$contents]】  編集$taikaiinfo
$taikainamestr
$str
</td>
</tr>
</table>
$footer
END_HTML

}


# -----------------------------------------------------------------
# データの削除処理
# -----------------------------------------------------------------
sub deleterecord {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
if($serial eq ""){	# serialがないとエラー
print "serial error.";
exit;
}	#if

$sql_str = "UPDATE $dbname SET koukaiflag = 9 WHERE serial = $serial";
$rs = $dbh->prepare($sql_str);
$rs->execute();
#
if($contents == 32){$contents = 31;}	#if
#
$url =<<"END_HTML";
<meta http-equiv="Refresh" content="0;URL=webpal.cgi?code=editlist&contents=$contents&taikaicode=$taikaicode&area=$area&kumi=$kumi">
END_HTML
#
if($contents == 0){	#大会を消したときだけ
$url =<<"END_HTML";
<meta http-equiv="Refresh" content="0;URL=webpal.cgi?code=top">
END_HTML
}	#if
if($contents == 31){	#大会を消したときだけ
$url =<<"END_HTML";
<meta http-equiv="Refresh" content="0;URL=webpal.cgi?code=editlist&contents=$contents&taikaicode=$taikaicode&area=$area&category=$category">
END_HTML
}	#if


#
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
$url
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>再読み込み中。。。</p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}

# -----------------------------------------------------------------
# データの一括削除処理
# -----------------------------------------------------------------
sub deleteset {
@SS = $query->param('deleteset');
@SN = $query->param('sortnum');
@SNS = $query->param('sortnumserial');
$contents = $paramhash{'contents'};
$taikaicode = $paramhash{'taikaicode'};
$category = $paramhash{'category'};
$area = $paramhash{'area'};
$kumi = $paramhash{'kumi'};
if($contents eq ""){	# contentsがないとエラー
print "contents error.";
exit;
}	#if
#一括削除
foreach $line(@SS){
$sql_str = "UPDATE $dbname SET koukaiflag = 9 WHERE serial = $line";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}	#for
#表示順位
$i=0;
foreach $line(@SNS){
$sql_str = "UPDATE $dbname SET sortnum = $SN[$i] WHERE serial = $line";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$i++;
}	#for

print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="3;URL=webpal.cgi?code=editlist&contents=$contents&taikaicode=$taikaicode&category=$category&area=$area&kumi=$kumi">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>処理を行いました。</p>
<p>３秒後に再読み込みします。</p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}
# -----------------------------------------------------------------
# ファイルの受け取り
# -----------------------------------------------------------------
sub fileup {
my ($fn,$contents,$dir) = (@_);
if($fn eq ""){return "";}
$fH = $query->upload($fn);
if($fH eq ""){return "";}
# エラーチェック
if ($query->cgi_error) {
$err = $query->cgi_error;
if ($err){&error("query cgi error:$err")};
}

#&error("更新するファイルを選択して下さい [$fn:$fH]") unless (defined($fH));
# MIMEタイプ取得
$mimetype = $query->uploadInfo($fH)->{'Content-Type'};
$ext = $hash_mime{$mimetype} ? $hash_mime{$mimetype} : &error("ファイル：$fH【$mimetype】 指定形式以外のファイルはアップロード出来ません");

#元のファイル名
if ($ENV{'HTTP_USER_AGENT'} =~ /MSIE/ ) {fileparse_set_fstype('MSDOS');}	#IE6対策
$sfn = ( fileparse( $fH ) )[0]; 
$sfn =~ s/:/：/gm;
$sfn =~ s/<>/&lg;&gt;/gm;
utf8::decode($sfn);
($sfn_name,$sfn_ext) = split(/\./,$sfn);
$sfn_ext = lc $sfn_ext;
if($ext eq "" && $sfn_ext eq ""){&error("ファイル形式が不明です。");}
if($ext eq "" and $sfn_ext ne ""){$ext = $sfn_ext;}
$ext = lc($ext);
if($ext eq "jpeg"){$ext = "jpg";}
# ファイルサイズ取得
$size = (stat($fH))[7];
# サイズ制限
$max=$maxsize/1000;
if ($size > $maxsize * 1000){&error("ファイルの容量が大きすぎます。 最大 $max MBまで。")};

# 画像じゃなければそのまま保存
if($ext ne "jpg"){
# 保存するファイル名をセット
$sfilename = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,int(rand(65535)),".$ext");
$set = "$dir$attach_dir/$sfilename";

#高速UP
my $temp_path = $query->tmpFileName($fH); # アップロードされたファイルのフルパスmy ($buffer);
move ($temp_path, $set) or &error("サーバー上で指定のファイル名が開けません。管理者にお問い合わせ下さい [$set]");   # File::Copy の moveメソッドで移動
close($fH);		# おまじない
chmod 0644,$set;

return "$sfn<>$sfilename<>$mimetype";
#------------------------------------
#画像だったら処理
}else{
#ピクセルサイズを取得
( $format, $w, $h ) = &GetImageSize( $set );
if( $w > $psize || $h > $psize ){unlink $set;&error("画像のピクセルが大きすぎます（ $w x $h px ）。最大（ $psize x $psize px ）");}
# 保存するファイル名をセット
# ファイル名を作成
my $a = int(rand(99999));
my $sfilename = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,".$ext");
my $set = "$dir$attach_dir/$sfilename";
my @OUTFILE = ();
$OUTFILE[0] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"s.$ext");
$OUTFILE[1] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"l.$ext");
$OUTFILE[2] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"pda.$ext");
$OUTFILE[3] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"jisyukikaku_list.$ext");
$OUTFILE[4] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"banner.$ext");
$OUTFILE[5] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"top.$ext");
$OUTFILE[6] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"eventmain.$ext");
$OUTFILE[7] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"eventsub.$ext");
$OUTFILE[8] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"myteam.$ext");
$OUTFILE[9] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"taikaiimage.$ext");
$OUTFILE[10] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"taikaiimage2.$ext");
$OUTFILE[11] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"taikaikiji1.$ext");
$OUTFILE[12] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"taikaikiji2.$ext");
$OUTFILE[13] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"convention.$ext");
$OUTFILE[14] = sprintf("%d_%04d%02d%02d%02d%02d%02d_%d%s",$contents,$year,$month,$mday,$hour,$min,$sec,$a,"banner2.$ext");
#高速UP
my $temp_path = $query->tmpFileName($fH); # アップロードされたファイルのフルパスmy ($buffer);
move ($temp_path, $set) or &error("サーバー上で指定のファイル名が開けません。管理者にお問い合わせ下さい [$set]");   # File::Copy の moveメソッドで移動
close($fH);		# おまじない
chmod 0644,$set;

my @QUALITY = (60,100,70,80,80,80,80,80,80,90,80,80,80,80,80);
my @SIZETEMPw = (64,600,240,100,208,127,322,75,533,900,289,400,223,790,440);
my @SIZETEMPh = (64,600,240,$psize,$psize,$psize,$psize,$psize,533,$psize,$psize,$psize,$psize,$psize,$psize);
$cnt = @QUALITY +1;
foreach $k(0..$cnt){
# リサイズ条件の設定
$ImgResize->{width}    = $SIZETEMPw[$k];
$ImgResize->{height}   = $SIZETEMPh[$k];
$ImgResize->{quality}  = $QUALITY[$k];
$ImgResize->{ext}      = '.jpg';
$ImgResize->{in}       = "$set";
$ImgResize->{out}      = "$dir$attach_dir/$OUTFILE[$k]";
$ImgResize->{exif_cut} =   1;
$ImgResize->resize;
}	#foreach
#元ファイルは削除：しない
#unlink $set;
return "$sfn<>$sfilename<>$mimetype";
}	#if ext
}	#sub


#----------------------------------------------#
sub wday {
    my ($year,$month,$day)=@_;
    if($month<3){ $month += 12; $year--; }
    return ($year+int($year/4)-int($year/100)+int($year/400)+int((13*$month+8)/5)+$day)% 7;
}
#----------------------------------------------#



# -----------------------------------------------------------------
# フォーム登録
# -----------------------------------------------------------------
sub member_formadd {
$serial = $paramhash{'serial'};
$serial_uid = $paramhash{'serial_uid'};
$contents = $paramhash{'contents'};

if($contents == 22 && $serial_uid == 0){
$serial_uid = $serial -0;
$serial = "";
}else{
$serial = $paramhash{'serial'};
$serial_uid = $paramhash{'serial_uid'};
}	#if

$koukaiflag = $paramhash{'koukaiflag'} -0;
$glevel = $paramhash{'glevel'} -0;

#メンバーTBL
$mailadr1 = $paramhash{'mailadr1'};
$mailadr2 = $paramhash{'mailadr2'};
$pwd = $paramhash{'pwd'};
$shimei1 = $paramhash{'shimei1'};
$shimei_kana1 = $paramhash{'shimei_kana1'};
$mailaddress1 = $paramhash{'mailaddress1'};
$tel1 = $paramhash{'tel1'};
$prefectural1 = $paramhash{'prefectural1'};
$cities1 = $paramhash{'cities1'};
$shimei2 = $paramhash{'shimei2'};
$shimei_kana2 = $paramhash{'shimei_kana2'};
$tel2 = $paramhash{'tel2'};
$mailaddress2 = $paramhash{'mailaddress2'};
$teamname = $paramhash{'teamname'};
$team_kana = $paramhash{'team_kana'};
$team_abbr = $paramhash{'team_abbr'};
$team_year = $paramhash{'team_year'};
$team_hp = $paramhash{'team_hp'};
$katsudou_week = $paramhash{'katsudou_week'};
$average_age = $paramhash{'average_age'};
$team_pref = $paramhash{'team_pref'};
$team_cities = $paramhash{'team_cities'};
$past_perform = $paramhash{'past_perform'};
$team_pr = $paramhash{'team_pr'};

#$nichiji1 = sprintf("%04d-%02d-%02d",$paramhash{'syear'},$paramhash{'smonth'},$paramhash{'sday'});
#if($contents == 7){
#	if(!Date::Simple->new($nichiji1)){
#		&error("日付にエラーがあります。「$nichiji1」");
#	}		#if
#}		#if

# --------------------------
# 添付ファイルの登録処理
$upfilename = "";
foreach $i(0..$gazoulimitnum){
if($paramhash{"file$i"} ne ""){$file = &fileup("file$i",$contents);}else{$file = $paramhash{"filename$i"};}
if($paramhash{"filedelete$i"} == 1){$file = "";}
$upfilename .= $file.":";
}	#foreach

#DB
if($serial eq ""){
# 新規登録
$sql_str = qq{INSERT INTO $member_tbl(serial_uid,contents,koukaiflag,glevel,mailadr1,mailadr2,pwd,shimei1,shimei_kana1,mailaddress1,tel1,prefectural1,cities1,shimei2,shimei_kana2,tel2,mailaddress2,teamname,team_kana,team_abbr,team_year,team_hp,katsudou_week,average_age,team_pref,team_cities,past_perform,team_pr,upfilename) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$serial_uid,
$contents,
$koukaiflag,
$glevel,
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
$team_pref,
$team_cities,
$past_perform,
$team_pr,
$upfilename,
);
}else{
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
$team_pref =~ s/\'/\'\'/gm;	#'
$team_cities =~ s/\'/\'\'/gm;	#'
$past_perform =~ s/\'/\'\'/gm;	#'
$team_pr =~ s/\'/\'\'/gm;	#'
$upfilename =~ s/\'/\'\'/gm;	#'

$str = "";
#$str.="sortnum = '$sortnum',";
#if($nichiji1 ne""){$str.="nichiji1 = '$nichiji1',";}
$str.="serial_uid = '$serial_uid',";
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
$str.="team_pref = '$team_pref',";
$str.="team_cities = '$team_cities',";
$str.="past_perform = '$past_perform',";
$str.="team_pr = '$team_pr',";
$str.="upfilename = '$upfilename',";
chop $str;
#
$sql_str = "UPDATE $member_tbl SET koukaiflag = '$koukaiflag',contents = '$contents',$str WHERE serial = $serial";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}	#if
&sqlcheck($sql_str);


#コンテンツ別戻り先
$backmes = << "END_HTML";
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('webpal.cgi')">トップに戻る</button></td>
</tr>
</table>
END_HTML

###
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
<!--
function urljump(url){
top.location.href=url;
}
-->
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" class="text-12">
<tr><td>
<center>
<p>登録が完了致しました。</p>
<br>
$backmes
</center>
</td>
</tr>
</table>
</td>
</tr>
</table>
$footer
END_HTML
}

# -----------------------------------------------------------------
# 編集リスト
# -----------------------------------------------------------------
sub member_editlist {

$contents = $paramhash{'contents'};
$serial = $paramhash{'serial'};

print << "END_HTML";
$header
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に削除してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
function delete_allset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = true;
}	//for
}	// func
function delete_allreset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = false;
}	//for
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg
END_HTML
# -----------------------------------------------------------------
#$allstr = <<"END_HTML";
#<a href="javascript:void(0);" onclick="delete_allset()">□全部を選択</a>　
#<a href="javascript:void(0);" onclick="delete_allreset()">□全部の選択を解除</a>　
#<input type=submit value="変更/登録">　<font color=red size=-1>※一括削除と表示順位設定は一度に処理されます。</font>
#END_HTML
#
$sql_str = "SELECT * FROM $member_tbl  WHERE contents = $contents and serial_uid = $serial and koukaiflag != 9 ";
#
if($contents == 22){	#大会エントリー
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>参加希望都道府県</td>
<td align=center nowrap>活動拠点</td>
<td align=center nowrap >第一担当者</td>
<td align=center nowrap >第二担当者</td>
<td align=center width=90% >活動実績</td>
</tr>
END_HTML
}	#if


#
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
#
print << "END_HTML";
<form action="webpal.cgi" method="post" enctype="multipart/form-data" name="form1" id="form1" onSubmit="return delete_kakunin()" >
<input name="code" type="hidden" id="code" value="deleteset" />
<input name="contents" type="hidden" id="contents" value="$contents" />
<input name="serial" type="hidden" id="serial" value="$serial" />
■【$CONTENTSNAME[$contents]】  編集<br>
$allstr
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>
<table  border="0" cellpadding="1" cellspacing="1" class="text-12" width=100%>
$disp
END_HTML
#
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$serial_uid = $REFHASH->{'serial_uid'};
$koukaiflag = $REFHASH->{'koukaiflag'};
$contents = $REFHASH->{'contents'};
$sortnum = $REFHASH->{'sortnum'};
$team_pref = &paramsetsql('team_pref');
$team_cities = &paramsetsql('team_cities');
$shimei1 = &paramsetsql('shimei1');
$shimei2 = &paramsetsql('shimei2');
$past_perform = &paramsetsql('past_perform');
#日時
#$nichiji1 = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji1')));



#
if($contents == 22){	#大会エントリー
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集する" onClick="urljump(\'$cgifile?code=member_editform&serial=$serial&contents=$contents\')">
</td>
<td class="tdpad" nowrap >$team_pref </td>
<td class="tdpad" nowrap >$team_cities </td>
<td class="tdpad" nowrap >$shimei1 </td>
<td class="tdpad" nowrap >$shimei2 </td>
<td class="tdpad" nowrap >$past_perform </td>
</tr>
END_HTML
}	#if





}	#for loop
print << "END_HTML";
</table>
</td>
</tr>
</table>
</form>

END_HTML
print $footer;
}



# -----------------------------------------------------------------
# 編集フォーム
# -----------------------------------------------------------------
sub member_editform {
$contents = $paramhash{'contents'};
$serial = $paramhash{'serial'};

$sql_str = "SELECT * FROM $member_tbl WHERE serial = $serial ";

$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$serial_uid = $REFHASH->{'serial_uid'};
$KFLAG[$REFHASH->{'koukaiflag'}-0] = " checked ";
$sortnum = &paramsetsql('sortnum');
if($sortnum eq ""){$sortnum = 1;}
$taikaicode = &paramsetsql('taikaicode');
#メンバーTBL
$mailadr1 = &paramsetsql('mailadr1');
$mailadr2 = &paramsetsql('mailadr2');
$pwd = &paramsetsql('pwd');
$shimei1 = &paramsetsql('shimei1');
$shimei_kana1 = &paramsetsql('shimei_kana1');
$mailaddress1 = &paramsetsql('mailaddress1');
$tel1 = &paramsetsql('tel1');
$prefectural1 = &paramsetsql('prefectural1');
$cities1 = &paramsetsql('cities1');
$shimei2 = &paramsetsql('shimei2');
$shimei_kana2 = &paramsetsql('shimei_kana2');
$tel2 = &paramsetsql('tel2');
$mailaddress2 = &paramsetsql('mailaddress2');
$teamname = &paramsetsql('teamname');
$team_kana = &paramsetsql('team_kana');
$team_abbr = &paramsetsql('team_abbr');
$team_year = &paramsetsql('team_year');
$team_hp = &paramsetsql('team_hp');
$katsudou_week = &paramsetsql('katsudou_week');
$average_age = &paramsetsql('average_age');
$team_cities = &paramsetsql('team_cities');
$past_perform = &paramsetsql('past_perform');
$team_pr = &paramsetsql('team_pr');


#画像
@IMGTEMPS = split(/:/,$REFHASH->{'upfilename'});
foreach $i(0..$gazoulimitnum){
utf8::decode($IMGTEMPS[$i]);
($sfn,$fn) = split(/<>/,$IMGTEMPS[$i]);
if($fn ne ""){
@TEMP = split(/\./,$fn);
$IMGSRC[$i] = "<img src=img/dat.gif><br>";
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=file/$TEMP[0]eventmain.$TEMP[1]><br>";}
if( $TEMP[1] eq "pdf"){$IMGSRC[$i] = "<img src=img/pdf.gif><br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
#都道府県
$team_pref = "<select name=team_pref>\n";
$team_pref .= &makeselect_pref(&paramsetsql('team_pref'));
$team_pref .= "</select>\n";
#日付
($y,$m,$d) = split(/-/,&paramsetsql('nichiji1'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji1 = "<select name=syear>\n";
$nichiji1 .= &makeselect($y-1,$year+1,$y);
$nichiji1 .= "</select>年\n";
$nichiji1 .= "<select name=smonth>\n";
$nichiji1 .= &makeselect(1,12,$m);
$nichiji1 .= "</select>月\n";
$nichiji1 .= "<select name=sday>\n";
$nichiji1 .= &makeselect(1,31,$d);
$nichiji1 .= "</select>日\n";
#
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"template/$FORMFILE[$contents]";
@TEMPLATE = <IN>;
close IN;
#
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%serial\%/$serial/;
$line =~ s/\%serial_uid\%/$serial_uid/;
$line =~ s/\%code\%/member_formadd/;
$line =~ s/\%koukaiflag0\%/$KFLAG[0]/;
$line =~ s/\%koukaiflag1\%/$KFLAG[1]/;
$line =~ s/\%contents\%/$contents/;

foreach $i(0..$gazoulimitnum){
$line =~ s/\%imgsrc$i\%/$IMGSRC[$i]/;
$line =~ s/\%filename$i\%/$FILENAME[$i]/;
$line =~ s/\%filedelete$i\%/$FILEDELETE[$i]/;
}

$line =~ s/\%mailadr\%/$mailadr1/;
$line =~ s/\%mailadr2\%/$mailadr2/;
$line =~ s/\%pwd\%/$pwd/;
$line =~ s/\%shimei1\%/$shimei1/;
$line =~ s/\%shimei_kana1\%/$shimei_kana1/;
$line =~ s/\%mailaddress1\%/$mailaddress1/;
$line =~ s/\%tel1\%/$tel1/;
$line =~ s/\%prefectural1\%/$prefectural1/;
$line =~ s/\%cities1\%/$cities1/;
$line =~ s/\%shimei2\%/$shimei2/;
$line =~ s/\%shimei_kana2\%/$shimei_kana2/;
$line =~ s/\%tel2\%/$tel2/;
$line =~ s/\%mailaddress2\%/$mailaddress2/;
$line =~ s/\%teamname\%/$teamname/;
$line =~ s/\%team_kana\%/$team_kana/;
$line =~ s/\%team_abbr\%/$team_abbr/;
$line =~ s/\%team_year\%/$team_year/;
$line =~ s/\%team_hp\%/$team_hp/;
$line =~ s/\%katsudou_week\%/$katsudou_week/;
$line =~ s/\%average_age\%/$average_age/;
$line =~ s/\%team_pref\%/$team_pref/;
$line =~ s/\%team_cities\%/$team_cities/;
$line =~ s/\%past_perform\%/$past_perform/;
$line =~ s/\%team_pr\%/$team_pr/;

#残り全て空白に
$line =~ s/\%(.*)\%//g;
$str .= $line;
}

print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
■【$CONTENTSNAME[$contents]】  編集
$str
</td>
</tr>
</table>
$footer
END_HTML

}




# -----------------------------------------------------------------
# 大会名GET
# -----------------------------------------------------------------
sub taikainame_get {
my ($taikaicode,$genre,$flag)=(@_);
my $sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag != 9 and serial = '$taikaicode' ";
my $rs = $dbh->prepare($sql_str);
$rs->execute();
my $count = $rs->rows;	# Hit件数を確保
if($count != 1){return "（大会名：不明）";}
my $REFHASH = $rs->fetchrow_hashref;
if($genre ne ""){$g = "（".$GENRENAME{$genre}."）";}
my $koukaiflag = &paramsetsql('koukaiflag',$REFHASH);
my $title = &paramsetsql('title',$REFHASH);
if($koukaiflag == 1 && $flag eq ""){$title .= "<span class='hikoukaicolor'>【非公開】</span>";}
return $title.$g;
}	#sub

# -----------------------------------------------------------------
# エリア名GET
# -----------------------------------------------------------------
sub taikaiareaname_get {
my ($area000)=(@_);
my $sql_str000 = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag != 9 and serial = '$area000' ";
my $rs000 = $dbh->prepare($sql_str000);
$rs000->execute();
my $count000 = $rs000->rows;	# Hit件数を確保
if($count000 != 1){return "（地区名：不明）";}
my $REFHASH000 = $rs000->fetchrow_hashref;
return &paramsetsql('title',$REFHASH000);
}	#sub

# -----------------------------------------------------------------
# 「組」名GET
# -----------------------------------------------------------------
sub taikaikuminame_get {
my ($kumi)=(@_);
my $sql_str = "SELECT * FROM $dbname WHERE contents = 31 and koukaiflag != 9 and serial = '$kumi' ";
my $rs = $dbh->prepare($sql_str);
$rs->execute();
my $count = $rs->rows;	# Hit件数を確保
if($count != 1){return "（組名：不明）";}
my $REFHASH = $rs->fetchrow_hashref;
return &paramsetsql('title',$REFHASH);
}	#sub

# -----------------------------------------------------------------
# 「チーム名」名GET：serialで。
# -----------------------------------------------------------------
sub taikaiteamname_get {
my ($ss)=(@_);
my $sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and serial = '$ss' ";
my $rs = $dbh->prepare($sql_str);
$rs->execute();
my $count = $rs->rows;	# Hit件数を確保
my $REFHASH = $rs->fetchrow_hashref;
return &paramsetsql('teamname',$REFHASH);
}	#sub

# -----------------------------------------------------------------
# 「チーム名」名GET：sessionで。
# -----------------------------------------------------------------
sub taikaiteamname_get2 {
my ($ses,$cate)=(@_);
my $sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and ssid = '$ses' ";
my $rs = $dbh->prepare($sql_str);
$rs->execute();
my $count = $rs->rows;	# Hit件数を確保
my $REFHASH = $rs->fetchrow_hashref;
my $teamname = &paramsetsql('teamname',$REFHASH);
my $tss = &paramsetsql('serial',$REFHASH);
if($cate ne ""){$teamname = "（".$GENRENAME{$cate}."）";}
return ($teamname,$tss);
}	#sub

# -----------------------------------------------------------------
# 「チーム名」名GET：serialで。sessionも返す
# -----------------------------------------------------------------
sub taikaiteamname_get3 {
my ($ss)=(@_);
my $sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and serial = '$ss' ";
my $rs = $dbh->prepare($sql_str);
$rs->execute();
my $count = $rs->rows;	# Hit件数を確保
my $REFHASH = $rs->fetchrow_hashref;
my $teamname = &paramsetsql('teamname',$REFHASH);
my $ssid = &paramsetsql('ssid',$REFHASH);
return ($teamname,$ssid);
}	#sub


# -----------------------------------------------------------------
# 対戦組み合わせ
# -----------------------------------------------------------------
sub vsdataset {
my ($taikaicode,$category,$area,$kumi,$vsdata,$REF)=(@_);
#print "($taikaicode,$area,$kumi,$vsdata)";

####################################
#リーグ
####################################
if($category == 1){
my %RDATA1 = ();
my %RDATA2 = ();

foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
my ($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
my ($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
my ($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
my ($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
my ($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
$RDATA1{$setu}{$num} = $tss1;
$RDATA2{$setu}{$num} = $tss2;
}	#foreach

#日付from
$body = &paramsetsql('body',$REF);
foreach( split(/<>/,$body)){
($setu,$n1,$n2) = split(/:/,$_);
($y,$m,$d) = split(/-/,$n1);
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji = "<select name='syear:$setu' >\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect($year-1,$year+1,$y);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='smonth:$setu'>\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect(1,12,$m);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='sday:$setu'>\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect(1,31,$d);
$nichiji .= "</select>日〜";
#日付to
($y,$m,$d) = split(/-/,$n2);
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji .= "<select name='eyear:$setu'>\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect($year-1,$year+1,$y);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='emonth:$setu'>\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect(1,12,$m);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='eday:$setu'>\n";
$nichiji .= "<option value=''>選択</option>\n";
$nichiji .= &makeselect(1,31,$d);
$nichiji .= "</select>日まで\n";
$NICHIJI[$setu] = $nichiji;
}	#foreach


my $data = "";
my %TSS = ();
my %NSS = ();
#「チーム」一覧
my $sql_str1 = "SELECT m.serial as serial,m.teamname as teamname FROM pridejapan as p,member_tbl as m WHERE p.contents = 32 and p.koukaiflag = 0 and p.taikaicode = '$taikaicode' and p.category = '$category' and p.area = '$area' and kumi = '$kumi' and p.teamnum = m.serial ORDER BY p.sortnum ASC, p.serial DESC ";
my $rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
my $count1 = $rs1->rows;	# Hit件数を確保
for(my $k = 0;$k < $count1;$k++){	# データベース１件ずつ
my $REFHASH1 = $rs1->fetchrow_hashref;
my $teamname = &paramsetsql('teamname',$REFHASH1);
my $tss = &paramsetsql('serial',$REFHASH1);
$TSS{$tss} = $teamname;
push(@NSS,$tss);
}	#for

#対戦組み合わせ登録
#対戦チーム数GET count1
$temp = int($count1 / 2);
foreach $setu(1..7){
foreach $num(1 .. 4){
#リスト作成
my $team1 = "";
my $team2 = "";
$lname = "";
$lss = "";
foreach $tss(@NSS){
if($tss == $RDATA1{$setu}{$num}){$flag = "selected";$lname = $TSS{$tss};$lss = $tss;}else{$flag = "";}
$team1 .=<<"END_HTML";
<option value="$tss" $flag >$TSS{$tss}</option>
END_HTML
}	#foreach
$rname = "";
$rss = "";
foreach $tss(@NSS){
if($tss == $RDATA2{$setu}{$num}){$flag = "selected";$rname = $TSS{$tss};$rss = $tss;}else{$flag = "";}
$team2 .=<<"END_HTML";
<option value="$tss" $flag >$TSS{$tss}</option>
END_HTML
}	#foreach

$result10 = "";
$result11 = "";
$resultstr1 = "";
$result20 = "";
$result21 = "";
$resultstr2 = "";
$result0 = "";
$result1 = "";
$senpyo1 = "";
$comment1 = "";
$lastupdated1 = "";
$senpyo2 = "";
$comment2 = "";
$lastupdated2 = "";
$reportscore = "";
$result10str = "";
$result11str = "";
$result20str = "";
$result21str = "";
$lnamestr = "";
$rnamestr = "";
#試合結果報告があるかチェック1
$count1 = "";
if($lname ne ""){
#報告のGET
($teamname,$ses) = &taikaiteamname_get3($lss);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = $num and linkadr = '$ses' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count1 = $rs2->rows;	# Hit件数を確保
#print "count1=$count1<br>";
@IMGSRC = ();
if($count1 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$ss = &paramsetsql('serial',$REFHASH2);
$result10 = &paramsetsql('result0',$REFHASH2);
$result11 = &paramsetsql('result1',$REFHASH2);
$resultstr1 = &paramsetsql('resultstr',$REFHASH2);
$posi1 = &paramsetsql('linkadrtitle',$REFHASH2);
if($posi1 != 0){($result10,$result11)=($result11,$result10);}
$senpyo1 = &paramsetsql2('senpyo',$REFHASH2);
$comment1 = &paramsetsql('comment',$REFHASH2);
$lastupdated1 = &paramsetsql('timestamp',$REFHASH2);
#画像
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH2));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$l] = "<a href='?code=download&s=$ss&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
@CAP = split(/<>/,&paramsetsql('caption',$REFHASH2));
if($resultstr1 == 4){	#不戦勝
$result10str = "（不戦勝）";
$result11str = "（不戦負）";
if($posi1 != 0){($result10,$result11)=($result11,$result10);}
}	#if
if($resultstr1 == 5){	#不戦勝
$result10str = "（不戦負）";
$result11str = "（不戦勝）";
if($posi1 != 0){($result10,$result11)=($result11,$result10);}
}	#if
$lnamestr =<<"END_HTML";
$lname<br>
<span style="color:red;">（戦評）</span>$senpyo1<br>
<span style="color:red;">（コメント）</span>$comment1<br>
<span style="color:red;">（投稿時間）</span>$lastupdated1<br>
<span style="color:red;">（報告スコア）</span>$lname <span class="scorebig">$result10</span>$result10str x <span class="scorebig">$result11</span>$result11str $rname<br>
<table cellpadding=2 cellspacing=1 bgcolor="#aaaaaa" width=350 class="text-12">
<tr><td bgcolor="#ffffff" align=center valign=top width=10% nowrap>$IMGSRC[0]</td><td bgcolor="#ffffff" valign=top>$CAP[0]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC[1]</td><td bgcolor="#ffffff" valign=top>$CAP[1]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC[2]</td><td bgcolor="#ffffff" valign=top>$CAP[2]</td></tr>
</table>
END_HTML
}	#if count1
}	#if lname

#試合結果報告があるかチェック2
$count2 = "";
if($rname ne ""){
#報告のGET
($teamname,$ses) = &taikaiteamname_get3($rss);
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = $num and linkadr = '$ses' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
@IMGSRC = ();
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$ss = &paramsetsql('serial',$REFHASH2);
$result20 = &paramsetsql('result0',$REFHASH2);
$result21 = &paramsetsql('result1',$REFHASH2);
$resultstr2 = &paramsetsql('resultstr',$REFHASH2);
$posi2 = &paramsetsql('linkadrtitle',$REFHASH2);
if($posi2 != 0){($result20,$result21)=($result21,$result20);}
$senpyo2 = &paramsetsql2('senpyo',$REFHASH2);
$comment2 = &paramsetsql('comment',$REFHASH2);
$lastupdated2 = &paramsetsql('timestamp',$REFHASH2);
#画像
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH2));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC[$l] = "<a href='?code=download&s=$ss&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
@CAP = split(/<>/,&paramsetsql('caption',$REFHASH2));
if($resultstr2 == 4){	#不戦勝
$result20str = "（不戦勝）";
$result21str = "（不戦負）";
if($posi2 != 0){($result20,$result21)=($result21,$result20);}
}	#if
if($resultstr2 == 5){	#不戦負
$result20str = "（不戦負）";
$result21str = "（不戦勝）";
if($posi2 != 0){($result20,$result21)=($result21,$result20);}
}	#if

$rnamestr =<<"END_HTML";
$rname<br>
<span style="color:red;">（戦評）</span>$senpyo2<br>
<span style="color:red;">（コメント）</span>$comment2<br>
<span style="color:red;">（投稿時間）</span>$lastupdated2<br>
<span style="color:red;">（報告スコア）</span>$rname <span class="scorebig">$result20</span>$result20str x <span class="scorebig">$result21</span>$result21str $lname<br>
<table cellpadding=2 cellspacing=1 bgcolor="#aaaaaa" width=350 class="text-12">
<tr><td bgcolor="#ffffff" align=center valign=top width=10% nowrap>$IMGSRC[0]</td><td bgcolor="#ffffff" valign=top>$CAP[0]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC[1]</td><td bgcolor="#ffffff" valign=top>$CAP[1]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC[2]</td><td bgcolor="#ffffff" valign=top>$CAP[2]</td></tr>
</table>
END_HTML
}	#if count2
}	#if


#スコアチェック
if($count1 != 0 && $count2 != 0){
#両方から報告があり、なおかつ正しい場合
if($result10 == $result21 && $result11 == $result20){
$result0 = "スコア ".$result10;
$result1 = $result11;
}	#if
}	#if count

if( ($count1 != 0 || $count2 != 0 ) and ($result10 != $result21 || $result11 != $result20) ){
$result0 = "スコア （未確定）";
$result1 = "（未確定）";
}	#if

#
$VSLIST[$setu] .=<<"END_HTML";
<table cellpadding=2 cellspacing=1 bgcolor="#aaaaaa" width=100% class="text-12">
<tr>
<td bgcolor="#ffffff" width=9% align=right valign=top>
<select name="team1:$setu.$num" id="team1:$setu.$num">
<option value=''>選択してください</option>
$team1
</select>
<br><br>
$result0
</td>
<td bgcolor="#ffffff" width=2% align="center" valign=top>vs<br><br>-</td>
<td bgcolor="#ffffff" width=9% align=left valign=top>
<select name="team2:$setu.$num" id="team2:$setu.$num">
<option value=''>選択してください</option>
$team2
</select>
<br><br>
$result1
</td>
<td bgcolor="#ffffff" width=40% valign=top>$lnamestr</td>
<td bgcolor="#ffffff" width=40% valign=top>$rnamestr</td>
</tr>
</table>
END_HTML
}	#foreach

#
if($NICHIJI[$setu] eq ""){
$nichiji = "<select name='syear:$setu' >\n";
$nichiji .= &makeselect($year-1,$year+1,$year);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='smonth:$setu'>\n";
$nichiji .= &makeselect(1,12,$month);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='sday:$setu'>\n";
$nichiji .= &makeselect(1,31,$mday);
$nichiji .= "</select>日〜";
#日付to
$nichiji .= "<select name='eyear:$setu'>\n";
$nichiji .= &makeselect($year-1,$year+1,$year);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='emonth:$setu'>\n";
$nichiji .= &makeselect(1,12,$month);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='eday:$setu'>\n";
$nichiji .= &makeselect(1,31,$mday);
$nichiji .= "</select>日まで\n";
$NICHIJI[$setu] = $nichiji;
}	#if
###
$data .=<<"END_HTML";
<table class="text-12" width=100%>
<tr>
<td class="tdpad2" bgcolor="#FFCC66">第${setu}節</td>
</tr>
<tr>
<td class="tdpad2">試合期日：$NICHIJI[$setu]</td>
</tr>
<tr>
<td>
$VSLIST[$setu]
</td>
</tr>
</table>
END_HTML
}	#foreach
$data =<<"END_HTML";
<table class="text-12" width=100%>
<tr>
<td>
$data
</td>
</tr>
<tr><td align=center><hr>
<input type="hidden" name="count" value="$count1" />
<input type="submit" value="登録" style="width:100px;" />
</td></tr>
</table>
<script>
$scriptlist
</script>
END_HTML
return $data;
}	#if

####################################
# トーナメント
####################################
if($category == 2){
#日時
$k = 1;
$n = &paramsetsql('nichiji1',$REF);
if($n ne ""){
@TEMP = split(/<>/,$n);
foreach(@TEMP){
($n1,$n2) = split(/:/,$_);
($y,$m,$d) = split(/-/,$n1);
$yy = $y;
$mm = $m;
$dd = $d;
if($y == 0){$y = $year;$m=$month;$d=$mday;$yy="";$mm="";$dd="";}
$nichiji = "<select name='syear:$k' >\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect($y-1,$y+1,$yy);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='smonth:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,12,$mm);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='sday:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,31,$dd);
$nichiji .= "</select>日～<br>";
#日付to
($y,$m,$d) = split(/-/,$n2);
$yy = $y;
$mm = $m;
$dd = $d;
if($y == 0){$y = $year;$m=$month;$d=$mday;$yy="";$mm="";$dd="";}
$nichiji .= "<select name='eyear:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect($y-1,$y+1,$yy);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='emonth:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,12,$mm);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='eday:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,31,$dd);
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= "</select>日まで\n";
$NICHIJI{$k++} = $nichiji;
}	#foreach
}else{
#初回
foreach $k(1..7){
$nichiji = "<select name='syear:$k' >\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect($year-1,$year+1);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='smonth:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,12);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='sday:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,31);
$nichiji .= "</select>日～<br>";
#日付to
$nichiji .= "<select name='eyear:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect($year-1,$year+1);
$nichiji .= "</select>年\n";
$nichiji .= "<select name='emonth:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,12);
$nichiji .= "</select>月\n";
$nichiji .= "<select name='eday:$k'>\n";
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= &makeselect(1,31);
$nichiji .= "<option value=''>-</option>\n";
$nichiji .= "</select>日まで\n";
$NICHIJI{$k} = $nichiji;
}	#foreach
}	#if
#チームリスト
@TEAMLISTTEMP = split(/:/,&paramsetsql('body',$REF));
#@SCORELIST = split(/:/,&paramsetsql('text1',$REF));
@CNT = (0,1,2,4,8,16,32,64,128);
$cnt = 1;
$cnt3 = 0;
foreach $y(1..7){
$cnt2 = $CNT[$y];
foreach $x(1..$cnt2){
$result10 = "";
$result11 = "";
$result20 = "";
$result21 = "";
$resultstr1="";
$resultstr2="";
$tss1 = $TEAMLISTTEMP[$cnt++];
($tss1name,$tss1session) = &taikaiteamname_get3($tss1);
$tss2 = $TEAMLISTTEMP[$cnt++];
($tss2name,$tss2session) = &taikaiteamname_get3($tss2);
@IMGSRC1 = ();
@IMGSRC2 = ();
@CAP1 = ();
@CAP2 = ();
#報告をGET：左チーム
if($tss1 ne ""){
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = '$tss2' and linkadr = '$tss1session' ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print "count1=$count1 $sql_str1<br>\n";
if($count1 == 1){
$REFHASH1 = $rs1->fetchrow_hashref;
$tss1serial = &paramsetsql('serial',$REFHASH1);
$resultstr1 = &paramsetsql('resultstr',$REFHASH1);
$result10 = &paramsetsql('result0',$REFHASH1);
$result11 = &paramsetsql('result1',$REFHASH1);
@CAP1 = split(/<>/,&paramsetsql('caption',$REFHASH1));
#print "tss1name=$tss1name<br>\n";
#if($tss1 == 197 && $tss2 == 181){
#画像
@IMGSRC = ();
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH1));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC1[$l] = "<a href='?code=download&s=$tss1serial&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
}	#if 報告あり
}	#if tss1
#報告をGET：右チーム
if($tss2 ne ""){
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = '$tss1' and linkadr = '$tss2session' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2 $sql_str2<br>\n";
if($count2 == 1){
$REFHASH2 = $rs2->fetchrow_hashref;
$tss2serial = &paramsetsql('serial',$REFHASH2);
$resultstr2 = &paramsetsql('resultstr',$REFHASH2);
$result20 = &paramsetsql('result0',$REFHASH2);
$result21 = &paramsetsql('result1',$REFHASH2);
@CAP2 = split(/<>/,&paramsetsql('caption',$REFHASH2));
#画像
@IMGSRC = ();
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH2));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC2[$l] = "<a href='?code=download&s=$tss2serial&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
}	#if count2 == 1
}	#if tss2
if($result10 ne "" || $result11 ne "" || $result20 ne "" || $result21 ne "" ){
$TEAMRESULT{$y}{$x}=<<"END_HTML";
<table cellpadding=2 cellspacing=1 bgcolor="#aaaaaa" class="text-12" width=600>
<tr><td width=50% bgcolor="#ffffff" align=center valign=top nowrap colspan=2>$tss1name</td><td bgcolor="#ffffff" align=center valign=top nowrap colspan=2>$tss2name</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[0]</td><td bgcolor="#ffffff" valign=top>$CAP1[0]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[0]</td><td bgcolor="#ffffff" valign=top>$CAP2[0]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[1]</td><td bgcolor="#ffffff" valign=top>$CAP1[1]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[1]</td><td bgcolor="#ffffff" valign=top>$CAP2[1]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[2]</td><td bgcolor="#ffffff" valign=top>$CAP1[2]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[2]</td><td bgcolor="#ffffff" valign=top>$CAP2[2]</td></tr>
</table>
END_HTML
#print "$tss1 ($result10 ne  && $result11 ne  && $result20 ne  && $result20 ne  ) $tss2<br>\n";
#print "resultstr1=$resultstr1<br>\n";
#print "resultstr2=$resultstr2<br>\n";
#if($resultstr1 == 1){
#$SCORELIST[$cnt3+0] = $result10;
#$SCORELIST[$cnt3+1] = $result11;
#}	#if
#if($resultstr2 == 1){
#$SCORELIST[$cnt3+0] = $result20;
#$SCORELIST[$cnt3+1] = $result21;
#}	#if
$SCORELIST[$cnt3+0] = $result10;
$SCORELIST[$cnt3+1] = $result11;


}	#if
$cnt3+=2;
}	#foreach x
}	#foreach y
###




$cnt = 2;
#チームリストの作成
# エントリーしていて、なおかつ入金済みのチームのみ列挙
$teamlist =<<"END_HTML";
<select name="teamnum%y%:%x%" id="teamnum%y%:%x%">
<option value=''>選択してください</option>
END_HTML
$sql_str1 = "SELECT * FROM entrylist WHERE taikaicode = '$taikaicode' and category = '$category' and payment = 1 ORDER BY lastupdated DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
for($i = 0;$i < $count1;$i++){	# データベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$teamserial = &paramsetsql('teamnum',$REFHASH1);
($teamname,$teamsession) = &taikaiteamname_get3($teamserial);
if($teamname eq ""){next;}	#削除チームは除く
#if( $TEAMLISTTEMP[] == 1){$flag = "disabled";}else{$flag = "";}
$teamlist .=<<"END_HTML";
<option value='$teamserial' %flag$teamserial%>$teamname</option>
END_HTML
}	#for
$teamlist .=<<"END_HTML";
</select>
END_HTML
##
$temp = $teamlist;
$temp =~ s/\%y\%/0/g;
$temp =~ s/\%x\%/1/g;
$temp =~ s/\%flag$TEAMLISTTEMP[0]\%/selected/g;
$temp =~ s/\%flag(.*?)\%//g;
$TEAMLIST{0}{1} = $temp;
$cnt =2;
$k = 1;
foreach $y(1..7){
$list = "";
foreach $x(1..$cnt){
$temp = $teamlist;
$temp =~ s/\%y\%/$y/g;
$temp =~ s/\%x\%/$x/g;
$temp =~ s/\%flag$TEAMLISTTEMP[$k++]\%/selected/g;
$temp =~ s/\%flag(.*?)\%//g;
$TEAMLIST{$y}{$x} = $temp;
}	#foreach x
$cnt *=2;
}	#foreach y
#
open IN,"template/tournament.html";
@TEMPLATE = <IN>;
close IN;
$data = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%teamlist0:1\%/$TEAMLIST{0}{1}/;

foreach $i(1..7){
$line =~ s/\%nichiji$i\%/$NICHIJI{$i}/;
}

$data .= $line;
}	#foreach
$data .= "";
$cnt =2;
$scorecnt=0;
foreach $y(1..7){
$list = "";
foreach $x(1..$cnt){
$data =~ s/\%teamlist$y:$x\%/$TEAMLIST{$y}{$x}/g;
$data =~ s/\%score$y:$x\%/$SCORELIST[$scorecnt++]/g;
$data =~ s/\%teamresult$y:$x\%/$TEAMRESULT{$y}{$x}/g;
}	#foreach x
$cnt *=2;
}	#foreach y
$data .= "";
$data =<<"END_HTML";
<input type="submit" value="登録" style="width:100px;" />
$data
<input type="submit" value="登録" style="width:100px;" />
END_HTML
}	#if
}	#sub




#------------------------------------
#エラー表示
#------------------------------------
sub error {
my ($mes,$flag) = (@_);
if($flag ne ""){print "Content-type: text/html;\n\n";}
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle システムエラー</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<br>
<p><font color=red><b>システムエラー</b></font></p>
<br>
<p>$mes</p>
<br>

<input type=button onclick="javascript:history.back();" value="前に戻る" />
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
exit;
}	#sub


#------------------------------------
# 勝ち点リスト
#------------------------------------
sub kachitenlist {
my ($r) = (@_);
my $flag = "";
my $kachiten =<<"END_HTML";
<select name="resultstr" id="resultstr">
END_HTML
for($n = 10;$n>=-5;$n--){
if($n == $r){$flag = "selected";}else{$flag = "";}
$kachiten .=<<"END_HTML";
<option value='$n' $flag >$n</option>
END_HTML
}	#foteach n
$kachiten .=<<"END_HTML";
</select>点
END_HTML
return $kachiten;
}	#sub



#------------------------------------
# エントリーチーム一覧
#------------------------------------
sub entrylist {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
#枠の確認
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 0 and serial = '$taikaicode' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
if($count == 1){
$REFHASH = $rs->fetchrow_hashref;
$category = &paramsetsql('category',$REFHASH);
}else{
&error("非公開大会はこの項目を扱うことはできません。");
}	#if

### エントリー一覧
$sql_str = "SELECT * FROM entrylist WHERE taikaicode = '$taikaicode' ORDER BY teamnum ASC,category ASC";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($k = 0;$k < $count;$k++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$teamnum = &paramsetsql('teamnum');
$teamname = &taikaiteamname_get($teamnum);
if($teamname eq ""){next;}
$pref = &paramsetsql('pref');
$pr = &paramsetsql2('pr');
$weeklist = &paramsetsql('weeklist');
$weeklist =~ s/:/、/g;
$payment = &paramsetsql('payment');
$category2 = &paramsetsql('category');
%PAYMENTFLAG = ();
$bgcol = "#FFCCCC";
if($payment != 0){$PAYMENTFLAG{$category2} = "checked=checked";$bgcol = "#CCFFCC";}	#if

@TEMP = split(/ /,&paramsetsql('paymentdate'));
$paymentdate = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
if($TEMP[0] == ""){$paymentdate="-";}
@TEMP = split(/ /,&paramsetsql('lastupdated'));
$lastupdated = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
$cate = "";
$cate =<<"END_HTML";
<tr>
<td align=left nowrap id="td$ss" bgcolor="$bgcol">
<input type="checkbox" onclick="ajax_payment($ss)" $PAYMENTFLAG{$category2} id="payment$ss" />$GENRENAME{$category2}</td>
<td align=right nowrap>
<span id="paymentdate$ss">$paymentdate</span>
</td>
</tr>
END_HTML
#
$entrylist .=<<"END_HTML";
<tr>
<td class="s2" bgcolor="#FFFFFF" align=center ><input type="button" value="削除" onclick="urljump_kakunin2('?code=entrydelete&s=$ss&taikaicode=$taikaicode')" /></td>
<td class="s2" bgcolor="#FFFFFF" align=center nowrap >$teamname</td>
<td class="s2" bgcolor="#FFFFFF" align=center >$pref</td>
<td class="s2" bgcolor="#FFFFFF" align=left width=50% >$pr</td>
<td class="s2" bgcolor="#FFFFFF" align=left >$weeklist</td>
<td class="s2" bgcolor="#FFFFFF" align=center nowrap >
<table width=100%>
$cate
</table>
</td>
<td class="s2" bgcolor="#FFFFFF" align=center nowrap >$lastupdated</td>
</tr>
END_HTML
}	#for


###
print <<"END_HTML";
$header
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script>
\$.ajaxSetup({ cache: false });
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に削除してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
function delete_allset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = true;
}	//for
}	// func
function delete_allreset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = false;
}	//for
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg

【エントリーチーム情報】<br>
大会名：<strong>$taikainame</strong><br>
<span class="attention">※入金情報のチェックはリアルタイムに処理されます。特に登録ボタンを押す必要はありません。</span>
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>

<table width="100%" border="0" align="center" cellpadding="1" cellspacing="1" class="text-12" bgcolor="#CC6666">
<tr>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >操作</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >チーム名</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >大会参加希望都道府県</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >活動実績</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >大会参加希望曜日</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >入金状況</td>
<td class="tdpad2" bgcolor="#CC6666" align=center nowrap >エントリー日時</td>
</tr>
$entrylist
</table>

</table>
</td>
</tr>
</table>

<script>
var ajax_flag = 0;
function ajax_payment(ss){
if(ajax_flag == 1){alert("処理中です。お待ちください。");return false;}
ajax_flag = 1;
\$.get("../system.cgi", { code: "ajaxsave_payment", s: ss },
	function(data){
		entryback(data);
});
}	//func

function entryback(data){
//alert(data);
var str = data.split("<>");
if(str[0] == 0){
	document.getElementById('payment'+str[1]).checked = false;
	document.getElementById('td'+str[1]).style.backgroundColor = "#FFCCCC";
}
if(str[0] == 1){
	document.getElementById('payment'+str[1]).checked = true;
	document.getElementById('td'+str[1]).style.backgroundColor = "#CCFFCC";
}
document.getElementById('paymentdate'+str[1]).innerHTML = str[2];
//alert(str[3]);
if(str[0] == 9){
	document.getElementById('attentionmessage').innerHTML = str[3];
}
ajax_flag = 0;
}	//func

</script>
<span id="attentionmessage" style="color:red;"></span>
$footer
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# データの削除処理
# -----------------------------------------------------------------
sub entrydelete {
$taikaicode = $paramhash{'taikaicode'};
$ss = $paramhash{'s'};

if($ss eq ""){	# serialがないとエラー
print "delete error.";
exit;
}	#if

$sql_str = "UPDATE entrylist SET category = 0-category ,taikaicode = 0-taikaicode WHERE serial = $ss";
$rs = $dbh->prepare($sql_str);
$rs->execute();
#
$sestemp = time;

#
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="0;URL=webpal.cgi?code=entrylist&taikaicode=$taikaicode&rnd=$sestemp">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>再読み込み中。。。</p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}



# -----------------------------------------------------------------
# 新規フォーム
# -----------------------------------------------------------------
sub othercontents_newform {
$code = $paramhash{'code'};
$contents = $paramhash{'contents'};
if($contents eq ""){print "contents error by othercontents_newform.";exit;}
#
$sql_str = "SELECT MAX(sortnum) as sortnum FROM $othercontents_dbname WHERE contents = $contents and koukaiflag != 9 ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
$REFHASH = $rs->fetchrow_hashref;
$sortnum = $REFHASH->{'sortnum'} + 1;
#
$nichiji = "<select name=nyear>\n";
$nichiji .= &makeselect($year+1,$year-5,$year);
$nichiji .= "</select>年\n";
$nichiji .= "<select name=nmonth>\n";
$nichiji .= &makeselect(1,12,$month);
$nichiji .= "</select>月\n";
$nichiji .= "<select name=nday>\n";
$nichiji .= &makeselect(1,31,$mday);
$nichiji .= "</select>日\n";
#
$nichiji_from = "<select name=syear>\n";
$nichiji_from .= &makeselect($year+1,$year-5,$year);
$nichiji_from .= "</select>年\n";
$nichiji_from .= "<select name=smonth>\n";
$nichiji_from .= &makeselect(1,12,$month);
$nichiji_from .= "</select>月\n";
$nichiji_from .= "<select name=sday>\n";
$nichiji_from .= &makeselect(1,31,$mday);
$nichiji_from .= "</select>日\n";
#
$nichiji_to = "<select name=eyear>\n";
$nichiji_to .= &makeselect($year+1,$year-5,$year);
$nichiji_to .= "</select>年\n";
$nichiji_to .= "<select name=emonth>\n";
$nichiji_to .= &makeselect(1,12,$month);
$nichiji_to .= "</select>月\n";
$nichiji_to .= "<select name=eday>\n";
$nichiji_to .= &makeselect(1,31,$mday);
$nichiji_to .= "</select>日\n";

#リンク集
$linklist =<<"END_HTML";
<select name=genre id=genre>
<option value=1 >$LINKGENRENAME[1]</option>
<option value=2 >$LINKGENRENAME[2]</option>
<option value=3 >$LINKGENRENAME[3]</option>
<option value=4 >$LINKGENRENAME[4]</option>
<option value=5 >$LINKGENRENAME[5]</option>
<option value=9 >$LINKGENRENAME[9]</option>
</select>
END_HTML

#
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"systemtemplate/$OTHERCONTENTS_FORMFILE[$contents]";
@TEMPLATE = <IN>;
close IN;
#
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%cgifile\%/$cgifile2/;
$line =~ s/\%code\%/othercontents_formadd/;
$line =~ s/\%contents\%/$contents/;
$line =~ s/\%koukaiflag0\%/checked/;
$line =~ s/\%sortnum\%/$sortnum/;
$line =~ s/\%nichiji\%/$nichiji/;
$line =~ s/\%nichiji_from\%/$nichiji_from/;
$line =~ s/\%nichiji_to\%/$nichiji_to/;
$line =~ s/\%title\%/$title/;
$line =~ s/\%body\%/$body/;
$line =~ s/\%linklist\%/$linklist/;

#残り全て空白に
$line =~ s/\%(.*)\%//g;
$str .= $line;
}
print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
■【$OTHERCONTENTSNAME[$contents]】 登録フォーム
$str
</td>
</tr>
</table>
$footer
END_HTML

}


# -----------------------------------------------------------------
# フォーム登録
# -----------------------------------------------------------------
sub othercontents_formadd {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
$koukaiflag = $paramhash{'koukaiflag'} -0;
$sortnum = &paramset('sortnum') -0;
$title = &paramset('title');
$body = &paramset('body');
$genre = &paramset('genre');

if($contents == 100){
$nichiji = sprintf("%04d-%02d-%02d",$paramhash{'nyear'},$paramhash{'nmonth'},$paramhash{'nday'});
	if(!Date::Simple->new($nichiji)){
		&othercontents_error("日付にエラーがあります。「$nichiji」");
	}		#if
$nichiji_from = sprintf("%04d-%02d-%02d",$paramhash{'syear'},$paramhash{'smonth'},$paramhash{'sday'});
	if(!Date::Simple->new($nichiji_from)){
		&othercontents_error("日付にエラーがあります。「$nichiji_from」");
	}		#if
$nichiji_to = sprintf("%04d-%02d-%02d",$paramhash{'eyear'},$paramhash{'emonth'},$paramhash{'eday'});
	if(!Date::Simple->new($nichiji_to)){
		&othercontents_error("日付にエラーがあります。「$nichiji_to」");
	}		#if
	if(Date::Simple->new($nichiji_from) > Date::Simple->new($nichiji_to)){
		&othercontents_error("日付にエラーがあります。「$nichiji_from ～ $nichiji_to」");
	}		#if
}		#if

#DB
if($serial eq ""){
# 新規登録
$sql_str = qq{INSERT INTO $othercontents_dbname(contents,koukaiflag,sortnum,nichiji,nichiji_from,nichiji_to,title,body,genre,createdate) VALUES (?,?,?,?,?,?,?,?,?,?);};
$rs = $dbh->prepare($sql_str);
$rs->execute(
$contents,
$koukaiflag,
$sortnum,
$nichiji,
$nichiji_from,
$nichiji_to,
$title,
$body,
$genre,
$nowdate,
);
}else{
#変更
$title =~ s/\'/\'\'/gm;	#'
$body =~ s/\'/\'\'/gm;	#'

$str = "";
$str.="sortnum = '$sortnum',";
$str.="nichiji = '$nichiji',";
$str.="nichiji_from = '$nichiji_from',";
$str.="nichiji_to = '$nichiji_to',";
$str.="title = '$title',";
$str.="body = '$body',";
$str.="genre = '$genre',";
chop $str;
#
$sql_str = "UPDATE $othercontents_dbname SET koukaiflag = '$koukaiflag',contents = '$contents',$str WHERE serial = $serial";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}	#if
&sqlcheck($sql_str);


#コンテンツ別戻り先
###
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
<!--
function urljump(url){
top.location.href=url;
}
-->
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" class="text-12">
<tr><td>
<center>
<p>登録が完了致しました。</p>
<br>
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('$cgifile2?code=othercontents_newform&contents=$contents')">続けて登録する</button></td>
<td><button onClick="urljump('$cgifile2?code=othercontents_editlist&contents=$contents')">一覧に戻る</button></td>
<td colspan=2><button onClick="urljump('$cgifile2')">トップに戻る</button></td>
</tr>
</table>

</center>
</td>
</tr>
</table>
</td>
</tr>
</table>
$footer
END_HTML
}

# -----------------------------------------------------------------
# 編集リスト
# -----------------------------------------------------------------
sub othercontents_editlist {

$contents = $paramhash{'contents'};

print << "END_HTML";
$header
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に削除してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
function delete_allset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = true;
}	//for
}	// func
function delete_allreset(){
for(i=0;i<document.form1.deleteset.length;i++){
document.form1.deleteset[i].checked = false;
}	//for
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg
END_HTML
# -----------------------------------------------------------------
$allstr = <<"END_HTML";
<a href="javascript:delete_allset()">□全部を選択</a>　
<a href="javascript:delete_allreset();">□全部の選択を解除</a>　
<input type=submit value="変更/登録">　<font color=red size=-1>※一括削除と表示順位設定は一度に処理されます。</font>
END_HTML
#
#
if($contents == 100){	#お知らせ
$sql_str = "SELECT * FROM $othercontents_dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY nichiji DESC, serial DESC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開の有無</td>
<td align=center nowrap>一括削除</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>表示日時</td>
<td align=center nowrap>公開期限</td>
<td align=center width=90% >タイトル</td>
</tr>
END_HTML
}	#if
if($contents == 101){	#リンク集
$genrekeep = 1;
$sql_str = "SELECT * FROM $othercontents_dbname  WHERE contents = $contents and koukaiflag != 9 ORDER BY genre ASC,sortnum DESC, serial DESC";
$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>公開の有無</td>
<td align=center nowrap>一括削除</td>
<td align=center nowrap>表示順</td>
<td align=center nowrap>カテゴリ</td>
<td align=center width=90% >タイトル</td>
</tr>
END_HTML
}	#if
#
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#
print << "END_HTML";
<form action="webpal.cgi" method="post" enctype="multipart/form-data" name="form1" id="form1" onSubmit="return delete_kakunin()" >
<input name="code" type="hidden" id="code" value="othercontents_deleteset" />
<input name="contents" type="hidden" id="contents" value="$contents" />
■【$OTHERCONTENTSNAME[$contents]】 編集<br>
$allstr
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>
<table  border="0" cellpadding="1" cellspacing="1" class="text-12" width=100%>
$disp
END_HTML
#
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$koukaiflag = $REFHASH->{'koukaiflag'};
$contents = $REFHASH->{'contents'};
$sortnum = $REFHASH->{'sortnum'};
$title = &paramsetsql('title');
$genre = &paramsetsql('genre');
#日時
$nichiji = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji')));
$nichiji_from = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji_from')));
$nichiji_to   = sprintf("%d年%d月%d日",split(/-/,&paramsetsql('nichiji_to')));
if($nichiji_from eq $nichiji_to){$nichijistr = "（無期限表示）";}else{$nichijistr = "$nichiji_from ～ $nichiji_to";}
#
if($contents == 100){
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile2?code=othercontents_editform&serial=$serial&contents=$contents\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile2?code=othercontents_deleterecord&serial=$serial&contents=$contents\')">
</td>
<td class="tdpad" nowrap align=center >$KOUKAIFLAG[$koukaiflag] </td>
<td align=center ><input type=checkbox name="deleteset" id="deleteset" value="$serial"></td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$nichiji</td>
<td class="tdpad" nowrap >$nichijistr</td>
<td class="tdpad"  >$title </td>
</tr>
END_HTML
}	#if
if($contents == 101){
if($genre != $genrekeep && $i != 0){
$genrekeep = $genre;
print $disp;
}	#if
print << "END_HTML";
<tr bgcolor="white">
<td nowrap >
<input type=button value="編集" onClick="urljump(\'$cgifile2?code=othercontents_editform&serial=$serial&contents=$contents\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile2?code=othercontents_deleterecord&serial=$serial&contents=$contents\')">
</td>
<td class="tdpad" nowrap align=center >$KOUKAIFLAG[$koukaiflag] </td>
<td align=center ><input type=checkbox name="deleteset" id="deleteset" value="$serial"></td>
<td class="tdpad"><input type=text size=5 name="sortnum" id="sortnum" value="$sortnum"><input type=hidden name="sortnumserial" id="sortnumserial" value="$serial"> </td>
<td class="tdpad" nowrap >$LINKGENRENAME[$genre] </td>
<td class="tdpad" nowrap >$title </td>
</tr>
END_HTML
}	#if

}	#for loop
print << "END_HTML";
</table>
</td>
</tr>
</table>
</form>

END_HTML
print $footer;
}


# -----------------------------------------------------------------
# 編集フォーム
# -----------------------------------------------------------------
sub othercontents_editform {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
if($serial eq ""){
$sql_str = "SELECT * FROM $othercontents_dbname WHERE contents = $contents ";
}else{
$sql_str = "SELECT * FROM $othercontents_dbname WHERE serial = $serial ";
}	#if
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$KFLAG[$REFHASH->{'koukaiflag'}-0] = " checked ";
$sortnum = &paramsetsql('sortnum');
if($sortnum eq ""){$sortnum = 10;}
$title = &paramsetsql('title');
$body = &paramsetsql('body');
$LINKFLAG[&paramsetsql('genre')]="selected";

#日付
($y,$m,$d) = split(/-/,&paramsetsql('nichiji'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji = "<select name=nyear>\n";
$nichiji .= &makeselect($year+1,$y-1,$y);
$nichiji .= "</select>年\n";
$nichiji .= "<select name=nmonth>\n";
$nichiji .= &makeselect(1,12,$m);
$nichiji .= "</select>月\n";
$nichiji .= "<select name=nday>\n";
$nichiji .= &makeselect(1,31,$d);
$nichiji .= "</select>日\n";
#
#日付
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_from'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_from = "<select name=syear>\n";
$nichiji_from .= &makeselect($year+1,$y-1,$y);
$nichiji_from .= "</select>年\n";
$nichiji_from .= "<select name=smonth>\n";
$nichiji_from .= &makeselect(1,12,$m);
$nichiji_from .= "</select>月\n";
$nichiji_from .= "<select name=sday>\n";
$nichiji_from .= &makeselect(1,31,$d);
$nichiji_from .= "</select>日\n";
#
#日付
($y,$m,$d) = split(/-/,&paramsetsql('nichiji_to'));
if($y eq "" || $y eq "0000"){$y =$year;$m =$month;$d =$mday;}
$nichiji_to = "<select name=eyear>\n";
$nichiji_to .= &makeselect($year+1,$y-1,$y);
$nichiji_to .= "</select>年\n";
$nichiji_to .= "<select name=emonth>\n";
$nichiji_to .= &makeselect(1,12,$m);
$nichiji_to .= "</select>月\n";
$nichiji_to .= "<select name=eday>\n";
$nichiji_to .= &makeselect(1,31,$d);
$nichiji_to .= "</select>日\n";
#リンク集
$linklist =<<"END_HTML";
<select name=genre id=genre>
<option value=1 $LINKFLAG[1]>$LINKGENRENAME[1]</option>
<option value=2 $LINKFLAG[2]>$LINKGENRENAME[2]</option>
<option value=3 $LINKFLAG[3]>$LINKGENRENAME[3]</option>
<option value=4 $LINKFLAG[4]>$LINKGENRENAME[4]</option>
<option value=5 $LINKFLAG[5]>$LINKGENRENAME[5]</option>
<option value=9 $LINKFLAG[9]>$LINKGENRENAME[9]</option>
</select>
END_HTML
#
#　テンプレートの読み込み　>> @TEMPLATE
open IN,"systemtemplate/$OTHERCONTENTS_FORMFILE[$contents]";
@TEMPLATE = <IN>;
close IN;
#
my $str = "";
foreach my $line(@TEMPLATE){
utf8::decode($line);
$line =~ s/\%cgifile\%/$cgifile2/;
$line =~ s/\%serial\%/$serial/;
$line =~ s/\%code\%/othercontents_formadd/;
$line =~ s/\%koukaiflag0\%/$KFLAG[0]/;
$line =~ s/\%koukaiflag1\%/$KFLAG[1]/;
$line =~ s/\%contents\%/$contents/;
$line =~ s/\%sortnum\%/$sortnum/;
$line =~ s/\%nichiji\%/$nichiji/;
$line =~ s/\%nichiji_from\%/$nichiji_from/;
$line =~ s/\%nichiji_to\%/$nichiji_to/;
$line =~ s/\%title\%/$title/;
$line =~ s/\%body\%/$body/;
$line =~ s/\%linklist\%/$linklist/;
$str .= $line;
}	#foreach
print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
■【$OTHERCONTENTSNAME[$contents]】  編集
$str
</td>
</tr>
</table>
$footer
END_HTML

}


# -----------------------------------------------------------------
# データの削除処理
# -----------------------------------------------------------------
sub othercontents_deleterecord {
$serial = $paramhash{'serial'};
$contents = $paramhash{'contents'};
if($serial eq ""){	# serialがないとエラー
print "serial error.";
exit;
}	#if

$sql_str = "UPDATE $othercontents_dbname SET koukaiflag = 9 WHERE serial = $serial";
$rs = $dbh->prepare($sql_str);
$rs->execute();

print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="0;URL=$cgifile2?code=othercontents_editlist&contents=$contents">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>再読み込み中。。。</p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}

# -----------------------------------------------------------------
# データの一括削除処理
# -----------------------------------------------------------------
sub othercontents_deleteset {
@SS = $query->param('deleteset');
@SN = $query->param('sortnum');
@SNS = $query->param('sortnumserial');
$contents = $paramhash{'contents'};
if($contents eq ""){	# contentsがないとエラー
print "contents error.";
exit;
}	#if
#一括削除
foreach $line(@SS){
$sql_str = "UPDATE $othercontents_dbname SET koukaiflag = 9 WHERE serial = $line";
$rs = $dbh->prepare($sql_str);
$rs->execute();
}	#for
#表示順位
$i=0;
foreach $line(@SNS){
$sql_str = "UPDATE $othercontents_dbname SET sortnum = $SN[$i] WHERE serial = $line";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$i++;
}	#for

print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Refresh" content="3;URL=$cgifile2?code=othercontents_editlist&contents=$contents">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>処理を行いました。</p>
<p>３秒後に再読み込みします。</p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}



# -----------------------------------------------------------------
# エラー表示
# -----------------------------------------------------------------
sub othercontents_error {
my ($str,$flag) = (@_);
if($flag ne ""){print "Content-type: text/html;\n\n";}	#if
###
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle システムエラー</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p><font color=red><b>$str</b></font></p>
</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
exit;
}	#sub




# -----------------------------------------------------------------
# 過去の大会
# -----------------------------------------------------------------
sub passedconvention {
$ty = $paramhash{'ty'};
if($ty eq ""){$ty = $year;}
$nn = " and (nichiji1 like '$ty-%')";

$nichiji = "<select name=ty>\n";
$nichiji .= &makeselect($year,2011,$ty);
$nichiji .= "</select>年\n";
$yearlist =<<"END_HTML";
<form action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="passedconvention" />
対象年：$nichiji
<input type="submit" value="検索" />
</form>
END_HTML
# 大会リスト
$sql_str = "SELECT * FROM $dbname WHERE contents = 0 and koukaiflag = 1 $nn ORDER BY sortnum ASC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$serial = $REFHASH->{'serial'};
$title = &paramsetsql('title');
$category = &paramsetsql('category');
$genre1 = &paramsetsql('genre1');
$genrename1 = $GENRENAME{$genre1};
$genre2 = &paramsetsql('genre2');
$genrename2 = $GENRENAME{$genre2};
$price1 = &ketakanma(&paramsetsql('price1'));
$price2 = &ketakanma(&paramsetsql('price2'));
$price3 = &ketakanma(&paramsetsql('price3'));
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

###
$list .=<<"END_HTML";
<table width="100%" border="0" align="center" cellpadding="1" cellspacing="1" class="text-12" bgcolor="#cccccc">
<tr class="s2" bgcolor="#73d783">
<td align=center >大会画像</td>
<td align=center nowrap  width=80%>概要</td>
</tr>
<tr bgcolor="white">
<td class="tdpad" valign=top align=center>$IMGSRC[$j] </td>
<td class="tdpad" valign=top nowrap >
大会名：<strong>$title</strong><br>
登録日：$nichiji1<br>
<input type=button value="編集" onClick="urljump(\'$cgifile?code=editform&serial=$serial&contents=0\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=deleterecord&serial=$serial&contents=0\')">
</td>
</tr>
</table>
<br>
END_HTML
}	#for i

print <<"HTML_VIEW";
$header
<table width="90%" border="0" cellpadding="2" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<br>
$yearlist
$list
$footer
HTML_VIEW

exit;
}	#sub





# -----------------------------------------------------------------
# 登録チーム一覧
# -----------------------------------------------------------------
sub teamlist {
$attention0 = "（最新の50チームを表示）";
$limit = " LIMIT 50";

$sy = $paramhash{'syear'};
$sm = $paramhash{'smonth'};
$keyword = $paramhash{'keyword'};
if($keyword ne ""){
$attention0 = "";
$attention = "（チーム名に「$keyword」を含む）";
$keyword =~ s/　/ /g;
$temp = "";
foreach (split(/ /,$keyword)){
$_ =~ s/'/''/gm;	#'
$temp .= " teamname like '%$_%' or";
}	#foreach
chop($temp);
chop($temp);
$keywordstr = " and ($temp) ";
}	#if

$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center nowrap >操作</td>
<td align=center nowrap>活動</td>
<td align=center width=90% >チーム名</td>
<td align=center nowrap >本登録年月日</td>
</tr>
END_HTML
##
if($sy != 0){
$attention0 = "";
$attention .= "（${sy}年${sm}月 登録のチーム）";
$limit = "";
$n = sprintf("%04d-%02d",$sy,$sm);
$nn = " and ( createdate like '$n%' ) ";
}	#if

$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and ( koukaiflag = 0 or koukaiflag = 1 ) $keywordstr $nn ORDER BY createdate DESC $limit";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$ses = &paramsetsql('ssid');
$email = &paramsetsql('mailadr1').'@'.&paramsetsql('mailadr2');
$pwd = &paramsetsql('pwd');
$teamname = &paramsetsql('teamname');
$koukaiflag = &paramsetsql('koukaiflag');
@TEMP = split(/ /,&paramsetsql('createdate'));
$createdate = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
$katsudou = $KATSUDOUNAME{&paramsetsql('koukaiflag')};
if($koukaiflag == 1){$katsudou = "<span style='color:red;'>$katsudou</span>";}	#if
##
$list .=<<"HTML_END";
<tr>
<td align=center bgcolor="#FFFFFF" class="tdpad" nowrap>
<input type=button value="編集" onClick="urljump(\'$cgifile?code=team_edit&ss=$ss&ses=$ses\')">
<input type=button value="削除" onClick="urljump_kakunin2(\'$cgifile?code=team_delete&serial=$ss&ses=$ses\')">
<input type=button value="ログイン" onClick="windowopen(\'../system.cgi?code=mypagelogin&email=$email&psw=$pwd\',1000,800)">
</td>
<td align=center bgcolor="#FFFFFF" class="tdpad" nowrap>$katsudou</td>
<td align=left bgcolor="#FFFFFF" class="tdpad">$teamname</td>
<td align=center bgcolor="#FFFFFF" class="tdpad" nowrap>$createdate</td>
</tr>
HTML_END

}	#for
#日付
#if($sy == 0){$sy =$year;$sm =$month;}
$nichiji = "<select name=syear>\n";
$nichiji .= "<option value=''>年を選択</option>\n";
$nichiji .= &makeselect($year,$year-10,,$sy);
$nichiji .= "</select>年\n";
$nichiji .= "<select name=smonth>\n";
$nichiji .= "<option value=''>月を選択</option>\n";
$nichiji .= &makeselect(1,12,$sm);
$nichiji .= "</select>月\n";

###
print << "END_HTML";
$header
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に抹消してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg

■登録チーム 編集<span style="color:red;font-size:12px;">$attention0$attention</span><br>
<table>
<tr>
<td>
<form name="form0" action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="teamlist" />
$nichiji
<input type="submit" value="検索" />
</form>
</td><td>
<form name="form0" action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="teamlist" />
<input type="text" name="keyword" size=20 value="$keyword" />
<input type="submit" value="検索" />
</form>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>
<table  border="0" cellpadding="1" cellspacing="1" class="text-12" width=100%>
$disp
$list
</table>
</td>
</tr>
</table>
</form>
$footer
END_HTML

exit;
}	#sub






# -----------------------------------------------------------------
# チーム：編集
# -----------------------------------------------------------------
sub team_edit {
$ss = $paramhash_dec{"ss"};
$ses = $paramhash_dec{"ses"};

foreach $n(0..29){
$TMNAME[$n] = $paramhash_dec{"teammember_name$n"};
$TMNUM[$n] = $paramhash_dec{"teammember_num$n"};
$TMPOSITION[$n] = $paramhash_dec{"teammember_position$n"};
}	#foreach

#リライト？
if($paramhash{'rewrite'} != 1){
#チーム情報のGET
$sql_str = "SELECT * FROM member_tbl WHERE contents = 21 and serial = '$ss' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
$count = $rs->rows;	# Hit件数を確保
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
$paramhash_dec{'koukaiflag'} = &paramsetsql('koukaiflag');
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
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=./file/$TEMP[0]pda.jpg>$sfn<br>";}
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
if( $TEMP[1] eq "jpg"){$IMGSRC[$i] = "<img src=./file/$TEMP[0]pda.jpg>$sfn<br>";}
$FILENAME[$i] = "<input type=hidden name=\"filename$i\" id=\"filename$i\" value=\"$IMGTEMPS[$i]\" >";
$FILEDELETE[$i] = "<input type=checkbox name=\"filedelete$i\" id=\"filedelete$i\" value=1 >登録ファイルの消去";
}	#if 存在
}	#foreach
}	#if rewrite

$KATSUDOFLAG{$paramhash_dec{'koukaiflag'}} = "checked=checked";

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
<form action="$cgifile" name="form1" method="post" enctype="multipart/form-data" />
<input type="hidden" name="code" value="team_check" />
<input type="hidden" name="ss" value="$ss" />
<input type="hidden" name="ses" value="$ses" />
<table width="100%" cellspacing="1" cellpadding="2" bgcolor="#aaaaaa">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">活動</font><font class="type1" color="#ff0000">*</font></td>
<td width="76%" align="left" bgcolor="#ffffff">
<input name="koukaiflag" type="radio" id="koukaiflag0" value="0" $KATSUDOFLAG{0} />活動中　
<input name="koukaiflag" type="radio" id="koukaiflag1" value="1" $KATSUDOFLAG{1} />凍結
<input name="koukaiflag" type="radio" id="koukaiflag1" value="9" $KATSUDOFLAG{9} />削除
</td>
</tr>
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
<td align="left" bgcolor="#ffffff"><input name="_チーム結成年" type="text" id="team_year" value="$paramhash_dec{'_チーム結成年'}" size="4" />
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
郵便番号<input name="_郵便番号" type="text" id="katsudou_week" value="$paramhash_dec{'_郵便番号'}" size="10" />
都道府県 <select name="_都道府県名">
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
<td align="left" bgcolor="#ffffff"><input name="_代表者メールアドレス" type="text" id="mailadr1" value="$paramhash_dec{'_代表者メールアドレス'}" size="20" />
＠
<input name="_代表者メールアドレス（ドメイン）" type="text" id="mailadr2" value="$paramhash_dec{'_代表者メールアドレス（ドメイン）'}" size="20" />
<br />
※PC、携帯どちらのアドレスでも構いません。</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者電話番号</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_代表者電話番号" type="text" id="tel1" value="$paramhash_dec{'_代表者電話番号'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">代表者住所</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff">
都道府県 <select name="_代表者都道府県名">
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
　市区町村
<input name="_代表者住所" type="text" id="cities1" value="$paramhash_dec{'_代表者住所'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font><font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名" type="text" id="shimei2" value="$paramhash_dec{'_第2担当者氏名'}" size="20" /></td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">第2担当者氏名</font>（フリガナ）<font class="type1" color="#ff0000">*</font></td>
<td align="left" bgcolor="#ffffff"><input name="_第2担当者氏名（フリガナ）" type="text" id="tel2" value="$paramhash_dec{'_第2担当者氏名（フリガナ）'}" size="20" />
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
<td align="left" bgcolor="#ffffff"><input name="LINEID" type="text" id="lineid" value="$paramhash_dec{'LINEID'}" size="20" /><br>
メールアプリLINE（ライン）をお使いの方は、LINEのIDをチーム間の連絡用としてチームページに表示させることができます。<br>
※このIDは、プライドジャパンにログインしている全てのチームが閲覧可能になります。
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム写真</font></td>
<td align="left" bgcolor="#ffffff">
<input type="file" name="file0" />$IMGSRC[0]$FILENAME[0]$FILEDELETE[0]
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメンバー紹介</font></td>
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
<center>
<input type="submit" value="　　確認画面へ　　" />
</center>
</form>
END_HTML

print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
$mes
</td>
</tr>
</table>
$footer
END_HTML
exit;
}	#sub



# -----------------------------------------------------------------
# チーム：確認
# -----------------------------------------------------------------
sub team_check {
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
<form action="$cgifile" name="form2" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="team_edit" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" />
</form>
END_HTML
&error($mes);
exit;
}	#if

#監督メルアド重複チェック2015.7.8
$email1  = $paramhash_dec{'_代表者メールアドレス'};
$email1 .= '@'.$paramhash_dec{'_代表者メールアドレス（ドメイン）'};
$ss = $paramhash_dec{'ss'};
$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 0 and mailaddress1 = '$email1' and serial != '$ss' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#print "$sql_str";
if($count != 0){
$mes =<<"END_HTML";
代表者メールアドレスの重複があります。<br>
<form action="$cgifile" name="form2" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="team_edit" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="修正する" />
</form>
END_HTML
&error($mes);
exit;
}



# 添付ファイルの登録処理
#print "f=".$paramhash{"file0"}."<br>\n";
if($paramhash{"file0"} ne ""){$file = &fileup("file0",21);}else{$file = $paramhash{"filename0"};}
#print "file=".$file."<br>\n";
if($paramhash{"filedelete0"} == 1){$file = "";}else{
#画像
if($file ne ""){
@TEMP = split(/<>/,$file);
@TEMP = split(/\./,$TEMP[1]);
$IMGSRC[0] = "<img src='./file/$TEMP[0]pda.jpg'>$sfn<br>";
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
<table width="100%" cellspacing="1" cellpadding="2" bgcolor="#aaaaaa">
<tbody>
<tr>
<td width="24%" align="center" bgcolor="#F2F2F2"><font class="type1">活動</font></td>
<td width="76%" align="left" bgcolor="#ffffff">$KATSUDOUNAME{$paramhash{'koukaiflag'}}</td>
</tr>
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
$paramhash_dec{'_郵便番号'} $paramhash_dec{'_都道府県名'} $paramhash_dec{'_主な活動場所'}</td>
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
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チーム写真</font></td>
<td align="left" bgcolor="#ffffff">&nbsp;
$IMGSRC[0]$FILENAME[0]$FILEDELETE[0]
</td>
</tr>
<tr>
<td align="center" bgcolor="#F2F2F2"><font class="type1">チームメンバー紹介</font></td>
<td align="left" bgcolor="#ffffff">
$teammemberlist
</td>
</tr></tbody>
</table>

<table align=center style="border:none;">
<tr>
<td style="border:none;">
<form action="$cgifile" name="form2" method="POST" enctype="multipart/form-data" />
<input type="hidden" name="code" value="team_edit" />
<input type="hidden" name="rewrite" value="1" />
$rewritestr
<input type="submit" value="　　修正する　　" />
</form>
</td>
<td style="border:none;">
</td>
<td style="border:none;">
<form action="$cgifile" name="form1" method="POST" enctype="multipart/form-data" />
<input type="hidden" name="code" value="team_add" />
$rewritestr
<input type="submit" value="　　送信する　　" />
</form>
</td>
</tr>
</table>
END_HTML

###
print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
$mes
</td>
</tr>
</table>
$footer
END_HTML
exit;
}	#sub


# -----------------------------------------------------------------
# チーム：登録
# -----------------------------------------------------------------
sub team_add {
$ss = $paramhash_dec{'ss'};
$ses = $paramhash_dec{'ses'};
$koukaiflag = $paramhash_dec{'koukaiflag'};
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
$str.="koukaiflag = '$koukaiflag',";
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
$sql_str = "UPDATE $member_tbl SET $str WHERE serial = '$ss' and ssid = '$ses' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
###
$mes =<<"END_HTML";
<p align="center" style="color:red;font-weight:bold;font-size:20px;">修正登録完了</p>
<p align="center">
<input type="button" value="TOPへ戻る" onclick="location.href='$cgifile';" />
<input type="button" value="登録チーム一覧へ戻る" onclick="location.href='$cgifile?code=teamlist';" />
</p>
END_HTML

###
print << "END_HTML";
$header
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
$mes
</td>
</tr>
</table>
$footer
END_HTML
exit;

exit;
}	#sub






# -----------------------------------------------------------------
# チームの削除処理
# -----------------------------------------------------------------
sub team_delete {
$serial = $paramhash{'serial'};
$ses = $paramhash{'ses'};
if($serial eq "" || $ses eq ""){	# serialがないとエラー
print "serial error.";
exit;
}	#if

$sql_str = "UPDATE $member_tbl SET koukaiflag = 9 WHERE serial = $serial and  ssid = '$ses'";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
#
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
<!--
function urljump(url){
top.location.href=url;
}
-->
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td align=cente>
$webpalimg
<center>
<p>チームを削除しました。</p>
<table border="0" cellspacing="1" cellpadding="1" align="center" >
<tr>
<td><button onClick="urljump('$cgifile?code=teamlist')">一覧に戻る</button></td>
</tr>
</table>

</center>
</td>
</tr>
</table>
</body>
</html>
END_HTML
}





# -----------------------------------------------------------------
# 書類のDownload
# -----------------------------------------------------------------
sub download {
#print "Content-type: text/html;\n\n";
$ds = $paramhash{'s'};
$num = $paramhash{'n'};
if($ds eq ""){	# serialがないとエラー
&error("serial error.",1);
exit;
}	#if
#GET
$sql_str = "SELECT * FROM $dbname WHERE serial = '$ds' ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);	#SQLチェック
$count = $rs->rows;	# Hit件数を確保
if($count < 1 ){	# serialがないとエラー
&error("count error.",1);
exit;
}	#if
$REFHASH = $rs->fetchrow_hashref;
if(&paramsetsql('koukaiflag') != 0){
&error("指定のファイルが用意されておりません。",1);
}	#if
#ダウンロードファイル
@IMGSRCTEMP = split(/:/,&paramsetsql('upfilename'));
$fn = $IMGSRCTEMP[$num];
if($fn eq ""){
&error("DB filename error.",1);
exit;
}	#if
#return "$sfn<>$sfilename<>$mimetype";
($sfilename,$tfn,$mimetype) = split(/<>/,$fn);
($temp,$ext) = split(/\./,$tfn);
$serverfile = $attach_dir."/".$tfn;	#サーバー上でのファイル名
#
if ($ENV{'HTTP_USER_AGENT'} =~ /MSIE/ ) {
$sfilename = Unicode::Japanese->new($sfilename)->sjis;		#SJISとして処理
}	#if
#if ($ENV{'HTTP_USER_AGENT'} =~ /Safari/) {$sfilename = "";}
#データのREAD
open IN,$serverfile or &error("ファイルが見つかりません。<p>ダウンロードファイル名：$sfilename<br>ファイル種別：$mimetype<br>サーバーファイル情報：$tfn",1);;
binmode(IN);
$size = read(IN,$data,-s $serverfile);
close(IN);
if($size eq "" || $size <=0){&error("ファイルサイズが不正です。<p>ダウンロードファイル名：$sfilename<br>ファイル種別：$mimetype<br>サーバーファイル情報：$tfn,",1);}
binmode(STDOUT);
#
print "Content-type: $mimetype\n";
print "Content-Disposition: attachment; filename=\"$sfilename\"\n\n";
#print "Content-Length: $size\n\n";
print $data;

}	#sub



# -----------------------------------------------------------------
# csvのDownload
# -----------------------------------------------------------------
sub csvdownload {
#print "Content-type: text/html;\n\n";

$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 0 and mailmagazine = 1 ORDER BY serial ASC";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#print $count;
$csvdata =<<"HTML_END";
"チーム名","チームメールアドレス","代表者名","代表者メールアドレス"
HTML_END

for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$ses = &paramsetsql('ssid');
$shimei1 = &paramsetsql('shimei1');
$mailaddress1 = &paramsetsql('mailaddress1');
$teamname = &paramsetsql('teamname');
$mailaddress2 = &paramsetsql('mailaddress2');
$csvdata .= "\"$teamname\",\"$mailaddress2\",\"$shimei1\",\"$mailaddress1\"\n";
}	#for
##
$csvdata =~ s/\n/\r\n/g;
$csvdata = Unicode::Japanese->new($csvdata,"utf8")->sjis;

$nichiji = sprintf("%04d%02d%02d%02d%02d%02d",$year,$month,$mday,$hour,$min,$sec);

print "Content-type: application/x-csv\n";
print "Content-Disposition: attachment; filename=\"mailmagazine_teamlist$nichiji.csv\"\n\n";
print $csvdata;

exit;

}	#sub







# -----------------------------------------------------------------
# 仮登録チーム一覧
# -----------------------------------------------------------------
sub nonteamlist {
$sy = $paramhash{'syear'};
$sm = $paramhash{'smonth'};

$disp =<< "END_HTML";
<tr class="s2" bgcolor="#73d783">
<td align=center >チーム名</td>
<td align=center >代表者氏名</td>
<td align=center >代表者電話番号</td>
<td align=center >メールアドレス</td>
<td align=center nowrap >仮登録年月日</td>
</tr>
END_HTML
##
if($sy == 0){
$attention = "（最新の50チームを表示）";
$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 2 ORDER BY serial DESC LIMIT 50";
}else{
$attention = "（${sy}年${sm}月 登録のチーム）";
$n = sprintf("%04d-%02d",$sy,$sm);
$sql_str = "SELECT * FROM $member_tbl WHERE contents = 21 and koukaiflag = 2 and timestamp like '$n%' ORDER BY serial DESC";
}	#if

$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$ss = &paramsetsql('serial');
$ses = &paramsetsql('ssid');
$shimei1 = &paramsetsql('shimei1');
$mailaddress1 = &paramsetsql('mailaddress1');
$tel1 = &paramsetsql('tel1');
$teamname = &paramsetsql('teamname');
$koukaiflag = &paramsetsql('koukaiflag');
@TEMP = split(/ /,&paramsetsql('timestamp'));
$createdate = sprintf("%d年%d月%d日 %d時%d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
##
$list .=<<"HTML_END";
<tr>
<td align=left bgcolor="#FFFFFF" class="tdpad">$teamname</td>
<td align=left bgcolor="#FFFFFF" class="tdpad">$shimei1</td>
<td align=left bgcolor="#FFFFFF" class="tdpad">$tel1</td>
<td align=left bgcolor="#FFFFFF" class="tdpad">$mailaddress1</td>
<td align=center bgcolor="#FFFFFF" class="tdpad" nowrap>$createdate</td>
</tr>
HTML_END

}	#for
#日付
if($sy == 0){$sy =$year;$sm =$month;}
$nichiji = "<select name=syear>\n";
$nichiji .= &makeselect($year-10,$year,$sy);
$nichiji .= "</select>年\n";
$nichiji .= "<select name=smonth>\n";
$nichiji .= &makeselect(1,12,$sm);
$nichiji .= "</select>月\n";

###
print << "END_HTML";
$header
<script>
function urljump(url){
top.location.href=url;
}
function urljump_kakunin2(url){
if (window.confirm("この作業は元に戻す事が出来ません。\\n本当に抹消してもよろしいですか")) {
	top.location.href=url;
}
}
function delete_kakunin(){
if (window.confirm("この作業は元に戻す事が出来ません。\\nよろしいですか")) {return true;}else{return false;}
}	// func
</script>
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr><td>
$webpalimg

■<span style="color:red;font-weight:bold;">仮登録チーム</span> 一覧 $attention<br>
<form name="form1" action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="code" value="nonteamlist" />
$nichiji
<input type="submit" value="検索" />
</form>
<table border="0" cellpadding="0" cellspacing="0" bgcolor="#666666" class="text-12" width="100%" align=center>
<tr class="s2" bgcolor="gray"><td>
<table  border="0" cellpadding="1" cellspacing="1" class="text-12" width=100%>
$disp
$list
</table>
</td>
</tr>
</table>
</form>
$footer
END_HTML

exit;
}	#sub




# -----------------------------------------------------------------
# 順位／星取り表
# -----------------------------------------------------------------
sub ranking2 {
$taikaicode = $paramhash{'taikaicode'};
$taikainame = &taikainame_get($taikaicode);
if($taikainame =~ /不明/){
$mes =<<"END_HTML";
大会情報が取得できませんでした。
END_HTML
&mypagehtmldisp($mes);
exit;
}	#if
$s_area = $paramhash{'area'};
$s_kumi = $paramhash{'kumi'};
$s_categorey = $paramhash{'categorey'};

&kachi2($s_categorey,$s_area,$s_kumi);


########################
########################
print << "END_HTML";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$sitetitle</title>
<link href="systemstyle.css" rel="stylesheet" type="text/css">
<script>
<!--
function urljump(url){
top.location.href=url;
}
-->
</script>
</head>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="90%" border="0" cellpadding="4" cellspacing="0" align=center>
<tr>
<td>
$webpalimg
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" class="text-12">
<tr><td>
<center>
$taikainame
<div id="mainbox">
<div id="pnl">
<div class="pnl">$areatag2</div>
</div>
$arealist2
</div>
</center>
</td>
</tr>
</table>
</td>
</tr>
</table>
$footer
END_HTML
exit;
}	#sub



# -----------------------------------------------------------------
# 順位計算
# -----------------------------------------------------------------
sub kachi {

##########################################################
# リーグ
##########################################################
#「勝ち点表」を大会データからGET
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 40 and koukaiflag = 0 and taikaicode = $taikaicode ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);	#SQLエラーチェック
$count3 = $rs3->rows;	# Hit件数を確保
if($count3 != 0){
$REFHASH3 = $rs3->fetchrow_hashref;
@KACHITENHYO = split(/:/,&paramsetsql('resultstr',$REFHASH3));

#エリアGET：ループ
@AREANUM = ();
%KUMINUM = ();
@TSS = ();

%AREASTR = ();
$sql_str = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  ORDER BY sortnum ASC, serial DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#print "count=$count<br>\n";
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$area = &paramsetsql('serial');
push(@AREANUM,$area);
$AREASS{$area} = &paramsetsql('title');
$AREASTR{$area} = "<h2 class='subti' id='$area'>$AREASS{$area}</h2>";
#組GET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 31 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
for($k = 0;$k < $count1;$k++){	# 組GETデータベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$kumi = &paramsetsql('serial',$REFHASH1 );
$KUMISS{$kumi} = &paramsetsql('title',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
$KUMINUM{$area} .= $kumi.":";
%TY = ();
# 組に登録されたチームをGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' ORDER BY serial ASC ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
&sqlcheck($sql_str2);
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>\n";
@TSS = ();
for($m = 0;$m < $count2;$m++){	# データベース１件ずつ
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH2);
push(@TSS,$teamnum);
$TY{$teamnum} = $m;
$TNAME{$teamnum} = &taikaiteamname_get($teamnum);
}	#for m

# 対戦組み合わせデータGET
%RDATA1 =();
%RDATA2 =();
%HOSI = ();
$teamcount = @TSS;
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
$count3 = $rs3->rows;	# Hit件数を確保
#print "count3=$count3<br>\n";
for($j=0;$j<$count3;$j++){
$REFHASH3 = $rs3->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH3);
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
#print $temp."<br>\n";
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
$RDATA1{$setu}{$num} = $tss1;
$RDATA2{$setu}{$num} = $tss2;
}	#foreach

###################
#print "teamcount=$teamcount<br>\n";
%HOSI = ();
%KACHISU = ();
%MAKESU = ();
%WAKESU = ();
%TOKUTEN = ();
%SITTEN = ();
%SIAISU = ();
%KACHITEN = ();

###################
# >>試合結果
# チームserialからチームsessionをGET
foreach $ss(@TSS){
#print "ss=$ss<br>\n";
$sql_str3 = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and serial = '$ss' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);
$count3 = $rs3->rows;	# Hit件数を確保
if($count3 != 0){
#print "count3=$count3<br>\n";
$REFHASH3 = $rs3->fetchrow_hashref;
$ses = &paramsetsql('ssid',$REFHASH3);
$SERI2SES{$ss} = $ses;
$SES2SERI{$ses} = $ss;
}	#count3
}	#foreach
#
$result ="";
foreach $setu(1..7){
$temp = "";
#
#得点表
#$half = int($teamcount/2);
foreach $num(1..4){
$tname1 = $TNAME{$RDATA1{$setu}{$num}};	#$RDATA1{$setu}{$num} はチームserial
$tname2 = $TNAME{$RDATA2{$setu}{$num}};	#$RDATA1{$setu}{$num} はチームserial

# 試合の報告をGET
@SES = ();
%RESULTSTR = ();
%RESULTSTR2 = ();
%RESULT0 = ();
%RESULT1 = ();
%SENPYO = ();
%COMMENT = ();


$sql_str3 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' and title = '$setu' and text1 = '$num' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);
$count3 = $rs3->rows;	# Hit件数を確保
for($i3=0;$i3<$count3;$i3++){
$REFHASH3 = $rs3->fetchrow_hashref;
$session = &paramsetsql('linkadr',$REFHASH3);
$ss = $SES2SERI{$session};
push(@SES,$session);
$teamnum = &paramsetsql('teamnum',$REFHASH3);
$RESULTSTR{$setu}{$num}{$ss} = &paramsetsql('resultstr',$REFHASH3);		#戦績
$RESULTSTR2{$setu}{$num}{$ss} = &paramsetsql('resultstr2',$REFHASH3);	#その他情報
$RESULT0{$setu}{$num}{$ss} = &paramsetsql('result0',$REFHASH3);			#スコア（自）
$RESULT1{$setu}{$num}{$ss} = &paramsetsql('result1',$REFHASH3);			#スコア（他）
$SENPYO{$setu}{$num}{$ss} = &paramsetsql2('senpyo',$REFHASH3);
$COMMENT{$setu}{$num}{$ss} = &paramsetsql('comment',$REFHASH3);
$POSI{$setu}{$num}{$ss} = &paramsetsql('linkadrtitle',$REFHASH3);	#報告位置
}	#for

#
$resultstr1 = $RESULTSTR{$setu}{$num}{$RDATA1{$setu}{$num}};
$resultstr2 = $RESULTSTR{$setu}{$num}{$RDATA2{$setu}{$num}};

$tokuten1 = $RESULT0{$setu}{$num}{$RDATA1{$setu}{$num}};
$tokuten2 = $RESULT1{$setu}{$num}{$RDATA1{$setu}{$num}};

#相違がある場合
if( ($POSI{$setu}{$num}{$RDATA1{$setu}{$num}} == 0 && $POSI{$setu}{$num}{$RDATA2{$setu}{$num}} == 1) || ($POSI{$setu}{$num}{$RDATA2{$setu}{$num}} == 0 && $POSI{$setu}{$num}{$RDATA1{$setu}{$num}} == 1) ){
if( ($RESULT0{$setu}{$num}{$RDATA1{$setu}{$num}} != $RESULT0{$setu}{$num}{$RDATA2{$setu}{$num}} || $RESULT1{$setu}{$num}{$RDATA1{$setu}{$num}} != $RESULT1{$setu}{$num}{$RDATA2{$setu}{$num}}) && ($resultstr1 != 4 && $resultstr1 != 5) ){next;}
}	#if
if( ($POSI{$setu}{$num}{$RDATA1{$setu}{$num}} == 0 && $POSI{$setu}{$num}{$RDATA2{$setu}{$num}} == 0) && ($POSI{$setu}{$num}{$RDATA2{$setu}{$num}} == 0 && $POSI{$setu}{$num}{$RDATA1{$setu}{$num}} == 0) ){
if( ($RESULT0{$setu}{$num}{$RDATA1{$setu}{$num}} != $RESULT1{$setu}{$num}{$RDATA2{$setu}{$num}} || $RESULT1{$setu}{$num}{$RDATA1{$setu}{$num}} != $RESULT0{$setu}{$num}{$RDATA2{$setu}{$num}}) && ($resultstr1 != 4 && $resultstr1 != 5) ){next;}
}	#if


#相違がある場合
#if($result10 != $result21 || $result11 != $result20 ){next;}



=pot
print <<"HTML_END";
<pre>
setu = $setu
num = $num
RDATA1 = $RDATA1{$setu}{$num}
RDATA2 = $RDATA2{$setu}{$num}
RESULT0 = $RESULT0{$setu}{$RDATA1{$setu}{$num}}
RESULT1 = $RESULT1{$setu}{$RDATA2{$setu}{$num}}
tokuten1 = $tokuten1
tokuten2 = $tokuten2
</pre>
HTML_END
=cut
$marubatu1 = "-";$marubatu2 = "-";
$winnercomment = "";
$comment1 = "$COMMENT{$setu}{$num}{$RDATA1{$setu}{$num}}（$tname1）";
$comment2 = "$COMMENT{$setu}{$num}{$RDATA2{$setu}{$num}}（$tname2）";

#報告のある結果のみ表示
if($resultstr1 ne "" && $resultstr2 ne ""){


#print "resultstr1=$resultstr1 , resultstr2=$resultstr2<br>";
$y = $TY{$RDATA1{$setu}{$num}};
$x = $TY{$RDATA2{$setu}{$num}};
#引き分け
if($resultstr1 == 3 && $resultstr2 == 3 ){
$marubatu1 = "△";$marubatu2 = "△";
#print "setu=$setu num=$num<br>";
$HOSI{$y}{$x} = "△<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "△<br>$tokuten1 - $tokuten2";
#$HOSI1{$setu}{$num} = "△<br>$tokuten1 - $tokuten2";
#$HOSI2{$setu}{$num} = "△<br>$tokuten1 - $tokuten2";
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$WAKESU{$RDATA1{$setu}{$num}}++;	#勝数
$WAKESU{$RDATA2{$setu}{$num}}++;	#負数
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[2];	#勝ち点（引き分け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[2];	#勝ち点（引き分け）
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<br>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）";
}	#if

#左の勝ち
if($resultstr1 == 1 && $resultstr2 == 2 ){
$marubatu1 = "○";$marubatu2 = "×";
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<br>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）";
$HOSI{$y}{$x} = "○<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "×<br>$tokuten2 - $tokuten1";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "○<br>$tokuten1 - $tokuten2";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "×<br>$tokuten2 - $tokuten1";
$KACHISU{$RDATA1{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA2{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[0];	#勝ち点（勝ち）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[1];	#勝ち点（負け）
}	#if

#右の勝ち
if($resultstr1 == 2 && $resultstr2 == 1 ){
$marubatu1 = "×";$marubatu2 = "○";
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<br>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）";
$HOSI{$y}{$x} = "×<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "○<br>$tokuten2 - $tokuten1";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "×<br>$tokuten1 - $tokuten2";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "○<br>$tokuten2 - $tokuten1";
$KACHISU{$RDATA2{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA1{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[1];	#勝ち点（負け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[0];	#勝ち点（勝ち）
}	#if

#不戦勝、不戦敗
#左の勝ち
if($resultstr1 == 4 && $resultstr2 == 5 ){
$marubatu1 = "○";$marubatu2 = "×";
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<br>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）";
$HOSI{$y}{$x} = "○<br>勝 - 敗";
$HOSI{$x}{$y} = "×<br>敗 - 勝";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "○<br>不戦勝 - 不戦敗";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "×<br>不戦敗 - 不戦勝";
$KACHISU{$RDATA1{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA2{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[3];	#勝ち点（勝ち）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[4];	#勝ち点（負け）
$tokuten1 = "不戦勝";
$tokuten2 = "不戦敗";
}	#if

#右の勝ち
if($resultstr1 == 5 && $resultstr2 == 4 ){
$marubatu1 = "×";$marubatu2 = "○";
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<br>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）";
$HOSI{$y}{$x} = "×<br>敗 - 勝";
$HOSI{$x}{$y} = "○<br>勝 - 敗";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "×<br>不戦敗 - 不戦勝";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "○<br>不戦勝 - 不戦敗";
$KACHISU{$RDATA2{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA1{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[4];	#勝ち点（負け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[3];	#勝ち点（勝ち）
$tokuten1 = "不戦敗";
$tokuten2 = "不戦勝";
}	#if


}else{
next;
#片方が未報告
#$marubatu1 = "-";$marubatu2 = "-";
#$tokuten1 = "-";$tokuten2 = "-";
#$winnercomment = "";
#$comment1 = "";
#$comment2 = "";
}	#if

###
if($tname1 ne "" && $tname2 ne ""){
$temp .=<<"END_HTML";
<div class="na">
<table width="760" border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td width="48">$marubatu1&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tname1&nbsp;</td>
<td width="72">$tokuten1&nbsp;</td>
<td width="53">―</td>
<td width="72">$tokuten2&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tname2&nbsp;</td>
<td width="55">$marubatu2&nbsp;</td>
</tr>
</table>
</div>
<div class="na2"><span style="color:red;">（戦評）</span><br>$winnercomment</div>
<div class="na3">
$comment1<br>
$comment2
</div>
END_HTML
}	#if
}	#foreach 
if($temp ne ""){
$result .=<<"END_HTML";
<div class="subti3">第${setu}節</div>
$temp
END_HTML
}	#if
}	#foreach setu

}

###################
# >>星取表
$w = int(95 / ($teamcount+3) );
$w2 = $w * 2;
$hositable =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="5%" bgcolor="#F2F2F2">　</th>
<th width="${w2}%" bgcolor="#F2F2F2" align=center>チーム名</th>
END_HTML
#横の続き
foreach (1..$teamcount){
$a = chr(64 + $_);
$hositable .=<<"END_HTML";
<th width="${w}%" bgcolor="#F2F2F2" align=center nowrap>$a</th>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</tr>
END_HTML
#縦の列。最初
foreach $y(1..$teamcount){
$a = chr(64 + $y);
$hositable .=<<"END_HTML";
<tr>
<td height=38 nowrap align=center>$a&nbsp;</td>
<td nowrap align=center>$TNAME{$TSS[$y-1]}&nbsp;</td>
END_HTML
#横の続き
foreach $x(1..$teamcount){
$bgcol = "#FFFFFF";
if($y == $x){$bgcol="#F2F2F2";}
$str = "&nbsp;";
#if($y < $x){$str = $HOSI1{$y}{$x};}
#if($y > $x){$str = $HOSI2{$y}{$x};}
#if($str =~ /不戦勝/){print "TSS $y-1 TSS $x-1 <br>";}
$hositable .=<<"END_HTML";
<td align=center bgcolor="$bgcol" nowrap>$HOSI{$y-1}{$x-1}&nbsp;</th>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</tr>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</table>
<div style="margin-top:-30px;">※「勝」…不戦勝、「敗」…不戦敗</div>
END_HTML


########################
# ページの組み立て
###################
# >>順位表
#順位テーブルクリア
$sql_str3 = "DELETE FROM jyunihyo WHERE taikaicode = '$taikaicode' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
#
foreach $teamnum(@TSS){
#順位計算
$kachisu = $KACHISU{$teamnum}-0;
$makesu = $MAKESU{$teamnum}-0;
$wakesu = $WAKESU{$teamnum}-0;
$kachiten = $KACHITEN{$teamnum}-0;
$tokuten = $TOKUTEN{$teamnum}-0;
$sitten = $SITTEN{$teamnum}-0;
$siaisu = $SIAISU{$teamnum}-0;
$tokusitutensa = $tokuten + $sitten;
$syouritu = 0;
#$temp = $kachisu + ($wakesu * 0.5);
if($siaisu != 0){$syouritu = $kachisu / $siaisu;}	#if
#順位テーブルに登録
$tname = $TNAME{$teamnum};
$sql_str3 = qq{INSERT INTO jyunihyo(teamname,taikaicode,area,kumi,num,teamnum,kachisu,makesu,wakesu,kachiten,tokuten,sitten,tokusitutensa,syouritu) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute(
$tname,
$taikaicode,
$area,
$kumi,
$num,
$teamnum,
$kachisu,
$makesu,
$wakesu,
$kachiten,
$tokuten,
$sitten,
$tokusitutensa,
$syouritu,
);
&sqlcheck($sql_str3);
}	#foreach

### 順位表から取り出し！
@JYUNI = ();
#%TEAMTABLE2 =();
$sql_str3 = "SELECT * FROM jyunihyo WHERE taikaicode = '$taikaicode' and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' ORDER BY kachiten DESC,tokusitutensa DESC,sitten DESC";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);	#SQLエラーチェック
$count3 = $rs3->rows;	# Hit件数を確保
for($k2 = 0;$k2 < $count3;$k2++){	# データベース１件ずつ
$REFHASH3 = $rs3->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH3);
push(@JYUNI,$teamnum);
$TEAMNAME{$teamnum} = &paramsetsql('teamname',$REFHASH3);
$KACHISU{$teamnum} = &paramsetsql('kachisu',$REFHASH3);
$MAKESU{$teamnum} = &paramsetsql('makesu',$REFHASH3);
$WAKESU{$teamnum} = &paramsetsql('wakesu',$REFHASH3);
$KACHITEN{$teamnum} = &paramsetsql('kachiten',$REFHASH3);
$TOKUTEN{$teamnum} = &paramsetsql('tokuten',$REFHASH3);
$SITTEN{$teamnum} = &paramsetsql('sitten',$REFHASH3);
$TOKUSITUTENSA{$teamnum} = &paramsetsql('tokusitutensa',$REFHASH3);
$SYOURITU{$teamnum} = sprintf("%.3f",&paramsetsql('syouritu',$REFHASH3));
}	#for
###
$teamtable =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="57" bgcolor="#F2F2F2" align=center>順位</th>
<th width="172" bgcolor="#F2F2F2" align=center>チーム名</th>
<th width="63" bgcolor="#F2F2F2" align=center>試合数</th>
<th width="63" bgcolor="#F2F2F2" align=center>勝</th>
<th width="63" bgcolor="#F2F2F2" align=center>負</th>
<th width="63" bgcolor="#F2F2F2" align=center>引</th>
<th width="63" bgcolor="#F2F2F2" align=center>勝点</th>
<th width="64" bgcolor="#F2F2F2" align=center>得点</th>
<th width="64" bgcolor="#F2F2F2" align=center>失点</th>
<th width="64" bgcolor="#F2F2F2" align=center>得失</th>
<th width="102" bgcolor="#F2F2F2" align=center>勝率</th>
</tr>
END_HTML
$KUMIR{$area}{$kumi} = $kuminame;
$TEAMTABLE2{$area}{$kumi} =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="57" bgcolor="#F2F2F2" align=center>順位</th>
<th width="172" bgcolor="#F2F2F2" align=center>チーム名</th>
</tr>
END_HTML
#順位で表示
$num = 1;
foreach $tn(@JYUNI){
$teamtable .=<<"END_HTML";
<tr>
<td align=center>$num&nbsp;</td>
<td>$TEAMNAME{$tn}&nbsp;</td>
<td align=center>&nbsp;$SIAISU{$tn}&nbsp;</td>
<td align=center>&nbsp;$KACHISU{$tn}&nbsp;</td>
<td align=center>&nbsp;$MAKESU{$tn}&nbsp;</td>
<td align=center>&nbsp;$WAKESU{$tn}&nbsp;</td>
<td align=center>&nbsp;$KACHITEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$TOKUTEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$SITTEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$TOKUSITUTENSA{$tn}&nbsp;</td>
<td align="right">&nbsp;$SYOURITU{$tn}&nbsp;</td>
</tr>
END_HTML
#
$numtemp = $num;
if($SYOURITU{$tn} == 0){$numtemp = "-";}
$TEAMTABLE2{$area}{$kumi} .=<<"END_HTML";
<tr>
<td align=center> $numtemp&nbsp;</td>
<td>$TEAMNAME{$tn}&nbsp;</td>
</tr>
END_HTML

$num++;
}	#foreach
$teamtable .=<<"END_HTML";
</table>
END_HTML
$TEAMTABLE2{$area}{$kumi} .=<<"END_HTML";
</table>
END_HTML





########################
$list1 .=<<"END_HTML";
<div class="subti2"><span>$kuminame</span></div>
<!-- 順位表 -->
<h3>順位表</h3>
$teamtable
<!-- /順位表 -->

<!-- 星取り表 -->
<h3>星取表</h3>
$hositable
<!-- /星取り表 -->

<h3>試合結果</h3>
$result
END_HTML

########################
}	#for 組
if($list1 ne ""){
$areatag .=<<"END_HTML";
<a href="#$area"><span>$AREASS{$area}</span></a>
END_HTML

$arealist .=<<"END_HTML";
$AREASTR{$area}
<div class="box">
$list1
</div>

END_HTML
}	#if
$list1 = "";

}	#for エリア

}	#if 勝ち点





##########################################################
# トーナメント
##########################################################
$result = "";
$areatag2 = "";
@CNT = (0,1,2,4,8,16,32,64,128);
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '2' ORDER BY area ASC,kumi ASC";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1."<br>\n";
for($j=0;$j<$count1;$j++){
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
$gedan = 0;
foreach(1..7){
if($NICHIJITEMP[$_] =~ /0000/){$gedan = $_ -1;}
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

$num = $y;	#○回戦
foreach $x(1..$CNT[$y]){

$tss1 = $TEAMLIST{$y}{$x}{1};	#左のチームnum
$tss2 = $TEAMLIST{$y}{$x}{2};	#右のチームnum

if($tss1 eq "" || $tss2 eq ""){next;}

$tss1name = &taikaiteamname_get($tss1);
$tss2name = &taikaiteamname_get($tss2);

#@TEMP = split(/:/,$NICHIJITEMP[$num]);
#$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));

$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($y - $num+2)."回戦";
}	#num

$editflag = "";
$reportflag = 0;
$tsstemp = "";
$result10 = "";
$result11 = "";
$score = "";
$winlose = "";
$attention = "";
$senpyo1 = "";
$senpyo2 = "";

#双方の報告をGET
#左
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = $tss2";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
$count3 = $rs3->rows;	# Hit件数を確保

$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = $tss1";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保
#print "count3=$count3 sql_str1=$sql_str1<br>\n";
#print "count2=$count2 sql_str2=$sql_str2<br>\n";
if($count3 == 0 || $count2 == 0 ){next;}

$REFHASH3 = $rs3->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH3);
$resultstr1 = &paramsetsql('resultstr',$REFHASH3);
$result10 = &paramsetsql('result0',$REFHASH3);
$result11 = &paramsetsql('result1',$REFHASH3);
$senpyo1 = &paramsetsql2('senpyo',$REFHASH3);
$comment1 = &paramsetsql('comment',$REFHASH3);
#右
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$resultstr2 = &paramsetsql('resultstr',$REFHASH2);
$result20 = &paramsetsql('result0',$REFHASH2);
$result21 = &paramsetsql('result1',$REFHASH2);
$senpyo2 = &paramsetsql2('senpyo',$REFHASH2);
$comment2 = &paramsetsql('comment',$REFHASH2);

#相違がある場合
#print "$result10 != $result21 || $result11 != $result20<br>";
if($result10 != $result21 || $result11 != $result20 ){next;}



$winnercomment  = $senpyo1."（$tss1name）<br>";
$winnercomment .= $senpyo2."（$tss2name）";

if($result10 == $result11){
$marubatu1 = "△";$marubatu2 = "△";
}	#if

#左の勝ち
if($result10 > $result11){
$marubatu1 = "○";$marubatu2 = "×";
#$winnercomment  = $senpyo1."（$tss1name）<br>";
#$winnercomment .= $senpyo2."（$tss2name）";
}	#if
#右の勝ち
if($result10 < $result11){
$marubatu1 = "×";$marubatu2 = "○";
#$winnercomment  = $senpyo1."（$tss1name）<br>";
#$winnercomment .= $senpyo2."（$tss2name）";
}	#if

if($resultstr1 == 4){$result10 = "不戦勝";$result11 = "不戦負";}	#if
if($resultstr1 == 5){$result10 = "不戦負";$result11 = "不戦勝";}	#if


$ground = "";
$nichijireport = "";
#試合日と開催地をGET
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and teamnum = $tss1 ";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$sql_str4<br>\n";
if($count4 != 0){
$REFHASH4 = $rs4->fetchrow_hashref;
$ground .= &paramsetsql('body',$REFHASH4);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH4));
$nichijireport = sprintf("%d年<br>%d月%d日<br>%d時%02d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
}	#if
##
$result .=<<"END_HTML";
<div class="na">
<table width="760" border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td width="48">$marubatu1&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tss1name&nbsp;</td>
<td width="72">&nbsp;$result10</td>
<td width="53">―</td>
<td width="72">$result11&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tss2name&nbsp;</td>
<td width="55">$marubatu2&nbsp;</td>
</tr>
</table>
</div>

<div class="na2"><span style="color:red;">（戦評）</span><br>$winnercomment</div>
<div class="na3">
$comment1（$tss1name）<br>
$comment2（$tss2name）
</div>
END_HTML
#}	#if count = 2

}	#if 双方の報告あり
}	#if nichiji
}	#foreach y
if($result ne ""){
$areatag2 .=<<"END_HTML";
<a href="#2:$area"><span>$areaname</span></a>
END_HTML
$arealist2 .=<<"END_HTML";
<h2 class='subti' id='2:$area'>$areaname</h2>
<div class="subti2"><span>$kuminame</span></div>
<h3>試合結果</h3>
$result
END_HTML
}
$result = "";
}	#for j
########################
########################




}	#sub




# -----------------------------------------------------------------
# 順位計算
# -----------------------------------------------------------------
sub kachi2 {
my ($s_categorey,$s_area,$s_kumi)=(@_);
##########################################################
# リーグ
##########################################################
#「勝ち点表」を大会データからGET
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 40 and koukaiflag = 0 and taikaicode = $taikaicode ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);	#SQLエラーチェック
$count3 = $rs3->rows;	# Hit件数を確保
if($count3 != 0){
$REFHASH3 = $rs3->fetchrow_hashref;
@KACHITENHYO = split(/:/,&paramsetsql('resultstr',$REFHASH3));

#エリアGET：ループ
@AREANUM = ();
%KUMINUM = ();
%AREASTR = ();
$sql_str = "SELECT * FROM $dbname WHERE contents = 30 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  ORDER BY sortnum ASC, serial DESC ";
$rs = $dbh->prepare($sql_str);
$rs->execute();
&sqlcheck($sql_str);
$count = $rs->rows;	# Hit件数を確保
#print "count=$count<br>\n";
for($i = 0;$i < $count;$i++){	# データベース１件ずつ
$REFHASH = $rs->fetchrow_hashref;
$area = &paramsetsql('serial');
push(@AREANUM,$area);
$AREASS{$area} = &paramsetsql('title');
$AREASTR{$area} = "<h2 class='subti' id='$area'>$AREASS{$area}</h2>";
#組GET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 31 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' ORDER BY sortnum ASC, serial DESC ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
&sqlcheck($sql_str1);
$count1 = $rs1->rows;	# Hit件数を確保
for($k = 0;$k < $count1;$k++){	# 組GETデータベース１件ずつ
$REFHASH1 = $rs1->fetchrow_hashref;
$kumi = &paramsetsql('serial',$REFHASH1 );
$KUMISS{$kumi} = &paramsetsql('title',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
$KUMINUM{$area} .= $kumi.":";
%TY = ();
# 組に登録されたチームをGET
$sql_str2 = "SELECT * FROM $dbname WHERE contents = 32 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' ORDER BY serial ASC ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
&sqlcheck($sql_str2);
$count2 = $rs2->rows;	# Hit件数を確保
#print "count2=$count2<br>\n";
@TSS = ();
for($m = 0;$m < $count2;$m++){	# データベース１件ずつ
$REFHASH2 = $rs2->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH2);
push(@TSS,$teamnum);
$TY{$teamnum} = $m;
$TNAME{$teamnum} = &taikaiteamname_get($teamnum);
}	#for m

# 対戦組み合わせデータGET
%RDATA1 =();
%RDATA2 =();
%HOSI = ();
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
$count3 = $rs3->rows;	# Hit件数を確保
#print "count3=$count3<br>\n";
for($j=0;$j<$count3;$j++){
$REFHASH3 = $rs3->fetchrow_hashref;
$vsdata = &paramsetsql('title',$REFHASH3);
# vsチームを分解
foreach $temp(split(/<>/,$vsdata)){	#team1:1.1.1|team2:1.1.8<>.....
#print $temp."<br>\n";
($team1,$team2) = split(/\|/,$temp);	#team1:1.1.1  team2:1.1.8
($temp1,$data1) = split(/:/,$team1);	#team1  1.1.1
($temp2,$data2) = split(/:/,$team2);	#team2  1.1.8
($setu,$num,$tss1) = split(/\./,$data1);	#1 1 1
($setu,$num,$tss2) = split(/\./,$data2);	#1 1 8
$RDATA1{$setu}{$num} = $tss1;
$RDATA2{$setu}{$num} = $tss2;
}	#foreach

###################
$teamcount = @TSS;
#print "teamcount=$teamcount<br>\n";

###################
# >>試合結果
# チームserialからチームsessionをGET
foreach $ss(@TSS){
#print "ss=$ss<br>\n";
$sql_str3 = "SELECT * FROM member_tbl WHERE contents = 21 and koukaiflag = 0 and serial = '$ss' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);
$count3 = $rs3->rows;	# Hit件数を確保
if($count3 != 0){
#print "count3=$count3<br>\n";
$REFHASH3 = $rs3->fetchrow_hashref;
$ses = &paramsetsql('ssid',$REFHASH3);
$SERI2SES{$ss} = $ses;
$SES2SERI{$ses} = $ss;
}	#count3
}	#foreach
#
$result ="";
foreach $setu(1..7){
$temp = "";
#
#得点表
#$half = int($teamcount/2);
foreach $num(1..4){
$tname1 = $TNAME{$RDATA1{$setu}{$num}};	#$RDATA1{$setu}{$num} はチームserial
$tname2 = $TNAME{$RDATA2{$setu}{$num}};	#$RDATA1{$setu}{$num} はチームserial

# 試合の報告をGET
@SES = ();
%RESULTSTR = ();
%RESULTSTR2 = ();
%RESULT0 = ();
%RESULT1 = ();
%SENPYO = ();
%COMMENT = ();
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 1  and area = '$area' and kumi = '$kumi' and title = '$setu' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);
$count3 = $rs3->rows;	# Hit件数を確保
for($i3=0;$i3<$count3;$i3++){
$REFHASH3 = $rs3->fetchrow_hashref;
$session = &paramsetsql('linkadr',$REFHASH3);
$ss = $SES2SERI{$session};
push(@SES,$session);
$teamnum = &paramsetsql('teamnum',$REFHASH3);
$RESULTSTR{$setu}{$ss} = &paramsetsql('resultstr',$REFHASH3);		#戦績
$RESULTSTR2{$setu}{$ss} = &paramsetsql('resultstr2',$REFHASH3);	#その他情報
$RESULT0{$setu}{$ss} = &paramsetsql('result0',$REFHASH3);			#スコア（自）
$RESULT1{$setu}{$ss} = &paramsetsql('result1',$REFHASH3);			#スコア（他）
$SENPYO{$setu}{$num}{$ss} = &paramsetsql2('senpyo',$REFHASH3);
$COMMENT{$setu}{$ss} = &paramsetsql('comment',$REFHASH3);
}	#for

#
$resultstr1 = $RESULTSTR{$setu}{$RDATA1{$setu}{$num}};
$resultstr2 = $RESULTSTR{$setu}{$RDATA2{$setu}{$num}};

$tokuten1 = $RESULT0{$setu}{$RDATA1{$setu}{$num}};
$tokuten2 = $RESULT1{$setu}{$RDATA1{$setu}{$num}};
=pot
print <<"HTML_END";
<pre>
setu = $setu
num = $num
RDATA1 = $RDATA1{$setu}{$num}
RDATA2 = $RDATA2{$setu}{$num}
RESULT0 = $RESULT0{$setu}{$RDATA1{$setu}{$num}}
RESULT1 = $RESULT1{$setu}{$RDATA2{$setu}{$num}}
tokuten1 = $tokuten1
tokuten2 = $tokuten2
</pre>
HTML_END
=cut
$marubatu1 = "-";$marubatu2 = "-";
$comment1 = "$COMMENT{$setu}{$RDATA1{$setu}{$num}}（$tname1）<hr>";
$comment2 = "$COMMENT{$setu}{$RDATA2{$setu}{$num}}（$tname2）<hr>";
$winnercomment = "";
$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";

#報告のある結果のみ表示
if($resultstr1 ne "" && $resultstr2 ne ""){
#print "resultstr1=$resultstr1 , resultstr2=$resultstr2<br>";
$y = $TY{$RDATA1{$setu}{$num}};
$x = $TY{$RDATA2{$setu}{$num}};
#引き分け
if($resultstr1 == 3 && $resultstr2 == 3 ){
$marubatu1 = "△";$marubatu2 = "△";
#print "setu=$setu num=$num<br>";
$HOSI{$y}{$x} = "△<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "△<br>$tokuten1 - $tokuten2";
#$HOSI1{$setu}{$num} = "△<br>$tokuten1 - $tokuten2";
#$HOSI2{$setu}{$num} = "△<br>$tokuten1 - $tokuten2";
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$WAKESU{$RDATA1{$setu}{$num}}++;	#勝数
$WAKESU{$RDATA2{$setu}{$num}}++;	#負数
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[2];	#勝ち点（引き分け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[2];	#勝ち点（引き分け）
#$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
#$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";
}	#if

#左の勝ち
if($resultstr1 == 1 && $resultstr2 == 2 ){
$marubatu1 = "○";$marubatu2 = "×";
#$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
#$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";
$HOSI{$y}{$x} = "○<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "×<br>$tokuten2 - $tokuten1";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "○<br>$tokuten1 - $tokuten2";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "×<br>$tokuten2 - $tokuten1";
$KACHISU{$RDATA1{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA2{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[0];	#勝ち点（勝ち）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[1];	#勝ち点（負け）
}	#if

#右の勝ち
if($resultstr1 == 2 && $resultstr2 == 1 ){
$marubatu1 = "×";$marubatu2 = "○";
#$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
#$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";
$HOSI{$y}{$x} = "×<br>$tokuten1 - $tokuten2";
$HOSI{$x}{$y} = "○<br>$tokuten2 - $tokuten1";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "×<br>$tokuten1 - $tokuten2";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "○<br>$tokuten2 - $tokuten1";
$KACHISU{$RDATA2{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA1{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[1];	#勝ち点（負け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[0];	#勝ち点（勝ち）
}	#if

#不戦勝、不戦敗
#左の勝ち
if($resultstr1 == 4 && $resultstr2 == 5 ){
$marubatu1 = "○";$marubatu2 = "×";
#$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
#$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";
$HOSI{$y}{$x} = "○<br>不戦勝 - 不戦敗";
$HOSI{$x}{$y} = "×<br>不戦敗 - 不戦勝";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "○<br>不戦勝 - 不戦敗";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "×<br>不戦敗 - 不戦勝";
$KACHISU{$RDATA1{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA2{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[3];	#勝ち点（勝ち）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[4];	#勝ち点（負け）
$tokuten1 = "不戦勝";
$tokuten2 = "不戦敗";
}	#if

#右の勝ち
if($resultstr1 == 5 && $resultstr2 == 4 ){
$marubatu1 = "×";$marubatu2 = "○";
#$winnercomment  = $SENPYO{$setu}{$num}{$RDATA1{$setu}{$num}}."（$tname1）<hr>";
#$winnercomment .= $SENPYO{$setu}{$num}{$RDATA2{$setu}{$num}}."（$tname2）<hr>";
$HOSI{$y}{$x} = "×<br>不戦敗 - 不戦勝";
$HOSI{$x}{$y} = "○<br>不戦勝 - 不戦敗";
#$HOSI1{$RDATA1{$setu}{$num}}{$RDATA2{$setu}{$num}} = "×<br>不戦敗 - 不戦勝";
#$HOSI2{$RDATA2{$setu}{$num}}{$RDATA1{$setu}{$num}} = "○<br>不戦勝 - 不戦敗";
$KACHISU{$RDATA2{$setu}{$num}}++;	#勝数
 $MAKESU{$RDATA1{$setu}{$num}}++;	#負数
$TOKUTEN{$RDATA1{$setu}{$num}}+=$tokuten1;	#得点
$TOKUTEN{$RDATA2{$setu}{$num}}+=$tokuten2;	#得点
$SITTEN{$RDATA1{$setu}{$num}}-=$tokuten2;	#失点
$SITTEN{$RDATA2{$setu}{$num}}-=$tokuten1;	#失点
$SIAISU{$RDATA1{$setu}{$num}}++;	#試合数
$SIAISU{$RDATA2{$setu}{$num}}++;	#試合数
$KACHITEN{$RDATA1{$setu}{$num}} += $KACHITENHYO[4];	#勝ち点（負け）
$KACHITEN{$RDATA2{$setu}{$num}} += $KACHITENHYO[3];	#勝ち点（勝ち）
$tokuten1 = "不戦敗";
$tokuten2 = "不戦勝";
}	#if


}else{

#片方が未報告
$marubatu1 = "-";$marubatu2 = "-";
$tokuten1 = "-";$tokuten2 = "-";
#$winnercomment = "";
#$comment1 = "";
#$comment2 = "";
}	#if

###
if($tname1 ne "" && $tname2 ne ""){
$temp .=<<"END_HTML";
<div class="na">
<table width="760" border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td width="48">$marubatu1&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tname1&nbsp;</td>
<td width="72">$tokuten1&nbsp;</td>
<td width="53">―</td>
<td width="72">$tokuten2&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tname2&nbsp;</td>
<td width="55">$marubatu2&nbsp;</td>
</tr>
</table>
</div>
<div class="na2"><span style="color:red;">（戦評）</span><br>$winnercomment</div>
<div class="na3">
【コメント】<br>
$comment1<hr>
【コメント】<br>
$comment2<hr>
<p>
</div>
END_HTML
}	#if
}	#foreach 
if($temp ne ""){
$result .=<<"END_HTML";
<div class="subti3">第${setu}節</div>
$temp
END_HTML
}	#if
}	#foreach setu

}

###################
# >>星取表
$hositable =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="10%" bgcolor="#F2F2F2">　</th>
<th width="20%" bgcolor="#F2F2F2" align=center>チーム名</th>
END_HTML
#横の続き
foreach (1..$teamcount){
$a = chr(64 + $_);
$hositable .=<<"END_HTML";
<th width="10%" bgcolor="#F2F2F2" align=center>$a</th>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</tr>
END_HTML
#縦の列。最初
foreach $y(1..$teamcount){
$a = chr(64 + $y);
$hositable .=<<"END_HTML";
<tr>
<td align=center>$a&nbsp;</td>
<td align=center>$TNAME{$TSS[$y-1]}&nbsp;</td>
END_HTML
#横の続き
foreach $x(1..$teamcount){
$bgcol = "#FFFFFF";
if($y == $x){$bgcol="#F2F2F2";}
$str = "&nbsp;";
#if($y < $x){$str = $HOSI1{$y}{$x};}
#if($y > $x){$str = $HOSI2{$y}{$x};}
#if($str =~ /不戦勝/){print "TSS $y-1 TSS $x-1 <br>";}
$hositable .=<<"END_HTML";
<td align=center bgcolor="$bgcol">$HOSI{$y-1}{$x-1}&nbsp;</th>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</tr>
END_HTML
}	#foreach
$hositable .=<<"END_HTML";
</table>
END_HTML


########################
# ページの組み立て
###################
# >>順位表
#順位テーブルクリア
$sql_str3 = "DELETE FROM jyunihyo WHERE taikaicode = '$taikaicode' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
#
foreach $teamnum(@TSS){
#順位計算
$kachisu = $KACHISU{$teamnum}-0;
$makesu = $MAKESU{$teamnum}-0;
$wakesu = $WAKESU{$teamnum}-0;
$kachiten = $KACHITEN{$teamnum}-0;
$tokuten = $TOKUTEN{$teamnum}-0;
$sitten = $SITTEN{$teamnum}-0;
$siaisu = $SIAISU{$teamnum}-0;
$tokusitutensa = $tokuten + $sitten;
$syouritu = 0;
#$temp = $kachisu + ($wakesu * 0.5);
if($siaisu != 0){$syouritu = $kachisu / $siaisu;}	#if
#順位テーブルに登録
$tname = $TNAME{$teamnum};
$sql_str3 = qq{INSERT INTO jyunihyo(teamname,taikaicode,area,kumi,num,teamnum,kachisu,makesu,wakesu,kachiten,tokuten,sitten,tokusitutensa,syouritu) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);};
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute(
$tname,
$taikaicode,
$area,
$kumi,
$num,
$teamnum,
$kachisu,
$makesu,
$wakesu,
$kachiten,
$tokuten,
$sitten,
$tokusitutensa,
$syouritu,
);
&sqlcheck($sql_str3);
}	#foreach

### 順位表から取り出し！
@JYUNI = ();
#%TEAMTABLE2 =();
$sql_str3 = "SELECT * FROM jyunihyo WHERE taikaicode = '$taikaicode' and taikaicode = '$taikaicode' and area = '$area' and kumi = '$kumi' ORDER BY kachiten DESC,tokusitutensa DESC,sitten DESC";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
&sqlcheck($sql_str3);	#SQLエラーチェック
$count3 = $rs3->rows;	# Hit件数を確保
for($k2 = 0;$k2 < $count3;$k2++){	# データベース１件ずつ
$REFHASH3 = $rs3->fetchrow_hashref;
$teamnum = &paramsetsql('teamnum',$REFHASH3);
push(@JYUNI,$teamnum);
$TEAMNAME{$teamnum} = &paramsetsql('teamname',$REFHASH3);
$KACHISU{$teamnum} = &paramsetsql('kachisu',$REFHASH3);
$MAKESU{$teamnum} = &paramsetsql('makesu',$REFHASH3);
$WAKESU{$teamnum} = &paramsetsql('wakesu',$REFHASH3);
$KACHITEN{$teamnum} = &paramsetsql('kachiten',$REFHASH3);
$TOKUTEN{$teamnum} = &paramsetsql('tokuten',$REFHASH3);
$SITTEN{$teamnum} = &paramsetsql('sitten',$REFHASH3);
$TOKUSITUTENSA{$teamnum} = &paramsetsql('tokusitutensa',$REFHASH3);
$SYOURITU{$teamnum} = sprintf("%.3f",&paramsetsql('syouritu',$REFHASH3));
}	#for
###
$teamtable =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="57" bgcolor="#F2F2F2" align=center>順位</th>
<th width="172" bgcolor="#F2F2F2" align=center>チーム名</th>
<th width="63" bgcolor="#F2F2F2" align=center>試合数</th>
<th width="63" bgcolor="#F2F2F2" align=center>勝</th>
<th width="63" bgcolor="#F2F2F2" align=center>負</th>
<th width="63" bgcolor="#F2F2F2" align=center>引</th>
<th width="63" bgcolor="#F2F2F2" align=center>勝点</th>
<th width="64" bgcolor="#F2F2F2" align=center>得点</th>
<th width="64" bgcolor="#F2F2F2" align=center>失点</th>
<th width="64" bgcolor="#F2F2F2" align=center>得失</th>
<th width="102" bgcolor="#F2F2F2" align=center>勝率</th>
</tr>
END_HTML
$KUMIR{$area}{$kumi} = $kuminame;
$TEAMTABLE2{$area}{$kumi} =<<"END_HTML";
<table width="100%" cellpadding="0" cellspacing="0" class="statsTbl">
<tr>
<th width="57" bgcolor="#F2F2F2" align=center>順位</th>
<th width="172" bgcolor="#F2F2F2" align=center>チーム名</th>
</tr>
END_HTML
#順位で表示
$num = 1;
foreach $tn(@JYUNI){
$teamtable .=<<"END_HTML";
<tr>
<td align=center>$num&nbsp;</td>
<td>$TEAMNAME{$tn}&nbsp;</td>
<td align=center>&nbsp;$SIAISU{$tn}&nbsp;</td>
<td align=center>&nbsp;$KACHISU{$tn}&nbsp;</td>
<td align=center>&nbsp;$MAKESU{$tn}&nbsp;</td>
<td align=center>&nbsp;$WAKESU{$tn}&nbsp;</td>
<td align=center>&nbsp;$KACHITEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$TOKUTEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$SITTEN{$tn}&nbsp;</td>
<td align=center>&nbsp;$TOKUSITUTENSA{$tn}&nbsp;</td>
<td align="right">&nbsp;$SYOURITU{$tn}&nbsp;</td>
</tr>
END_HTML
#
$numtemp = $num;
if($SYOURITU{$tn} == 0){$numtemp = "-";}
$TEAMTABLE2{$area}{$kumi} .=<<"END_HTML";
<tr>
<td align=center> $numtemp&nbsp;</td>
<td>$TEAMNAME{$tn}&nbsp;</td>
</tr>
END_HTML
$num++;
}	#foreach
$teamtable .=<<"END_HTML";
</table>
END_HTML
$TEAMTABLE2{$area}{$kumi} .=<<"END_HTML";
</table>
END_HTML
########################
$list1 .=<<"END_HTML";
<div class="subti2"><span>$kuminame</span></div>
<!-- 順位表 -->
<h3>順位表</h3>
$teamtable
<!-- /順位表 -->
<!-- 星取り表 -->
<h3>星取表</h3>
$hositable
<!-- /星取り表 -->
<h3>試合結果</h3>
$result
END_HTML
########################
}	#for 組
if($list1 ne ""){
$areatag .=<<"END_HTML";
<a href="#$area"><span>$AREASS{$area}</span></a>
END_HTML

$arealist .=<<"END_HTML";
$AREASTR{$area}
<div class="box">
$list1
</div>
END_HTML
}	#if
$list1 = "";
}	#for エリア
}	#if 勝ち点






##########################################################
# トーナメント
##########################################################
$result = "";
$areatag2 = "";
@CNT = (0,1,2,4,8,16,32,64,128);
# 対戦組み合わせデータGET
$sql_str1 = "SELECT * FROM $dbname WHERE contents = 33 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = '2' and area = $s_area and kumi = $s_kumi ";
$rs1 = $dbh->prepare($sql_str1);
$rs1->execute();
$count1 = $rs1->rows;	# Hit件数を確保
#print $count1."<br>\n";

for($j=0;$j<$count1;$j++){
$REFHASH1 = $rs1->fetchrow_hashref;
$area = &paramsetsql('area',$REFHASH1);
$areaname = &taikaiareaname_get($area);
if($areaname =~ /不明/){next;}
$kumi = &paramsetsql('kumi',$REFHASH1);
$kuminame = &taikaikuminame_get($kumi);
if($kuminame =~ /不明/){next;}
#if($s_categorey == 2 && $s_area ne "" && $s_area != $area&& $s_kumi ne ""  && $s_kumi != $kumi){next;}	#エリア指定がある場合
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
if($NICHIJITEMP[$_] =~ /0000/){$gedan = $_ -1;}
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

$num = $y;	#○回戦
foreach $x(1..$CNT[$y]){

$tss1 = $TEAMLIST{$y}{$x}{1};	#左のチームnum
$tss2 = $TEAMLIST{$y}{$x}{2};	#右のチームnum

if($tss1 eq "" || $tss2 eq ""){next;}
#print "j=$j,y=$y,x=$x,tss1=$tss1,tss2=$tss2<br>\n";


($tss1name,$tss1ses) = &taikaiteamname_get3($tss1);
($tss2name,$tss2ses) = &taikaiteamname_get3($tss2);

#@TEMP = split(/:/,$NICHIJITEMP[$num]);
#$nichiji = sprintf("%d年%d月%d日～%d年%d月%d日まで",split(/-/,$TEMP[0]),split(/-/,$TEMP[1]));

$numstr = "";
if($num == 1){$numstr = "決勝戦";}
if($num == 2){$numstr = "準決勝";}
if($num == 3){$numstr = "準々決勝";}
if($numstr eq ""){
$numstr = "".($y - $num+2)."回戦";
}	#num

$editflag = "";
$reportflag = 0;
$tsstemp = "";
$result10 = "";
$result11 = "";
$score = "";
$winlose = "";
$attention = "";
$marubatu1 = "";
$marubatu2 = "";
$result_left = "";
$result_right = "";
$senpyo1 = "";
$senpyo2 = "";
$comment1 = "";
$comment2 = "";
$lastupdated1 = "";
$lastupdated2 = "";

#双方の報告をGET
#左
$sql_str3 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = $tss2 and linkadr = '$tss1ses' ";
$rs3 = $dbh->prepare($sql_str3);
$rs3->execute();
$count3 = $rs3->rows;	# Hit件数を確保

$sql_str2 = "SELECT * FROM $dbname WHERE contents = 35 and koukaiflag = 0 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$x' and text1 = '$y' and teamnum = $tss1 and linkadr = '$tss2ses' ";
$rs2 = $dbh->prepare($sql_str2);
$rs2->execute();
$count2 = $rs2->rows;	# Hit件数を確保


#print "count3=$count3 sql_str1=$sql_str3<br>\n";
#print "count2=$count2 sql_str2=$sql_str2<br>\n";
if( $count3 == 0 && $count2 == 0 ){next;}

@IMGSRC1 = ();
@CAP1 = ();
$s1 = "";
$resultstr1 = "";
$result10 = "";
$result11 = "";
$senpyo1 = "";
$comment1 = "";
$lastupdated1 = "";
if( $count3 == 1 ){
$REFHASH3 = $rs3->fetchrow_hashref;
$s1 = &paramsetsql('serial',$REFHASH3);
$resultstr1 = &paramsetsql('resultstr',$REFHASH3);
$result10 = &paramsetsql('result0',$REFHASH3);
$result11 = &paramsetsql('result1',$REFHASH3);
$senpyo1 = &paramsetsql2('senpyo',$REFHASH3);
$comment1 = &paramsetsql('comment',$REFHASH3);
$lastupdated1 = &paramsetsql('timestamp',$REFHASH3);
@CAP1 = split(/<>/,&paramsetsql('caption',$REFHASH3));
#画像
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH3));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC1[$l] = "<a href='?code=download&s=$s1&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
}	#if

@IMGSRC2 = ();
@CAP2 = ();
$s2 = "";
$resultstr2 = "";
$result20 = "";
$result21 = "";
$senpyo2 = "";
$comment2 = "";
$lastupdated2 = "";
if( $count2 == 1 ){
$REFHASH2 = $rs2->fetchrow_hashref;
$s2 = &paramsetsql('serial',$REFHASH2);
$resultstr2 = &paramsetsql('resultstr',$REFHASH2);
$result20 = &paramsetsql('result0',$REFHASH2);
$result21 = &paramsetsql('result1',$REFHASH2);
$senpyo2 = &paramsetsql2('senpyo',$REFHASH2);
$comment2 = &paramsetsql('comment',$REFHASH2);
$lastupdated2 = &paramsetsql('timestamp',$REFHASH2);
@CAP2 = split(/<>/,&paramsetsql('caption',$REFHASH2));
#画像
@IMGTEMPS = split(/:/,&paramsetsql('upfilename',$REFHASH2));
foreach $l(0..2){
if($IMGTEMPS[$l] ne ""){
($sfn,$fn) = split(/<>/,$IMGTEMPS[$l]);
@TEMP = split(/\./,$fn);
if( $TEMP[1] eq "jpg"){$IMGSRC2[$l] = "<a href='?code=download&s=$s2&n=$l'><img src=$sitefulladr/system/file/$TEMP[0]s.$TEMP[1] border=0><br>【画像のダウンロード】</a>";}
}	#if 存在
}	#foreach
}	#if



#相違がある場合
#print "$result10 != $result21 || $result11 != $result20<br>";
#if($result10 != $result21 || $result11 != $result20 ){next;}

#画像
$TEAMRESULT{$y}{$x} =<<"END_HTML";
<table cellpadding=2 cellspacing=1 bgcolor="#aaaaaa" class="text-12" width=400>
<tr><td width=50% bgcolor="#ffffff" align=center valign=top nowrap colspan=2>$tss1name</td><td bgcolor="#ffffff" align=center valign=top nowrap colspan=2>$tss2name</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[0]</td><td bgcolor="#ffffff" valign=top>$CAP1[0]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[0]</td><td bgcolor="#ffffff" valign=top>$CAP2[0]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[1]</td><td bgcolor="#ffffff" valign=top>$CAP1[1]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[1]</td><td bgcolor="#ffffff" valign=top>$CAP2[1]</td></tr>
<tr><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC1[2]</td><td bgcolor="#ffffff" valign=top>$CAP1[2]</td><td bgcolor="#ffffff" align=center valign=top nowrap>$IMGSRC2[2]</td><td bgcolor="#ffffff" valign=top>$CAP2[2]</td></tr>
</table>
END_HTML

$winnercomment  = "<span style='color:red;'>（戦評）</span><br>".$senpyo1."（$tss1name）<hr>";
$winnercomment .= "<span style='color:red;'>（戦評）</span><br>".$senpyo2."（$tss2name）<hr>";
#両チーム：報告OK
if( $count3 == 1 && $count2 == 1){

###相違なし
if($result10 == $result21 && $result11 == $result20){
$marubatu1 = "△";$marubatu2 = "△";
#左の勝ち
if($result10 > $result11){
$marubatu1 = "○";$marubatu2 = "×";
#$winnercomment  = "<span style='color:red;'>（戦評）</span><br>".$senpyo1."（$tss1name）<hr>";
#$winnercomment .= "<span style='color:red;'>（戦評）</span><br>".$senpyo2."（$tss2name）<hr>";
}	#if
#右の勝ち
if($result10 < $result11){
$marubatu1 = "×";$marubatu2 = "○";
#$winnercomment  = "<span style='color:red;'>（戦評）</span><br>".$senpyo1."（$tss1name）<hr>";
#$winnercomment .= "<span style='color:red;'>（戦評）</span><br>".$senpyo2."（$tss2name）<hr>";
}	#if
$result_left = $result10;
$result_right = $result11;
}else{
###相違あり
#$marubatu1 = "";$marubatu2 = "";
#左の勝ち
#if($result10 > $result11){
$marubatu1 = "（相違あり）";$marubatu2 = "（相違あり）";
#$winnercomment = $senpyo1."（$tss1name）";
#}	#if
#右の勝ち
#if($result10 < $result11){
#$marubatu1 = "-";$marubatu2 = "-";
#$winnercomment = $senpyo2."（$tss2name）";
#}	#if
$result_left = "$result10($result21)";
$result_right = "$result11($result20)";
}	#if相違

}	#if 両チーム：報告OK


#片チーム：その１
if( $count3 == 1 && $count2 == 0){
$marubatu1 = "";$marubatu2 = "";
#左の勝ち
if($resultstr1 == 1){
$marubatu1 = "○";$marubatu2 = "×";
$result_left = $result10;
$result_right = $result11;
}	#if
#左の負け
if($resultstr1 == 2){
$marubatu1 = "×";$marubatu2 = "○";
$result_left = $result10;
$result_right = $result11;
}	#if
#$winnercomment  = "<span style='color:red;'>（戦評）</span><br>".$senpyo1."（$tss2name）<hr>";
#$winnercomment .= "<span style='color:red;'>（戦評）</span><br>".$senpyo2."（$tss1name）<hr>";
}	#if 片チーム：その１


#片チーム：その２
if( $count3 == 0 && $count2 == 1){
$marubatu1 = "";$marubatu2 = "";
#右の勝ち
if($resultstr2 == 1){
$marubatu2 = "○";$marubatu1 = "×";
$result_left = $result21;
$result_right = $result20;
}	#if
#右の負け
if($resultstr2 == 2){
$marubatu2 = "×";$marubatu1 = "○";
$result_left = $result21;
$result_right = $result20;
}	#if
#$winnercomment  = "<span style='color:red;'>（戦評）</span><br>".$senpyo2."（$tss2name）<hr>";
#$winnercomment .= "<span style='color:red;'>（戦評）</span><br>".$senpyo1."（$tss1name）<hr>";
}	#if 片チーム：その２

if($resultstr1 == 4){$result_left = "不戦勝";$result_right = "不戦負";}	#if
if($resultstr1 == 5){$result_left = "不戦負";$result_right = "不戦勝";}	#if


$ground = "";
$nichijireport = "";
#試合日と開催地をGET
$sql_str4 = "SELECT * FROM $dbname WHERE contents = 34 and taikaicode = '$taikaicode' and category = 2 and area = '$area' and kumi = '$kumi' and title = '$gedan' and teamnum = $tss1 ORDER BY serial ASC LIMIT 1";
$rs4 = $dbh->prepare($sql_str4);
$rs4->execute();
&sqlcheck($sql_str4);
$count4 = $rs4->rows;	# Hit件数を確保
#print "count4=$sql_str4<br>\n";
if($count4 != 0){
$REFHASH4 = $rs4->fetchrow_hashref;
$ground .= &paramsetsql('body',$REFHASH4);
@TEMP = split(/ /,&paramsetsql('nichiji1',$REFHASH4));
$nichijireport = sprintf("%d年<br>%d月%d日<br>%d時%02d分",split(/-/,$TEMP[0]),split(/:/,$TEMP[1]));
}	#if
##
$result .=<<"END_HTML";
<div style='border:solid 1px #aaaaaa;padding:10px;margin-bottom:10px;'>
<div class="na">
<table width="760" border="0" cellpadding="0" cellspacing="0" class="na">
<tr>
<td width="48">$marubatu1&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tss1name&nbsp;</td>
<td width="72">&nbsp;$result_left</td>
<td width="53">―</td>
<td width="72">$result_right&nbsp;</td>
<td width="230" bgcolor="#F2EEE6">$tss2name&nbsp;</td>
<td width="55">$marubatu2&nbsp;</td>
</tr>
</table>
</div>

<div class="na2" style="text-align:left;">$winnercomment</div>
<div class="na3"  style="text-align:left;">
【コメント】$lastupdated1<br>
$comment1（$tss1name）<hr>
【コメント】$lastupdated2<br>
$comment2（$tss2name）
</div>
$TEAMRESULT{$y}{$x}
</div>
END_HTML
#}	#if count = 2

}	#foreach x
}	#if nichiji
}	#foreach y
if($result ne ""){
$areatag2 .=<<"END_HTML";
<a href="#2:$area"><span>$areaname</span></a>
END_HTML
$arealist2 .=<<"END_HTML";
<h2 class='subti' id='2:$area'>$areaname</h2>
<div class="subti2"><span>$kuminame</span></div>
<h3>試合結果</h3>
$result
END_HTML
}	#if
$result = "";
}	#for j
if($count1 != 0 && $areatag2 eq ""){
$areatag2 = "<p class='attention'>※まだ結果報告が揃っておりません。</p>";
}	#if


########################
########################


}	#sub





# -----------------------------------------------------------------
# アクセスログ
# -----------------------------------------------------------------
sub accesslog {
my $remoteaddr = $ENV{'REMOTE_ADDR'};
my $referer = $ENV{'HTTP_REFERER'};
my $remotehost = $ENV{'REMOTE_HOST'};
my $data = "";

foreach $key(keys(%ENV)) {
    $data .= "$key:$ENV{$key}\n";
}	#foreach

my $mes =<<"HTML_END";
referer:$referer\n\n
remotehost:$remotehost\n\n
remoteaddr:$remoteaddr\n\n
$data
HTML_END
#
my $sql_str = qq{INSERT INTO accesslog(logtext) VALUES (?);};
my $rs = $dbh->prepare($sql_str);
$rs->execute(
$mes,
);
&sqlcheck($sql_str);	#SQLエラーチェック


}	#sub





1;