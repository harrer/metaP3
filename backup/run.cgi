#!/usr/bin/perl
#FILE:    run.cgi
#AUTHOR:  Karsten Suhre
#DATE:    Mon Oct  6 11:09:03 CEST 2008
#PURPOSE: metaP web server
#BUGS:    
#MODIF:   

# "Beware of bugs in the above code; I have only proved it correct, not
# tried it."
#               -- Donald Knuth

use CGI;#, strict;
use Math::BigFloat;

my $maxlen = 1000000; # maximum allowed number of allowed input lines

sub get_options ( $ $ ) {
	( my $optionsfile, my $keyword ) = @_;
	my @value = `grep '^$keyword' $optionsfile 2> /dev/null`;
	my $value = "unknown";
	$value = $value[0] if(defined $value);
	chomp $value; $value =~ s/^M//; $value =~ s/^$keyword[ \t]*=[\t ]*//;
	$value;
}

sub error ( $ ) {
	( $message ) = @_;
	print "<HTML><br><H1>$message</H1>\n";
	print "<br><H2>Please report this error to g.kastenmueller\@helmholtz-muenchen.de</H2>\n";
	print <<EEOOFF777;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
EEOOFF777
	print "</HTML>\n";
	exit;
}

sub print_subheadder () {

	# define the options file
	$optionsfile = "$BASE/options";

	# show job ID and identifier
	$ORG = &get_options( $optionsfile, 'ORG' );
	$jobid = &get_options( "$BASE/options", 'JOBID' );
	print "<H4>JobID: <A HREF=\"$CGI?TASK=SHOWSEQ&ID=$ID\">$ID</A></H4>\n";
	print "<H2>***&nbsp <FONT COLOR=\"E50030\">$jobid</FONT>&nbsp ***</H2>\n";

	# show the submenu
	print <<EOF444;
<table border="0" cellpadding="0" cellspacing="0">
<tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
&nbsp
<a href="$CGI?TASK=MODIFY&ID=$ID"><font color="#FFFFFF">Modify this job</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=RUN&ID=$ID"><font color="#FFFFFF">Metabolites</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=SAMPLES&ID=$ID"><font color="#FFFFFF">Samples</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=QUALITY&ID=$ID"><font color="#FFFFFF">Quality Check</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=PCA&ID=$ID"><font color="#FFFFFF">PCA</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=KENDALL&ID=$ID"><font color="#FFFFFF">Kendall</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=HYPOTHESIS&ID=$ID"><font color="#FFFFFF">Hypothesis test</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=SHOWLOG&ID=$ID"><font color="#FFFFFF">Logs</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$CGI?TASK=SHOWSEQ&ID=$ID"><font color="#FFFFFF">Input data</font></a>
<font color="#FFFFFF">&nbsp|&nbsp</font>
<a href="$HTMLBASE/download.zip"><font color="#FFFFFF">Download results</font></a>

&nbsp
</td></tr>
</table>
<p>
EOF444

}

	
$query = new CGI;

$CGItask = $query->param("TASK"); chomp($CGItask);
$CGIatom = $query->param("ATOM"); chomp($CGIatom);
$filename = $query->param("UPLOAD"); chomp($filename);
$CGIformat = $query->param("FORMAT"); chomp($CGIformat);
$CGImissing = $query->param("MISSING"); chomp($CGImissing);
$CGIoutlier = $query->param("OUTLIER"); chomp($CGIoutlier);
$CGIdelMetabs = $query->param("DEL_METABS"); chomp($CGIdelMetabs);
$CGIreference = $query->param("REFERENCE"); chomp($CGIreference);
$CGIratios = $query->param("RATIOS"); chomp($CGIratios);
$CGIjobID = $query->param("JOBID"); chomp($CGIjobID);
$CGIprivat = $query->param("PRIVAT"); chomp($CGIprivat);
$CGIemail = $query->param("EMAIL"); chomp($CGIemail);
$CGIatom2 = $query->param("ATOM2"); chomp($CGIatom2);
$filename2 = $query->param("UPLOAD2"); chomp($filename2);
$CGIatom3 = $query->param("ATOM3"); chomp($CGIatom3);
$CGIupload3 = $query->param("UPLOAD3"); chomp($CGIupload3); #TODO: not tested yet!!
$CGImetaboliteset = $query->param("METABOLITESET"); chomp($CGImetaboliteset);
$CGIspecies = $query->param("SPECIES"); chomp($CGIspecies);

$TASK = $query->url_param("TASK"); chomp($TASK);
$ID = $query->url_param("ID"); chomp($ID);
$PHENO = $query->url_param("PHENO"); chomp($PHENO);

if(defined $CGItask) {
	$TASK = $CGItask;
}


print "Content-type: text/html", "\n\n";

# CGI internal PATHs
$RACINE = "/var/www/metap3";
$USERDATA = "$RACINE/users";
$EXEC = "/var/www/metap3/exec";
$DATA = "/var/www/metap3/data";
$LOG = "/tmp/metap3.log";

# HTML PATHs
$HTML = ".";
$HTMLUSERDATA = "users";
$IMAGES = "images";

# path to this CGI
$CGI = $0;
$CGI =~ s/.*\///;

# log the query
#system "echo `date +'%F_%R'`'\t$ENV{'REMOTE_ADDR'}'\t$ENV{'REMOTE_HOST'}'\t$ENV{'QUERY_STRING'}'>>$LOG"; 


#############################################################
################ NEW ########################################
#############################################################
if($TASK eq "NEW" || $TASK eq "NEWCHILD") {
$number = time;
chomp($number);
$extraNumber = int(rand()*1000000);
chomp($extraNumber);
if($TASK eq "NEW"){
	$ID = "$number$extraNumber";
	$ID .= $ID;
}
else{
	if($CGIjobID =~ m/^(\d{16})(\d{16})$/){
	$ID = $2.$number.$extraNumber; chomp($ID);
	}
	elsif($CGIjobID =~ m/^(\d{16})$/){
		$ID .= $number.$extraNumber; chomp($ID);
	}
	else{print "unsupported ID format";}
}
$upload_dir = "$USERDATA/$ID";
chomp($upload_dir);

# create a directory for this job
system("mkdir $upload_dir");
system("chmod 777 $upload_dir");
system "mkdir $upload_dir/barplots; chmod 777 $upload_dir/barplots";

$BASE = $upload_dir;

$allok = 1;

# get the form parameters and set defaults
if(defined $CGIformat) { $FORMAT = $CGIformat; } else { $FORMAT = 'undef'; };
if(defined $CGImissing) { $MISSING  = $CGImissing; } else { $MISSING  = 'undef'; };
if(defined $CGIoutlier) { $OUTLIER  = $CGIoutlier; } else { $OUTLIER  = 'undef'; };
if(defined $CGIdelMetabs) { $DEL_METABS  = $CGIdelMetabs; } else { $DEL_METABS  = 'undef'; };
if(defined $CGIreference) { $REFERENCE  = $CGIreference; } else { $REFERENCE  = 'undef'; };
if(defined $CGIratios) { $RATIOS  = $CGIratios; } else { $RATIOS  = 'undef'; };
if(defined $CGImetaboliteset) { $METABOLITESET  = $CGImetaboliteset; } else { $METABOLITESET  = 'other'; };
if(defined $CGIspecies) { $SPECIES  = $CGIspecies; } else { $SPECIES  = 'other'; };


# e-mail user id and the-like
if(defined $CGIprivat) { $PRIVAT = $CGIprivat; } else { $PRIVAT = 0; };
if(defined $CGIjobID) { $JOBID = $CGIjobID; } else { $JOBID = ""; };
$JOBID =~ s/[`\\'"]//g;
if(defined $CGIemail) {
	$EMAIL = $CGIemail;
	$EMAIL =~ s/[`\\'"; ]//g;
} else { $EMAIL = "unknown" }
if(length($EMAIL) <= 0) { $EMAIL = "unknown"; };
$USERID = $EMAIL;
$USERID =~ s/@.*//;

$JOBID = "no job-name" if(length($JOBID) == 0);

# get the first file (AbsoluteIDQ data)
if((defined $filename) and (length($filename) > 3)) {
	$upload_filehandle = $query->upload("UPLOAD"); # from file
	open UPLOADFILE, ">$BASE/input.tmp";
	while(<$upload_filehandle>) {
		print UPLOADFILE;
	}
	close UPLOADFILE;
	system("cp $BASE/input.tmp $BASE/input.csv");
	$syserr = `/usr/bin/perl /var/www/metap3/R-2.15.1/library/gdata/perl/xls2csvB.pl -s $BASE/input.tmp $BASE/input.csv 1`;
	system("cat $BASE/input.csv | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/input");
	local $/ = undef;
	open FILE, "$BASE/input" or die "Couldn't open file: $!";
	$ATOM = <FILE>;
	close FILE;
} else {
	$ATOM = $CGIatom; # from paste
	open(ATOM, ">$BASE/input.tmp") or &error("Error 999 in CGI-script, sorry.");
	print ATOM $ATOM;
	close ATOM;
	system("cat $BASE/input.tmp | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/input");
}
if(not defined $ATOM) { $ATOM = ""; };
chomp $ATOM;

# get the second file (e.g. Phenotype data)
if((defined $filename2) and (length($filename2) > 3)) {
	$upload_filehandle2 = $query->upload("UPLOAD2"); # from file
	open UPLOADFILE2, ">$BASE/phenotypes.txt.tmp";
	while(<$upload_filehandle2>) {
		print UPLOADFILE2;
	}
	close UPLOADFILE2;
	#system("cp $BASE/phenotypes.txt.tmp $BASE/phenotypes.txt.tmp2");
	#$syserr = `/usr/bin/perl /home/metap3/R-2.15.1/library/gdata/perl/xls2csvB.pl -s $BASE/phenotypes.txt.tmp2 $BASE/phenotypes.txt.tmp 1`;
	system("cat $BASE/phenotypes.txt.tmp | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/phenotypes.txt");
	local $/ = undef;
	open FILE2, "$BASE/phenotypes.txt" or die "Couldn't open file: $!";
	$ATOM2 = <FILE2>;
	close FILE2;
} else {
	$ATOM2  = $CGIatom2; # from paste
	open(ATOM2, ">$BASE/phenotypes.txt.tmp") or &error("Error 999 in CGI-script, sorry.");
	print ATOM2 $ATOM2;
	close ATOM2;
	system("cat $BASE/phenotypes.txt.tmp | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/phenotypes.txt");
}
if(not defined $ATOM2) { $ATOM2 = ""; };
chomp $ATOM2;

# get the third file (something else - we keep this option for later usage)
if((defined $filename3) and (length($filename3) > 3)) {
	$upload_filehandle3 = $query->upload("UPLOAD3"); # from file
	open UPLOADFILE3, ">$BASE/aux.txt";
	while(<$upload_filehandle3>) {
		print UPLOADFILE3;
	}
	close UPLOADFILE3;
	local $/ = undef;
	open FILE3, "$BASE/aux.txt" or die "Couldn't open file: $!";
	$ATOM3 = <FILE3>;
	close FILE3;
} else {
	$ATOM3  = $CGIatom3; # from paste
	open(ATOM3, ">$BASE/aux.txt") or &error("Error 999 in CGI-script, sorry.");
	print ATOM3 $ATOM3;
	close ATOM3;
}
if(not defined $ATOM3) { $ATOM3 = ""; };
chomp $ATOM3;


# test the length of the input sequence
$totline = `cat $BASE/input | wc -l`;
if($totline > $maxlen) {
	$allok = 0;
	$errmsg = "<H4>ERROR: input file exceeds limit of $maxlen records</H4>
	This limit is imposed to assure that unmonitored jobs will finish within a reasonable time-frame.
	Upon request, we will be glad to open the server to larger jobs.
	Your job would require a limit of $totline records.
	\n";
}

# test if the scan mode is properly defined
if($FORMAT eq "undef") {
	$allok = 0;
	$errmsg = "<H4>ERROR: Data format has not been defined!</H4>
	Please specify your data format.<P>
	\n";
}

# check if there is enough data (empty submission?)
if(($totline) <= 0) {
	$allok = 0;
	$errmsg = "<H4>ERROR: no valid data uploaded (empty file??)</H4>\n$BASE\n";
}

# print HTML header
print "<HTML>\n";
if($allok) { print "<HEAD><META HTTP-EQUIV=\"Refresh\" CONTENT=\"60; URL=$CGI?TASK=RUN&ID=$ID\"> </HEAD>\n"; }
print <<EOF1;
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF1

if($allok) { # if all OK generate the job

	print <<EOF2;
	<H1>Your job has been submitted successfully ... </H1>
	<IMG SRC="$IMAGES/gears.gif">
	<BR>
EOF2

	print "<H4>Your requestid is <A HREF=$CGI?ID=$ID>$ID</A></H4>\n";
	print "<H1><A HREF=$CGI?TASK=RUN&ID=$ID>CLICK HERE</A></H1>\n";
	if($EMAIL =~ '@') {
		print "<BR>you will be notified by e-mail about the status of your job<BR>\n";
	}
	open(CMD,">$BASE/metaPjob.cmd") or &error("Error 998 in CGI-script, sorry.");
	print CMD <<EOFCMD1;
	export PATH=$EXEC:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
	export DATADIR=$DATA
	cd $EXEC
	notify.sh $EMAIL $ID START
	cd $BASE || exit 1
	metaP.sh  1>server_log.txt 2>&1
	chmod 777 * 2> /dev/null
	cd $EXEC
	notify.sh $EMAIL $ID END
	cd $BASE || exit 1
	mv $USERDATA/$ID.metaPjob.started $USERDATA/$ID.metaPjob.finished
EOFCMD1
	close CMD;
	print <<EOF12;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF12
# close STDOUT to flush buffer
	close STDOUT;

# print the options to a file
	open(OPT,">$BASE/options") or &error("Error 995 in CGI-script, sorry.");
	print OPT <<EOFOPT1;
ID        \t=\t $ID
JOBID     \t=\t $JOBID
EMAIL     \t=\t $EMAIL
USERID    \t=\t $USERID
PRIVAT    \t=\t $PRIVAT

FORMAT    \t=\t $FORMAT
METABOLITESET \t=\t $METABOLITESET
SPECIES   \t=\t $SPECIES
MISSING   \t=\t $MISSING
OUTLIER   \t=\t $OUTLIER
DEL_METABS   \t=\t $DEL_METABS
REFERENCE   \t=\t $REFERENCE
RATIOS    \t=\t $RATIOS
DEVELOPT  \t=\t $DEVELOPT
EOFOPT1

# submit the job to the queue
	system "
	chmod +x $BASE/metaPjob.cmd
	ln -s $BASE/metaPjob.cmd $USERDATA/$ID.metaPjob.spooled
	$EXEC/notify.sh $EMAIL $ID SPOOL >/dev/null 2>/dev/null 
	$EXEC/notify.sh $EMAIL $ID INFO >/dev/null 2>/dev/null
	";

} else { # ERROR: give the user some info about his input
	print $errmsg;
	system "rm -r -f $BASE";
	print <<EOF11;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF11

}
}

#############################################################
################ MODIFY #####################################
#############################################################
elsif($TASK eq 'MODIFY') {
my $parent_ID = $ID;
$number = time;
chomp($number);
$extraNumber = int(rand()*1000000);
chomp($extraNumber);
if($ID =~ m/^(\d{16})(\d{16})$/){
	$ID = $2.$number.$extraNumber; chomp($ID);
}
elsif($ID =~ m/^(\d{16})$/){
	$ID .= $number.$extraNumber; chomp($ID);
}
else{print "unsupported ID format";}

print <<html;
<!DOCTYPE html>
<html><head><title>jobs-tree of $parent_ID</title></head><body background=\"images/white.png\" link=\"#014294\" vlink=\"#014294\" alink=\"#014294\" leftmargin=\"0\" topmargin=\"0\" marginwidth=\"0\" marginheight=\"0\"><h4>child-jobs of $parent_ID:</h4><ul>
html

my @ls = `ls`;
my @parents;
my $currentID = $ID;
$currentID =~ m/(\d{16})(\d{16})/;
#do{#trace back to root
	foreach(@ls){
		if(($_ =~ m/(\d{16})(\d{16})/) && ((substr $currentID, 0, 16) eq ($2))){
			#$currentID = $_;
			push(@parents, $_);
			last;
		}
	}
	#$_ =~ m/(\d{16})(\d{16})/;
#}while(($1 ne $2) || $currentID !~ m/^\d{16}$/);
$parent_ID =~ m/^(\d{16})/;
my @children = `ls users/  | egrep $1\[0-9\]{16}\$`;# add all children of the parent job
if(scalar @children == 0){print "<a>no children yet</a>";}
else{
	for(1..scalar @children-1){
  		print "<li><a href = \"$CGI?ID=$children[$_]\">$children[$_]</a></li>";
	}
}
print "</ul> <a href=\"$CGI?ID=$parent_ID\">back</a><br>";#<a href=\"$CGI?TASK=NEWCHILD&ID=$ID\">create new child job</a> <br>
open FILE, "$USERDATA/$parent_ID/input" or die $!;
my @input = <FILE>;
print <<child;

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
<H1>Start a new job</H1>

<FORM ENCTYPE="multipart/form-data" ACTION="run.cgi" METHOD="POST" NAME="frm">
<TABLE WIDTH=600 BGCOLOR="#CCCCCC">
<INPUT TYPE='HIDDEN' NAME='TASK' VALUE='NEWCHILD'>
<INPUT TYPE='HIDDEN' NAME='JOBID' VALUE='$parent_ID'>
<!-- =============================================== -->
<TR>
<TD WIDTH=600 BGCOLOR="#9C9C9C">
<b>Data upload</b>
</TD>
</TR>
<TR>
<TD>
Enter your data<a href="doc.html#format_help" target="_new"><sup>help</sup></a>
<br>
<br><br>
<br>
</TD>
</TR>
<TR>
<TD>
<b>Upload a file<b>
<INPUT TYPE="FILE" NAME="UPLOAD" SIZE=20>
</TD>
</TR>
<TR>
<TD>
<b>or paste your data into the field below</b>
</TD>
</TR>
<TR>
<TD>
  <TEXTAREA ROWS="10" COLS="80" NAME="ATOM">@input</TEXTAREA><!--inlude input -->
</TD>
</TR>
<!-- =============================================== -->
<TR>
<TD WIDTH=600 BGCOLOR="#9C9C9C">
<b>Parameters</b>
</TD>
</TR>
<TR>
<TD>
<TABLE>
<!-- ------------------------------------------------- -->
<TR>
<TD><b><font color="#E50030">Data format</font></b><a href="doc.html#format_help" target="_new"><sup>help</sup></a></TD>
<TD>
<SELECT NAME="FORMAT" SIZE=1>
<OPTION SELECTED VALUE="undef">--- select data format ---</OPTION>
<OPTION VALUE="absoluteIDQ">AbsoluteIDQ Kit 150</OPTION>
<OPTION VALUE="absoluteIDQ180">AbsoluteIDQ Kit 180</OPTION>
<OPTION VALUE="csv">Quant. data (without KEGG Ids)</OPTION>
<OPTION VALUE="csv_kegg">Quant. data (with KEGG Ids)</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Metabolite set</TD>
<TD>
<SELECT NAME="METABOLITESET" SIZE=1>
<OPTION SELECTED VALUE="biocrates">biocrates</OPTION>
<OPTION VALUE="metabolon">metabolon</OPTION>
<OPTION VALUE="other">other</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Species</TD>
<TD>
<SELECT NAME="SPECIES" SIZE=1>
<OPTION SELECTED VALUE="human">human</OPTION>
<OPTION VALUE="mouse">mouse</OPTION>
<OPTION VALUE="other">other</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Validation data in AbsoluteIDQ<a href="doc.html#max_error" target="_new"><sup>help</sup></a> </TD>
<TD>
<SELECT NAME="MISSING" SIZE=1>
<OPTION SELECTED VALUE="n">include out of quantification data</OPTION>
<OPTION VALUE="y">drop out of quantification data</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Outliers<a href="doc.html#outliers" target="_new"><sup>help</sup></a> </TD>
<TD>
<SELECT NAME="OUTLIER" SIZE=1>
<OPTION SELECTED VALUE="n">include outliers</OPTION>
<OPTION VALUE="y">drop outliers</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Noisy metabolites<a href="doc.html#del_metabs" target="_new"><sup>help</sup></a> </TD>
<TD>
<SELECT NAME="DEL_METABS" SIZE=1>
<OPTION SELECTED VALUE="n">include all analytes</OPTION>
<OPTION VALUE="y">drop analytes with cv>0.25</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>References<a href="doc.html#reference" target="_new"><sup>help</sup></a> </TD>
<TD>
<SELECT NAME="REFERENCE" SIZE=1>
<OPTION SELECTED VALUE="n">include references</OPTION>
<OPTION VALUE="y">drop references</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>Metabolite ratios<a href="doc.html#ratios" target="_new"><sup>help</sup></a> </TD>
<TD>
<SELECT NAME="RATIOS" SIZE=1>
<OPTION SELECTED VALUE="n">no ratios</OPTION>
<OPTION VALUE="y">calculate ratios</OPTION>
</SELECT>
</TD>
</TR>
<!-- ------------------------------------------------ -->
</TABLE>
</TD>
</TR>
<!-- =============================================== -->
<TR>
<TD WIDTH=600 BGCOLOR="#9C9C9C">
<b>Job information</b>
</TD>
</TR>
<TR>
<TD>
You may enter a name for your job here.
It will be used as a title for all output
and to identify your job on the <A HREF="run.cgi?TASK=LIST">job status</a> page.<BR>
<INPUT TYPE="TEXT" NAME="JOBID" SIZE=40>
<B>job identifier, optional</B><a href="doc.html#job_identifier" target="_new"><sup>help</sup></a>
</TD>
</TR>
<TR>
<TD>
By default, all jobs are kept privat (remember to keep track of your job-id). 
To make jobs visible to everyone via the
<A HREF="run.cgi?TASK=LIST">job status</a>
page, untick the checkbox below.
<BR>
<INPUT TYPE="CHECKBOX" NAME="PRIVAT" CHECKED>
<B>keep my job private</B><a href="doc.html#privacy" target="_new"><sup>help</sup></a>
</TD>
</TR>
<TR>
<TD>
If you wish to be notified by e-mail once your job is finished,
enter your e-mail address into the field below
(recommended if your job is kept private). Your e-mail
will never be shown on the internet and is used ONLY
to notify you about your job status.
If you enter a pseudonym (any name without a @ character), this will
be used to identify your jobs on the
<A HREF="run.cgi?TASK=LIST">job status</a>
page.<BR>
<INPUT TYPE="TEXT" NAME="EMAIL" SIZE=40>
<B>pseudonym or e-mail, optional</B><a href="doc.html#email" target="_new"><sup>help</sup></a>
<br>
<br>
</TD>
</TR>
<!-- =============================================== -->
<TR>
<TD WIDTH=600 BGCOLOR="#9C9C9C">
<b>Data analysis (optional)</b>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>
Phenotype data for statistical analysis (hypothesis tests etc.)
</TD>
</TR>
<TR>
<TD ALIGN="MIDDLE">
<TABLE WIDTH=500>
  <TR>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
  <b>Paste your phenotype data into the field below</b><a href="doc.html#phenotype_help" target="_new"><sup>help</sup></a>
  <br>
  <TEXTAREA ROWS="5" COLS="10" NAME="ATOM2"></TEXTAREA>
  </TD>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
  <b>or upload a file</b>
  <br>
  <INPUT TYPE="FILE" NAME="UPLOAD2" SIZE=20>
  </TD>
  </TR>
</TABLE>
</TD>
</TR>
<!-- ------------------------------------------------ -->
<TR>
<TD>
Auxiliary data that can be used for setting further parameters may be uploaded here
</TD>
</TR>
<TR>
<TD ALIGN="MIDDLE">
<TABLE WIDTH=500>
  <TR>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
  <b>Paste your data into the field below</b><a href="doc.html#aux_help" target="_new"><sup>help</sup></a>
  <br>
  <TEXTAREA ROWS="5" COLS="10" NAME="ATOM3"></TEXTAREA>
  </TD>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
  <b>or upload a file</b>
  <br>
  <INPUT TYPE="FILE" NAME="UPLOAD3" SIZE=20>
  </TD>
  </TR>
</TABLE>
</TD>
</TR>
<!-- ------------------------------------------------
<TR>
<TD>
Further job options ....
</TD>
</TR>
<TR>
<TD ALIGN="MIDDLE">
<TABLE WIDTH=500>
  <TR>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
  <b>Select the R-script to be used</b><a href="doc.html#script_help" target="_new"><sup>help</sup></a>
  </TD>
  <TD WIDTH=200 ALIGN="MIDDLE" VALIGN="TOP">
    <SELECT NAME="DEVELOPT" SIZE=1>
    <OPTION SELECTED VALUE="default">use the default R scripts</OPTION>
    </SELECT>
  </TD>
  </TR>
</TABLE>
</TD>
</TR>
=============================================== -->
<TR>
<TD WIDTH=600 BGCOLOR="#9C9C9C">
<b>Submission</b>
</TD>
</TR>
<TR ALIGN=CENTER>
<TD>
<br>
  <INPUT TYPE="submit" VALUE="submit">
  <INPUT TYPE="reset" VALUE="reset form">
<br><br>
</TD>
</TR>
<!-- =============================================== -->
</TABLE>
</FORM>

<br> <br> <br>

<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
child
}

 elsif($TASK eq 'LIST') {
#############################################################
################ LIST ######################################
#############################################################
# display a list of all existing jobs

# check if you are administrator
$admin = 0;
$adm = $query->param("ADMIN"); chomp($adm);
$sfall = $query->param("ALL"); chomp($sfall);
if((defined $adm) and ($adm eq "metaP007")) { $admin=1; };
if((defined $sfall)or($admin)) { $lines=999999; } else { $lines=100; };

print <<EOF405;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF405

print "<H1>List of existing jobs</H1>";
if($admin) {
	print "<H1><FONT COLOR=\"FF0000\">administrator access</FONT> <A HREF=\"test.html\">X</A></H1>";
};


# KS BUG FIX: the following line overflows when too many files are in the directory
# @LIBS = `ls -dt $USERDATA/* | sed 's/.*\\///' | grep -v patch | sort -r | head -$lines 2> /dev/null `;
@LIBS = `ls -t $USERDATA/ | sed 's/.*\\///' | grep -v patch | sort -ur | head -$lines 2> /dev/null `;

if($#LIBS < 0) {
	print "<H4>No jobs available; <A HREF=\"$HTML/index.html\">RETURN</A></H4>";
} else {
	print <<EOF407;
<p>
<b>To access a private job, enter its id below</b><br>
<FORM ACTION="$CGI">
<INPUT TYPE="TEXT" NAME="ID" SIZE="20">
</FORM>
<p>
EOF407

	print "<H4>Click on the job id that you wish to explore<H4>";

	if($admin) {
		print "<FORM ACTION=\"$CGI\" METHOD=POST>\n";
		print "<INPUT TYPE=HIDDEN NAME=TASK VALUE=DELETE>\n";
		print "<INPUT TYPE=HIDDEN NAME=ADMIN VALUE=\"$adm\">\n";#TODO: funktioniert??
	}

	print "<TABLE BORDER=1>";
	print "<TR><TH ALIGN=MIDDLE>ID (recent jobs first)</TH><TH ALIGN=MIDDLE>job description</TH><TH ALIGN=MIDDLE>owner</TH><TH ALIGN=MIDDLE>status</TH></TR>";
	for($i=0; $i<=$#LIBS; $i++) {
		$id = $LIBS[$i];
		chomp $id;
		$id =~ s/^M//;

		if(-d "$USERDATA/$id") {
			# determine the status of this runs
			$startfile = "$USERDATA/$id.metaPjob.started";
			$spoolfile = "$USERDATA/$id.metaPjob.spooled";
			$finishfile = "$USERDATA/$id.metaPjob.finished";
			$resultfile = "$USERDATA/$id/success";
			$optionsfile = "$USERDATA/$id/options";
			$status = "unknown";
			if(-e $finishfile) { 
				if(! -e $resultfile) { 
					$status = "failed";
				} else {
					$status = "finished";
				}
			} elsif(-e $spoolfile) {
				$status = "spooled";
			} elsif(-e $startfile) {
				$status = "running";
			}

		# get user name and privacy options
		$user = &get_options( $optionsfile, 'USERID' );
		$privat = &get_options( $optionsfile, 'PRIVAT' );
		$jobid = &get_options( $optionsfile, 'JOBID' );

		# show the record
		print "<TR>";
		if(($privat =~ "on") and (not $admin)) {
			print "<TD ALIGN=MIDDLE>private</TD>";
		} else {
			print "<TD ALIGN=MIDDLE><A HREF=\"$CGI?ID=$id\">$id</A></TD>";
		}
		if(($privat =~ "on") and (not $admin)) {
			print "<TD ALIGN=MIDDLE>-</TD>";
		} else {
			print "<TD ALIGN=MIDDLE>";
			if($admin and ($privat =~ "on")) { print "<FONT COLOR=\"FF0000\">"; };
			print "$jobid";
			if($admin and ($privat =~ "on")) { print "</FONT>"; };
			print "</TD>";
		}
		print "<TD ALIGN=MIDDLE>$user</TD>";
		print "<TD ALIGN=MIDDLE>$status</TD>";
		if($admin) {
			print "<TD><INPUT TYPE=CHECKBOX NAME=DEL VALUE=\"$id\"></TD>";
		}
		print "</TR>";
		}
	}
	print "</TABLE>";

	if($lines<99999) {
		print "<H4>only the most recent jobs are shown;<br>";
		print "<a href=\"$CGI?TASK=LIST&ALL=1\">click here to view all jobs</a></H4>";
	} else {
		print "<br><br>";
	}

}
if($admin) {
	print "<INPUT TYPE=SUBMIT VALUE=\"delete marked jobs\"><P>";
	print "</FORM>";
}


if($admin) {
print "<H2>Machine status</H2></CENTER><PRE>";
	system "echo ' ';
          uname -a;
          echo ' ';
          uptime;
          echo ' ';
          echo \ulimit: \`ulimit`;
          echo ' ';
          df -h;
          echo ' '; 
          who;
          echo ' ' ;
          top -b -n 1 | head -20;
          echo ' ' ;
          echo '/tmp/metap3.log:'
          echo '-----------------------------'
          cat /tmp/metap3.log | uniq | tail -50 
          echo ' ' ;
          echo '/tmp/METAP3_SCHEDULER.err:'
          echo '----------------------'
          cat /tmp/METAP3_SCHEDULER.err | uniq | tail -10 
          echo ' ' ;
          echo '/tmp/METAP3_SCHEDULER.log:'
          echo '----------------------'
          cat /tmp/METAP3_SCHEDULER.log | uniq | tail -10 
  ";
	print "</PRE><CENTER><P>";
  
}

print <<EOF409;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF409

} elsif(($TASK eq 'RUN') or (not defined $TASK and defined $ID)) {
#############################################################
################ RUN #######################################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


# check if admin access is requested, then ask for a password
if($ID eq "admin") {
	system "cat $RACINE/admin.html";
	exit 0;
}


# read metabName2htmlMapping to a hash
%name2html=();

if(-f "$HTML/metabId2htmlMapping.csv") {
	open(NAME2HTML, "<$HTML/metabId2htmlMapping.csv");
	while(<NAME2HTML>) {
		$line = $_;
		my($rName,$htmlName) = split(/;/, $line);
		$name2html{$rName}=$htmlName;
	}
	close NAME2HTML;
}


print <<EOF400;
<HTML>
<HEAD>
<TITLE>Run: $ID</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
EOF400
if(not -e "$USERDATA/$ID.metaPjob.finished") { print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"60; URL=$CGI?TASK=RUN&ID=$ID\">"; }
print <<EOF401;
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF401


if(not -d "$BASE") { # no such query
	print "<H4>ERROR: no query with ID='$ID' available</H4>\n";
} elsif(not -e "$USERDATA/$ID.metaPjob.finished") {
	if(-e "$USERDATA/$ID.metaPjob.started") {
		print "<H1>Your job with ID $ID is currently running</H1>\n";
	} elsif(-e "$USERDATA/$ID.metaPjob.spooled") {
		print "<H1>Your job is still waiting (see <A HREF=\"$CGI?TASK=LIST\">status list</A>) </H1>\n";
	} else {
		print "<H1>The status of your job is unclear (see <A HREF=\"$CGI?TASK=LIST\">status list</A>) </H1>\n";
	}
	print "<IMG SRC=\"$IMAGES/gears.gif\"><br>";

	if(-f "$BASE/server_log.txt") {
		print "<H4>Here is the <A HREF=\"$CGI?TASK=SHOWLOG&ID=$ID\">log file</A> and the <A HREF=\"$CGI?TASK=SHOWSEQ&ID=$ID\">input</A> for this run.</H4>\n";
	}
	print "<A HREF=$CGI?ID=$ID>click here or reload this page (automatic reload every 60 s)</A>\n";
	print "<BR> or bookmark this page for a later visit<BR> \n";

###############################################################
################ METABOLITES ##################################
###############################################################
} else { # all is OK, start query

# print the headder
	&print_subheadder ();


# show the results
	print "<H2>METABOLITES</H2>";
	if(-f "$BASE/histograms.pdf") {
		print "<a href=\"$HTMLBASE/histograms.pdf\" TYPE=\"application/pdf\">distribution plots</a>\n";
	}
	if(-f "$BASE/summary.csv") {
		system "$EXEC/metabolite_table.pl $BASE/summary.csv $BASE $ID $CGI";
	} else {
		print "<h3>ERROR: there is an error in the uploaded data file; maybe you did not use a semicolon as separator of data columns or maybe your metabolite or sample names contain semicolons;</h3>\n";
	}
#   if (-f "$BASE/plot1.pdf") {
#     print "<H4><A HREF=\"$HTMLBASE/plot1.pdf\" TYPE=\"application/pdf\">Some graphics (PDF)</A>\n";
#   } else {
#     print "<H4>no plot available</A>\n";
#   }
#   if (-f "$BASE/.R.Rout") {
#     print "<H4><A HREF=\"$HTMLBASE/.R.Rout\" TYPE=\"text/plain\">R listing (text)</A>\n";
#   } else {
#     print "<H4>no R listing available</A>\n";
#   }

	print "</center>\n";

  # PDF files
#  @LIBS = `ls -t $BASE/*.pdf | sed 's/.*\\///' 2> /dev/null `;
#  if ($#LIBS < 0) {
#    print "<H4>no pdf files available</H4>";
#  } else {
#    print "<H4>pdf files generated by this job:</H4>";
#    print "<pre>\n";
#    for ($i=0; $i<=$#LIBS; $i++) {
#      $fic = $LIBS[$i];
#      chomp $fic;
#      $fic =~ s/^M//;
#      print "<a href=\"$HTMLBASE/$fic\" TYPE=\"application/pdf\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }

  # CSV files
#  @LIBS = `ls -t $BASE/*.csv | sed 's/.*\\///' 2> /dev/null `;
#  if ($#LIBS < 0) {
#    print "<H4>no csv files available</H4>";
#  } else {
#    print "<H4>csv files generated by this job:</H4>";
#    print "<pre>\n";
#    for ($i=0; $i<=$#LIBS; $i++) {
#      $fic = $LIBS[$i];
#      chomp $fic;
#      $fic =~ s/^M//;
#      print "<a href=\"$HTMLBASE/$fic\" TYPE=\"application/excel\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }

# LOG files
	@LIBS = `ls -t $BASE/*log\.txt | sed 's/.*\\///' 2> /dev/null `;
	if($#LIBS < 0) {
		print "<H4>no log files available</H4>";
	} else {
		print "<H4>log files generated by this job:</H4>";
		print "<pre>\n";
		for($i=0; $i<=$#LIBS; $i++) {
			$fic = $LIBS[$i];
			chomp $fic;
			$fic =~ s/^M//;
			print "<a href=\"$HTMLBASE/$fic\" TYPE=\"text/plain\">$fic</a>\n";
			system "cat $BASE/$fic | grep '^out:'|sed 's/out://'";
			print "\n";
		}
		print "</pre>\n";
	}


  # other files
#  @LIBS = `ls -t $BASE/* | sed 's/.*\\///' | grep -v .pdf  | grep -v .csv | grep -v .png | grep -v .map | grep -v log 2> /dev/null `;
#  if ($#LIBS < 0) {
#    print "<H4>no other files available</H4>";
#  } else {
#    print "<H4>other files generated by this job:</H4>";
#    print "<pre>\n";
#    for ($i=0; $i<=$#LIBS; $i++) {
#      $fic = $LIBS[$i];
#      chomp $fic;
#      $fic =~ s/^M//;
#      print "<a href=\"$HTMLBASE/$fic\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }
		print "<center>\n";

		print "<BR><BR> \n";

# show listing
		print "<H4><A HREF=\"$CGI?TASK=SHOWLOG&ID=$ID\">If these results do not correspond to what you expected, take a look at the log files</A></H4>\n";

}

print <<EOF499;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF499

} elsif($TASK eq 'QUALITY' and defined $ID) {
#############################################################
################## QUALITY ##################################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


print <<EOF599;
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
</HTML>
EOF599

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>QUALITY CHECK</H2>";

	if(-f "$BASE/data.csv") {
		print "<a href=\"$HTMLBASE/data.csv\" type=\"application/excel\">ms_data</a>";
	}
	print "; ";
	if(-f "$BASE/phenotypes.csv") {
		print "<a href=\"$HTMLBASE/phenotypes.csv\" type=\"application/excel\">phenotypes</a>";
	}
	print "; ";
	if(-f "$BASE/phenotypes_for_QC.csv") {
		print "<a href=\"$HTMLBASE/phenotypes_for_QC.csv\" type=\"application/excel\">phenotypes_for_QC</a>";
	}
	print "; ";
	if(-f "$BASE/data_all.csv") {
		print "<a href=\"$HTMLBASE/data_all.csv\" type=\"application/excel\">ms_data_and_phenotypes</a>";
	}

	print "<br><br>";

	print "<table border=1 width=600>";
	print "<colgroup><col width=80><col width=400><col width=120></colgroup>";
	print "<tr><th></th><th>log information</th><th>plots/files</th></tr>";

	# data.csv
	print "<tr><td>";
	print "<H4>Concentration data:</H4></td>";
	if(-f "$BASE/input" && -f "$BASE/data.csv") {
#$nSamples = `cat $BASE/data.csv | wc -l` - 1;
#print "<td>" . $nSamples . " samples</td>";
#print "<td>$FORMAT $MISSING</td>";
		print "<td>";
		print `grep "EXTRACT:" $BASE/processing_log.txt | sed -n 's/EXTRACT://gp'`;
		print "</td>";
		print "<td><a href=\"$HTMLBASE/data_beforeCheck.csv\">extracted data</a>;<br>";
		print "<a href=\"$HTMLBASE/input\">uploaded file</a></td></tr>";

	} else {
		print "<td>ERROR: data could not be uploaded properly.</td><td></td></tr>";
	}


# phenotypes.csv
	print "<tr><td>";
	print "<H4>Phenotype data:</H4></td>";
	if(-f "$BASE/phenotypes.txt" && -f "$BASE/phenotypes.csv") {
#open(PHENO, "<$BASE/phenotypes.csv");
#my $firstline = <PHENO>;
#close(PHENO);
#my($id,@phenotypes) = split (/;/, $firstline);
#$nPhenotypes=scalar(@phenotypes);
#print "<td>" . $nPhenotypes . " phenotypes</td>";
#print "<td></td>";
		print "<td><p>";
		print `grep "PHENOTYPES_UPLOAD:" $BASE/processing_log.txt | sed -n 's/PHENOTYPES_UPLOAD://gp'`;
		print "</p></td>";
		print "<td><a href=\"$HTMLBASE/phenotypes_beforeCheck.csv\">phenotype data</a>;<br>";
		print "<a href=\"$HTMLBASE/data_all_beforeCheck.csv\">matched data</a>;<br>";
		print "<a href=\"$HTMLBASE/phenotypes.txt\">uploaded file</a></td></tr>";
	} else {
		print "<td>ERROR: phenotype data could not be uploaded properly.</td><td></td></tr>";
	}


# outliers.csv
	print "<tr><td>";
	print "<H4>Outliers:</H4></td>";
#   if ( -f "$BASE/outliers.csv" ) {
#     $nOutliers = `cat $BASE/outliers.csv | wc -l` - 1;
#     print "<td>" . $nOutliers . " outliers</td>";
#     print "<td>$OULIER</td>";
	print "<td>";
	print `grep "OUTLIER:" $BASE/processing_log.txt | sed -n 's/OUTLIER://gp'`;
#TODO deleted na rows
	#print `grep "DEL_METABS:" $BASE/processing_log.txt | sed -n 's/OUTLIER://gp'`;
	print "</td><td>";
	if(-f "$BASE/lowerOutliers.csv") {
		print "<a href=\"$HTMLBASE/lowerOutliers.csv\">lower outliers</a>";
	}
	if(-f "$BASE/upperOutliers.csv") {
		print "<br><a href=\"$HTMLBASE/upperOutliers.csv\">upper outliers</a>";
	} else {
		print " ";
	}
	print " </td></tr>";



# replicates
	print "<tr><td>";
	print "<H4>Replicates:</H4></td>";
	print "<td>";
	print `grep "REPLICATES:" $BASE/processing_log.txt | sed -n 's/REPLICATES://gp'`;
	print "</td><td>";
	if(-f "$BASE/cv.pdf") {
		print "<a href=\"$HTMLBASE/cv.pdf\">cv plot</a><br>";
	} else {
		print " ";
	}
#TODO: lesen wie viele refs  for schleife fuer alle _cv.csv
	#  if ( -f "$BASE/....._cv.csv" ) {
	#    print "<td><a href=\"$HTMLBASE/upperOutliers.csv\">upper outliers</a>";
	#  }
	print " </td></tr>";



# bad metabolites
	print "<tr><td>";
	print "<H4>Noisy metabolites:</H4></td>";
	print "<td>";
	print `grep "DEL_METABS:" $BASE/processing_log.txt | sed -n 's/DEL_METABS://gp'`;
	print "</td><td>";
	#  if( -f "$BASE/NA_metabolites.csv" ) {
	#    print "<a href=\"$HTMLBASE/na_metabolites.csv\">cv above 0.25</a>";
	#  }
	if(-f "$BASE/metabolitesForDropping.csv") {
		print "<a href=\"$HTMLBASE/metabolitesForDropping.csv\">cv above 0.25</a>";
	} else {
		print " ";
	}
	print " </td></tr>";


	# batches
	print "<tr><td>";
	print "<H4>Batches:</H4></td>";
	print "<td>";
	print `grep "BATCHES:" $BASE/processing_log.txt | sed -n 's/BATCHES://gp'`;
	print "</td><td>";
	if(-f "$BASE/batchBoxplot.pdf") {
		print "<a href=\"$HTMLBASE/batchBoxplot.pdf\">batch boxplots</a>";
	} else {
		print " ";
	}
	if(-f "$BASE/pValuesForAllMetabolites__Batch.key.csv") {
		print "<br><a href=\"$HTMLBASE/pValuesForAllMetabolites__Batch.key.csv\">batch p-values</a>";
	}
	if(-f "$BASE/refBatchBoxplot.pdf") {
		print "<br><a href=\"$HTMLBASE/refBatchBoxplot.pdf\">ref/batch boxplots</a>";
	}
	print "</td></tr>";


	print "</table>";


} else { # no such ID
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF598;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF598

} elsif($TASK eq 'SAMPLES' and defined $ID) {
#############################################################
################ SAMPLES ####################################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


print <<EOF399;
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
</HTML>
EOF399

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>SAMPLES</H2>";

	if(-f "$BASE/phenotypes.csv") {
		system "$EXEC/csv2htmltable.pl $BASE/phenotypes.csv $BASE $ID $CGI";
	} else {
		print "<H4>no sample list available</H4\n";
	}
} else { # no such ID
  print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF398;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF398

} elsif($TASK eq 'PCA' and defined $ID) {
#############################################################
##################### PCA ###################################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";

$pheno = $query->url_param("PHENO"); chomp($pheno);
if(not defined $pheno) {
	$pheno = "";
}


print <<EOF888;
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
</HTML>
EOF888

if(-f "$BASE/metaPjob.cmd") {

	# print the headder
	&print_subheadder ();

	print "<H2>PRINCIPAL COMPONENT ANALYSIS</H2>";

	if(-f "$BASE/pca.pdf") {
		print "<a href=\"$HTMLBASE/pca.pdf\">PCA plot</a>";
	} elsif(-f "$BASE/PCA.pdf") {
		#print "<a href=\"$HTMLBASE/PCA.pdf\">PCA plot</a>";
	} else {
		print "<H4>no plot available</H4>\n";
	}

	$pcaplot12="PCA";
	if($pheno ne "") {
		$pcaplot12=$pcaplot12 . $pheno;
	}
	$pcaplot12=$pcaplot12 . "_PC1_PC2";
	$pcaplot12MAP=$pcaplot12 . ".map";
	$pcaplot12PNG=$pcaplot12 . ".png";

	$pcaplot13="PCA";
	if($pheno ne "") {
		$pcaplot13=$pcaplot13 . $pheno;
	}
	$pcaplot13=$pcaplot13 . "_PC1_PC3";
	$pcaplot13MAP=$pcaplot13 . ".map";
	$pcaplot13PNG=$pcaplot13 . ".png";

	$pcaplot23="PCA";
	if($pheno ne "") {
		$pcaplot23=$pcaplot23 . $pheno;
	}
	$pcaplot23=$pcaplot23 . "_PC2_PC3";
	$pcaplot23MAP=$pcaplot23 . ".map";
	$pcaplot23PNG=$pcaplot23 . ".png";


	$pcaplotPropOfVar="PCA";
	if($pheno ne "") {
		$pcaplotPropOfVar=$pcaplotPropOfVar . $pheno;
	}
	$pcaplotPropOfVarPNG=$pcaplotPropOfVar . "_propOfVar.png";


	if(-f "$BASE/$pcaplot12PNG" && -f "$BASE/$pcaplot12MAP" &&
	   -f "$BASE/$pcaplot13PNG" && -f "$BASE/$pcaplot13MAP" &&
	   -f "$BASE/$pcaplot23PNG" && -f "$BASE/$pcaplot23MAP" &&
	   -f "$BASE/$pcaplotPropOfVarPNG") {

		$firstline="";

		if(-f "$BASE/phenotypes_nominal.csv") {
			open(PHENO, "<$BASE/phenotypes_nominal.csv");
			$firstline = <PHENO>;
			close(PHENO);
		} elsif(-f "$BASE/phenotypes.csv") {  # muss noch bleiben fuer alte Berechnungen 
			open(PHENO, "<$BASE/phenotypes.csv");
			$firstline = <PHENO>;
			close(PHENO);
		}

		if($firstline ne "") {
			($id,@phenotypes) = split(/;/, $firstline);

			$nPhenotypes=scalar(@phenotypes);

			if($nPhenotypes > 0) {
				print "<h3>Color plot by phenotype:</h3>";
				print "<table cellspacing=\"10\%\" border=\"1\" bgcolor=\"lightgrey\"><tr>";
				foreach $phenotype (@phenotypes) {
					#if($phenotype ne $pheno) {
					print "<td><a href=\"$CGI?ID=$ID&TASK=PCA&PHENO=$phenotype\">$phenotype</a></td>";
					#}
				}
				#if($pheno ne "") {
				print "<td><a href=\"$CGI?ID=$ID&TASK=PCA\">no color</a></td>";
				#}
				print "</tr></table>";
			}
		}


		print "<table width=\"800\" border=\"0\">";
		print "<tr><td>";
		print "<IMG src=\"$HTMLBASE/$pcaplotPropOfVarPNG\" border=\"0\">";
		print "</td>";

		print "<td>";
		print "<IMG src=\"$HTMLBASE/$pcaplot12PNG\" usemap=\"#$pcaplot12MAP\" border=\"0\" ISMAP>";
		print "<map name=\"$pcaplot12MAP\">";
		open(MAP, "grep \"area shape\" $BASE/$pcaplot12MAP |");
		while(<MAP>) {
			$line = $_;
			$line =~ s/SMPL=/$CGI?ID=$ID&TASK=SHOWSMPL&SMPL=/;
			print $line;
		}
		close MAP;
		print "</map>";
		print "</td></tr>";

		print "<tr><td>";
		print "<IMG src=\"$HTMLBASE/$pcaplot13PNG\" usemap=\"#$pcaplot13MAP\" border=\"0\" ISMAP>";
		print "<map name=\"$pcaplot13MAP\">";
		open(MAP, "grep \"area shape\" $BASE/$pcaplot13MAP |");
		while(<MAP>) {
			$line = $_;
			$line =~ s/SMPL=/$CGI?ID=$ID&TASK=SHOWSMPL&SMPL=/;
			print $line;
		}
		close MAP;
		print "</map>";
		print "</td>";

		print "<td>";
		print "<IMG src=\"$HTMLBASE/$pcaplot23PNG\" usemap=\"#$pcaplot23MAP\" border=\"0\" ISMAP>";
		print "<map name=\"$pcaplot23MAP\">";
		open(MAP, "grep \"area shape\" $BASE/$pcaplot23MAP |");
		while(<MAP>) {
			$line = $_;
			$line =~ s/SMPL=/$CGI?ID=$ID&TASK=SHOWSMPL&SMPL=/;
			print $line;
		}
		close MAP;
		print "</map>";
		print "</td></tr></table>";
	}


#  @LIBS = `ls -t $BASE/pca.rotations*.csv | sed 's/.*\\///' 2> /dev/null `;
#  if ($#LIBS < 0) {
#    print "<H4>no pca rotations available</H4>";
#  } else {
#    print "<H4>pca rotations:</H4>";
#    print "<pre>\n";
#    for ($i=0; $i<=$#LIBS; $i++) {
#      $fic = $LIBS[$i];
#      chomp $fic;
#      $fic =~ s/^M//;
#      print "<a href=\"$HTMLBASE/$fic\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }

	if(-f "$BASE/pca.loadings.csv") {
		print "<a href=\"$HTMLBASE/pca.loadings.csv\">Download PCA loadings</a>";
	} elsif(-f "$BASE/pca.rotations.csv") {
		print "<a href=\"$HTMLBASE/pca.rotations.csv\">Download PCA loadings</a>";
		#print "<a href=\"$HTMLBASE/PCA.pdf\">PCA plot</a>";
	} else {
		print "<H4>no PCA loadings available</H4>\n";
	}

	#print "</center>\n";


} else { # no such ID
	print "<H1>ERROR: no job with ID $ID found</H1>\n";
}

print <<EOF887;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF887

} elsif($TASK eq 'HYPOTHESIS' and defined $ID) {
#############################################################
#################### HYPOTHESIS #############################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


print <<EOF848;
<!-- include TOP -->
<style>
H4,H2,H3,a
{
font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
font-size:20px;
}
#customers
{
font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
width:100%;
border-collapse:collapse;
}
#customers td, #customers th 
{
font-size:1em;
border:1px solid #9C9C9C;
padding:3px 7px 2px 7px;
}
#customers th 
{
font-size:1.1em;
text-align:left;
padding-top:5px;
padding-bottom:4px;
background-color:#9C9C9C;
color:#ffffff;
}
#customers tr.alt td 
{
color:#000000;
background-color:#9C9C9C;
}
</style>
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>
      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
</HTML>
EOF848

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();
	
	$imgPath = "images/";
	#$imgPath = "http://metabolomics.helmholtz-muenchen.de/metap3/images/";

	print "<script type=\"text/javascript\" language=\"javascript\" src=\"GraphMLViewer.js\"></script>\n";

	# Open new window for metabolite networks
	print "<script type=\"text/javascript\" language=\"javascript\">\n";
	print "<!--//\n";
	print "function showMetNet(ttle,netw,twodirections,minPval,maxPval) {\n";
	print "	var fenster = window.open(\"\");\n";
	print "	if (fenster!=null) {\n";
	print "		fenster.document.open();\n";
	print "     fenster.document.title = \"Metabolite network: \"+ttle;\n";
	print "		fenster.document.write(\"<HTML><head>\");\n";
	print "		fenster.document.write(\"<script type='text/javascript' language='javascript' src='GraphMLViewer.js'></script>\");\n";
	print "		fenster.document.write(\"</head><BODY>\");\n";
	print "		fenster.document.write(\"<h4>\"+ttle+\"</h4>\");\n";
	print "		fenster.document.write(\"<FORM ENCTYPE='multipart/form-data' ACTION='graph.cgi' METHOD='POST' NAME='graphForm'>\");\n";
	print "		fenster.document.write(\"<input type='hidden' name='htmlbase' value='$HTMLBASE'>\");\n";
	print "		fenster.document.write(\"<input type='hidden' name='graphml' value='\"+netw+\"'>\");\n";
	print "		if(twodirections == \"false\") {\n";
	print "			fenster.document.write(\"<table width='100%' border = '0'>\");\n";
	print "			fenster.document.write(\" <tr>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."white0.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."redGradient.png' hight='30px' width='250px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."red.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."grey.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td>gradient scale:</td>\");\n";
	print "			fenster.document.write(\" </tr>\");\n";
	print "			fenster.document.write(\" <tr>\");\n";
	print "			fenster.document.write(\"  <td><center>not significant</center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><input type='int' name='limit2' value='\"+maxPval+\"' size='5'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-<input type='int' name='limit1' value='\"+minPval+\"' size='2'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>beyond threshold</center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>not assigned</center></td>\");\n";
	print "			fenster.document.write(\"  <td><input type='radio' name='gradientscale' value='true' checked>log<br><input type='radio' name='gradientscale' value='false'>linear</td>\");\n";
	print "			fenster.document.write(\"  <td><input type='submit' value='submit'></td>\");\n";
	print "			fenster.document.write(\" </tr>\");\n";
	print "			fenster.document.write(\"</table>\");\n";
	print "			fenster.document.write(\"<br>\");\n";
	print "		} else {\n";
	print "			twodirs = twodirections.split('::')\n";
	print "			fenster.document.write(\"<table width='100%' border = '0'>\");\n";
	print "			fenster.document.write(\" <tr>\");\n";
	print "			fenster.document.write(\"  <td>value:</td>\");\n";
	print "			fenster.document.write(\"  <td><center>\"+twodirs[2]+\"</center></td>\");\n";
	print "			fenster.document.write(\"  <td></td>\");\n";
	print "			fenster.document.write(\"  <td><center>\"+twodirs[3]+\"</center></td>\");\n";
	print "			fenster.document.write(\" </tr>\");\n";
	print "			fenster.document.write(\" <tr>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."blue.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."blueGradient.png' hight='30px' width='250px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."white0.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."redGradient.png' hight='30px' width='250px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."red.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><img src='".$imgPath."grey.png' hight='30px' width='30px' border='1'></center></td>\");\n";
	print "			fenster.document.write(\"  <td>gradient scale:</td>\");\n";
	print "			fenster.document.write(\" </tr>\");\n";
	print "			fenster.document.write(\" <tr>\");\n";
	print "			fenster.document.write(\"  <td><center>beyond threshold</center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>1e-<input type='int' name='limit4' value='\"+minPval+\"' size='2'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type='int' name='limit3' value='\"+maxPval+\"' size='5'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>not significant</center></td>\");\n";
	print "			fenster.document.write(\"  <td><center><input type='int' name='limit2' value='\"+maxPval+\"' size='5'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-<input type='int' name='limit1' value='\"+minPval+\"' size='2'></center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>beyond threshold</center></td>\");\n";
	print "			fenster.document.write(\"  <td><center>not assigned</center></td>\");\n";
	print "			fenster.document.write(\"  <td><input type='radio' name='gradientscale' value='true' checked>log<br><input type='radio' name='gradientscale' value='false'>linear</td>\");\n";
	print "			fenster.document.write(\"  <td><input type='submit' value='submit'></td>\");\n";
	print "			fenster.document.write(\" </tr>\");\n";
	print "			fenster.document.write(\"</table>\");\n";
	print "			fenster.document.write(\"<br>\");\n";
	print "		}\n";
	print "		fenster.document.write('</form>');\n";
	print "		fenster.document.write(\"<script language='javascript' type='text/javascript'>\");\n";
	print "		fenster.document.write('if(!RunPlayer(');\n";
	print "		fenster.document.write('  \"width\", \"100%\",');\n";
	print "		fenster.document.write('  \"height\", \"80%\",');\n";
	print "		fenster.document.write('  \"graphUrl\", \"$HTMLBASE/'+netw+'\",');\n";
	print "		fenster.document.write('  \"overview\", \"true\",');\n";
	print "		fenster.document.write('  \"toolbar\", \"true\",');\n";
	print "		fenster.document.write('  \"tooltips\", \"true\",');\n";
	print "		fenster.document.write('  \"movable\", \"true\",');\n";
	print "		fenster.document.write('  \"links\", \"true\",');\n";
	print "		fenster.document.write('  \"linksInNewWindow\", \"true\",');\n";
	print "		fenster.document.write('  \"viewport\", \"full\")) {');\n";
	print "		fenster.document.write('	if(!InstallFlashUpdate(\"width\", \"100%\", \"height\", \"100%\")) {');\n";
	print "		fenster.document.write('		document.write(\"Adobe Flash Player Version 9.0.38 or newer is required. <a href=http://www.adobe.com/go/getflash/>Get Flash Player</a>\");');\n";
	print "		fenster.document.write('	}');\n";
	print "		fenster.document.write('}');\n";
	print "		fenster.document.write(\"</script>\");\n";
	print "		fenster.document.write(\"</BODY></HTML>\");\n";
	print "		fenster.document.close();\n";
	print "	}\n";
	print "}\n";
	print "//-->\n";
	print "</script>\n";

	print "<H2>HYPOTHESIS TESTS</H2>\n";

	#print "<a href=\"#metaboliteNetworks\"><h3>NEW: Metabolite Network</h3></a>\n";
	print "<h3>NEW: Metabolite Networks</h3>\n";

	if(-f "$BASE/hypothesisTests.pdf") {
		print "<a href=\"$HTMLBASE/hypothesisTests.pdf\">Click here for hypothesis tests</a>\n";
	} elsif(-f "$BASE/hypothesisTests_complete_data.pdf") {
		print "<a href=\"$HTMLBASE/hypothesisTests_complete_data.pdf\">Click here for hypothesis tests based on complete data set</a>";
		@HLIBS = `ls -t $BASE/hypothesisTests_separated_for*.pdf | sed 's/.*\\///' 2> /dev/null `;
		if($#HLIBS >= 0) {
			print "<pre>\n";
			for($i=0; $i<=$#HLIBS; $i++) {
				$fic = $HLIBS[$i];
				chomp $fic;
				$fic =~ s/^M//;
				$hText = $fic;
				$hText =~ s/hypothesisTests_separated_for_//;
				$hText =~ s/.pdf//;
				$hText="Click here for groupwise hypothesis tests: " . $hText;
				print "<a href=\"$HTMLBASE/$fic\">$hText</a>\n";
			}
			print "</pre>\n";
		}
	} else {
	print "<H4>no plot available</H4\n";
	}
	print "<br><br>\n";

	@LIBS = `ls -t $BASE/pValuesForAllMetabolites_*.csv | sed 's/.*\\///' | grep -v Batch.key  2> /dev/null `;
	if($#LIBS < 0) {
		print "<H4>no p-values available</H4>\n";
	} else {
		print "<H4>p-values:</H4>\n";
		print "<pre>\n";
		#initialize the table and its top line:
		my $upDown = 0;
		my $table = "<table border=\"1\" id=\"customers\">
				  <tr>
					<th>metabolite</th>
					<th>p-value</th>
					<th>link to table</th></tr>";######
		for($i=0; $i<=$#LIBS; $i++) {
			$fic = $LIBS[$i];
			chomp $fic;
			$fic =~ s/^M//;
			#print "<a href=\"$HTMLBASE/$fic\">$fic</a>\n";
		#}
		########### Find minimal five entries of each column and display them in a table:
		open FILE, "$HTMLBASE/$fic" or die $!;#open current .csv-file
		my @lines = <FILE>;
		my @minValues;#arrays to store the found minimal entries and their position in the .csv-file
		my @mvNames;
		my @mvUpDown;
		#my $Columns = scalar(split(';', @lines[0]));#find out #of columns
		my @columns = split(';', @lines[0]);
		my $Columns = 0;
		foreach my $element(@columns){#exclude empty columns
			unless($element =~ m/\"\"/){$Columns++;}
		}
		my $ud=1;
		@columns = split(';', $lines[$ud]);
		do{#check if last column is up/down:
			@columns = split(';', $lines[$ud]);
			if($columns[$Columns-1] =~ m/up|down/){
				$Columns-=1;#if so, do not consider last column for the five best p-values
				$upDown = -1;#shows that there is a up/down column
			}
		} while($columns[$Columns-1] !~ m/\d+/);#only consider cells where there is no "NA" etc., but a digit.
		close FILE or die $!;
		for(my $cols=1; $cols<$Columns; $cols++){#foreach column
			open FILE, "$HTMLBASE/$fic" or die $!;
			@lines = <FILE>;# file has to be re-read in because 5 lines will be deleted within each loop
			for(my $fiveBest = 0; $fiveBest < 5; $fiveBest++){
				my $minValue = 999999999;
				my $mV_Position = -1;
				for(my $i=1; $i<scalar(@lines);$i++){#iterate over each line of the .csv-file
					my @line = split(';', $lines[$i]);
					if($line[$cols] !~ m/\d+/){if($i<scalar(@lines)-1){$i++; redo;}else{last;}}#check if content is a number, exclude "NA" etc.
					$line[$cols] =~ m/\"(.+)\"/;#extract the current p-value without the ""
					if($fiveBest==0){#check if the current p-value is lower than the lowest predecessor
						if($1 < $minValue){
							$minValue = $1;
							$mV_Position = $i;
						}
					}
					else{
						if($1 < $minValue && $1>=$minValues[$fiveBest-1]){
							$minValue = $1;
							$mV_Position = $i;
						}
					}
				}
				push (@minValues, $minValue);#store the minimal p-value and its position, delete its line inorder not to find it wihtin the next loop.
				my @line = split(';', $lines[$mV_Position]);
				$line[0] =~ m/\"(.+)\"/;
				push (@mvNames, $1);
				if($line[$Columns] =~ m/up/){
					push(@mvUpDown, 1);}
				elsif($line[$Columns] =~ m/down/){
					push(@mvUpDown, -1);}
				else{
					push(@mvUpDown, 0);}
				delete $lines[$mV_Position];
			}
		}#print the table in HTML
		$table.="<td></td><td></td><td><a href=\"$HTMLBASE/$fic\">$fic</a></td>";#link to the respective table	<td></td>
		for(my $i=0;$i<5*($Columns-1);$i++){
			$table.="<tr>";
			if($i%5==0){#after 5 loops a new column starts
				my $col = int $i/5;
				my $mannWhitney = "";
				if($mvUpDown[$i] !=0){
					my @firstLine = split(';', @lines[0]);
					$firstLine[$col+2] =~ m/Mann-Whitney U::DOSE_MG_KG::(\d+)::(\d+)/;
					$mannWhitney .= " $1_$2";
				}
				my @firstLine = split(';', @lines[0]);
				if($firstLine[$col+1] =~ m/complete_data/){
					$fic =~ m/pValuesForAllMetabolites__(.+).csv/;
					$table.="<td></td><th>".$1.$mannWhitney.":</th></tr><tr>";
				}
				elsif($firstLine[$col+1] =~ m/\"(.+)\"/){
					$table.="<td></td><th>".$1.$mannWhitney.":</th></tr><tr>";
				}
			}
			#my $metaboliteName = $mvNames[$i];#parse the metabolites' names to match their html-files:
			#if($mvNames[$i] =~ m/(\w+)\.\.?(\w+)\.\.?(\w+)\.(\w+)/){$metaboliteName = "$1$2$3_$4";}#SM..OH..C14.1
			#elsif($mvNames[$i] =~ m/(\w+)\.\.?(\d+)\.\.?(\w+)/){$metaboliteName = "$1_$2-$3"}#C18.1.OH
			#elsif($mvNames[$i] =~ m/(\w+)\.\.?(\w+)\.(\w+)/){$metaboliteName = "$1$2_$3";}#SM.C16.0
			#elsif($mvNames[$i] =~ m/(\w+)\.(\d+)/){$metaboliteName = "$1_$2";}#C5.1
			#elsif($mvNames[$i] =~ m/(\w+)\.(([A-Z]|[a-z])+)/){$metaboliteName = "$1-$3";}#Tyr.PTC, C3.OH
			#elsif($mvNames[$i] =~ m/\w+/){}#no need to parse
			#my $metaboliteHTML = "metabolites/Details/".$metaboliteName.".html";#make a link to the metabolite HTML-site
			#if(-e $metaboliteHTML){
		 	#	$table.="<td><a href=\"$metaboliteHTML\" target=\"_newtab\">".$mvNames[$i]."</a></td>";
			#}
			#else{
			#	$table.="<td>".$mvNames[$i]."</td>";
			#}
			$table.="<td><a href=\"$CGI?ID=$ID&TASK=SHOWCMPD&CMPD=".$mvNames[$i]."\" target=\"_newtab\">".$mvNames[$i]."</a></td>";
			my $upDownArrow = "";
			if($mvUpDown[$i] == -1){$upDownArrow.=" &#8595";}
			elsif($mvUpDown[$i] == 0){$upDownArrow.=" ";}
			elsif($mvUpDown[$i] == 1){$upDownArrow.=" &#8593";}
			if($minValues[$i] =~ m/(\d+e|E\d+)/){
				my $pValue = sprintf("%.3e", $minValues[$i]);
		   	 	$table.="<td>".$pValue.$upDownArrow."</td></tr>";
			}
			elsif($minValues[$i] =~ m/(0\.0*\d{3})\d*/){
		   	 	$table.="<td>".$1.$upDownArrow."</td></tr>";
			}
			else{$table.="<td>".$minValues[$i].$upDownArrow."</td></tr>";}
		}
		close FILE or die $!;
	}
	$table.="</table><br>";
		print $table;##########
		print "<br>";

		if(-f "$BASE/bonferroni.csv") {
			print "<a href=\"$HTMLBASE/bonferroni.csv\">Bonferroni corrected significance levels</a>\n";
		}
		print "</pre>\n";
	}
	#print "</center>\n";
	print "<br><br>\n";

	# Print Metabolite Networks
	@MLIBS = `ls -t $BASE/ggm_*.graphml | sed 's/.*\\///' | grep -v Batch.key  2> /dev/null `;
	if($#MLIBS < 0) {
		print "<a name=\"metaboliteNetworks\"><H4>no metabolite network available</H4></a>\n";
	} else {
		print "<a name=\"metaboliteNetworks\"><h4>Metabolite Networks:</a><br>\n";
		for($i=0; $i<=$#MLIBS; $i++) {
			$fic = $MLIBS[$i];
			chomp $fic;
			$ttle = $fic;
			$ttle =~ s/^ggm_//i;
			$ttle =~ s/.graphml$//i;
			$fpvf = "pValuesForAllMetabolites_$ttle.csv";
			$ttle =~ s/_/ /g;
			open(CSVFILE,"< $HTMLBASE/$fpvf") or die "Error: $!";
			$nrOfMets = 0;
			$minPval = 1;
			$twodirections = "false";
			while(defined($line = <CSVFILE>)) {
				chomp($line);
				$line = lc($line);
				$line =~ s/"//ig;
				if($line =~ m/Mann-Whitney U/i) {
					$twodirections = $line;
				}
				@pvflds = split(/;/, $line);
				$actPV = $pvflds[1];
				if($actPV =~ m/\d/ig) {
					$nrOfMets = $nrOfMets + 1;
					$actPV = Math::BigFloat->new($pvflds[1]);
					if($actPV < $minPval) {
						$minPval = $actPV;
					}
				}
			}
			close(CSVFILE);
			$pvUpperlimit = Math::BigFloat->new(0.01/$nrOfMets);
			$pvUpperlimit = sprintf("%.6f" , $pvUpperlimit);
			$minPval =~ m/0.(0*)[1-9]/ig;
			$minPval = length($1)+1;
			system($^X, $EXEC."/makeGraph.pl", ("$HTMLBASE/$fpvf","$HTMLBASE/$fic","$HTMLBASE/$fic",Math::BigFloat->new("1e-".$minPval),$pvUpperlimit,$pvUpperlimit,Math::BigFloat->new("1e-".$minPval),"true"));
			if($i == 0) {
				print "<h4>$ttle (Preview)</h4>\n";
				if($twodirections eq "false") {
					print "<table width='100%' border = '0'>";
					print " <tr>";
					print "  <td><center><img src='".$imgPath."white0.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."redGradient.png' hight='30px' width='250px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."red.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."grey.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td>gradient scale:</td>";
					print " </tr>";
					print " <tr>";
					print "  <td><center>not significant</center></td>";
					print "  <td><center>$pvUpperlimit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-$minPval</center></td>";
					print "  <td><center>beyond threshold</center></td>";
					print "  <td><center>not assigned</center></td>";
					print "  <td><center>log</center></td>";
					print " </tr>";
					print "</table>";
					print "<br>";
				} else {
					@twodirs = split(/::/, $twodirections);
					print "<table width='100%' border = '0'>";
					print " <tr>";
					print "  <td>$twodirs[2]:</td>";
					print "  <td><center><img src='".$imgPath."blue.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."blueGradient.png' hight='30px' width='250px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."white0.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."grey.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td>gradient scale:</td>";
					print " </tr>";
					print " <tr>";
					print "  <td></td>";
					print "  <td><center>beyond threshold</center></td>";
					print "  <td><center>1e-$minPval&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pvUpperlimit</center></td>";
					print "  <td><center>not significant</center></td>";
					print "  <td><center>not assigned</center></td>";
					print " </tr>";
					print " <tr>";
					print "  <td>$twodirs[3]:</td>";
					print "  <td><center><img src='".$imgPath."white0.png' hight='30px' width='30px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."redGradient.png' hight='30px' width='250px' border='1'></center></td>";
					print "  <td><center><img src='".$imgPath."red.png' hight='30px' width='30px' border='1'></center></td>";
					print " </tr>";
					print " <tr>";
					print "  <td></td>";
					print "  <td><center>not significant</center></td>";
					print "  <td><center>$pvUpperlimit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-$minPval</center></td>";
					print "  <td><center>beyond threshold</center></td>";
					print "  <td><center>log</center></td>";
					print " </tr>";
					print "</table>";
					print "<br>";
				}
				print "<script language=\"javascript\" type=\"text/javascript\">\n";
				print "<!--//\n";
				print "if(!RunPlayer(\n";
				print "  \"width\", \"100%\",\n";
				print "  \"height\", \"250%\",\n";
				print "  \"graphUrl\", \"$HTMLBASE/".$fic."\",\n";
				print "  \"overview\", \"false\",\n";
				print "  \"toolbar\", \"false\",\n";
				print "  \"tooltips\", \"false\",\n";
				print "  \"movable\", \"false\",\n";
				print "  \"links\", \"false\",\n";
				print "  \"linksInNewWindow\", \"true\",\n";
				print "  \"viewport\", \"full\")) {\n";
				print "	// Flash Player is to old or not installed. Try to install the latest version automatically.\n";
				print "	if(!InstallFlashUpdate(\"width\", \"100%\", \"height\", \"100%\")) {\n";
				print "		// Flash Player is to old to be installed automatically or it is not installed.\n";
				print "		document.write('Adobe Flash Player Version 9.0.38 or newer is required. ' + '<a href=http://www.adobe.com/go/getflash/>Get Flash Player</a>');\n";
				print "	}\n";
				print "}\n";
				print "//-->\n";
				print "</script>\n";
				print "<h4>Show metabolite network in a new window:";
			}
			print "&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"javascript:showMetNet('$ttle','$fic','$twodirections','$minPval','$pvUpperlimit')\">$ttle</a>";
		}
		print "</h4><br>\n";
	}

} else { # no such ID
	print "<H1>ERROR: no job with ID $ID found</H1>\n";
}

print <<EOF847;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF847


} elsif($TASK eq 'KENDALL' and defined $ID) {
#############################################################
##################### KENDALL ###############################
#############################################################

# set some other useful variables
$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


print <<EOF688;
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
</HTML>
EOF688

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>KENDALL CORRELATION TEST</H2>";

	if(-f "$BASE/kendall.pdf") {
		print "<a href=\"$HTMLBASE/kendall.pdf\" type=\"application/pdf\">Click here for the results of Kendall correlation test in PDF format</a>";
	} else {
		print "<H4>no plot available</H4\n";
	}
	print "<br><br>";

	if(-f "$BASE/kendall.png") {
		print "<IMG src=\"$HTMLBASE/kendall.png\"  border=\"0\" >"
	}
	print "<br><br>";

	if(-f "$BASE/kendall.csv") {
		print "<a href=\"$HTMLBASE/kendall.csv\" type=\"application/excel\">Kendall's tau and p-values</a>";
	} else {
		print "<H4>list of Kendall's tau and p-values not available</H4\n";
	}
	print "<br>";
	
	if(-f "$BASE/kendall_ratios.csv") {
		print "<a href=\"$HTMLBASE/kendall_ratios.csv\" type=\"application/excel\">Kendall's tau and p-values for metabolite ratios</a>";
	}
	#print "</center>\n";


} else { # no such ID
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF687;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF687


} elsif($TASK eq 'DELETE') {
#############################################################
################ DELETE #####################################
#############################################################
# delete files

print <<EOF201;
<HTML>
<HEAD>
<TITLE>Delete Job</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF201

$adm = $query->param("ADMIN"); chomp($adm);
if(defined $adm and $adm eq "metaP007") {
	$del = $query->param("DEL"); chomp($del);
	@list = split /#/, $del;
	$ndel = $#list+1;

	print "<H1>Deleting $ndel job(s)</H1>";
	print "<PRE>";
	for($i=0; $i<=$#list; $i++) {
		system "

echo \"removing job $list[$i]\"
rm -r -f $USERDATA/$list[$i]*
";
	}
	print "</PRE>";
	print "<H3><A HREF=\"$CGI?TASK=LIST&ADMIN=$adm\">BACK to job status</A></H3>";
} else {
	print "<H1>access refused</H1>";
}



print <<EOF367;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF367

} elsif($TASK eq 'SHOWCMPD') {
#############################################################
################ SHOWCMPD ###################################
#############################################################
# display metabolite data

$metabolite = $query->param("CMPD"); chomp($metabolite);
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";
$pheno = $query->param("PHENO"); chomp($pheno);
if(not defined $pheno) {
	$pheno = "";
}

print <<EOF403;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF403

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>Metabolite: $metabolite</H2>";

	$barplot=$metabolite . "_barplot";
	$barplotMAP=$barplot . ".map";

	if($pheno ne "") {
		$barplot=$barplot . "_" . $pheno;
	}
	$barplotPNG=$barplot . ".png";

	if(-f "$BASE/barplots/$barplotPNG" && -f "$BASE/barplots/$barplotMAP") {
		$firstline="";

		if(-f "$BASE/phenotypes_nominal.csv") {
			open(PHENO, "<$BASE/phenotypes_nominal.csv");
			$firstline = <PHENO>;
			close(PHENO);
		} elsif(-f "$BASE/phenotypes.csv") {  # muss noch bleiben fuer alte Berechnungen 
			open(PHENO, "<$BASE/phenotypes.csv");
			$firstline = <PHENO>;
			close(PHENO);
		}
		
		if($firstline ne "") {
			($id,@phenotypes) = split(/;/, $firstline);

			$nPhenotypes=scalar(@phenotypes);

			if($nPhenotypes > 0) {
				print "<h3>Color barplot by phenotype:</h3>";
				print "<table cellspacing=\"10\%\" border=\"1\" bgcolor=\"lightgrey\"><tr>";
				foreach $phenotype (@phenotypes) {
					#if($phenotype ne $pheno) {
					print "<td><a href=\"$CGI?ID=$ID&TASK=SHOWCMPD&CMPD=$metabolite&PHENO=$phenotype\">$phenotype</a></td>";
					#}
				}
				#if($pheno ne "") {
				print "<td><a href=\"$CGI?ID=$ID&TASK=SHOWCMPD&CMPD=$metabolite\">no color</a></td>";
				#}
				print "</tr></table>";
			}
		}

		print "<IMG src=\"$HTMLBASE/barplots/$barplotPNG\" usemap=\"#$barplotMAP\" border=\"0\" ISMAP>";
		print "<map name=\"$barplotMAP\">";
		open(MAP, "grep \"area shape\" $BASE/barplots/$barplotMAP |");
		while(<MAP>) {
			$line = $_;
			$line =~ s/SMPL=/$CGI?ID=$ID&TASK=SHOWSMPL&SMPL=/;
			print $line;
		}
		close MAP;
		print "<\map>";

		#print "<IMG src=\"$HTMLBASE/barplots/$barplot\">";
	} else {
		print "<H4>no barplot available<\H4>\n";
	}


	# read metabName2htmlMapping to a hash TODO: muss hier weg
	%name2html=();

	if(-f "$HTML/metabId2htmlMapping.csv") {
		open(NAME2HTML, "<$HTML/metabId2htmlMapping.csv");
		while(<NAME2HTML>) {
			$line = $_;
			my($rName,$htmlName) = split(/;/, $line);
			$name2html{$rName}=$htmlName;
		}
		close NAME2HTML;
	}


	if(exists $name2html{$metabolite}) {
		$metabFile = "metabolites/Details_short/" . $name2html{$metabolite};
		#   if ( -f $metabFile ) { # funktioniert leider nicht mehr, warum auch immer
		print "<H3>Analyte Report</H3>";
		system "cat $metabFile";
		#   }
	}

} else {
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF499;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF499



} elsif($TASK eq 'SHOWSMPL') {
#############################################################
################ SHOWSMPL ###################################
#############################################################
# display sample data

$sample = $query->param("SMPL"); chomp($sample);
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";

print <<EOF404;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF404

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>Sample: $sample</H2>";

	if(-f "$BASE/phenotypes_beforeCheck.csv") {

		$firstline="";

		print "<table border=\"1\"><tr><td>";

		open(ALLPHENO1, "<$BASE/phenotypes_beforeCheck.csv");
		$firstline = <ALLPHENO1>;
		$firstline =~ s/;/\<\/td\>\<td\>/g;
		close(ALLPHENO1);
		print $firstline;
		print "</td></tr>";

		print "<tr><td>";
		open(ALLPHENO2, "grep \"^$sample\" $BASE/phenotypes_beforeCheck.csv|");  #sample ids muessen unique sein
		#if ..eq wenn punkte drin sind
		$line = <ALLPHENO2>;
		$line =~ s/;/\<\/td\>\<td\>/g;
		close ALLPHENO2;
		print $line;
		print "</td></tr></table><br>";
	}

	print "<table border=\"0\"><tr valign=\"top\"><td>";

	$sbarplot=$sample . "_sbarplot";
	$sbarplotPNG=$sbarplot . ".png";
	$sbarplotMAP=$sbarplot . ".map";

	if(-f "$BASE/barplots/$sbarplotPNG" && -f "$BASE/barplots/$sbarplotMAP") {
		print "<IMG src=\"$HTMLBASE/barplots/$sbarplotPNG\" usemap=\"#$sbarplotMAP\" border=\"0\" ISMAP>";
		print "<map name=\"$sbarplotMAP\">";
		open(SMAP, "grep \"area shape\" $BASE/barplots/$sbarplotMAP |");
		while(<SMAP>) {
			$line = $_;
			$line =~ s/CMPD=/$CGI?ID=$ID&TASK=SHOWCMPD&CMPD=/;
			print $line;
		}
		close SMAP;
		print "<\map></td>";
		#print "<IMG src=\"$HTMLBASE/barplots/$barplot\">";
	} else {
		print "<H4>no plot available<\H4>\n</td>";
	}


	# KEGG start
	$keggFile= "$BASE/barplots/" . $sample . "_4keggColoring.csv";
	if(-f $keggFile) {

		print "<td><br><br><br><br>";
		print <<EOF234;
		<form enctype="multipart/form-data" method="post" action="http://www.genome.jp/kegg-bin/color_pathway_object" target="_new">
		<input type="hidden" name="org_name" value="map">

		<textarea name="unclassified" cols="15" rows="2">
EOF234

		#print "C00031 green\nC00062 red\nC00078 blue\nC00079 green\n";

		system "cat $keggFile";

		# list compounds to be submitted
		#system "tail +2 $BASE/masses.annotated | awk '{print \$7}' | sort -u";

		print <<EOF235;
		</textarea>
		<input type="hidden" name="reference" value="white" />
		<input type="hidden" name="warning" value="yes" />
		<input type="hidden" name="default" value="pink" />
		<br>
		<input type="submit" value="Color Compounds in KEGG" />
		</form>
EOF235

		#<input type="file" name="color_list" size="34" maxlength="0" />
		print "</td>";
		# KEGG end
	}

	print "</tr></table>";

	if(-f "$BASE/phenotypes.list") {
#
	}

} else {
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF490;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF490



} elsif($TASK eq 'SHOWSEQ' and defined $ID) {
#############################################################
################ SHOWSEQ ####################################
#############################################################
# display the the input data

$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";

print <<EOF7403;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF7403

if(-f "$BASE/metaPjob.cmd") {

# print the headder
	&print_subheadder ();

	print "<H2>INPUT DATA</H2>";

	if(-f "$BASE/options") {
		print "<H4>Job options:</H4>";
		print "</center><pre>\n";
		system "cat $BASE/options | grep -v EMAIL";
		print "</pre><center><br><br>\n";
	}

	if(-f "$BASE/phenotypes.txt") {
		print "<H4>Submitted phenotype data:</H4>";
		print "</center><pre>\n";
		system "cat $BASE/phenotypes.txt";
		print "</pre><center><br><br>\n";
	}

	if(-f "$BASE/aux.txt") {
		print "<H4>Submitted auxillary data:</H4>";
		print "</center><pre>\n";
		system "cat $BASE/aux.txt";
		print "</pre><center><br><br>\n";
	}

	if(-f "$BASE/input") {
		print "<H4>Input data for this run:</H4>";
		print "</center><pre>\n";
		system "cat $BASE/input";
		print "</pre><center><br><br>\n";
	}

} else {
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF7497;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF7497

} elsif($TASK eq 'SHOWLOG' and defined $ID) {
#############################################################
################ SHOWLOG ####################################
#############################################################
# display the log file

$BASE = "$USERDATA/$ID";
$HTMLBASE = "$HTMLUSERDATA/$ID";

print <<EOF404;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
EOF404

if(-f "$BASE/server_log.txt") {

# print the headder
	&print_subheadder ();

	print "<H2>LOGFILES</H2>";

	print "<H4><a href=\"doc.html#faq\">In case of trouble, check out our FAQs!</a></H4>\n";

	print "</center><pre>\n";
	system "cat $BASE/server_log.txt | sed 's/\@[^ ]*//' | sed 's/^\\(....................................................................................................\\).*/\\1.../'";
	if(-f "$BASE/server_log.txt") {
		print "<br><br>-----<br><br>";
		system "cat $BASE/processing_log.txt";
	}
	print "</pre><center><br><br>\n";

} else {
	print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF417;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF417

} else {
#############################################################
################ UNIDENTIFIED INPUT #########################
############################################################# TODO: Output
	print <<EOF13;
<HTML>
<HEAD>
<TITLE>metaP-server</TITLE>
<!-- META TAGS ... -->
<meta name="Karsten Suhre" content="metaP-server">
<meta name="keywords" content="mass spectrometry, web server, MassTRIX, AbsoluteIDQ, Biocrates">
<meta http-equiv="expires" content="0">
<meta NAME="robots" CONTENT="index,follow">
</HEAD>
<!-- include TOP -->
<title>metaP server</title>
<BODY background="images/white.png" link="#014294" vlink="#014294" alink="#014294" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<TABLE width="860" height="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <TR valign="top">
    <TD width="20" background="images/white.png">&nbsp;</TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="820">
      <table width="820" border="0" cellpadding="0" cellspacing="0">
        <tr><td nowrap align="center"><img src="images/white.png" width=849 height=20 border="0"></td></tr>
        <tr><td nowrap align="center"><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/yellow.png" width=560 height=75 border="0"></a><a href="http://metabolomics.helmholtz-muenchen.de"><img src="images/metabolomips_v1_wide_75px_schraeg_yellow.png" border="0" height=75></a></td></tr>
        <tr><td nowrap align="left"><a href="http://www.helmholtz-muenchen.de"><img SRC="images/200dpi_engl_40px.jpg" border=0 align="left"></a>
                                    <a href="http://mips.helmholtz-muenchen.de"><img SRC="images/mipsLogo_40px.png" border=0 align="right"></a>
                                    <a href="http://www.helmholtz-muenchen.de/gac/metabolomics/scientific-intitiative-metap/index.html"><img src="images/MetaP_LogoShadow_40px.png" border="0" align="center"></a></td></tr>
        <tr><td height="0" align="right" valign="top" bgcolor="#9C9C9C">
          <a href="index.html"><font color="#FFFFFF">Home</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="start.html"><font color="#FFFFFF">Start a new run</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="run.cgi?TASK=LIST"><font color="#FFFFFF">Job status</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="examples.html"><font color="#FFFFFF">Examples</font></a>
          <font color="#FFFFFF">&nbsp|&nbsp</font>
          <a href="doc.html"><font color="#FFFFFF">Documentation</font></a>
          &nbsp
        </td></tr>
        <tr><td align=center>
          <img src="images/MetaP_LogoShadow_width245.png" border="0" width=245>
          <b><font color="9C9C9C" size=7>server</font></b>
        </td></tr>
      </table>

      <TABLE width="800" align="center" border="0" cellpadding="0" cellspacing="0">



        <TR>
          <TD>
<CENTER>
<H1>Page not found!</H1>
</center>
<H4>The input parameters from the CGI script were ... </H4><br>
...
EOF13

print <<EOF16;
<center>
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
  <BR><BR>
   If you find results from this site helpful for your research, please cite:
   <BR>
   <P>
    G. Kastenm&uuml;ller, W. R&ouml;misch-Margl, B. W&auml;gele, E. Altmaier, and K. Suhre, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2946609/?tool=pubmed" target="_new"><i>meta</i>P-<i>Server</i>: A Web-Based Metabolomics Data Analysis Tool</a>,
    <i>J Biomed Biotechnol.</i>, pii: 839862. 2011, Epub 2010 Sep 5.</P>
   <BR>
   This work was supported in part by:
   <BR>
    <a href="http://www.dzd-ev.de/"><img SRC="images/logo_DZD.png" height=40 align=CENTER></a>
    <a href="http://www.medizin.uni-greifswald.de/gani_med/index.php"><img SRC="images/logo_ganimed.gif" height=40 align=CENTER></a>
    <a href="http://www.sysmbo.de/"><img SRC="images/logo_SysMBo.gif" height=40 align=CENTER></a>
    <a href="http://www.pathogenomics-era.net/index.php"><img SRC="images/logo_ERA-Net.gif" height=40 align=CENTER></a>
   <BR>
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 12th March 2013
</H4>
Visit our NAR-web server:
  <BR>
<a href="http://www.masstrix.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/masstrix_banner.gif" height=25 align=CENTER></a>
<a href="http://www.elnemo.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/elnemo_banner.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/FusionDB/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/FusionDB_logo.gif" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/Caspr2/index.cgi"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/Caspr_logo2.JPG" height=25 align=CENTER></a>
<a href="http://www.igs.cnrs-mrs.fr/phydbac/"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_phydbac.jpg" height=25 align=CENTER></a>
<a href="http://www.tcoffee.org"><img SRC="http://metabolomics.helmholtz-muenchen.de/suhre/logo_tcoffee2.jpg" height=25 align=CENTER></a>
  <BR>
</CENTER>
<!-- end of main centering -->
          </TD>
        </TR>
      </TABLE>
    </TD>
    <TD></TD>
    <TD width="1" bgcolor="#000000"></TD>
    <TD width="20" background="images/white.png">&nbsp;</TD>
  </TR>
</TABLE>
</body>
</html>
</HTML>
EOF16
}
