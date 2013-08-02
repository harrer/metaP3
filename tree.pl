#!/usr/bin/perl
use strict; use warnings;

sub findRoot{
	my $ID = $_[0];
	$ID =~ m/(\d{16})(\d{16})/;
	my $parent = $1;
	my $child = $2;
	my @names = `ls users`;
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
	}
}

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

&buildTree("13754284785691341375428478569134");

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

#&mkdirs(1375428504584837);


