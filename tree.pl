#!/usr/bin/perl
use strict; use warnings;

sub findParent{}

sub buildTree
{
	my $parentID = $_[0];
	my @ls = `ls users/`;
	#my @sons = ($parentID);
	my $tabs = (defined $_[1])? $_[1] : 0;
	foreach(@ls){
		my $parent = substr($parentID, 16, 16);
		if($_ =~ m/^($parent\d{16})$/ && $1 ne $parentID){
			#my @son = &buildTree($1);
			my $t = "";
			for(1..$tabs){
				$t .= "\t";
			}
			print $t.$1."\n";
			&buildTree($1, $tabs+1);
			#my $ref = \@son;
			#push(@sons, $ref);
		}
	}
	#return(@sons);
}

&buildTree("13748300604521801374830060452180");
#my @tree = &buildTree("13748300604521801374830060452180");
#my $i=0;
#foreach(@tree){
#	print $_->[0]."\n" unless $i==0;
#	$i++;
#}

sub mkdirs
{
	my $number = time;
	chomp($number);
	my $extraNumber = int(rand()*1000000);
	while($extraNumber<100000){############## IN RUN.CGI ÜBERNEHMEN!!!
		$extraNumber = int(rand()*1000000);
	}
	chomp($extraNumber);
	$number .= $extraNumber;
	chomp($number);
	if(defined $_[0]){
		`mkdir users/$_[0]$number`;
	}
	else{
		`mkdir users/$number$number`;
	}
	print $number."\n";
}

#&mkdirs(1374830086569720);


