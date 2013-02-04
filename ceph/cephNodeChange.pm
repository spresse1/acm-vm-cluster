# IBM(c) 2007 EPL license http://www.eclipse.org/legal/epl-v10.html
use strict;
use warnings;
package xCAT_monitoring::cephNodeChange;
1;

#--------------------------------------------------------------------------------
#=head3   processTableChanges
#  This subroutine get called when new nodes are added into the cluster
#   or nodes are removed from the cluster, or a row is modified.
#    Arguments:
#      action - table action. It can be d for rows deleted, a for rows added
#                    or u for rows updated.
#      tablename - string. The name of the DB table whose data has been changed.
#      old_data - an array reference of the old row data that has been changed.
#           The first element is an array reference that contains the column names.
#           The rest of the elelments are also array references each contains
#           attribute values of a row.
#           It is set when the action is u or d.
#      new_data - a hash refernce of new row data; only changed values are present
#           in the hash.  It is keyed by column names.
#           It is set when the action is u or a.
#    Returns:
#      0
#    Comment:
#       To test, 
#        1. copy this file to /opt/xcat/lib/perl/xCAT_monitoring directory.
#        2. run regnotif /opt/xcat/lib/perl/xCAT_monitoring/mycode.pm nodelist -o a,u,d
#        3. Then change the nodelist table (add node, remove node, or change status column).
#        4. Watch /var/log/mycode.log for output.
#=cut
#-------------------------------------------------------------------------------
sub removeFromCeph {
  my $node=shift;
  print FILE "Removing $node... ";
  
  #TODO: fill in.
  
  print FILE "done.\n";
}

sub addToCeph {
  my $node-shift;
  print FILE "Adding $node as MDS... ";
  
  #TODO: fill in.
  
  print FILE "done.\n";
}

sub processTableChanges {
  my $action=shift;
  if ($action =~ /xCAT_monitoring::cephNodeChange/){
    $action=shift;
  }

  my $tablename=shift;
  my $old_data=shift;
  my $new_data=shift;

  my @nodenames=();
  open(FILE, ">>/var/log/cephNodeChange.log") or dir ("cannot open the file\n");
  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
  printf FILE "\n-----------%2d-%02d-%04d %02d:%02d:%02d-----------\n", $mon+1,$mday,$year+1900,$hour,$min,$sec;  
  if ($action eq "a") { #nodes added in the cluster
    if ($new_data) {
      push(@nodenames, $new_data->{node});
      my $noderange=join(',', @nodenames);
      print (FILE "new nodes in the cluster are: $noderange\n"); 
    }
  }
  elsif ($action eq "d") { #nodes removed from the cluster
    #find out the index of "node" column
    if ($old_data->[0]) {
      my $colnames=$old_data->[0];
      my $i;
      for ($i=0; $i<@$colnames; ++$i) {
        if ($colnames->[$i] eq "node") {last;}
      }

      for (my $j=1; $j<@$old_data; ++$j) {
        removeFromCeph($old_data->[$j]->[$i]);
      }
    }
  } else { #update case, assuminmg monitoring nodelist.status
    my $newstatus;
    if ($new_data) {
      $newstatus=$new_data->{status};
    }
    if ($old_data->[0]) {
      my $colnames=$old_data->[0];
      my $m;
      my $k;
      for (my $i=0; $i<@$colnames; ++$i) {
        if ($colnames->[$i] eq "node") {$m=$i}
        if ($colnames->[$i] eq "status") {$k=$i; }
      }

      for (my $j=1; $j<@$old_data; ++$j) {
        print FILE "node=". $old_data->[$j]->[$m] . " ,";
        print FILE "old_status=". $old_data->[$j]->[$k] . " ,";
        print FILE "new_status=$newstatus\n";
        
        # Now, lets filter action based on the transition...
        # Actually, if its installing, we ought to remove from the cluster
        # then re-add
        if ($newstatus eq "installing") {
          removeFromCeph($old_data->[$j]->[$m]);
          addToCeph($old_data->[$j]->[$m]);
        }
      }
    }
  }
  close(FILE);
  return 0;
}
