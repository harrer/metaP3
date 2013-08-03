<?php

function findRoot($ID = "12348765") {
    $parent = substr($ID, 0, 16);
    $child = substr($ID, 16);
    $names = `ls users/`;
//    foreach ($names as $value) {
//        print $value;
//    }
    print $names;
//  preg_match("/[0-9]{4,}[0-9]{4,}/", $ID, $matches))
}

findRoot();

/* 	
  while($1 ne $2){#is not root
  foreach(@names){
  $_ =~ m/(\d{16})(\d{16})/;
  if($2 eq $parent){
  $parent = $1;
  $child = $2;
  $ID = $_;
  last;
  }
  }
  $ID =~ m/(\d{16})(\d{16})/;
  }
  $ID =~ m/(\d{16})(\d{16})/;
  if($1 eq $2){
  $ID;
  } */
?>

