<?php
error_reporting(1);
ini_set('max_execution_time', 0);
set_time_limit(0);
ignore_user_abort(true);
ini_set('memory_limit', '512M');

$file = 'test.txt';
$rez = 'Result.txt';

$text = file($file);
$row_number = 0;
foreach ($text as $nomerStr => $stroka)
{
    $row_number++;
    $arr = array();
    list($brand, $part_n) = explode(";", $stroka);
    $row_in_file = $row_number-1;
    file_put_contents("temp.txt", $text[$row_in_file], FILE_APPEND);
    //unset($text[$row_in_file]);
    file_put_contents($file, implode("", $text));
    $part_nForSearch = strtolower($part_n);
    $part_n2=str_replace('-','',$part_n);
    $part_nThroughDef = str_replace(' ','-',$part_n);
    $brandForSearch = strtolower($brand);
    $host = 'http://www.trident-supply.com';
    $n=10;

    $proxi1 = '166.88.107.15:8800';
    $proxi2 = '166.88.107.151:8800';
    $proxi3 = '192.126.161.16:8800';
    $proxi4 = '192.126.161.45:8800';
    $proxi5 = '192.126.178.71:8800';
    $proxi6 = '192.126.178.118:8800';
    $proxi7 = '192.126.178.35:8800';
    $proxi8 = '192.126.178.85:8800';
    $proxi9 = '192.161.163.226:3128';
    $proxi10 = '192.161.163.79:3128';

    $arrayProxi  = array ($proxi1, $proxi2, $proxi3, $proxi4, $proxi5, $proxi6, $proxi7, $proxi8, $proxi9, $proxi10);
    $proxy = $arrayProxi[rand(0,9)];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_USERAGENT, 'IE20');
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, '1');
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_CIPHER_LIST, 'TLSv1');
    //curl_setopt($ch, CURLOPT_PROXY, $proxy);
    //curl_setopt($ch, CURLOPT_URL, 'http://www.combustiondepot.com/search_results/'.$part_n.'/70');
    curl_setopt($ch, CURLOPT_URL, 'http://www.trident-supply.com/SearchResults.asp?searching=Y&sort=11&search=' . urlencode($part_n) . '&show=45&page=1&brand=Rothenberger');
    $html = curl_exec($ch);

    if($html == FALSE){
        for ($c = 0; $c < 7; $c++){

            //curl_setopt($ch, CURLOPT_PROXY, $proxy);
            curl_setopt($ch, CURLOPT_URL, 'http://www.trident-supply.com/SearchResults.asp?searching=Y&sort=11&search=' . urlencode($part_n) . '&show=45&page=1&brand=Rothenberger');
            $html = curl_exec($ch);

            if($html == TRUE){
                break;
            }
            sleep(rand(3,8));
        }
    }




        preg_match_all( '/<td valign=\"top\" width=\"33%\" align=\"center\">.{0,20}<a href=\"([^`]*?)\"/is', $html, $link);




        for($i=0; $i<count($link[1]); $i++)
        {
            $url = $link[1][$i];


            //$data = file_get_contents($url);
            //curl_setopt($ch, CURLOPT_PROXY, $proxy);
            curl_setopt($ch, CURLOPT_URL, $url);
            $data = curl_exec($ch);

            if($data == FALSE){
                for ($c = 0; $c < 7; $c++){

                    //curl_setopt($ch, CURLOPT_PROXY, $proxy);
                    curl_setopt($ch, CURLOPT_URL, $url);
                    $data = curl_exec($ch);

                    if($data == TRUE){
                        break;
                    }
                    sleep(rand(3,8));
                }
            }


            preg_match_all( '/<input type=\"hidden\" name=\"ProductCode\" value=\"([^`]*?)\"/is', $data, $sku);
            $skuItem = trim(strip_tags(strtolower($sku[1][0])));
            $skuItem = str_ireplace(array(" ", "\r", "\n"),"",$skuItem);



            preg_match_all( '/<span itemprop=\"name\">([^`]*?)<\/span>/is', $data, $name);

            if(strcasecmp($skuItem, $part_n) == 0 && stripos('  ' . $name[1][0], 'Rothenberger') > 0)
            {

                preg_match_all( '/<span itemprop=\'price\' content=\'([^`]*?)\'/is', $data, $prices);


                $priceItem = str_replace(array(" ","\r","\n","\t", "&#36;"),"",trim(strip_tags($prices[1][0])));
                //echo 'res ' . $brand .';'. $part_n . ';' . $priceItem . "</br>";
                $priceItem = str_replace(array("$",","),"",$priceItem);
                $product_row = $brand . ';' . $part_n . ';' . $priceItem.';'.$url;

                file_put_contents($rez, $product_row."\r\n", FILE_APPEND);
                $n--;
                break;
            }
        }


    curl_close($ch);
    if($n == 10)
    {
        $product_row = $brand.';'.$part_n.';0;' . 'http://www.trident-supply.com/SearchResults.asp?searching=Y&sort=11&search=' . urlencode($part_n) . '&show=45&page=1&brand=Rothenberger';
        file_put_contents($rez, $product_row."\r\n", FILE_APPEND);
        sleep(rand(0,2));
        //echo 'res ' . $brand .';'. $part_n . ';no product L' . "</br>";
    }
    //echo "res " . $product_row . "</br>";
}
?>
done!

