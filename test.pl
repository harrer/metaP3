#!usr/bin/perl
use strict; use warnings;
use feature qw(say);

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

sub getSons{
	my $root = $_[0];
	my @names = `cat directories`;# ls
	my @tree = ($root);
	my $level = 1;
	foreach(@names){
		$_ =~ m/(\d{16})(\d{16})/;
	}
}

say &findRoot("13754284785691341375428497863563");

# k_f is father to k_s_i <=> k_f(16..31) eq k_s_i(0..15)
