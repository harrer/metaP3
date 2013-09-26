<?php

$idLength = 16;
$pattern = "/([0-9]{".$idLength."})([0-9]{".$idLength."})$/";
$usersDir = "/home/metabolomics/tmp/users/*";//metap-dev/metaP/users/*";

function findRoot($ID) {
	global $idLength, $pattern, $usersDir;
	preg_match($pattern, $ID, $matches);
    $parent = $matches[1];
    $child = $matches[2];
	$names = lsToArray($usersDir);
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

function findAllRoots(){
	global $idLength, $usersDir;
	$roots = array();
	$users = lsToArray($usersDir);
	foreach($users as $value){
		if(strcmp(substr($value, 0, $idLength), substr($value, $idLength, $idLength)) == 0){ //is a root (parent) job
			array_push($roots, $value);
		}
	}
	return $roots;
}

function buildTree($parentID) {
	$tree = array();
	global $idLength, $usersDir;
    array_push($tree, $parentID);
    $ls = lsToArray($usersDir);
    foreach ($ls as $value) {
        $parent = substr($parentID, $idLength, $idLength);
        if (preg_match("/" . $parent . "[0-9]{" . $idLength . "}/", $value, $matches) && $matches[0] != $parentID) {#found a son
			array_push($tree, buildTree($value));
        }
    }
    return $tree;
}

function lsToArray($path) {
    $ls = glob($path, GLOB_ONLYDIR);
    foreach ($ls as &$value) {
        $value = basename($value);
    }
    return $ls;
}

function showTree(){
	$roots = findAllRoots();
	foreach ($roots as $root){
		echo(showTreeAux(buildTree($root)));
	}
}

function showTreeAux($roots = array()){
	$echo = "<ul>";
	foreach($roots as $index => $root){
		if($index == 0){
			$echo .= "<li>" . $root . "</li>\n";
		}
		else{ //sizeof($root) > 1	if($index > 0)
			$echo .= "<li>" . showTreeAux($root) . "</li>\n";
		}
	}
	$echo .= "</ul>";
	return $echo;
}

function showTreeSimple(){
	$roots = findAllRoots();
	foreach($roots as $root){
		print_r(buildTree($root));
		echo("<br>");
	}
}

//print_r(findAllRoots());
//print_r(unserialize(serialize(buildtree(findRoot("13754285186895301375434289583874")))));
//print_r(buildtree(findRoot("13794182717410031379418417430622")));
?>

