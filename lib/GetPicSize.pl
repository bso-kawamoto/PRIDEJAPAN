#!/usr/bin/perl

while( $PicFile = shift @ARGV ){
    ( $PicFormat, $PicWidth, $PicHeight )
	= &GetImageSize( $PicFile, 'PIC' );

    if( $PicWidth > 0 && $PicHeight > 0 ){
	print "*$PicFile \t($PicFormat)\t $PicWidth x $PicHeight\n";
	
    }else{
	print "-$PicFile\n";
    }
}


#############################################################################
#
# 画像のサイズ(幅と高さ)を取得するサブルーチン
#
#                    2001-2006 Copyright (C) cachu <cachu@cocoa.ocn.ne.jp>
#
#  使い方:
#
#      ( $format, $width, $height ) =  &GetImageSize( $FileName, [$out] );
#
#            $format : 画像フォーマット
#             $width : 幅
#            $height : 高さ
#          $FileName : 画像ファイル名
#               $out : ファイルハンドル(省略可)
#
#
#      ファイル名を引数として渡すと画像フォーマット、幅、高さの情報を
#   返します。画像フォーマットの値は
#
#       'JPEG-JFIF'       … JFIF フォーマットの JPEG 形式
#       'JPEG-JFIF-EXIF'  … JFIF フォーマットの JPEG 形式 (Exif 情報あり)
#       'JPEG-EXIF'       … Exif フォーマットの JPEG 形式
#       'PNG'             … PNG 形式
#       'GIF'             … GIF 形式
#       'BMP'             … Windows ビットマップ形式
#       'TIFF'            … TIFF 形式
#       'TIFF-EXIF'       … Exif フォーマットの TIFF 形式
#       'PBM'             … PBM 形式
#       'PGM'             … PGM 形式
#       'PPM'             … PPM 形式
#       'TGA'             … TGA 形式
#
#   となります。 Exif フォーマットの JPEG 画像(デジカメの画像)には
#   さまざまな情報が記録されています。その内容を表示したい場合には
#   ExifInfo.pl をご利用下さい。
#
#
#   2004/05/09 現在対応済画像フォーマット:
#       - GIF
#       - Windows Bit Map
#       - JPEG (JFIF)
#       - JPEG (Exif)
#       - TIFF
#       - TIFF (Exif)
#       - PNG
#       - PPM/PGM/PBM
#       - TGA
#
#   更新履歴
#      
#      ・2006/01/27 - バグ修正
#      ・2004/08/02 - バグ修正
#      ・2004/05/09 - Exif 情報の画像情報はオリジナルのものとは限らない
#                     ため JPEG 形式の処理の変更
#      ・2003/09/10 - 8/22 変更個所について処理する順番を変更した
#      ・2003/08/22 - 某サイトで取得できないというものに対応してみた
#                         + 試しですので採用するかどうかはまだ分かりません
#      ・2003/07/13 - Exif 形式の TIFF 画像の処理を追加
#      ・2003/05/27 - バグ修正
#      ・2003/03/27 - Exif 情報に関しては独立して別サブルーチン化した
#      ・2003/01/06 - 引数の調整
#      ・2002/12/15 - Exif 情報を返すようにした
#                         + まだ不完全(Olympus C-2 ZOOM で使われている
#                           タグしか処理していません)
#      ・2002/07/17 - PGM/PBM, TGA 形式に対応 (TGA 形式はちょっとあやしい…)
#      ・2002/07/04 - Exif 形式データ取得に関するバグ修正
#      ・2002/06/05 - Exif 形式データ取得に関するバグ修正
#                   - 読み込みをファイルハンドルからファイル名に修正
#      ・2001/12/14 - 初期バージョン
#
sub GetImageSize{
    my ( $IMG, $in ) = @_;
    my ( %SHT, %LNG );
    my ( $buf, $mark, $type, $f_size, $width, $height );
    my ( $TAG, $TYPE, $COUNT, $V_OFFSET, $PK, $ENTRY, $Exif_IFD );
    my ( $endian, $dummy1, $dummy2, $dummy, $EOI, $APP1, $length, $exif );
    my ( $format, $offset, $line, $CODE, $jfif, $i );
    my @TGA;
    my $ntag;

    # 定数
    $mark = pack("C", 0xff);
    %SHT = ( 'II' => 'v', 'MM' => 'n' );
    %LNG = ( 'II' => 'V', 'MM' => 'N' );

    # 初期値
    $endian   = '';
    $width    = -1;
    $height   = -1;
    $format   = '';
    $Exif_IFD = -1;

    if( $in eq '' ){
	$in = 'IMG';
    }

    open( $in, $IMG ) || return( '', -1, -1 );

    binmode($in);
    seek( $in, 0, 0 );
    read( $in, $buf, 6 );

    # GIF 形式
    if($buf =~ /^GIF/i){
	$format = 'GIF';
	read( $in, $buf, 2 );
	$width  = unpack("v*", $buf);
	read( $in, $buf, 2);
	$height = unpack("v*", $buf);

    # Windows Bit Map 形式
    }elsif($buf =~ /BM/){
	$format = 'BMP';
	seek( $in, 12, 1 );
	read( $in, $buf, 8 );
	($width, $height) = unpack("VV", $buf);

    # TIFF 形式
    }elsif( $buf =~ /(II)/ || $buf =~ /(MM)/ ){
	$format = 'TIFF';
	$endian = $1;
	seek( $in, 0, 0 );
	read( $in, $buf, 8 );
	( $endian, $dummy1, $offset ) = 
	    unpack( "A2$SHT{$endian}$LNG{$endian}", $buf );

	seek( $in, $offset, 0 );
	read( $in, $buf, 2 );
	$ENTRY = unpack( $SHT{$endian}, $buf );

	for( $i = 0 ; $i < $ENTRY ; $i++ ){
	    read( $in, $buf, 8 );
	    $PK = "$SHT{$endian}$SHT{$endian}$LNG{$endian}";
	    ( $TAG, $TYPE, $COUNT ) = unpack( $PK, $buf );

	    read( $in, $buf, 4 );
	    ( $TAG != 256 && $TAG != 257 ) and next;
	    if( $TYPE == 3 ){
		$PK = "$SHT{$endian}";
	    }elsif( $TYPE == 4 ){
		$PK = "$LNG{$endian}";
	    }else{
		next;
	    }

	    $V_OFFSET = unpack( $PK, $buf );

	    # Image width and height
	    ( $TAG == 256   ) and ( $width  = $V_OFFSET   );
	    ( $TAG == 257   ) and ( $height = $V_OFFSET   );
	    ( $TAG == 34665 ) and ( $format .= '-EXIF'    );
	}

    # PPM 形式
    }elsif( $buf =~ /^(P[123456])\n/ ){
	if( $1 eq 'P1' || $1 eq 'P4' ){
	    $format = 'PBM';
	}elsif( $1 eq 'P2' || $1 eq 'P5' ){
	    $format = 'PGM';
	}else{
	    $format = 'PPM';
	}
	seek( $in, 0, 0 );
	<$in>;
	while( <$in> ){
	    next if ( /^\#/ );
	    chomp;
	    ( $width, $height ) = split( /\s+/, $_ );
	    last;
	}

    # PNG 形式
    }elsif( $buf =~ /PNG/){
	$format = 'PNG';
	seek( $in, 8, 0 );

	while(1){
	    read( $in, $buf, 8 );
	    ( $offset, $CODE ) = unpack( "NA4", $buf );

	    if( $CODE eq 'IHDR' ){
		read( $in, $buf, 8 );
		( $width, $height ) = unpack( "NN", $buf );
		seek( $in, $offset-8+4, 1 );
		last;

	    }elsif( $CODE eq 'IEND' ){
		last;

	    }else{
		seek( $in, $offset+4, 1 );
	    }
	}

    }else{
	# JPEG 形式
	seek( $in, 0, 0 );
	read( $in, $buf, 2 );
	( $buf, $type ) = unpack("C*", $buf );
	if( $buf == 0xFF && $type == 0xD8 ){
	    $format = 'JPEG';
	  JPEG:while(read( $in, $buf, 1 )){
	      if(($buf eq $mark) && read( $in, $buf, 3 )){
		  $type   = unpack("C*", substr($buf, 0, 1));
		  $f_size = unpack("n*", substr($buf, 1, 2));

		  ( $type == 0xD9 ) and ( last JPEG );
		  ( $type == 0xDA ) and ( last JPEG );

		  if($type == 0xC0 || $type == 0xC2){
		      read( $in, $buf, $f_size-2 );
		      $height = unpack("n*", substr($buf, 1, 2));
		      $width  = unpack("n*", substr($buf, 3, 2));
		      ( $format =~ /EXIF/ ) and ( last JPEG );

		  }elsif( $type == 0xE1 ){
		      read( $in, $buf, $f_size-2 );
		      $exif = unpack( "A4", substr( $buf, 0, 4 ) );
		      if( $exif =~ /exif/i ){
			  $format .= '-EXIF';
			  ( $width > 0 && $height > 0 ) and ( last JPEG );
		      }

		  }elsif( $type == 0xE0 ){
		      read( $in, $buf, $f_size-2 );
		      $jfif = unpack( "A4", substr( $buf, 0, 4 ) );
		      if( $jfif =~ /jfif/i ){
			  $format .= '-JFIF';
		      }

		  }elsif( $type == 0x01 || $type == 0xFF ||
			  ( $type >= 0xD0 && $type < 0xD9 ) ){
		      seek( $in, -2, 1 );

		  }else{
		      read( $in, $buf, $f_size-2 );
		  }
	      }
	  }
	}

	if( $width > 0 && $height > 0 ){
	    close( $in );
	    return( $format, $width, $height );
	}

	# TGA 形式
	seek( $in, 0, 0 );
	read( $in, $buf, 18 );
	@TGA = unpack( "CCCvvCvvvvCC", $buf );
	if( $TGA[1] == 0 || $TGA[1] == 1 ){
	    if( $TGA[2] ==  0 || $TGA[2] == 1 || $TGA[2] ==  2 ||
		$TGA[2] ==  3 || $TGA[2] == 9 || $TGA[2] == 10 ||
		$TGA[1] == 11 ){
		$format = 'TGA';
		$width  = $TGA[8];
		$height = $TGA[9];
	    }
	}

    }

    close( $in );
    return( $format, $width, $height );
}

1;

#############################################################################
