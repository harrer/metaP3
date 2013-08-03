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
	my $parentID = $_[0]; chomp($parentID);
	my @ls = `ls users/`;
	my $tabs = (defined $_[1])? $_[1] : 0;
	foreach(@ls){
		my $parent = substr($parentID, 16, 16);
		if($_ =~ m/^($parent\d{16})$/ && $1 ne $parentID){#found a son
			my $t = "";
			for(1..$tabs){#append tabs
				$t .= "\t";
			}
			print "$t$1\n";
			&buildTree($1, $tabs+1);
		}
	}
}



&buildTree(&findRoot("13754285045848371375428518689530"));
#print &findRoot("13754285045848371375428518689530");

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
		my $pID = substr($_[0], 16, 16);
		`mkdir users/$pID$number`;
	}
	else{
		`mkdir users/$number$number`;
	}
	print $number."\n";
}

#&mkdirs("13754284785691341375428504584837");
