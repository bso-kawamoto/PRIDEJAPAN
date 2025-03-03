/* ページ全体 */
* {
    font-size : 100% ;
    margin : 0 ;
    padding : 0 ;
}

/* body全体 */
body {
    font-family:"ＭＳ Ｐゴシック", Osaka, "ヒラギノ角ゴ Pro W3";
    text-align : center ;
    font-size : 75% ;
}

/* メールフォーム全体を囲うidタグ */
#contents_wrapper {
    width : {$basic_formwidth}px ;
    margin : 0 auto 30px ;
    padding : 20px 15px 0 ;
    {$color_background}
    {$color_line}
}

/* 入力フォームを囲うclassタグ */
.setting_section {
    margin-bottom : 25px ;
}

/* ボタンを囲うclassタグ */
.button_box {
    clear : both ;
    padding : 8px ;
    text-align : center ;
}

/* 赤文字を表示するためのclassタグ */
.red_txt {
    {$color_error}
}

/* 左詰の文字を表示するためのclassタグ */
.left_txt {
    text-align : left;
}

/* 説明文を表示するためのidタグ */
#txt_explain {
    {$color_explain}
}

/* コンテンツ内の[p]タグ */
#contents p {
    margin-bottom : 1em ;
    text-align : left ;
}

/* コンテンツ内の[h3]タグ */
#contents h3 {
    {$color_title}
    padding : 5px 10px 5px 6px ;
    text-align : left ;
    font-size : 120% ;
    margin-bottom : 10px ;
}

/* コンテンツ内の内部タグ */
#contents .inner {
    padding : 0 15px ;
}

/* コンテンツ内のフォームに使用する[table]タグ */
#contents table {
    width : {$basic_tablewidth}px ;
    border-collapse : collapse ;
    border-left : 1px solid #b3b3b3 ;
    border-top : 1px solid #b3b3b3 ;
    border-right : none ; 
    border-bottom : none ;
}

/* コンテンツ内のフォームに使用する[th]タグ */
#contents table th {
    border-right : 1px solid #b3b3b3 ;
    border-bottom : 1px solid #b3b3b3 ;
    border-top : none ; 
    border-left : none ;
    {$color_menubg}
    {$color_menufont}
    padding : 3px 5px ;
}

/* コンテンツ内のフォームに使用する[td]タグ */
#contents table td {
    border-right : 1px solid #b3b3b3 ;
    border-bottom : 1px solid #b3b3b3 ;
    border-top : none ; 
    border-left : none ;
    padding : 3px 5px ;
    text-align : left ;
}

/* フォーム全体 */
#main_table * {
	font-family : sans-serif ;
}

/* フォーム内の入力欄 */
#main_table input {
    width : {$basic_inputwidth}px ;
}

/* フォーム内の入力欄 */
#main_table textarea {
    width : {$basic_textareawidth}px ;
}
