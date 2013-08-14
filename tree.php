<?php

$idLength = 16;
$pattern = "/([0-9]{".$idLength."})([0-9]{".$idLength."})$/";

function findRoot($ID = "13748300638451741374830063845174") {
	global $idLength;
	global $pattern;
	preg_match($pattern, $ID, $matches);
    $parent = $matches[1];
    $child = $matches[2];
	$names = lsToArray("users/*");
	while($matches[1] != $matches[2]){#is not root
		foreach($names as $value){
			preg_match($pattern, $value, $matches);
			if($matches[2] == $parent){
				$parent = $matches[1];
				$child = $matches[2];
				$ID = $value;
				break;
			}
		}
	preg_match($pattern, $ID, $matches);
	}

	preg_match($pattern, $ID, $matches);
	if($matches[1] == $matches[2]){
		return $ID;
	}
}

//echo(findRoot());

$tree = array();

function buildTree($parentID){
	global $tree;
	push($tree, $parentID);
	$ls = lsToArray("users/*");
	foreach($ls as $value){
		$parent = substr($parentID, $idLength, $idLength);
		if(preg_match("/".$parent."[0-9]{".$idLength."}/", $value, $matches) && $matches[1] != $parentID){#found a son
			$son = &buildTree($matches[1]);
			push($t
			return
		}
	}
	return $tree;
}

function lsToArray($path){
	$ls = glob($path, GLOB_ONLYDIR);
	foreach($ls as &$value){
		$value = basename($value);
	}
	return $ls;
}

?>

