#!/usr/bin/perl
select(STDOUT);
$| = 1;
while (<>) {
    if (/^(|\d+\s+)((\w+):\/+)([^\/:]+)(|:(\d+))(|\/\S*)(|\s.*)$/) {
        my $channel = $1;
        my $protocolClean = $3;
        my $domain = $4;
        my $port = $5;
        my $portClean = $6;
        my $urlPath = $7;
        if ($protocolClean eq 'http' && ($port eq '' || $portClean eq '80')) {
            print STDOUT "${channel}OK rewrite-url=\"https://${domain}${urlPath}\"\n";
        } else {
            print STDOUT "${channel}ERR\n";
        }
    