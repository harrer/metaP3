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

$maxlen = 1000000; # maximum allowed number of allowed input lines

sub get_options ( $ $ ) {
  ( my $optionsfile, my $keyword ) = @_;
  my @value = `grep '^$keyword' $optionsfile 2> /dev/null`;
  my $value = "unknown";
  $value = $value[0] if (defined $value);
  chomp $value; $value =~ s///; $value =~ s/^$keyword[ \t]*=[\t ]*//;
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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



sub parse_form_data {
  local (*FORM_DATA) = @_;
  local ($request_method, 
         $query_string,
         @key_value_pairs,
         $key_value,
         $key,
         $value);
  $request_method = $ENV{'REQUEST_METHOD'};
  if ($request_method eq "GET") {
    $query_string = $ENV{'QUERY_STRING'};
  } elsif ($request_method eq "POST") {
    read (STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
  } else {
    print "Error: method $request_method not supported\n";
    exit (1);
  };

  if ( $query_string =~ /^--/ ) { # this is a multipart form
    # @d=split (/-{2,}\d+.*\n/, $query_string);
    # BUG fixed for Safari
    # @d=split (/-{2,}[a-zA-Z\d]+.*\n/, $query_string);
    # a more stable (?) version of the same theme 
    @d=split (/[^\n]-{2,}[a-zA-Z\d]+.*\n/, $query_string);
    foreach $val (@d) {
      $val =~ s/(Content.*)\n.*\n//g;
      $type=$1;
      $val =~ s/$//g;
      $val =~ s/\n$//;
      $name = $type;
      $name =~ s/.*; name=//;
      $name =~ s/;.*//;
      $name =~ s/^"//;
      $name =~ s/".*//;
      $FORM_DATA{$name} = $val;
    }
  } else {
    @key_value_pairs = split (/&/, $query_string);
    foreach $key_value(@key_value_pairs) {
      ($key, $value) = split (/=/, $key_value);
      $value =~ tr/+/ /;
      $value =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack ("C", hex ($1))/eg;
  
      if (defined($FORM_DATA{$key})) {
        $FORM_DATA{$key} = join("#", $FORM_DATA{$key}, $value);
      } else {
        $FORM_DATA{$key} = $value;
      };
    };
  };
};

# parse query string
print "Content-type: text/html", "\n\n";
&parse_form_data (*simple_form);


# CGI internal PATHs
$RACINE="/var/www/metap2";
$USERDATA="$RACINE/users";
$EXEC="/var/www/metap2_ed/exec";
$DATA="/var/www/metap2_ed/data";
$LOG="/tmp/metap2.log";

# HTML PATHs
$HTML=".";
$HTMLUSERDATA="users";
$IMAGES="images";

# path to this CGI
$CGI = $0;
$CGI =~ s/.*\///;

# log the query
system "echo `date +'%F_%R'`'\t$ENV{'REMOTE_ADDR'}'\t$ENV{'REMOTE_HOST'}'\t$ENV{'QUERY_STRING'}'>>$LOG"; 

#############################################################
################ NEW ########################################
#############################################################
if ($simple_form{'TASK'} eq 'NEW') {

# generate a unique ID for this run
$ID=`date +%y%m%d%H%M%S$$`;
chomp $ID;
$BASE="$USERDATA/$ID";

# create a directory for this job
system "mkdir $BASE; chmod 777 $BASE";
system "mkdir $BASE/barplots; chmod 777 $BASE/barplots";

$allok = 1;

# get the form parameters and set defaults
if (defined $simple_form{'FORMAT'}) { $FORMAT = $simple_form{'FORMAT'} } else { $FORMAT = 'undef' };
if (defined $simple_form{'MISSING'})  { $MISSING  = $simple_form{'MISSING'}  } else { $MISSING  = 'undef' };
if (defined $simple_form{'OUTLIER'})  { $OUTLIER  = $simple_form{'OUTLIER'}  } else { $OUTLIER  = 'undef' };
if (defined $simple_form{'DEL_METABS'})  { $DEL_METABS  = $simple_form{'DEL_METABS'}  } else { $DEL_METABS  = 'undef' };
if (defined $simple_form{'REFERENCE'})  { $REFERENCE  = $simple_form{'REFERENCE'}  } else { $REFERENCE  = 'undef' };
if (defined $simple_form{'RATIOS'})  { $RATIOS  = $simple_form{'RATIOS'}  } else { $RATIOS  = 'undef' };


# e-mail user id and the-like
if (defined $simple_form{'PRIVAT'}) { $PRIVAT = $simple_form{'PRIVAT'} } else { $PRIVAT = 0 };
if (defined $simple_form{'JOBID'}) { $JOBID = $simple_form{'JOBID'} } else { $JOBID = "" };
$JOBID =~ s/[`\\'"]//g;
if (defined $simple_form{'EMAIL'}) {
  $EMAIL = $simple_form{'EMAIL'};
  $EMAIL =~ s/[`\\'"; ]//g;
} else { $EMAIL = "unknown" }
if ( length ($EMAIL) <= 0 ) { $EMAIL = "unknown" };
$USERID = $EMAIL;
$USERID =~ s/@.*//;

$JOBID = "no job-id" if (length($JOBID) == 0);

# get the first file (AbsoluteIDQ data)
if ((defined $simple_form{'UPLOAD'}) and (length($simple_form{'UPLOAD'})>2)) {
  $ATOM  = $simple_form{'UPLOAD'}; # upload from file
} else {
  $ATOM  = $simple_form{'ATOM'}; # from paste
}
if (not defined $ATOM) {$ATOM = ""};;
chomp $ATOM;

# get the second file (e.g. Phenotype data)
if ((defined $simple_form{'UPLOAD2'}) and (length($simple_form{'UPLOAD2'})>2)) {
  $ATOM2  = $simple_form{'UPLOAD2'}; # upload from file
} else {
  $ATOM2  = $simple_form{'ATOM2'}; # from paste
}
if (not defined $ATOM2) {$ATOM2 = ""};;
chomp $ATOM2;

# get the third file (something else - we keep this option for later usage)
if ((defined $simple_form{'UPLOAD3'}) and (length($simple_form{'UPLOAD3'})>2)) {
  $ATOM3  = $simple_form{'UPLOAD3'}; # upload from file
} else {
  $ATOM3  = $simple_form{'ATOM3'}; # from paste
}
if (not defined $ATOM3) {$ATOM3 = ""};;
chomp $ATOM3;

# put the AbsoluteIDQ data into a file called input
open (ATOM, ">$BASE/input.tmp") or &error("Error 999 in CGI-script, sorry.");
print ATOM $ATOM;
close ATOM;
system("cat $BASE/input.tmp | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/input");

# put the phenotype data into a file called phenotypes.txt
open (ATOM2, ">$BASE/phenotypes.txt.tmp") or &error("Error 997 in CGI-script, sorry.");
print ATOM2 $ATOM2;
close ATOM2;
system("cat $BASE/phenotypes.txt.tmp | sed 's/^M//g' | sed 's/,//g' | sed 's/\"//g' > $BASE/phenotypes.txt");

# put the auxillary data into a file called aux.txt
open (ATOM3, ">$BASE/aux.txt") or &error("Error 996 in CGI-script, sorry.");
print ATOM3 $ATOM3;
close ATOM3;


# test the length of the input sequence
$totline = `cat $BASE/input | wc -l`;
if ( $totline > $maxlen) {
  $allok = 0;
  $errmsg = "<H4>ERROR: input file exceeds limit of $maxlen records</H4>
  This limit is imposed to assure that unmonitored jobs will finish within a reasonable time-frame.
  Upon request, we will be glad to open the server to larger jobs.
  Your job would require a limit of $totline records.
  \n";
}

# test if the scan mode is properly defined
if ( $FORMAT eq "undef") {
  $allok = 0;
  $errmsg = "<H4>ERROR: Data format has not been defined!</H4>
  Please specify your data format.<P>
  \n";
}

# check if there is enough data (empty submission?)
if ( ($totline) <= 0) {
  $allok = 0;
  $errmsg = "<H4>ERROR: no valid data uploaded (empty file??)</H4>\n";
}

# print HTML header
print "<HTML>\n";
if ($allok) {print "<HEAD><META HTTP-EQUIV=\"Refresh\" CONTENT=\"60; URL=$CGI?TASK=RUN&ID=$ID\"> </HEAD>\n";}
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

if ($allok) { # if all OK generate the job

  print <<EOF2;
  <H1>Your job has been submitted successfully ... </H1>
  <IMG SRC="$IMAGES/gears.gif">
  <BR>
EOF2

  print "<H4>Your requestid is <A HREF=$CGI?ID=$ID>$ID</A></H4>\n";
  print "<H1><A HREF=$CGI?TASK=RUN&ID=$ID>CLICK HERE</A></H1>\n";
  if ( $EMAIL =~ '@') {
    print "<BR>you will be notified by e-mail about the status of your job<BR>\n";
  }
  open (CMD,">$BASE/metaPjob.cmd") or &error("Error 998 in CGI-script, sorry.");
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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
  open (OPT,">$BASE/options") or &error("Error 995 in CGI-script, sorry.");
  print OPT <<EOFOPT1;
ID        \t=\t $ID
JOBID     \t=\t $JOBID
EMAIL     \t=\t $EMAIL
USERID    \t=\t $USERID
PRIVAT    \t=\t $PRIVAT

FORMAT    \t=\t $FORMAT
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ($simple_form{'TASK'} eq 'LIST') {
#############################################################
################ LIST ######################################
#############################################################
# display a list of all existing jobs

# check if you are administrator
$admin = 0;
if ((defined $simple_form{'ADMIN'}) and ($simple_form{'ADMIN'} eq "metaP007")) { $admin=1 };
if ((defined $simple_form{'ALL'})or($admin)) { $lines=999999 } else {$lines=100};

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
if ($admin) {
  print "<H1><FONT COLOR=\"FF0000\">administrator access</FONT> <A HREF=\"test.html\">X</A></H1>"
};


# KS BUG FIX: the following line overflows when too many files are in the directory
# @LIBS = `ls -dt $USERDATA/* | sed 's/.*\\///' | grep -v patch | sort -r | head -$lines 2> /dev/null `;
@LIBS = `ls -t $USERDATA/ | sed 's/.*\\///' | grep -v patch | sort -ur | head -$lines 2> /dev/null `;

if ($#LIBS < 0) {
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

  if ( $admin) {
    print "<FORM ACTION=\"$CGI\" METHOD=POST>\n";
    print "<INPUT TYPE=HIDDEN NAME=TASK VALUE=DELETE>\n";
    print "<INPUT TYPE=HIDDEN NAME=ADMIN VALUE=\"$simple_form{'ADMIN'}\">\n";
  }

  print "<TABLE BORDER=1>";
  print "<TR><TH ALIGN=MIDDLE>ID (recent jobs first)</TH><TH ALIGN=MIDDLE>job description</TH><TH ALIGN=MIDDLE>owner</TH><TH ALIGN=MIDDLE>status</TH></TR>";
  for ($i=0; $i<=$#LIBS; $i++) {
    $id = $LIBS[$i];
    chomp $id;
    $id =~ s///;;

    if ( -d "$USERDATA/$id" ) {
      # determine the status of this runs
      $startfile = "$USERDATA/$id.metaPjob.started";
      $spoolfile = "$USERDATA/$id.metaPjob.spooled";
      $finishfile = "$USERDATA/$id.metaPjob.finished";
      $resultfile = "$USERDATA/$id/success";
      $optionsfile = "$USERDATA/$id/options";
      $status = "unknown";
      if ( -e $finishfile ) { 
        if (! -e $resultfile ) { 
          $status = "failed";
        } else {
          $status = "finished";
        }
      } elsif ( -e $spoolfile ) {
          $status = "spooled";
      } elsif ( -e $startfile ) {
          $status = "running";
      }

      # get user name and privacy options
      $user = &get_options( $optionsfile, 'USERID' );
      $privat = &get_options( $optionsfile, 'PRIVAT' );
      $jobid = &get_options( $optionsfile, 'JOBID' );

      # show the record
      print "<TR>";
      if ( ( $privat =~ "on" ) and (not $admin)) {
        print "<TD ALIGN=MIDDLE>private</TD>";
      } else {
        print "<TD ALIGN=MIDDLE><A HREF=\"$CGI?ID=$id\">$id</A></TD>";
      }
      if ( ( $privat =~ "on" ) and (not $admin)) {
        print "<TD ALIGN=MIDDLE>-</TD>";
      } else {
      print "<TD ALIGN=MIDDLE>";
      if ($admin and ( $privat =~ "on" )) {print "<FONT COLOR=\"FF0000\">"};
      print "$jobid";
      if ($admin and ( $privat =~ "on" )) {print "</FONT>"};
      print "</TD>";
      }
      print "<TD ALIGN=MIDDLE>$user</TD>";
      print "<TD ALIGN=MIDDLE>$status</TD>";
      if ( $admin) {
        print "<TD><INPUT TYPE=CHECKBOX NAME=DEL VALUE=\"$id\"></TD>";
      }
      print "</TR>";
    }
  }
  print "</TABLE>";

  if ($lines<99999) {
    print "<H4>only the most recent jobs are shown;<br>";
    print "<a href=\"$CGI?TASK=LIST&ALL=1\">click here to view all jobs</a></H4>";
  } else {
    print "<br><br>";
  }

}
if ( $admin) {
  print "<INPUT TYPE=SUBMIT VALUE=\"delete marked jobs\"><P>";
  print "</FORM>";
}


if ( $admin) {
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
          echo '/tmp/metap2.log:'
          echo '-----------------------------'
          cat /tmp/metap2.log | uniq | tail -50 
          echo ' ' ;
          echo '/tmp/METAP2_SCHEDULER.err:'
          echo '----------------------'
          cat /tmp/METAP2_SCHEDULER.err | uniq | tail -10 
          echo ' ' ;
          echo '/tmp/METAP2_SCHEDULER.log:'
          echo '----------------------'
          cat /tmp/METAP2_SCHEDULER.log | uniq | tail -10 
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ( ($simple_form{'TASK'} eq 'RUN') 
          or ( (not exists $simple_form{'TASK'} ) and (exists $simple_form{'ID'}))) {
#############################################################
################ RUN #######################################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


# check if admin access is requested, then ask for a password
if ( $ID eq "admin" ) {
  system "cat $RACINE/admin.html";
  exit 0;
}


# read metabName2htmlMapping to a hash
%name2html=();

if ( -f "$HTML/metabId2htmlMapping.csv") {
  open (NAME2HTML, "<$HTML/metabId2htmlMapping.csv");
  while (<NAME2HTML>) {
    $line = $_;
    my($rName,$htmlName) = split (/;/, $line);
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
if (not -e "$USERDATA/$ID.metaPjob.finished") { print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"60; URL=$CGI?TASK=RUN&ID=$ID\">" }
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


if (not -d "$BASE") { # no such query
  print "<H4>ERROR: no query with ID='$ID' available</H4>\n";
} elsif (not -e "$USERDATA/$ID.metaPjob.finished") {
  if (-e "$USERDATA/$ID.metaPjob.started") {
    print "<H1>Your job with ID $ID is currently running</H1>\n";
  } elsif (-e "$USERDATA/$ID.metaPjob.spooled") {
    print "<H1>Your job is still waiting (see <A HREF=\"$CGI?TASK=LIST\">status list</A>) </H1>\n";
  } else {
    print "<H1>The status of your job is unclear (see <A HREF=\"$CGI?TASK=LIST\">status list</A>) </H1>\n";
  }
  print "<IMG SRC=\"$IMAGES/gears.gif\"><br>";

  if (-f "$BASE/server_log.txt") {
    print "<H4>Here is the <A HREF=\"$CGI?TASK=SHOWLOG&ID=$ID\">log file</A> and 
           the <A HREF=\"$CGI?TASK=SHOWSEQ&ID=$ID\">input</A> for this run.</H4>\n";
  }
  print "<A HREF=$CGI?ID=$ID>click here or reload this page (automatic reload every 60 s)</A>\n";
  print "<BR> or bookmark this page for a later visit<BR> \n";

#############################################################
################ METABOLITES ##################################
#############################################################
} else { # all is OK, start query

  # print the headder
  &print_subheadder ();


  # show the results
  print "<H2>METABOLITES</H2>";
  if (-f "$BASE/histograms.pdf") {
    print "<a href=\"$HTMLBASE/histograms.pdf\" TYPE=\"application/pdf\">distribution plots</a>\n";
  }
  if (-f "$BASE/summary.csv") {
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
#      $fic =~ s///;
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
#      $fic =~ s///;
#      print "<a href=\"$HTMLBASE/$fic\" TYPE=\"application/excel\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }

  # LOG files
  @LIBS = `ls -t $BASE/*log\.txt | sed 's/.*\\///' 2> /dev/null `;
  if ($#LIBS < 0) {
    print "<H4>no log files available</H4>";
  } else {
    print "<H4>log files generated by this job:</H4>";
    print "<pre>\n";
    for ($i=0; $i<=$#LIBS; $i++) {
      $fic = $LIBS[$i];
      chomp $fic;
      $fic =~ s///;
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
#      $fic =~ s///;
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ( ($simple_form{'TASK'} eq 'QUALITY') and (exists $simple_form{'ID'}) ) {
#############################################################
################## QUALITY ##################################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>QUALITY CHECK</H2>";

  if (-f "$BASE/data.csv") {
    print "<a href=\"$HTMLBASE/data.csv\" type=\"application/excel\">ms_data</a>";
  }
  print "; ";
  if (-f "$BASE/phenotypes.csv") {
    print "<a href=\"$HTMLBASE/phenotypes.csv\" type=\"application/excel\">phenotypes</a>";
  }
  print "; ";
  if (-f "$BASE/phenotypes_for_QC.csv") {
    print "<a href=\"$HTMLBASE/phenotypes_for_QC.csv\" type=\"application/excel\">phenotypes_for_QC</a>";
  }
  print "; ";
  if (-f "$BASE/data_all.csv") {
    print "<a href=\"$HTMLBASE/data_all.csv\" type=\"application/excel\">ms_data_and_phenotypes</a>";
  }

  print "<br><br>";

  print "<table border=1 width=600>";
  print "<colgroup><col width=80><col width=400><col width=120></colgroup>";
  print "<tr><th></th><th>log information</th><th>plots/files</th></tr>";

  # data.csv
  print "<tr><td>";
  print "<H4>Concentration data:</H4></td>";
  if ( -f "$BASE/input" && -f "$BASE/data.csv" ) {
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
  if ( -f "$BASE/phenotypes.txt" && -f "$BASE/phenotypes.csv" ) {
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
#     print `grep "DEL_METABS:" $BASE/processing_log.txt | sed -n 's/OUTLIER://gp'`;
  print "</td><td>";
  if ( -f "$BASE/lowerOutliers.csv" ) {
    print "<a href=\"$HTMLBASE/lowerOutliers.csv\">lower outliers</a>";
  }
  if ( -f "$BASE/upperOutliers.csv" ) {
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
  if ( -f "$BASE/cv.pdf" ) {
    print "<a href=\"$HTMLBASE/cv.pdf\">cv plot</a><br>";
  } else {
    print " ";
  }
#  TODO: lesen wie viele refs  for schleife fuer alle _cv.csv
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
  if( -f "$BASE/metabolitesForDropping.csv" ) {
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
  if( -f "$BASE/batchBoxplot.pdf" ) {
    print "<a href=\"$HTMLBASE/batchBoxplot.pdf\">batch boxplots</a>";
  } else {
    print " ";
  }
  if( -f "$BASE/pValuesForAllMetabolites__Batch.key.csv" ) {
    print "<br><a href=\"$HTMLBASE/pValuesForAllMetabolites__Batch.key.csv\">batch p-values</a>";
  }
  if( -f "$BASE/refBatchBoxplot.pdf" ) {
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ( ($simple_form{'TASK'} eq 'SAMPLES') and (exists $simple_form{'ID'}) ) {
#############################################################
################ SAMPLES ##################################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>SAMPLES</H2>";

  if (-f "$BASE/phenotypes.csv") {

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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ( ($simple_form{'TASK'} eq 'PCA') and (exists $simple_form{'ID'}) ) {
#############################################################
##################### PCA  ##################################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";
$pheno = "";
if (defined $simple_form{'PHENO'}) {
  $pheno = $simple_form{'PHENO'};
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>PRINCIPAL COMPONENT ANALYSIS</H2>";

  if (-f "$BASE/pca.pdf") {
    print "<a href=\"$HTMLBASE/pca.pdf\">PCA plot</a>";
  } elsif (-f "$BASE/PCA.pdf") {
    #print "<a href=\"$HTMLBASE/PCA.pdf\">PCA plot</a>";
  } else {
    print "<H4>no plot available</H4>\n";
  }

  $pcaplot12="PCA";
  if ($pheno ne "") {
    $pcaplot12=$pcaplot12 . $pheno;
  }
  $pcaplot12=$pcaplot12 . "_PC1_PC2";
  $pcaplot12MAP=$pcaplot12 . ".map";
  $pcaplot12PNG=$pcaplot12 . ".png";


  $pcaplot13="PCA";
  if ($pheno ne "") {
    $pcaplot13=$pcaplot13 . $pheno;
  }
  $pcaplot13=$pcaplot13 . "_PC1_PC3";
  $pcaplot13MAP=$pcaplot13 . ".map";
  $pcaplot13PNG=$pcaplot13 . ".png";


  $pcaplot23="PCA";
  if ($pheno ne "") {
    $pcaplot23=$pcaplot23 . $pheno;
  }
  $pcaplot23=$pcaplot23 . "_PC2_PC3";
  $pcaplot23MAP=$pcaplot23 . ".map";
  $pcaplot23PNG=$pcaplot23 . ".png";


  $pcaplotPropOfVar="PCA";
  if ($pheno ne "") {
    $pcaplotPropOfVar=$pcaplotPropOfVar . $pheno;
  }
  $pcaplotPropOfVarPNG=$pcaplotPropOfVar . "_propOfVar.png";


  
  if (-f "$BASE/$pcaplot12PNG" && -f "$BASE/$pcaplot12MAP" &&
      -f "$BASE/$pcaplot13PNG" && -f "$BASE/$pcaplot13MAP" &&
      -f "$BASE/$pcaplot23PNG" && -f "$BASE/$pcaplot23MAP" &&
      -f "$BASE/$pcaplotPropOfVarPNG") {

    $firstline="";

    if (-f "$BASE/phenotypes_nominal.csv") {

      open(PHENO, "<$BASE/phenotypes_nominal.csv");
      $firstline = <PHENO>;
      close(PHENO);

    } elsif (-f "$BASE/phenotypes.csv") {  # muss noch bleiben fuer alte Berechnungen 
      open(PHENO, "<$BASE/phenotypes.csv");
      $firstline = <PHENO>;
      close(PHENO);
    }

    if ($firstline ne "") {
      ($id,@phenotypes) = split (/;/, $firstline);

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
    open (MAP, "grep \"area shape\" $BASE/$pcaplot12MAP |");
    while (<MAP>) {
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
    open (MAP, "grep \"area shape\" $BASE/$pcaplot13MAP |");
    while (<MAP>) {
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
    open (MAP, "grep \"area shape\" $BASE/$pcaplot23MAP |");
    while (<MAP>) {
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
#      $fic =~ s///;
#      print "<a href=\"$HTMLBASE/$fic\">$fic</a>\n";
#    }
#    print "</pre>\n";
#  }


  if (-f "$BASE/pca.loadings.csv") {
    print "<a href=\"$HTMLBASE/pca.loadings.csv\">Download PCA loadings</a>";
  } elsif (-f "$BASE/pca.rotations.csv") {
   print "<a href=\"$HTMLBASE/pca.rotations.csv\">Download PCA loadings</a>";
    #print "<a href=\"$HTMLBASE/PCA.pdf\">PCA plot</a>";
  } else {
    print "<H4>no PCA loadings available</H4>\n";
  }



  #print "</center>\n";


} else { # no such ID
  print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF887;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ( ($simple_form{'TASK'} eq 'HYPOTHESIS') and (exists $simple_form{'ID'}) ) {
#############################################################
#################### HYPOTHESIS #############################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";


print <<EOF848;
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
EOF848

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>HYPOTHESIS TESTS</H2>";

  if (-f "$BASE/hypothesisTests.pdf") {
    print "<a href=\"$HTMLBASE/hypothesisTests.pdf\">Click here for hypothesis tests</a>";
  } elsif (-f "$BASE/hypothesisTests_complete_data.pdf") {
    print "<a href=\"$HTMLBASE/hypothesisTests_complete_data.pdf\">Click here for hypothesis tests based on complete data set</a>";
    @HLIBS = `ls -t $BASE/hypothesisTests_separated_for*.pdf | sed 's/.*\\///' 2> /dev/null `;
    if ($#HLIBS >= 0) {
      print "<pre>\n";
      for ($i=0; $i<=$#HLIBS; $i++) {
        $fic = $HLIBS[$i];
        chomp $fic;
        $fic =~ s///;
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


  print "<br><br>";

  @LIBS = `ls -t $BASE/pValuesForAllMetabolites_*.csv | sed 's/.*\\///' | grep -v Batch.key  2> /dev/null `;
  if ($#LIBS < 0) {
    print "<H4>no p-values available</H4>";
  } else {
    print "<H4>p-values:</H4>";
    print "<pre>\n";
    for ($i=0; $i<=$#LIBS; $i++) {
      $fic = $LIBS[$i];
      chomp $fic;
      $fic =~ s///;
      print "<a href=\"$HTMLBASE/$fic\">$fic</a>\n";
    }

    print "<br>";

    if (-f "$BASE/bonferroni.csv") {
      print "<a href=\"$HTMLBASE/bonferroni.csv\">Bonferroni corrected significance levels</a>";
    }

    print "</pre>\n";

  }



  #print "</center>\n";


} else { # no such ID
  print "<H1>ERROR: no job with ID $ID found</H1>";
}

print <<EOF847;
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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


} elsif ( ($simple_form{'TASK'} eq 'KENDALL') and (exists $simple_form{'ID'}) ) {
#############################################################
##################### KENDALL ###############################
#############################################################

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;

# set some other useful variables
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>KENDALL CORRELATION TEST</H2>";


  if (-f "$BASE/kendall.pdf") {
    print "<a href=\"$HTMLBASE/kendall.pdf\" type=\"application/pdf\">Click here for the results of Kendall correlation test in PDF format</a>";
  } else {
    print "<H4>no plot available</H4\n";
  }

  print "<br><br>";

  if (-f "$BASE/kendall.png") {
    print "<IMG src=\"$HTMLBASE/kendall.png\"  border=\"0\" >"
  }


  print "<br><br>";

  if (-f "$BASE/kendall.csv") {
    print "<a href=\"$HTMLBASE/kendall.csv\" type=\"application/excel\">Kendall's tau and p-values</a>";
  } else {
    print "<H4>list of Kendall's tau and p-values not available</H4\n";
  }

  print "<br>";
  if (-f "$BASE/kendall_ratios.csv") {
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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


} elsif ($simple_form{'TASK'} eq 'DELETE') {
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

if ((defined $simple_form{'ADMIN'}) and ($simple_form{'ADMIN'} eq "metaP007")) {

  $del = $simple_form{'DEL'};
  @list = split /#/, $del;
  $ndel = $#list+1;

  print "<H1>Deleting $ndel job(s)</H1>";
  print "<PRE>";
  for ($i=0; $i<=$#list; $i++) {
    system "

echo \"removing job $list[$i]\"
rm -r -f $USERDATA/$list[$i]*
";
  }
  print "</PRE>";
  print "<H3><A HREF=\"$CGI?TASK=LIST\">BACK to job status</A></H3>";
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ($simple_form{'TASK'} eq 'SHOWCMPD') {
#############################################################
################ SHOWCMPD ###################################
#############################################################
# display metabolite data

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;
$metabolite = $simple_form{'CMPD'};
$BASE="$USERDATA/$ID";
$HTMLBASE="$HTMLUSERDATA/$ID";
$optionsfile = "$BASE/options";
$pheno = "";
if (defined $simple_form{'PHENO'}) {
  $pheno = $simple_form{'PHENO'};
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>Metabolite: $metabolite</H2>";

  $barplot=$metabolite . "_barplot";
  $barplotMAP=$barplot . ".map";

  if ($pheno ne "") {
    $barplot=$barplot . "_" . $pheno;
  }

  $barplotPNG=$barplot . ".png";

  
  if (-f "$BASE/barplots/$barplotPNG" && -f "$BASE/barplots/$barplotMAP") {

    $firstline="";

    if (-f "$BASE/phenotypes_nominal.csv") {

      open(PHENO, "<$BASE/phenotypes_nominal.csv");
      $firstline = <PHENO>;
      close(PHENO);

    } elsif (-f "$BASE/phenotypes.csv") {  # muss noch bleiben fuer alte Berechnungen 
      open(PHENO, "<$BASE/phenotypes.csv");
      $firstline = <PHENO>;
      close(PHENO);
    }

    if ($firstline ne "") {

      ($id,@phenotypes) = split (/;/, $firstline);

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
    open (MAP, "grep \"area shape\" $BASE/barplots/$barplotMAP |");
    while (<MAP>) {
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

  if ( -f "$HTML/metabId2htmlMapping.csv") {
    open (NAME2HTML, "<$HTML/metabId2htmlMapping.csv");
    while (<NAME2HTML>) {
      $line = $_;
      my($rName,$htmlName) = split (/;/, $line);
      $name2html{$rName}=$htmlName;
    }
    close NAME2HTML;
  }


  if (exists $name2html{$metabolite}) {

    $metabFile= "metabolites/Details_short/" . $name2html{$metabolite};
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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



} elsif ($simple_form{'TASK'} eq 'SHOWSMPL') {
#############################################################
################ SHOWSMPL ###################################
#############################################################
# display sample data

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;
$sample = $simple_form{'SMPL'};
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

if ( -f "$BASE/metaPjob.cmd" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>Sample: $sample</H2>";

  if ( -f "$BASE/phenotypes_beforeCheck.csv" ) {

    $firstline="";

    print "<table border=\"1\"><tr><td>";

    open(ALLPHENO1, "<$BASE/phenotypes_beforeCheck.csv");
    $firstline = <ALLPHENO1>;
    $firstline =~ s/;/\<\/td\>\<td\>/g;
    close(ALLPHENO1);
    print $firstline;
    print "</td></tr>";

    print "<tr><td>";
    open (ALLPHENO2, "grep \"^$sample\" $BASE/phenotypes_beforeCheck.csv|");  #sample ids muessen unique sein
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
  
  if (-f "$BASE/barplots/$sbarplotPNG" && -f "$BASE/barplots/$sbarplotMAP") {
    print "<IMG src=\"$HTMLBASE/barplots/$sbarplotPNG\" usemap=\"#$sbarplotMAP\" border=\"0\" ISMAP>";
    print "<map name=\"$sbarplotMAP\">";
    open (SMAP, "grep \"area shape\" $BASE/barplots/$sbarplotMAP |");
    while (<SMAP>) {
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
  if ( -f $keggFile ) {

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

  if (-f "$BASE/phenotypes.list") {
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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



} elsif ($simple_form{'TASK'} eq 'SHOWSEQ') {
#############################################################
################ SHOWSEQ ###################################
#############################################################
# display the the input data

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;
$BASE="$USERDATA/$ID";
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

if ( -f "$BASE/metaPjob.cmd" ) {


  # print the headder
  &print_subheadder ();

  print "<H2>INPUT DATA</H2>";
  

  if ( -f "$BASE/options" ) {
    print "<H4>Job options:</H4>";
    print "</center><pre>\n";
    system "cat $BASE/options | grep -v EMAIL";
    print "</pre><center><br><br>\n";
  }

  if (-f "$BASE/phenotypes.txt") {
    print "<H4>Submitted phenotype data:</H4>";
    print "</center><pre>\n";
    system "cat $BASE/phenotypes.txt";
    print "</pre><center><br><br>\n";
  }
  
  if (-f "$BASE/aux.txt") {
    print "<H4>Submitted auxillary data:</H4>";
    print "</center><pre>\n";
    system "cat $BASE/aux.txt";
    print "</pre><center><br><br>\n";
  }
  
  if (-f "$BASE/input") {
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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

} elsif ($simple_form{'TASK'} eq 'SHOWLOG') {
#############################################################
################ SHOWLOG ###################################
#############################################################
# display the log file

$ID = $simple_form{'ID'};
$ID =~ s/[^a-z^A-Z^0-9^_]*//g;
$BASE="$USERDATA/$ID";

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

if ( -f "$BASE/server_log.txt" ) {

  # print the headder
  &print_subheadder ();

  print "<H2>LOGFILES</H2>";

  print "<H4><a href=\"doc.html#faq\">In case of trouble, check out our FAQs!</a></H4>\n";

  print "</center><pre>\n";
  system "cat $BASE/server_log.txt | sed 's/\@[^ ]*//' | sed 's/^\\(....................................................................................................\\).*/\\1.../'";
  if ( -f "$BASE/server_log.txt" ) {
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
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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
#############################################################
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
<H4>The input parameters from the CGI script were ... </H4>
EOF13

foreach $k (keys %simple_form) { # print arguments

  print "form{$k} = '", $simple_form{"$k"}, "'<br>\n";

}

print <<EOF16;
<center>
<!-- include BOT -->
  <BR><BR><BR><BR>

   KEGG Data is provided by the <a href="http://www.kegg.org">Kanehisa Laboratories</a>
   for academic use.  Any commercial use of KEGG data requires a license
   agreement from <a href="http://www.pathway.jp">Pathway Solutions Inc</a>.
  <BR>
   The Helmholtz Zentrum M&uuml;nchen <a href="http://www.helmholtz-muenchen.de/en/serviceline/imprint/index.html">imprint</a> applies.
<H4>
  This page is maintained by Gabi Kastenm&uuml;ller and Werner R&ouml;misch-Margl.
<br>
  Last modification: 28 December 2009
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
