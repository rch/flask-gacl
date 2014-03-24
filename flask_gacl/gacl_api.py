"""
    port of phpGACL - every effort will be made to release the enclosing flask extension under a permissive license
    and ultimately this code will be moved to an independent package (likely called pygacl) anyway
    
    Original License:
    
    phpGACL - Generic Access Control List
    Copyright (C) 2002,2003 Mike Benoit
    
    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    
    For questions, help, comments, discussion, etc., please join the
    phpGACL mailing list. http:# sourceforge.net/mail/?group_id=57103
    
    You may contact the author of phpGACL by e-mail at:
    ipso@snappymail.ca
    
    The latest version of phpGACL can be obtained from:
    http:# phpgacl.sourceforge.net/
    
    @package phpGACL
"""
from utils import *
from gacl import Gacl
from model import *

#
#   For examples, see example.php or the Administration interface,
#   as it makes use of nearly every API Call.
#

"""
 * gacl_api Extended API Class
 *
 * Class gacl_api should be used for applications that must interface directly with
 * phpGACL's data structures, objects, and rules.
 *
 * @package phpGACL
 * @author Mike Benoit <ipso@snappymail.ca>
 *
"""

class GaclApi(Gacl):
        
    """
     * showarray()
     *
     * Dump all contents of an array in HTML (kinda)
     *
     * @param array
     *
    """
    def showarray(self, array):
        print "<br><pre>\n"
        print array
        print "</pre><br>\n"
    
    """
     * count_all()
     *
     * Recursively counts elements in an array and sub-arrays.
     *
     * This is different from count(arg, COUNT_RECURSIVE)
     * in PHP >= 4.2.0, which includes sub-arrays in the count.
     *
     * @return int The returned count is a count of all scalar elements found.
     *
     * @param array Array to count
    """
    def count_all(self, arg = None):
        if is_list(arg):
            count = 0
            for val in arg:
               count += self.count_all(val)
            return count
        elif arg:
            #  single object
            return 1
        return False
    
    """
     * get_version()
     *
     * Grabs phpGACL version from the database.
     *
     * @return string Version of phpGACL
    """
    def get_version(self):
        query = "select value from " + self._db_table_prefix + "phpgacl where name = 'version'"
        version = self.db.execute(query).fetchone()[0]
        return version
    
    """
     * get_schema_version()
     *
     * Grabs phpGACL schema version from the database.
     *
     * @return string Schema Version
    """
    def get_schema_version(self):
        query = "select value from " + self._db_table_prefix + "phpgacl where name = 'schema_version'"
        version = self.db.execute(query).fetchone()[0]
        return version
    
    """
     * consolidated_edit_acl()
     *
     * Add's an ACL but checks to see if it can consolidate it with another one first.
     *
     * This ONLY works with ACO's and ARO's. Groups, and AXO are excluded.
     * As well this function is designed for handling ACLs with return values,
     * and consolidating on the return_value, in hopes of keeping the ACL count to a minimum.
     *
     * A return value of False must _always_ be handled outside this function.
     * As this function will remove AROs from ACLs and return False, in most cases
     * you will need to a create a completely new ACL on a False return.
     *
     * @return bool Special boolean return value. See note.
     *
     * @param string ACO Section Value
     * @param string ACO Value
     * @param string ARO Section Value
     * @param string ARO Value
     * @param string Return Value of ACL
    """
    def consolidated_edit_acl(self, aco_section_value, aco_value, aro_section_value, aro_value, return_value):

        self.debug_text("consolidated_edit_acl(): ACO Section Value: aco_section_value ACO Value: aco_value ARO Section Value: aro_section_value ARO Value: aro_value Return Value: return_value")

        acl_ids = list()

        if not aco_section_value:
            self.debug_text("consolidated_edit_acl(): ACO Section Value (aco_section_value) is empty, this is required!")
            return False
        

        if not aco_value:
            self.debug_text("consolidated_edit_acl(): ACO Value (aco_value) is empty, this is required!")
            return False
        

        if not aro_section_value:
            self.debug_text("consolidated_edit_acl(): ARO Section Value (aro_section_value) is empty, this is required!")
            return False
        

        if not aro_value:
            self.debug_text("consolidated_edit_acl(): ARO Value (aro_value) is empty, this is required!")
            return False
        

        if not return_value:
            self.debug_text("consolidated_edit_acl(): Return Value (return_value) is empty, this is required!")
            return False
        

        # See if a current ACL exists with the current objects, excluding return value
        current_acl_ids = self.search_acl(aco_section_value, aco_value, aro_section_value, aro_value, False, False, False, False, False)
        # showarray(current_acl_ids)

        if (is_array(current_acl_ids)) :
            self.debug_text("add_consolidated_acl(): Found current ACL_IDs, counting ACOs")

            for current_acl_id in current_acl_ids:
                # Check to make sure these ACLs only have a single ACO mapped to them.
                current_acl_array = self.get_acl(current_acl_id)

                # showarray(current_acl_array)
                self.debug_text("add_consolidated_acl(): Current Count: " + self.count_all(current_acl_array['aco']) + "")

                if ( self.count_all(current_acl_array['aco']) == 1) :
                    self.debug_text("add_consolidated_acl(): ACL ID: current_acl_id has 1 ACO.")

                    # Test to see if the return values match, if they do, no need removing or appending ARO. Just return True.
                    if (current_acl_array['return_value'] == return_value) :
                        self.debug_text("add_consolidated_acl(): ACL ID: current_acl_id has 1 ACO, and the same return value. No need to modify.")
                        return True
                    
                    acl_ids.append(current_acl_id)
        
        # showarray(acl_ids)
        acl_ids_count = count(acl_ids)

        # If acl_id's turns up more then one ACL, lets remove the ARO from all of them in hopes to
        # eliminate any conflicts.
        if (is_list(acl_ids) and acl_ids_count > 0) :
            self.debug_text("add_consolidated_acl(): Removing specified ARO from existing ACL.")
            for acl_id in acl_ids:
                # Remove ARO from current ACLs, so we don't create conflicting ACLs later on.
                if not self.shift_acl(acl_id, {aro_section_value: list(aro_value)}):
                    self.debug_text("add_consolidated_acl(): Error removing specified ARO from ACL ID: acl_id")
                    return False
        else:
            self.debug_text("add_consolidated_acl(): Didn't find any current ACLs with a single ACO. ")
        # unset(acl_ids)
        acl_ids = list()
        acl_ids_count = None
        # At this point there should be no conflicting ACLs, searching for an existing ACL with the new values.
        new_acl_ids = self.search_acl(aco_section_value, aco_value, False, False, None, None, None, None, return_value)
        new_acl_count = count(new_acl_ids)
        # showarray(new_acl_ids)

        if (is_array(new_acl_ids)) :
            self.debug_text("add_consolidated_acl(): Found new ACL_IDs, counting ACOs")

            for new_acl_id in new_acl_ids:
                # Check to make sure these ACLs only have a single ACO mapped to them.
                new_acl_array = self.get_acl(new_acl_id)
                # showarray(new_acl_array)
                self.debug_text("add_consolidated_acl(): New Count: " + self.count_all(new_acl_array['aco']) + "")
                if ( self.count_all(new_acl_array['aco']) == 1) :
                    self.debug_text("add_consolidated_acl(): ACL ID: new_acl_id has 1 ACO, append should be able to take place.")
                    acl_ids.append(new_acl_id)
        
        # showarray(acl_ids)
        acl_ids_count = count(acl_ids)
        if (is_list(acl_ids) and acl_ids_count == 1) :
            self.debug_text("add_consolidated_acl(): Appending specified ARO to existing ACL.")
            acl_id = acl_ids[0]
            if not self.append_acl(acl_id, {aro_section_value: list(aro_value)}):
                self.debug_text("add_consolidated_acl(): Error appending specified ARO to ACL ID: acl_id")
                return False
            self.debug_text("add_consolidated_acl(): Hot damn, ACL consolidated!")
            return True
        elif(acl_ids_count > 1) :
            self.debug_text("add_consolidated_acl(): Found more then one ACL with a single ACO. Possible conflicting ACLs.")
            return False
        elif (acl_ids_count == 0) :
            self.debug_text("add_consolidated_acl(): No existing ACLs found, create a new one.")
            if (not self.add_acl({aco_section_value: list(aco_value)},
                                    {aro_section_value: list(aro_value)},
                                    None,
                                    None,
                                    None,
                                    True,
                                    True,
                                    return_value,
                                    None)
                                ):
                self.debug_text("add_consolidated_acl(): Error adding new ACL for ACO Section: aco_section_value ACO Value: aco_value Return Value: return_value")
                return False
            
            self.debug_text("add_consolidated_acl(): ADD_ACL() successfull, returning True.")
            return True
        
        self.debug_text("add_consolidated_acl(): Returning False.")
        return False
    

    """
     * search_acl()
     *
     * Searches for ACL's with specified objects mapped to them.
     *
     * None values are included in the search, if you want to ignore
     * for instance aro_groups use False instead of None.
     *
     * @return array containing ACL IDs if search is successful
     *
     * @param string ACO Section Value
     * @param string ACO Value
     * @param string ARO Section Value
     * @param string ARO Value
     * @param string ARO Group Name
     * @param string AXO Section Value
     * @param string AXO Value
     * @param string AXO Group Name
     * @param string Return Value
    """
    def search_acl(self, aco_section_value=None, aco_value=None, aro_section_value=None, aro_value=None, aro_group_name=None, axo_section_value=None, axo_value=None, axo_group_name=None, return_value=None) :
        self.debug_text("search_acl(): aco_section_value: aco_section_value aco_value: aco_value, aro_section_value: aro_section_value, aro_value: aro_value, aro_group_name: aro_group_name, axo_section_value: axo_section_value, axo_value: axo_value, axo_group_name: axo_group_name, return_value: return_value")

        query = 'SELECT a.id FROM ' +  self._db_table_prefix + 'acl a'
        where_query = list()
        
        #  ACO
        if (aco_section_value != False and aco_value != False) :
            query += 'LEFT JOIN    ' +  self._db_table_prefix + 'aco_map ac ON a.id=ac.acl_id'
            if (aco_section_value == None and aco_value == None) :
                where_query.append('(ac.section_value IS None AND ac.value IS None)')
            else:
                where_query.append('(ac.section_value=' +  self.db.quote(aco_section_value) + ' AND ac.value=' +  self.db.quote(aco_value) + ')')
        
        #  ARO
        if (aro_section_value != False and aro_value != False) :
            query += 'LEFT JOIN    ' +  self._db_table_prefix + 'aro_map ar ON a.id=ar.acl_id'
            if (aro_section_value == None and aro_value == None) :
                where_query.append('(ar.section_value IS None AND ar.value IS None)')
            else:
                where_query.append('(ar.section_value=' +  self.db.quote(aro_section_value) + ' AND ar.value=' +  self.db.quote(aro_value) + ')')
        
        #  AXO
        if (axo_section_value != False and axo_value != False) :
            query += 'LEFT JOIN    ' +  self._db_table_prefix + 'axo_map ax ON a.id=ax.acl_id'
            if (axo_section_value == None and axo_value == None) :
                where_query.append('(ax.section_value IS None AND ax.value IS None)')
            else:
                where_query.append('(ax.section_value=' +  self.db.quote(axo_section_value) + ' AND ax.value=' +  self.db.quote(axo_value) + ')')
        
        #  ARO Group
        if (aro_group_name != False) :
            query += 'LEFT JOIN ' +  self._db_table_prefix + 'aro_groups_map arg ON a.id=arg.acl_id' + \
                     'LEFT JOIN    ' +  self._db_table_prefix + 'aro_groups rg ON arg.group_id=rg.id'
            if (aro_group_name == None) :
                where_query.append('(rg.name IS None)')
            else:
                where_query.append('(rg.name=' +  self.db.quote(aro_group_name) + ')')
        
        #  AXO Group
        if (axo_group_name != False) :
            query += 'LEFT JOIN    ' +  self._db_table_prefix + 'axo_groups_map axg ON a.id=axg.acl_id' + \
                     'LEFT JOIN    ' +  self._db_table_prefix + 'axo_groups xg ON axg.group_id=xg.id'
            if (axo_group_name == None) :
                where_query.append('(xg.name IS None)')
            else:
                where_query.append('(xg.name=' +  self.db.quote(axo_group_name) + ')')
        
        if (return_value != False):
            if (return_value == None):
                where_query.append('(a.return_value IS None)')
            else:
                where_query.append('(a.return_value=' +  self.db.quote(return_value) + ')')
        
        if len(where_query) > 0:
            query += 'WHERE ' +  ' AND '.join(where_query)
        
        return self.db.GetCol(query)
    
    """
     * append_acl()
     *
     * Appends objects on to a specific ACL.
     *
     * @return bool True if successful, False otherwise.
     *
     * @param int ACL ID #
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
    """
    def append_acl(self, acl_id, aro_array=None, aro_group_ids=None, axo_array=None, axo_group_ids=None, aco_array=None) :
        self.debug_text("append_acl(): ACL_ID: acl_id")

        update = 0

        if not acl_id:
            self.debug_text("append_acl(): No ACL_ID specified! ACL_ID: acl_id")
            return False
        

        # Grab ACL data.
        acl_array = self.get_acl(acl_id)
        
        # Append each object type seperately.
        if (is_array(aro_array) and count(aro_array) > 0) :
            self.debug_text("append_acl(): Appending ARO's")
            
            for aro_section_value, aro_value_array in aro_array:
                for aro_value in aro_value_array:
                    if len(acl_array['aro'][aro_section_value]) != 0:
                        if not aro_value in acl_array['aro'][aro_section_value]:
                            self.debug_text("append_acl(): ARO Section Value: aro_section_value ARO VALUE: aro_value")
                            acl_array['aro'][aro_section_value].append(aro_value)
                            update = 1
                        else:
                            self.debug_text("append_acl(): Duplicate ARO, ignoring... ")
                     
                    else: # Array is empty so add this aro value.
                        acl_array['aro'][aro_section_value].append(aro_value)
                        update = 1
        
        if is_list(aro_group_ids) and len(aro_group_ids) > 0:
            self.debug_text("append_acl(): Appending ARO_GROUP_ID's")    
            for aro_group_id in aro_group_ids:
                if not isinstance(acl_array['aro_groups'], collections.Iterable) or not aro_group_id in acl_array['aro_groups']:
                    self.debug_text("append_acl(): ARO Group ID: aro_group_id")
                    acl_array['aro_groups'].append(aro_group_id)
                    update = 1
                else:
                    self.debug_text("append_acl(): Duplicate ARO_Group_ID, ignoring... ")
        
        if is_list(axo_array) and len(axo_array) > 0:
            self.debug_text("append_acl(): Appending AXO's")
            for axo_section_value, axo_value_array in axo_array:
                for axo_value in axo_value_array:
                    if not axo_value in acl_array['axo'][axo_section_value]:
                        self.debug_text("append_acl(): AXO Section Value: axo_section_value AXO VALUE: axo_value")
                        acl_array['axo'][axo_section_value].append(axo_value)
                        update = 1
                    else:
                        self.debug_text("append_acl(): Duplicate AXO, ignoring... ")
        
        if is_list(axo_group_ids) and len(axo_group_ids) > 0:
            self.debug_text("append_acl(): Appending AXO_GROUP_ID's")
            for axo_group_id in axo_group_ids:
                if not isinstance(acl_array['axo_groups'], collections.Iterable) or not axo_group_id in acl_array['axo_groups']:
                    self.debug_text("append_acl(): AXO Group ID: axo_group_id")
                    acl_array['axo_groups'].append(axo_group_id)
                    update = 1
                else:
                    self.debug_text("append_acl(): Duplicate ARO_Group_ID, ignoring... ")
        
        if is_list(aco_array) and len(aco_array) > 0 :
            self.debug_text("append_acl(): Appending ACO's")
            for aco_section_value, aco_value_array in aco_array:
                for aco_value in aco_value_array:
                    if not aco_value in acl_array['aco'][aco_section_value]:
                        self.debug_text("append_acl(): ACO Section Value: aco_section_value ACO VALUE: aco_value")
                        acl_array['aco'][aco_section_value].append(aco_value)
                        update = 1
                    else:
                        self.debug_text("append_acl(): Duplicate ACO, ignoring... ")
        
        if (update == 1) :
            self.debug_text("append_acl(): Update flag set, updating ACL.")
            # function edit_acl(acl_id, aco_array, aro_array, aro_group_ids=None, axo_array=None, axo_group_ids=None, allow=1, enabled=1, return_value=None, note=None) :
            return self.edit_acl(acl_id, acl_array['aco'], acl_array['aro'], acl_array['aro_groups'], acl_array['axo'], acl_array['axo_groups'], acl_array['allow'], acl_array['enabled'], acl_array['return_value'], acl_array['note'])
        

        # Return True if everything is duplicate and no ACL id updated.
        self.debug_text("append_acl(): Update flag not set, NOT updating ACL.")
        return True
    

    """
     * shift_acl()
     *
     * Opposite of append_acl(). Removes objects from a specific ACL. (named after PHP's array_shift())
     *
     * @return bool True if successful, False otherwise.
     *
     * @param int ACL ID #
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
    """
    def shift_acl(self, acl_id, aro_array=None, aro_group_ids=None, axo_array=None, axo_group_ids=None, aco_array=None) :
        self.debug_text("shift_acl(): ACL_ID: acl_id")

        update = 0

        if not acl_id:
            self.debug_text("shift_acl(): No ACL_ID specified! ACL_ID: acl_id")
            return False
        

        # Grab ACL data.
        acl_array = self.get_acl(acl_id)

        # showarray(acl_array)
        # Remove each object type seperately.
        if (is_array(aro_array) and count(aro_array) > 0) :
            self.debug_text("shift_acl(): Removing ARO's")

            for aro_section_value, aro_value_array in aro_array:
                for aro_value in aro_value_array:
                    self.debug_text("shift_acl(): ARO Section Value: aro_section_value ARO VALUE: aro_value")
                    
                    # Only search if aro array contains data.
                    if ( len(acl_array['aro'][aro_section_value]) != 0 ) :
                        aro_key = array_search(aro_value, acl_array['aro'][aro_section_value])
                        
                        if (aro_key != False) :
                            self.debug_text("shift_acl(): Removing ARO. (aro_key)")
                            unset(acl_array['aro'][aro_section_value][aro_key])
                            update = 1
                        else:
                            self.debug_text("shift_acl(): ARO doesn't exist, can't remove it.")
        
        if (is_array(aro_group_ids) and len(aro_group_ids) > 0) :
            self.debug_text("shift_acl(): Removing ARO_GROUP_ID's")

            for aro_group_id in aro_group_ids:
                self.debug_text("shift_acl(): ARO Group ID: aro_group_id")
                aro_group_key = array_search(aro_group_id, acl_array['aro_groups'])
                
                if (aro_group_key != False) :
                    self.debug_text("shift_acl(): Removing ARO Group. (aro_group_key)")
                    unset(acl_array['aro_groups'][aro_group_key])
                    update = 1
                else:
                    self.debug_text("shift_acl(): ARO Group doesn't exist, can't remove it.")

        
        if (is_array(axo_array) and count(axo_array) > 0) :
            self.debug_text("shift_acl(): Removing AXO's")

            for axo_section_value, axo_value_array in axo_array:
                for axo_value in axo_value_array:
                    self.debug_text("shift_acl(): AXO Section Value: axo_section_value AXO VALUE: axo_value")
                    axo_key = array_search(axo_value, acl_array['axo'][axo_section_value])
                    
                    if (axo_key != False) :
                        self.debug_text("shift_acl(): Removing AXO. (axo_key)")
                        unset(acl_array['axo'][axo_section_value][axo_key])
                        update = 1
                    else:
                        self.debug_text("shift_acl(): AXO doesn't exist, can't remove it.")
        
        if (is_array(axo_group_ids) and len(axo_group_ids) > 0) :
            self.debug_text("shift_acl(): Removing AXO_GROUP_ID's")
            for axo_group_id in axo_group_ids:
                self.debug_text("shift_acl(): AXO Group ID: axo_group_id")
                axo_group_key = array_search(axo_group_id, acl_array['axo_groups'])
                if (axo_group_key != False) :
                    self.debug_text("shift_acl(): Removing AXO Group. (axo_group_key)")
                    unset(acl_array['axo_groups'][axo_group_key])
                    update = 1
                else:
                    self.debug_text("shift_acl(): AXO Group doesn't exist, can't remove it.")
        
        if (is_array(aco_array) and len(aco_array) > 0) :
            self.debug_text("shift_acl(): Removing ACO's")
            for aco_section_value, aco_value_array in aco_array:
                for aco_value in aco_value_array:
                    self.debug_text("shift_acl(): ACO Section Value: aco_section_value ACO VALUE: aco_value")
                    aco_key = array_search(aco_value, acl_array['aco'][aco_section_value])

                    if (aco_key != False) :
                        self.debug_text("shift_acl(): Removing ACO. (aco_key)")
                        unset(acl_array['aco'][aco_section_value][aco_key])
                        update = 1
                    else:
                        self.debug_text("shift_acl(): ACO doesn't exist, can't remove it.")
                    
                
            
        

        if (update == 1) :
            # We know something was changed, so lets see if no ACO's or no ARO's are left assigned to this ACL, if so, delete the ACL completely.
            # self.showarray(acl_array)
            self.debug_text("shift_acl(): ACOs: " + self.count_all(acl_array['aco']) + " AROs: " + self.count_all(acl_array['aro']) + "")

            if ( self.count_all(acl_array['aco']) == 0
                    or ( self.count_all(acl_array['aro']) == 0
                        and ( self.count_all(acl_array['axo']) == 0 or acl_array['axo'] == False)
                        and (count(acl_array['aro_groups']) == 0 or acl_array['aro_groups'] == False)
                        and (count(acl_array['axo_groups']) == 0 or acl_array['axo_groups'] == False)
                        ) ) :
                self.debug_text("shift_acl(): No ACOs or ( AROs AND AXOs AND ARO Groups AND AXO Groups) left assigned to this ACL (ID: acl_id), deleting ACL.")

                return self.del_acl(acl_id)
            

            self.debug_text("shift_acl(): Update flag set, updating ACL.")

            return self.edit_acl(acl_id, acl_array['aco'], acl_array['aro'], acl_array['aro_groups'], acl_array['axo'], acl_array['axo_groups'], acl_array['allow'], acl_array['enabled'], acl_array['return_value'], acl_array['note'])
        

        # Return True if everything is duplicate and no ACL id updated.
        self.debug_text("shift_acl(): Update flag not set, NOT updating ACL.")
        return True
    

    """
     * get_acl()
     *
     * Grabs ACL data.
     *
     * @return bool False if not found, or Associative Array with the following items:
     *
     *    - 'aco' => Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     *    - 'aro' => Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     *    - 'axo' => Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     *    - 'aro_groups' => Array of Group IDs
     *    - 'axo_groups' => Array of Group IDs
     *    - 'acl_id' => int ACL ID #
     *    - 'allow' => int Allow flag
     *    - 'enabled' => int Enabled flag
     *    - 'return_value' => string Return Value
     *    - 'note' => string Note
     *
     * @param int ACL ID #
    """
    def get_acl(self, acl_id) :

        self.debug_text("get_acl(): ACL_ID: acl_id")

        if  not acl_id:
            self.debug_text("get_acl(): No ACL_ID specified! ACL_ID: acl_id")
            return False
        

        # Grab ACL information
        query = "select id, allow, enabled, return_value, note from " + self._db_table_prefix + "acl where id = " + acl_id + ""
        acl_row = self.db.GetRow(query)

        #  return False if not found
        if (not acl_row) :
            self.debug_text("get_acl(): No ACL found for that ID! ACL_ID: acl_id")
            return False
        
        retarr['acl_id'], retarr['allow'], retarr['enabled'], retarr['return_value'], retarr['note'] = acl_row

        # Grab selected ACO's
        query = "select distinct a.section_value, a.value, c.name, b.name from " + self._db_table_prefix + "aco_map a, " + self._db_table_prefix + \
            "aco b, " + self._db_table_prefix + "aco_sections c " + \
            "where ( a.section_value=b.section_value AND a.value = b.value) AND b.section_value=c.value AND a.acl_id = acl_id"
        rs = self.db.Execute(query)
        rows = rs.GetRows()
        
        retarr['aco'] = list()
        for row in rows:
            section_value, value, section, aco = row
            self.debug_text("Section Value: section_value Value: value Section: section ACO: aco")
            retarr['aco'][section_value].append(value)

        
        # showarray(aco)

        # Grab selected ARO's
        query = "select distinct a.section_value, a.value, c.name, b.name from " + self._db_table_prefix + "aro_map a, " + \
            self._db_table_prefix + "aro b, " + self._db_table_prefix + "aro_sections c " + \
            "where ( a.section_value=b.section_value AND a.value = b.value) AND b.section_value=c.value AND a.acl_id = acl_id"
        rs = self.db.Execute(query)
        rows = rs.GetRows()
        
        retarr['aro'] = list()
        for row in rows:
            section_value, value, section, aro = row
            self.debug_text("Section Value: section_value Value: value Section: section ARO: aro")
            retarr['aro'][section_value].append(value)
        
        # showarray(options_aro)
        # Grab selected AXO's
        query = "select distinct a.section_value, a.value, c.name, b.name from " + self._db_table_prefix + "axo_map a, " + \
            self._db_table_prefix + "axo b, " + self._db_table_prefix + "axo_sections c " + \
            "where ( a.section_value=b.section_value AND a.value = b.value) AND b.section_value=c.value AND a.acl_id = acl_id"
        rs = self.db.Execute(query)
        rows = rs.GetRows()

        retarr['axo'] = list()
        for row in rows:
            section_value, value, section, axo = row
            self.debug_text("Section Value: section_value Value: value Section: section AXO: axo")
            retarr['axo'][section_value].append(value)
        
        # showarray(options_aro)
        # Grab selected ARO groups.
        retarr['aro_groups'] = list()
        query = "select distinct group_id from " + self._db_table_prefix + "aro_groups_map where  acl_id = acl_id"
        retarr['aro_groups'] = self.db.GetCol(query)
        # showarray(selected_groups)
        # Grab selected AXO groups.
        retarr['axo_groups'] = list()
        query = "select distinct group_id from " + self._db_table_prefix + "axo_groups_map where  acl_id = acl_id"
        retarr['axo_groups'] = self.db.GetCol(query)
        # showarray(selected_groups)
        return retarr
    
    """
     * is_conflicting_acl()
     *
     * Checks for conflicts when adding a specific ACL.
     *
     * @return bool Returns True if conflict is found.
     *
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Array of ACL IDs to ignore from the result set.
     *
    """
    def is_conflicting_acl(self, aco_array, aro_array, aro_group_ids=None, axo_array=None, axo_group_ids=None, ignore_acl_ids=None) :
        # Check for potential conflicts. Ignore groups, as groups will almost always have "conflicting" ACLs.
        # Thats part of inheritance.

        if (not is_array(aco_array)) :
            self.debug_text('is_conflicting_acl(): Invalid ACO Array+ ')
            return False
        

        if (not is_array(aro_array)) :
            self.debug_text('is_conflicting_acl(): Invalid ARO Array+ ')
            return False
        

        query  = 'SELECT        a.id' + \
            'FROM        ' +  self._db_table_prefix + 'acl a ' + \
            'LEFT JOIN    ' +  self._db_table_prefix + 'aco_map ac ON ac.acl_id=a.id ' + \
            'LEFT JOIN    ' +  self._db_table_prefix + 'aro_map ar ON ar.acl_id=a.id ' + \
            'LEFT JOIN    ' +  self._db_table_prefix + 'axo_map ax ON ax.acl_id=a.id ' + \
            'LEFT JOIN    ' +  self._db_table_prefix + 'axo_groups_map axg ON axg.acl_id=a.id ' + \
            'LEFT JOIN    ' +  self._db_table_prefix + 'axo_groups xg ON xg.id=axg.group_id '
        
        # ACO
        for aco_section_value, aco_value_array in aco_array:
            self.debug_text("is_conflicting_acl(): ACO Section Value: aco_section_value ACO VALUE: aco_value_array")
            # showarray(aco_array)
            if (not is_array(aco_value_array)) :
                self.debug_text('is_conflicting_acl(): Invalid Format for ACO Array item. Skipping...')
                continue
                #  return True
            
            # Move the below line in to the LEFT JOIN above for PostgreSQL sake.
            # 'ac1' => 'ac.acl_id=a.id',
            where_query = {
                'ac2': '(ac.section_value=' +  self.db.quote(aco_section_value) + ' AND ac.value IN (\'' +  implode('\',\'', aco_value_array) + '\'))'
            }

            # ARO
            for aro_section_value, aro_value_array in aro_array:
                self.debug_text("is_conflicting_acl(): ARO Section Value: aro_section_value ARO VALUE: aro_value_array")
                if (not is_array(aro_value_array)):
                    self.debug_text('is_conflicting_acl(): Invalid Format for ARO Array item. Skipping...')
                    continue
                    #  return True
                
                self.debug_text("is_conflicting_acl(): Search: ACO Section: aco_section_value ACO Value: aco_value_array ARO Section: aro_section_value ARO Value: aro_value_array")
                # Move the below line in to the LEFT JOIN above for PostgreSQL sake.
                # where_query['ar1'] = 'ar.acl_id=a.id'
                where_query['ar2'] = '(ar.section_value=' +  self.db.quote(aro_section_value) + ' AND ar.value IN (\'' +  implode ('\',\'', aro_value_array) + '\'))'
                
                if (is_array(axo_array) and count(axo_array) > 0) :
                    for axo_section_value, axo_value_array in axo_array:
                        self.debug_text("is_conflicting_acl(): AXO Section Value: axo_section_value AXO VALUE: axo_value_array")
                        if (not is_array(axo_value_array)) :
                            self.debug_text('is_conflicting_acl(): Invalid Format for AXO Array item. Skipping...')
                            continue
                            #  return True
                        
                        self.debug_text("is_conflicting_acl(): Search: ACO Section: aco_section_value ACO Value: aco_value_array ARO Section: aro_section_value ARO Value: aro_value_array AXO Section: axo_section_value AXO Value: axo_value_array")
                        
                        # where_query['ax1'] = 'ax.acl_id=x.id'
                        where_query['ax1'] = 'ax.acl_id=a.id'
                        where_query['ax2'] = '(ax.section_value=' +  self.db.quote(axo_section_value) + ' AND ax.value IN (\'' +  '\',\''.join(axo_value_array) + '\'))'
                        
                        where  = 'WHERE ' + ' AND '.join(where_query)
                        
                        conflict_result = self.db.GetCol(query + where)
                        
                        if is_list(conflict_result) and conflict_result:
                            #  showarray(conflict_result)

                            if is_list(ignore_acl_ids):
                                conflict_result = array_diff(conflict_result, ignore_acl_ids)
                            

                            if len(conflict_result) > 0:
                                conflicting_acls_str = ','.join(conflict_result)
                                self.debug_text("is_conflicting_acl(): Conflict FOUND!!! ACL_IDS: (conflicting_acls_str)")
                                return True
                            
                        
                    
                else:
                    where_query['ax1'] = '(ax.section_value IS None AND ax.value IS None)'
                    where_query['ax2'] = 'xg.name IS None'

                    where  = 'WHERE ' . implode(' AND ', where_query)

                    conflict_result = self.db.GetCol(query . where)

                    if is_list(conflict_result) and conflict_result:
                        
                        if is_list(ignore_acl_ids):
                            conflict_result = set(conflict_result).difference(set(ignore_acl_ids))
                        

                        if (len(conflict_result) > 0) :
                            conflicting_acls_str = ','.join(conflict_result)
                            self.debug_text("is_conflicting_acl(): Conflict FOUND!!! ACL_IDS: (conflicting_acls_str)")
                            return True
                        
                    
                
            
        

        self.debug_text('is_conflicting_acl(): No conflicting ACL found.')
        return False
    

    """
     * add_acl()
     *
     * Add's an ACL. ACO_IDS, ARO_IDS, GROUP_IDS must all be arrays.
     *
     * @return bool Return ACL ID of new ACL if successful, False otherewise.
     *
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param int Allow flag
     * @param int Enabled flag
     * @param string Return Value
     * @param string Note
     * @param string ACL Section Value
     * @param int ACL ID # Specific Request

    """
    def add_acl(self, aco_array, aro_array, aro_group_ids=None, axo_array=None, axo_group_ids=None, allow=1, enabled=1, return_value=None, note=None, section_value=None, acl_id=False ) :

        self.debug_text("add_acl():")

        if (len(aco_array) == 0) :
            self.debug_text("Must select at least one Access Control Object")
            return False
        

        if (len(aro_array) == 0 and len(aro_group_ids) == 0) :
            self.debug_text("Must select at least one Access Request Object or Group")
            return False
        

        if (not allow) :
            allow=0
        

        if (not enabled) :
            enabled=0
        

        if section_value and not self.get_object_section_section_id(None, section_value, 'ACL'):
            self.debug_text("add_acl(): Section Value: section_value DOES NOT exist in the database.")
            return False
        
        # Unique the group arrays. Later one we unique ACO/ARO/AXO arrays.
        if is_list(aro_group_ids):
            aro_group_ids = array_unique(aro_group_ids)
        
        if is_list(axo_group_ids):
            axo_group_ids = array_unique(axo_group_ids)
        
        # Check for conflicting ACLs.
        if (self.is_conflicting_acl(aco_array,aro_array,aro_group_ids,axo_array,axo_group_ids,array(acl_id))) :
            self.debug_text("add_acl(): Detected possible ACL conflict, not adding ACL!")
            return False
        
        # Edit ACL if acl_id is set. This is simply if we're being called by edit_acl().
        if (self.get_acl(acl_id) == False):
            if not section_value:
                section_value='system'
                if not self.get_object_section_section_id(None, section_value, 'ACL'):
                    #  Use the acl section with the lowest order value.
                    acl_sections_table = self._db_table_prefix + 'acl_sections'
                    acl_section_order_value = self.db.GetOne("SELECT min(order_value) from acl_sections_table")

                    query = 'SELECT value ' + \
                        'FROM acl_sections_table ' + \
                        'WHERE order_value = acl_section_order_value ' 
                    
                    section_value = self.db.GetOne(query)

                    if not section_value:
                        self.debug_text("add_acl(): No valid acl section found.")
                        return False
                    else:
                        self.debug_text("add_acl(): Using default section value: section_value.")
                    
                
            
            # ACL not specified, so create acl_id
            if not acl_id:
                # Create ACL row first, so we have the acl_id
                acl_id = self.db.GenID(self._db_table_prefix+ 'acl_seq',10)

                # Double check the ACL ID was generated.
                if not acl_id:
                    self.debug_text("add_acl(): ACL_ID generation failed!")
                    return False
                
            

            # Begin transaction _after_ GenID. Because on the first run, if GenID has to create the sequence,
            # the transaction will fail.
            self.db.BeginTrans()

            query = 'INSERT INTO ' + self._db_table_prefix+ 'acl (id,section_value,allow,enabled,return_value,note,updated_date) VALUES(' +  acl_id + ',' +  self.db.quote(section_value) + ',' +  allow + ',' +  enabled + ',' +  self.db.quote(return_value) + ', ' +  self.db.quote(note) + ',' +  time() + ')'
            result = self.db.Execute(query)
        else:
            section_sql = ''
            if section_value:
                section_sql = 'section_value=' +  self.db.quote (section_value) + ','
            

            self.db.BeginTrans()

            # Update ACL row, and remove all mappings so they can be re-inserted.
            query  = 'UPDATE    ' +  self._db_table_prefix + 'acl ' + \
                        ' SET             ' + section_sql + \
                        ' allow=' +  allow + ', ' + \
                        ' enabled=' +  enabled + ', ' + \
                        ' return_value=' +  self.db.quote(return_value) + ', ' + \
                        ' note=' +  self.db.quote(note) + ', ' + \
                        ' updated_date=' +  time() + ' WHERE    id=' +  acl_id
            
            result = self.db.Execute(query)

            if (result) :
                self.debug_text("Update completed without error, delete mappings...")
                # Delete all mappings so they can be re-inserted.
                for xmap in ('aco_map', 'aro_map', 'axo_map', 'aro_groups_map', 'axo_groups_map'):
                    query = 'DELETE FROM ' +  self._db_table_prefix + xmap + ' WHERE acl_id=' +  acl_id
                    rs = self.db.Execute(query)
                    if (not is_object(rs)):
                        self.debug_db('add_acl')
                        self.db.RollBackTrans()
                        return False
        
        if not is_object(result):
            self.debug_db('add_acl')
            self.db.RollBackTrans()
            return False
        
        self.debug_text("Insert or Update completed without error, insert new mappings.")
        #  Insert ACO/ARO/AXO mappings
        for map_base, map_array in (('aco',aco_array), ('aro',aro_array), ('axo',axo_array)):
            
            if not is_list(map_array):
                continue
            
            for section_value, value_array in map_array:
                self.debug_text('Insert: ' + map_base.upper()  + ' Section Value: ' + section_value +' '+ map_base.upper() +' VALUE: '+ value_array)
                
                if not is_list(value_array):
                    self.debug_text ('add_acl (): Invalid Format for ' + map_base.upper() + ' Array item. Skipping...')
                    continue
                
                value_array = set(value_array)
                
                for value in value_array:
                    object_id = self.get_object_id(section_value, value, map_base)

                    if not object_id:
                        self.debug_text('add_acl(): ' + map_base.upper() + " Object Section Value: section_value Value: value DOES NOT exist in the database. Skipping...")
                        self.db.RollBackTrans()
                        return False
                    
                    query  = 'INSERT INTO ' + self._db_table_prefix + map_base + '_map (acl_id,section_value,value) VALUES (' + acl_id + ', ' + self.db.quote(section_value) + ', ' + self.db.quote(value)  + ')'
                    rs = self.db.Execute(query)

                    if not rs:
                        self.debug_db('add_acl')
                        self.db.RollBackTrans()
                        return False
        
        #  Insert ARO/AXO GROUP mappings
        for map_base, map_group_ids in (('aro', aro_group_ids0), ('axo',axo_group_ids)):
            
            if not is_list(map_group_ids):
                continue
            
            for group_id in map_group_ids:
                self.debug_text ('Insert: ' +  strtoupper(map) + ' GROUP ID: ' +  group_id)
                
                group_data = self.get_group_data(group_id, map)
                
                if not group_data:
                    self.debug_text('add_acl(): ' + map_base.upper() + " Group: group_id DOES NOT exist in the database. Skipping...")
                    self.db.RollBackTrans()
                    return False
                

                query  = 'INSERT INTO ' + self._db_table_prefix + map_base + '_groups_map (acl_id,group_id) VALUES (' + acl_id  + ', ' + group_id + ')'
                rs = self.db.Execute(query)
                
                # maybe None
                if not rs:
                    self.debug_db('add_acl')
                    self.db.RollBackTrans()
                    return False
        
        self.db.CommitTrans()
        
        if (self._caching == True and self._force_cache_expire == True):
            # Expire all cache.
            self.Cache_Lite.clean('default')
        
        # Return only the ID in the first row.
        return acl_id
    
    """
     * edit_acl()
     *
     * Edit's an ACL, ACO_IDS, ARO_IDS, GROUP_IDS must all be arrays.
     *
     * @return bool Return True if successful, False otherewise.
     *
     * @param int ACL ID # to edit
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     * @param array Array of Group IDs
     * @param int Allow flag
     * @param int Enabled flag
     * @param string Return Value
     * @param string Note
     * @param string ACL Section Value
    """
    def edit_acl(self, acl_id, aco_array, aro_array, aro_group_ids=None, axo_array=None, axo_group_ids=None, allow=1, enabled=1, return_value=None, note=None, section_value=None):
        
        self.debug_text("edit_acl():")
        
        if not acl_id:
            self.debug_text("edit_acl(): Must specify a single ACL_ID to edit")
            return False
        
        if len(aco_array) == 0:
            self.debug_text("edit_acl(): Must select at least one Access Control Object")
            return False
        
        if len(aro_array) == 0 and len(aro_group_ids) == 0:
            self.debug_text("edit_acl(): Must select at least one Access Request Object or Group")
            return False
        
        if not allow:
            allow=0
        
        if not enabled:
            enabled=0
        
        # if (self.add_acl(aco_array, aro_array, group_ids, allow, enabled, acl_id)) :
        if (self.add_acl(aco_array, aro_array, aro_group_ids, axo_array, axo_group_ids, allow, enabled, return_value, note, section_value, acl_id)) :
            return True
        else:
            self.debug_text("edit_acl(): error in add_acl()")
            return False
        
    
    """
     * del_acl()
     *
     * Deletes a given ACL
     *
     * @return bool Returns True if successful, False otherwise.
     *
     * @param int ACL ID # to delete
    """
    def del_acl(self, acl_id):

        self.debug_text("del_acl(): ID: acl_id")

        if not acl_id:
            self.debug_text("del_acl(): ACL_ID (acl_id) is empty, this is required")
            return False
        
        self.db.BeginTrans()

        #  Delete all mappings to the ACL first
        for map_base in ('aco_map', 'aro_map', 'axo_map', 'aro_groups_map', 'axo_groups_map'):
            query  = 'DELETE FROM ' + self._db_table_prefix + map_base + ' WHERE acl_id=' + acl_id
            rs = self.db.Execute(query)

            if not rs:
                self.debug_db('del_acl')
                self.db.RollBackTrans()
                return False
        
        #  Delete the ACL
        query  = 'DELETE FROM ' + self._db_table_prefix + 'acl WHERE id=' + acl_id
        self.debug_text('delete query: ' + query)
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('del_acl')
            self.db.RollBackTrans()
            return False
        
        self.debug_text("del_acl(): deleted ACL ID: acl_id")
        self.db.CommitTrans()
        
        if (self._caching == True and self._force_cache_expire == True) :
            # Expire all cache.
            self.Cache_Lite.clean('default')
        
        return True
    
    """
     *
     * Groups
     *
    """

    """
     * sort_groups()
     *
     * Grabs all the groups from the database doing preliminary grouping by parent
     *
     * @return array Returns 2-Dimensional array: array[<parent_id>][<group_id>] = <group_name>
     *
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def sort_groups(self, group_type='ARO'):
        if group_type.strip() == 'axo':
            table = self._db_table_prefix + 'axo_groups'
        else:
            table = self._db_table_prefix + 'aro_groups'
        
        # Grab all groups from the database.
        query  = 'SELECT id, parent_id, name FROM ' + table + ' ORDER BY parent_id, name'
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('sort_groups')
            return False
        
        # Save groups in an array sorted by parent. Should be make it easier for later on.
        sorted_groups = list()
        row = rs.FetchRow()
        while row:
            id = row[0]
            parent_id = row[1]
            name = row[2]
            sorted_groups[parent_id][id] = name
            row = rs.FetchRow()
        
        return sorted_groups
    
    """
     * format_groups()
     *
     * Takes the array returned by sort_groups() and formats for human
     * consumption. Recursively calls itself to produce the desired output.
     *
     * @return array Array of formatted text, ordered by group id, formatted according to type
     *
     * @param array Output from gacl_api.sorted_groups(group_type)
     * @param array Output type desired, either 'TEXT', 'HTML', or 'ARRAY'
     * @param int Root of tree to produce
     * @param int Current level of depth
     * @param array Pass the current formatted groups object for appending via recursion.
    """
    def format_groups(self, sorted_groups, dtype='TEXT', root_id=0, level=0, formatted_groups=None):
        if not is_list(sorted_groups):
            return False
        
        if not is_list(formatted_groups):
            formatted_groups = array ()
        
        if sorted_groups[root_id]:
            keys = sorted_groups[root_id].keys()
            last_id = keys[-1] # RCH may not be sorted
            keys = None
            
            # RCH this needs serious work
            for id, name in sorted_groups[root_id].iteritems():
                if dtype.upper() == 'TEXT':                
                    # Formatting optimized for TEXT (combo box) output.
                    if level.isdigit():
                        level = '&nbsp;&nbsp; '*level
                        if len(level) >= 8:
                            if id == last_id:
                                spacing = level[0:len(level)-8] + '\'- '
                                level = level[0:len(level)-8] + '&nbsp;&nbsp; '
                            else:
                                spacing = level[0:len(level)-8] + '|- '
                        else:
                            spacing = level
                        
                        next = level + '|&nbsp; '
                        text = spacing + name
                elif dtype.upper() == 'HTML':
                    # Formatting optimized for HTML (tables) output.
                    width= level * 20
                    spacing = "<img src=\"s.gif\" width=\"width\">"
                    next = level + 1
                    text = spacing + " " + name
                elif dtype.upper() == 'ARRAY':
                    next = level
                    text = name
                else:
                    return False
                
                formatted_groups[id] = text
                # Recurse if we can.
                
                if sorted_groups[id]:
                    formatted_groups = self.format_groups(sorted_groups, type, id, next, formatted_groups)
                else:
                    # self.debug_text("format_groups(): Found last branch!")
                    pass
        
        return formatted_groups
    
    """
     * get_group_id()
     *
     * Gets the group_id given the name or value.
     *
     * Will only return one group id, so if there are duplicate names, it will return False.
     *
     * @return int Returns Group ID if found and Group ID is unique in database, otherwise, returns False
     *
     * @param string Group Value
     * @param string Group Name
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def get_group_id(self, value = None, name = None, group_type = 'ARO') :

        self.debug_text("get_group_id(): Value: value, Name: name, Type: group_type" )

        if group_type.strip().lower() == 'axo':
            table = self._db_table_prefix + 'axo_groups'
        else:
            table = self._db_table_prefix + 'aro_groups'
        name = name.strip()
        value = value.strip()
        
        if not name and not value:
            self.debug_text("get_group_id(): name and value, at least one is required")
            return False
        
        query = 'SELECT id FROM ' + table + ' WHERE '
        if value:
            query += ' value=' + self.db.quote(value)
        else:
            query += ' name=' + self.db.quote(name)
        
        rs = self.db.Execute(query)

        if not rs:
            self.debug_db('get_group_id')
            return False
        
        row_count = rs.RecordCount()
        
        if (row_count > 1) :
            self.debug_text("get_group_id(): Returned row_count rows, can only return one. Please make your names unique.")
            return False
        
        if (row_count == 0) :
            self.debug_text("get_group_id(): Returned row_count rows")
            return False
        
        row = rs.FetchRow()
        
        # Return the ID.
        return row[0]
    
    """
     * get_group_children()
     *
     * Gets a groups child IDs
     *
     * @return array Array of Child ID's of the referenced group
     *
     * @param int Group ID #
     * @param int Group Type, either 'ARO' or 'AXO'
     * @param string Either 'RECURSE' or 'NO_RECURSE', to recurse while fetching group children.
    """
    def get_group_children(self, group_id, group_type = 'ARO', recurse = 'NO_RECURSE') :
        self.debug_text("get_group_children(): Group_ID: group_id Group Type: group_type Recurse: recurse")

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix  + 'axo_groups'    
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
        
        if not group_id:
            self.debug_text("get_group_children(): ID (group_id) is empty, this is required")
            return False
        
        query  = 'SELECT        g1.id ' + \
                 'FROM        ' + table + ' g1'
        
        # FIXME-mikeb: Why is group_id in quotes?
        if recurse.upper() == 'RECURSE':
            query += 'LEFT JOIN     ' + table + ' g2 ON g2.lft<g1.lft AND g2.rgt>g1.rgt ' + \
                     'WHERE        g2.id=' + group_id
        else:
            query += 'WHERE        g1.parent_id=' + group_id
        
        query += 'ORDER BY    g1.value'
        
        return self.db.GetCol(query)
    
    """
     * get_group_data()
     *
     * Gets the group data given the GROUP_ID.
     *
     * @return array Returns numerically indexed array with the following columns:
     *    - array[0] = (int) Group ID #
     *    - array[1] = (int) Parent Group ID #
     *    - array[2] = (string) Group Value
     *    - array[3] = (string) Group Name
     *    - array[4] = (int) lft MPTT Value
     *    - array[5] = (int) rgt MPTT Value
     *
     * @param int Group ID #
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def get_group_data(self, group_id, group_type = 'ARO') :

        self.debug_text("get_group_data(): Group_ID: group_id Group Type: group_type")

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'axo_groups'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
        
        if not group_id:
            self.debug_text("get_group_data(): ID (group_id) is empty, this is required")
            return False
        
        query  = 'SELECT id, parent_id, value, name, lft, rgt FROM ' + table  + ' WHERE id=' + group_id
        row = self.db.GetRow(query)
        
        if row:
            return row
        else:
            self.debug_text("get_object_data(): Group does not exist.")
            return False
    
    """
     * get_group_parent_id()
     *
     * Grabs the parent_id of a given group
     *
     * @return int Parent ID of the Group
     *
     * @param int Group ID #
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def get_group_parent_id(self, id, group_type='ARO'):
        self.debug_text("get_group_parent_id(): ID: id Group Type: group_type")
        if group_type.strip().lower() == 'axo':
            table = self._db_table_prefix + 'axo_groups'    
        else:
          table = self._db_table_prefix + 'aro_groups'
        
        if not id:
            self.debug_text("get_group_parent_id(): ID (id) is empty, this is required")
            return False
        
        query = 'SELECT parent_id FROM ' + table + ' WHERE id=' + id
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('get_group_parent_id')
            return False
        
        row_count = rs.RecordCount()
        
        if (row_count > 1):
            self.debug_text("get_group_parent_id(): Returned row_count rows, can only return one. Please make your names unique.")
            return False
        
        if (row_count == 0):
            self.debug_text("get_group_parent_id(): Returned row_count rows")
            return False
        
        row = rs.FetchRow()
        
        # Return the ID.
        return row[0]
    
    """
     * get_root_group_id ()
     *
     * Grabs the id of the root group for the specified tree
     *
     * @return int Root Group ID #
     *
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def get_root_group_id(self, group_type='ARO') :
        self.debug_text('get_root_group_id(): Group Type: ' +  group_type)
        if group_type.lower() == 'axo':
            table = self._db_table_prefix + 'axo_groups'
        elif group_type.lower() == 'aro':
            table = self._db_table_prefix + 'aro_groups'
        else:
            self.debug_text('get_root_group_id(): Invalid Group Type: ' +  group_type)
            return False
        query = 'SELECT id FROM ' + table + ' WHERE parent_id=0'
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('get_root_group_id')
            return False
        
        row_count = rs.RecordCount()
        
        if row_count == 1:
            row = rs.FetchRow()
            #  Return the ID.
            return row[0]
        elif row_count == 0:
            self.debug_text('get_root_group_id(): Returned 0 rows, you do not have a root group defined yet.')
            return False
        
        self.debug_text('get_root_group_id(): Returned ' +  row_count + ' rows, can only return one. Your tree is very broken.')
        return False
    
    """
     * add_group()
     *
     * Inserts a group, defaults to be on the "root" branch.
     *
     * Since v3.3.x you can only create one group with Parent_ID=0
     * So, its a good idea to create a "Virtual Root" group with Parent_ID=0
     * Then assign other groups to that.
     *
     * @return int New Group ID # if successful, False if otherwise.
     *
     * @param string Group Value
     * @param string Group Name
     * @param int Parent Group ID #
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def add_group(self, value, name, parent_id=0, group_type='aro'):
        assert group_type in ['aro','axo']
        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'axo_groups'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
        
        self.debug_text("add_group(): Name: name Value: value Parent ID: parent_id Group Type: group_type")
        name = name.strip()
        value = value.strip()
        if name == '':
            raise Exception("add_group(): name (name) OR parent id (parent_id) is empty, this is required")
        
        groups = getattr(gacl_groups, table)
        
        self.db.begin()
        
        #  special case for root group
        if parent_id == 0:
            #  check a root group is not already defined
            query = 'SELECT id FROM ' + table + ' WHERE parent_id=0'
            rs = self.db.Execute(query)
            if not rs:
                self.debug_db('add_group')
                self.db.RollBackTrans()
                return False
            
            if rs.RowCount() > 0:
                self.debug_text('add_group (): A root group already exists.')
                self.db.RollBackTrans()
                return False
            
            parent_lft = 0
            parent_rgt = 1
        else:
            if not parent_id:
                self.debug_text("add_group (): parent id (parent_id) is empty, this is required")
                self.db.RollbackTrans()
                return False
            
            #  grab parent details from database
            query = 'SELECT id, lft, rgt FROM ' + table + ' WHERE id=' + parent_id
            row = self.db.GetRow(query)
            
            if not is_list(row):
                self.debug_db('add_group')
                self.db.RollBackTrans()
                return False
            
            if not row:
                self.debug_text('add_group (): Parent ID: ' +  parent_id + ' not found.')
                self.db.RollBackTrans()
                return False
            
            parent_lft = row[1]
            parent_rgt = row[2]
            
            #  make room for the new group
            query  = 'UPDATE ' + table + ' SET rgt=rgt+2 WHERE rgt>=' + parent_rgt
            rs = self.db.Execute(query)
            if not rs:
                self.debug_db('add_group')
                self.db.RollBackTrans()
                return False
            

            query  = 'UPDATE ' +  table + ' SET lft=lft+2 WHERE lft>' +  parent_rgt
            rs = self.db.Execute(query)

            if (not is_object(rs)) :
                self.debug_db('add_group')
                self.db.RollBackTrans()
                return False
            
        

        query = 'INSERT INTO ' +  table + ' (id,parent_id,name,value,lft,rgt) VALUES (' +  insert_id + ',' +  parent_id + ',' +  self.db.quote(name) + ',' +  self.db.quote(value) + ',' +  parent_rgt + ',' +  (parent_rgt + 1) + ')'
        rs = self.db.Execute(query)

        if (not is_object(rs)) :
            self.debug_db('add_group')
            self.db.RollBackTrans()
            return False
        

        self.db.CommitTrans()

        self.debug_text('add_group (): Added group as ID: ' +  insert_id)
        return insert_id
    

    """
     * get_group_objects()
     *
     * Gets all objects assigned to a group.
     *
     * If option == 'RECURSE' it will get all objects in child groups as well.
     * defaults to omit child groups.
     *
     * @return array Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]

     *
     * @param int Group ID #
     * @param string Group Type, either 'ARO' or 'AXO'
     * @param string Option, either 'RECURSE' or 'NO_RECURSE'
    """
    def get_group_objects(self, group_id, group_type='ARO', option='NO_RECURSE') :

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            object_table = self._db_table_prefix + 'axo'
            group_table = self._db_table_prefix + 'axo_groups'
            map_table = self._db_table_prefix + 'groups_axo_map'    
        else:
            group_type = 'aro'
            object_table = self._db_table_prefix + 'aro'
            group_table = self._db_table_prefix + 'aro_groups'
            map_table = self._db_table_prefix + 'groups_aro_map'
            
        self.debug_text("get_group_objects(): Group ID: group_id")

        if (empty(group_id)) :
            self.debug_text("get_group_objects(): Group ID:  (group_id) is empty, this is required")
            return False
        
        query  = 'SELECT        o.section_value,o.value'
        if (option == 'RECURSE') :
            query += '' + \
                ' FROM        ' +  group_table + ' g2 ' + \
                ' JOIN        ' +  group_table + ' g1 ON g1.lft>=g2.lft AND g1.rgt<=g2.rgt ' + \
                ' JOIN        ' +  map_table + ' gm ON gm.group_id=g1.id ' + \
                ' JOIN        ' +  object_table + ' o ON o.id=gm+ ' +  group_type + '_id ' + \
                ' WHERE        g2.id=' +  group_id
        else:
            query += '' + \
                ' FROM        ' +  map_table + ' gm ' + \
                ' JOIN        ' +  object_table + ' o ON o.id=gm+ ' +  group_type + '_id ' + \
                ' WHERE        gm.group_id=' +  group_id
        
        rs = self.db.Execute(query)

        if (not is_object(rs)) :
            self.debug_db('get_group_objects')
            return False
        
        self.debug_text("get_group_objects(): Got group objects, formatting array.")
        
        retarr = list()
        
        # format return array.
        row = rs.FetchRow()
        while row:
            section = row[0]
            value = row[1]
            retarr[section].append(value)
            row = rs.FetchRow()
        return retarr
    
    """
     * add_group_object()
     *
     * Assigns an Object to a group
     *
     * @return bool Returns True if successful, False otherwise.
     *
     * @param int Group ID #
     * @param string Object Section Value
     * @param string Object Value
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def add_group_object(self, group_id, object_section_value, object_value, group_type='ARO'):
        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'groups_axo_map'
            object_table = self._db_table_prefix + 'axo'
            group_table = self._db_table_prefix + 'axo_groups'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'groups_aro_map'
            object_table = self._db_table_prefix + 'aro'
            group_table = self._db_table_prefix + 'aro_groups'
        
        self.debug_text("add_group_object(): Group ID: group_id Section Value: object_section_value Value: object_value Group Type: group_type")
        object_section_value = object_section_value.strip()
        object_value = object_value.strip()

        if (empty(group_id) or empty(object_value) or empty(object_section_value)) :
            self.debug_text("add_group_object(): Group ID: (group_id) OR Value (object_value) OR Section value (object_section_value) is empty, this is required")
            return False
        
        #  test to see if object & group exist and if object is already a member
        query  = '' + \
                ' SELECT        o.id AS id,g.id AS group_id,gm.group_id AS member ' + \
                ' FROM        ' +  object_table + ' o ' + \
                ' LEFT JOIN    ' +  group_table + ' g ON g.id=' +  group_id + \
                ' LEFT JOIN    ' +  table + ' gm ON (gm+ ' +  group_type + '_id=o.id AND gm.group_id=g.id) ' + \
                ' WHERE        (o.section_value=' +  self.db.quote(object_section_value) + ' AND o.value=' +  self.db.quote(object_value) + ')'
        rs = self.db.Execute(query)
        
        if (not is_object(rs)) :
            self.debug_db('add_group_object')
            return False
        
        if (rs.RecordCount() != 1) :
            self.debug_text('add_group_object(): Value (' +  object_value + ') OR Section value (' +  object_section_value + ') is invalid. Does this object exist?')
            return False
        
        row = rs.FetchRow()
        
        if (row[1] != group_id) :
            self.debug_text('add_group_object(): Group ID (' +  group_id + ') is invalid. Does this group exist?')
            return False
        
        # Group_ID == Member
        if (row[1] == row[2]) :
            self.debug_text('add_group_object(): Object: (' +  object_section_value + ' . ' +  object_value + ') is already a member of Group: (' +  group_id + ')')
            # Object is already assigned to group. Return True.
            return True
        
        object_id = row[0]

        query = 'INSERT INTO ' +  table + ' (group_id,' +  group_type + '_id) VALUES (' +  group_id + ',' +  object_id + ')'
        rs = self.db.Execute(query)

        if (not is_object(rs)) :
            self.debug_db('add_group_object')
            return False
        

        self.debug_text('add_group_object(): Added Object: ' +  object_id + ' to Group ID: ' +  group_id)

        if (self._caching == True and self._force_cache_expire == True) :
            # Expire all cache.
            self.Cache_Lite.clean('default')
        

        return True
    

    """
     * del_group_object()
     *
     * Removes an Object from a group.
     *
     * @return bool Returns True if successful, False otherwise
     *
     * @param int Group ID #
     * @param string Object Section Value
     * @param string Object Value
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def del_group_object(self, group_id, object_section_value, object_value, group_type='ARO') :

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'groups_axo_map'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'groups_aro_map'
        
        self.debug_text("del_group_object(): Group ID: group_id Section value: object_section_value Value: object_value")
        
        object_section_value = trim(object_section_value)
        object_value = trim(object_value)
        
        if (empty(group_id) or empty(object_value) or empty(object_section_value)):
            self.debug_text("del_group_object(): Group ID:  (group_id) OR Section value: object_section_value OR Value (object_value) is empty, this is required")
            return False
        
        object_id = self.get_object_id(object_section_value, object_value, group_type)
        if not object_id:
            self.debug_text ("del_group_object (): Group ID (group_id) OR Value (object_value) OR Section value (object_section_value) is invalid. Does this object exist?")
            return False
        
        query = 'DELETE FROM ' +  table + ' WHERE group_id=' +  group_id + ' AND ' +  group_type + '_id=' +  object_id
        rs = self.db.Execute(query)
        
        if (not is_object(rs)) :
            self.debug_db('del_group_object')
            return False
        
        self.debug_text("del_group_object(): Deleted Value: object_value to Group ID: group_id assignment")
        
        if (self._caching == True and self._force_cache_expire == True) :
            # Expire all cache.
            self.Cache_Lite.clean('default')
        
        return True
    
    """
     * edit_group()
     *
     * Edits a group
     *
     * @returns bool Returns True if successful, False otherwise
     *
     * @param int Group ID #
     * @param string Group Value
     * @param string Group Name
     * @param int Parent ID #
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def edit_group(self, group_id, value=None, name=None, parent_id=None, group_type='ARO') :
        self.debug_text("edit_group(): ID: group_id Name: name Value: value Parent ID: parent_id Group Type: group_type")

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'axo_groups'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
        
        if not group_id:
            self.debug_text('edit_group(): Group ID (' +  group_id + ') is empty, this is required')
            return False
        
        curr = self.get_group_data(group_id, group_type)
        if not is_list(curr):
            self.debug_text('edit_group(): Invalid Group ID: ' +  group_id)
            return False
        name = name.strip()
        #  don't set name if it is unchanged
        if (name == curr[3]):
            unset(name)
        
        #  don't set parent_id if it is unchanged
        if (parent_id == curr[1]):
            unset(parent_id)
        
        if isset(parent_id):
            if (group_id == parent_id):
                self.debug_text('edit_group(): Groups can\'t be a parent to themselves. Incest is bad. ;)')
                return False
            
            # Make sure we don't re-parent to our own children.
            # Grab all children of this group_id.
            children_ids = self.get_group_children(group_id, group_type, 'RECURSE')
            if isinstance(children_ids, collections.Iterable):
                if parent_id in children_ids:
                    self.debug_text('edit_group(): Groups can\'t be re-parented to their own children, this would be incestuous!')
                    return False
            children_ids = None
            
            #  make sure parent exists
            if not self.get_group_data(parent_id, group_type):
                self.debug_text('edit_group(): Parent Group (' +  parent_id + ') doesn\'t exist')
                return False
        
        xset = list()

        #  update name if it is specified.
        if name:
            xset.append('name=' + self.db.quote(name))
        

        #  update parent_id if it is specified.
        if parent_id:
            xset.append('parent_id=' + parent_id)
        

        #  update value if it is specified.
        if value:
            xset.append('value=' + self.db.quote(value))
        

        if not xset:
            self.debug_text('edit_group(): Nothing to update+ ')
            return False
        

        self.db.BeginTrans()

        query  = 'UPDATE ' + table + ' SET ' +  implode(',', set) + ' WHERE id=' + group_id
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('edit_group')
            self.db.RollbackTrans()
            return False
        
        self.debug_text('edit_group(): Modified group ID: ' + group_id)
        
        #  rebuild group tree if parent_id has changed
        if not parent_id:
            if not self._rebuild_tree(table, self.get_root_group_id(group_type)):
                self.db.RollbackTrans()
                return False
        
        self.db.CommitTrans()
        
        if (self._caching == True and self._force_cache_expire == True) :
            #  Expire all cache.
            self.Cache_Lite.clean('default')
        return True
    
    """
     * rebuild_tree ()
     *
     * rebuilds the group tree for the given type
     *
     * @return bool Returns True if successful, False otherwise
     *
     * @param string Group Type, either 'ARO' or 'AXO'
     * @param int Group ID #
     * @param int Left value of Group
    """
    def rebuild_tree(self, group_type = 'ARO', group_id = None, left = 1) :
        self.debug_text("rebuild_tree(): Group Type: group_type Group ID: group_id Left: left")

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'axo_groups'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
        
        if not group_id:
            group_id = self.get_root_group_id(group_type)
            if group_id:
                left = 1
                self.debug_text('rebuild_tree(): No Group ID Specified, using Root Group ID: ' +  group_id)
            else:
                self.debug_text('rebuild_tree(): A Root group could not be found, are there any groups defined?')
                return False
        
        self.db.BeginTrans()
        rebuilt = self._rebuild_tree(table, group_id, left)
        
        if (rebuilt == False) :
            self.debug_text('rebuild_tree(): Error rebuilding tree!')
            self.db.RollBackTrans()
            return False
        
        self.db.CommitTrans()
        self.debug_text('rebuild_tree(): Tree rebuilt+ ')
        return True
    
    """
     * _rebuild_tree ()
     *
     * Utility recursive function called by rebuild_tree()
     *
     * @return int Returns right value of this node + 1
     *
     * @param string Table name of group type
     * @param int Group ID #
     * @param int Left value of Group
    """
    def _rebuild_tree(self, table, group_id, left = 1) :
        self.debug_text("_rebuild_tree(): Table: table Group ID: group_id Left: left")
        #  get all children of this node
        query = 'SELECT id FROM ' +  table + ' WHERE parent_id=' +  group_id
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('_rebuild_tree')
            return False

        #  the right value of this node is the left value + 1
        right = left + 1
        row = rs.FetchRow()
        while row:
            #  recursive execution of this function for each
            #  child of this node
            #  right is the current right value, which is
            #  incremented by the rebuild_tree function
            right = self._rebuild_tree(table, row[0], right)
            if (right == False) :
                return False
            row = rs.FetchRow()
        #  we've got the left value, and now that we've processed
        #  the children of this node we also know the right value
        query  = 'UPDATE ' + table + ' SET lft=' + left + ', rgt=' + right + ' WHERE id=' + group_id
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('_rebuild_tree')
            return False
        
        #  return the right value of this node + 1
        return right + 1
    
    """
     * del_group()
     *
     * deletes a given group
     *
     * @return bool Returns True if successful, False otherwise.
     *
     * @param int Group ID #
     * @param bool If True, child groups of this group will be reparented to the current group's parent.
     * @param string Group Type, either 'ARO' or 'AXO'
    """
    def del_group(self, group_id, reparent_children=True, group_type='ARO') :

        if group_type.strip().lower() == 'axo':
            group_type = 'axo'
            table = self._db_table_prefix + 'axo_groups'
            groups_map_table = self._db_table_prefix + 'axo_groups_map'
            groups_object_map_table = self._db_table_prefix + 'groups_axo_map'
        else:
            group_type = 'aro'
            table = self._db_table_prefix + 'aro_groups'
            groups_map_table = self._db_table_prefix + 'aro_groups_map'
            groups_object_map_table = self._db_table_prefix + 'groups_aro_map'
        
        self.debug_text("del_group(): ID: group_id Reparent Children: reparent_children Group Type: group_type")
        
        if not group_id:
            self.debug_text("del_group(): Group ID (group_id) is empty, this is required")
            return False
        
        #  Get details of this group
        query = 'SELECT id, parent_id, name, lft, rgt FROM ' + table + ' WHERE id=' + group_id
        group_details = self.db.GetRow(query)
        if not is_list(group_details):
            self.debug_db('del_group')
            return False
        
        parent_id = group_details[1]
        left = group_details[3]
        right = group_details[4]
        self.db.BeginTrans()
        #  grab list of all children
        children_ids = self.get_group_children(group_id, group_type, 'RECURSE')
        #  prevent deletion of root group & reparent of children if it has more than one immediate child
        if parent_id == 0:
            query = 'SELECT count(*) FROM ' + table + ' WHERE parent_id=' + group_id
            child_count = self.db.GetOne(query)
            if child_count > 1 and reparent_children:
                self.debug_text ('del_group (): You cannot delete the root group and reparent children, this would create multiple root groups.')
                self.db.RollbackTrans()
                return False
        
        success = False
        
        
        # Handle children here.
        try:
            if not is_list(children_ids) or len(children_ids) == 0:
                #  remove acl maps
                query = 'DELETE FROM ' + groups_map_table + ' WHERE group_id=' + group_id
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove group object maps
                query = 'DELETE FROM ' + groups_object_map_table + ' WHERE group_id=' + group_id
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove group
                query = 'DELETE FROM ' + table + ' WHERE id=' + group_id
                rs = self.db.Execute(query)
                
                if (not is_object(rs)) :
                    raise AnnoyingError("GOTO")
                
                #  move all groups right of deleted group left by width of deleted group
                query = 'UPDATE ' + table + ' SET lft=lft-' + (right-left+1) + ' WHERE lft>' + right
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                query = 'UPDATE ' + table + ' SET rgt=rgt-' + (right-left+1) + ' WHERE rgt>' + right
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                success = True
            
            elif reparent_children == True:
                #  remove acl maps
                query = 'DELETE FROM ' + groups_map_table + ' WHERE group_id=' + group_id
                rs = self.db.Execute(query)
    
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove group object maps
                query = 'DELETE FROM ' + groups_object_map_table + ' WHERE group_id=' + group_id
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove group
                query = 'DELETE FROM ' + table + ' WHERE id=' + group_id
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  set parent of immediate children to parent group
                query = 'UPDATE ' + table + ' SET parent_id=' + parent_id + ' WHERE parent_id=' + group_id
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  move all children left by 1
                query = 'UPDATE ' + table + ' SET lft=lft-1, rgt=rgt-1 WHERE lft>' + left + ' AND rgt<' + right
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  move all groups right of deleted group left by 2
                query = 'UPDATE ' + table + ' SET lft=lft-2 WHERE lft>' + right
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                query = 'UPDATE ' + table + ' SET rgt=rgt-2 WHERE rgt>' + right
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                success = True
                
            else:
                #  make list of group and all children
                group_ids = children_ids
                group_ids.append(group_id)
    
                #  remove acl maps
                query = 'DELETE FROM ' + groups_map_table + ' WHERE group_id IN (' + ','.join(group_ids) + ')'
                rs = self.db.Execute(query)
    
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove group object maps
                query = 'DELETE FROM ' + groups_object_map_table + ' WHERE group_id IN (' + ','.join(group_ids) + ')'
                rs = self.db.Execute(query)
                
                if not rs:
                    raise AnnoyingError("GOTO")
                
                #  remove groups
                query = 'DELETE FROM ' + table + ' WHERE id IN (' + ','.join(group_ids) + ')'
                rs = self.db.Execute(query)
    
                if not rs:
                    raise AnnoyingError("GOTO")
                
    
                #  move all groups right of deleted group left by width of deleted group
                query = 'UPDATE ' + table + ' SET lft=lft-' + (right - left + 1) + ' WHERE lft>' + right
                rs = self.db.Execute(query)
    
                if not rs:
                    raise AnnoyingError("GOTO")
                
                query = 'UPDATE ' + table + ' SET rgt=rgt-' + (right - left + 1) + ' WHERE rgt>' + right
                rs = self.db.Execute(query)
    
                if not rs:
                    raise AnnoyingError("GOTO")
                
                success = True
                
        except AnnoyingError: 
            pass
        
        #  if the delete failed, rollback the trans and return False
        if not success: # RCH is it success or not success?
            self.debug_db('del_group')
            self.db.RollBackTrans()
            return False
        
        self.debug_text("del_group(): deleted group ID: group_id")
        self.db.CommitTrans()
        if (self._caching == True and self._force_cache_expire == True) :
            # Expire all cache.
            self.Cache_Lite.clean('default')
        return True
    
    """
     *
     * Objects (ACO/ARO/AXO)
     *
    """

    """
     * get_object()
     *
     * Grabs all Objects's in the database, or specific to a section_value
     *
     * @return ADORecordSet  Returns recordset directly, with object ID only selected:
     *
     * @param string Filter to this section value
     * @param int Returns hidden objects if 1, leaves them out otherwise.
     * @param string Object Type, either 'ACO', 'ARO', 'AXO', or 'ACL'
    """
    def get_object(self, section_value = None, return_hidden=1, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix + 'axo'
        elif ot == 'acl':
            object_type = 'acl'
            table = self._db_table_prefix + 'acl'
        else:
            self.debug_text('get_object(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("get_object(): Section Value: section_value Object Type: object_type")

        query = 'SELECT id FROM ' + table

        where = list()

        if not section_value:
            where.append('section_value=' + self.db.quote(section_value))
        
        if return_hidden==0 and object_type != 'acl':
            where.append('hidden=0')
        
        if not where:
            query += ' WHERE ' + implode(' AND ', where)
        
        rs = self.db.GetCol(query)
        if not is_list(rs):
            self.debug_db('get_object')
            return False
        
        #  Return Object IDs
        return rs
    
    """
     * get_ungrouped_objects()
     *
     * Grabs ID's of all Objects (ARO's and AXO's only) in the database not assigned to a Group.
     *
     * This function is useful for applications that synchronize user databases with an outside source.
     * If syncrhonization doesn't automatically place users in an appropriate group, this function can
     * quickly identify them so that they can be assigned to the correct group.
     *
     * @return array Returns an array of object ID's
     *
     * @param int Returns hidden objects if 1, does not if 0.
     * @param string Object Type, either 'ARO' or 'AXO' (groupable types)
    """
    def get_ungrouped_objects(self, return_hidden=1, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        if ot == 'axo':
           object_type = 'axo'
           table = self._db_table_prefix  + 'axo'
        else:
            self.debug_text('get_ungrouped_objects(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("get_ungrouped_objects(): Object Type: object_type")
        
        query = 'SELECT id FROM ' + table + ' a ' + \
                ' LEFT JOIN ' + self._db_table_prefix + 'groups_' + object_type+ '_map b ON a.id = b+ ' + object_type + '_id'
        where = list()
        where.append('b.group_id IS None')
    
        if (return_hidden==0) :
            where.append('a.hidden=0')
        
        if where:
            query += ' WHERE ' + ' AND '.join(where)
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('get_ungrouped_objects')
            return False

        while (not rs.EOF):
            retarr.append(rs.fields[0])
            rs.MoveNext()
        
        #  Return Array of object IDS
        return retarr
    
    """
     * get_objects ()
     *
     * Grabs all Objects in the database, or specific to a section_value
     *
     * @return array Returns objects in format suitable for add_acl and is_conflicting_acl
     *    - i.e. Associative array, item=:Section Value, key=:Array of Object Values i.e. ["<Section Value>" => ["<Value 1>", "<Value 2>", "<Value 3>"], ...]
     *
     * @param string Filter for section value
     * @param int Returns hidden objects if 1, does not if 0
     * @param string Object Type, either 'ACO', 'ARO', 'AXO'
    """
    def get_objects(self, section_value = None, return_hidden = 1, object_type = None):
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix + 'axo'
        else:
            self.debug_text('get_objects(): Invalid Object Type: ' +  object_type)
            return False
        self.debug_text("get_objects(): Section Value: section_value Object Type: object_type")
        query = 'SELECT section_value,value FROM ' + table
        where = list()
        if section_value:
            where.append('section_value=' + self.db.quote(section_value))
        if return_hidden == 0:
            where.append('hidden=0')
        if where:
            query += ' WHERE ' + ' AND '.join(where)
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('get_objects')
            return False
        
        retarr = list()
        row = rs.FetchRow()
        while row:
            retarr[row[0]].append(row[1])
            row = rs.FetchRow()
        #  Return objects
        return retarr
    
    """
     * get_object_data()
     *
     * Gets all data pertaining to a specific Object.
     *
     * @return array Returns 2-Dimensional array of rows with columns = ( section_value, value, order_value, name, hidden )
     *
     * @param int Object ID #
     * @param string Object Type, either 'ACO', 'ARO', 'AXO'
    """
    def get_object_data(self, object_id, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
                
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix + 'axo'
        else:
            self.debug_text('get_object_data(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("get_object_data(): Object ID: object_id Object Type: object_type")

        if not object_id:
            self.debug_text("get_object_data(): Object ID (object_id) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("get_object_data(): Object Type (object_type) is empty, this is required")
            return False
        
        query  = 'SELECT section_value,value,order_value,name,hidden FROM ' + table + ' WHERE id=' + object_id
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('get_object_data')
            return False
        
        if (rs.RecordCount() < 1) :
            self.debug_text('get_object_data(): Returned  ' + row_count + ' rows')
            return False
        
        #  Return all objects
        return rs.GetRows()
    
    """
     * get_object_id()
     *
     * Gets the object_id given the section_value AND value of the object.
     *
     * @return int Object ID #
     *
     * @param string Object Section Value
     * @param string Object Value
     * @param string Object Type, either 'ACO', 'ARO', 'AXO'
    """
    def get_object_id(self, section_value, value, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix + 'axo'
        else:
            self.debug_text('get_object_id(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("get_object_id(): Section Value: section_value Value: value Object Type: object_type")
        section_value = section_value.strip()
        value = value.strip()
        if not section_value and not value:
            self.debug_text("get_object_id(): Section Value (value) AND value (value) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("get_object_id(): Object Type (object_type) is empty, this is required")
            return False
        
        query = 'SELECT id FROM ' + table + ' WHERE section_value=' + self.db.quote(section_value) + ' AND value=' + self.db.quote(value)
        rs = self.db.Execute(query)

        if not rs:
            self.debug_db('get_object_id')
            return False
        
        row_count = rs.RecordCount()
        if row_count > 1:
            self.debug_text("get_object_id(): Returned row_count rows, can only return one. This should never happen, the database may be missing a unique key.")
            return False
        
        if row_count == 0:
            self.debug_text("get_object_id(): Returned row_count rows")
            return False
        
        row = rs.FetchRow()
        # Return the ID.
        return row[0]
    
    """
     * get_object_section_value()
     *
     * Gets the object_section_value given object id
     *
     * @return string Object Section Value
     *
     * @param int Object ID #
     * @param string Object Type, either 'ACO', 'ARO', or 'AXO'
    """
    def get_object_section_value(self, object_id, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix + 'aro'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix + 'axo'
        else:
            self.debug_text('get_object_section_value(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("get_object_section_value(): Object ID: object_id Object Type: object_type")
        if not object_id:
            self.debug_text("get_object_section_value(): Object ID (object_id) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("get_object_section_value(): Object Type (object_type) is empty, this is required")
            return False
        
        query = 'SELECT section_value FROM ' + table + ' WHERE id=' + object_id
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('get_object_section_value')
            return False
        
        row_count = rs.RecordCount()
        if row_count > 1:
            self.debug_text("get_object_section_value(): Returned row_count rows, can only return one.")
            return False
        
        if row_count == 0:
            self.debug_text("get_object_section_value(): Returned row_count rows")
            return False
        
        row = rs.FetchRow()
        # Return the ID.
        return row[0]
    
    """
     * get_object_groups()
     *
     * Gets all groups an object is a member of.
     *
     * If option == 'RECURSE' it will get all ancestor groups.
     * defaults to only get direct parents.
     *
     * @return array Array of Group ID #'s, or False if Failed
     *
     * @param int Object ID #
     * @param string Object Type, either 'ARO' or 'AXO'
     * @param string Option, either 'RECURSE', or 'NO_RECURSE'
    """
    def get_object_groups(self, object_id, object_type = 'ARO', option = 'NO_RECURSE') :
        self.debug_text('get_object_groups(): Object ID: ' +  object_id + ' Object Type: ' +  object_type + ' Option: ' +  option)
        ot = object_type.strip().lower()
        if ot == 'axo':
            object_type = 'axo'
            group_table = self._db_table_prefix + 'axo_groups'
            map_table = self._db_table_prefix + 'groups_axo_map'
        elif ot == 'aro':
            object_type = 'aro'
            group_table = self._db_table_prefix + 'aro_groups'
            map_table = self._db_table_prefix + 'groups_aro_map'
        else:
            self.debug_text('get_object_groups(): Invalid Object Type: ' +  object_type)
            return False
        
        if not object_id:
            self.debug_text('get_object_groups(): Object ID: (' +  object_id + ') is empty, this is required')
            return False
        
        if option.upper() == 'RECURSE':
            query = 'SELECT        DISTINCT g.id AS group_id ' + \
                ' FROM        ' + map_table + ' gm ' + \
                ' LEFT JOIN    ' + group_table + ' g1 ON g1.id=gm.group_id ' + \
                ' LEFT JOIN    ' + group_table + ' g ON g.lft<=g1.lft AND g.rgt>=g1.rgt'
        else:
            query = 'SELECT        gm.group_id ' + ' FROM        ' + map_table + ' gm'
        
        query += 'WHERE        gm+ ' + object_type + '_id=' + object_id
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('get_object_groups')
            return False
        
        retarr = list()
        row = rs.FetchRow()
        while row:
            retarr.append(row[0])
        
        return retarr
    

    """
     * add_object()
     *
     * Inserts a new object
     *
     * @return int Returns the ID # of the new object if successful, False otherwise
     *
     * @param string Object Section Value
     * @param string Object Name
     * @param string Object Value
     * @param int Display Order
     * @param int Hidden Flag, either 1 to hide, or 0 to show.
     * @param string Object Type, either 'ACO', 'ARO', or 'AXO'
    """
    def add_object(self, section_value, name, value=0, order=0, hidden=0, object_type=None):
        assert object_type in ['aco','aro','axo']
        if object_type == 'aco':
            table = self._db_table_prefix + 'aco'
            object_sections_table = self._db_table_prefix + 'aco_sections'
        elif object_type == 'aro':
            table = self._db_table_prefix + 'aro'
            object_sections_table = self._db_table_prefix + 'aro_sections'
        elif object_type == 'axo':
            table = self._db_table_prefix + 'axo'
            object_sections_table = self._db_table_prefix + 'axo_sections'
        else:
            self.debug_text('add_object(): Invalid Object Type: ' +  object_type)
            raise Exception('add_object(): Invalid Object Type: ' +  object_type)
        
        self.debug_text("add_object(): Section Value: section_value Value: value Order: order Name: name Object Type: object_type")
        section_value = section_value.strip()
        name = name.strip()
        value = value.strip()
        order = int(order)
        hidden = int(hidden)
        
        if not name or not section_value:
            raise Exception("add_object(): name (name) OR section value (section_value) is empty, this is required")
        
        if len(name) >= 255 or len(value) >= 230:
            raise Exception("add_object(): name (name) OR value (value) is too long.")
        
        if not object_type:
            raise Exception("add_object(): Object Type (object_type) is empty, this is required")
        
        #  Test to see if the section is invalid or object already exists.
        # query  = '' + \
        #    ' SELECT        CASE WHEN o.id IS None THEN 0 ELSE 1 END AS object_exists ' + \
        #    ' FROM        ' + object_sections_table + ' s ' + \
        #    ' LEFT JOIN    ' + table + ' o ON (s.value=o.section_value AND o.value='+  self.db.quote(value) + ') ' + \
        #    ' WHERE        s.value=' + self.db.quote(section_value)
        #rs = self.db.Execute(query)
        #if not rs:
        #    self.debug_db('add_object')
        #    return False
        
        #TODO check for error conditions
        #       - invalid section
        #       - object already exists
        #
        
        objects = getattr(gacl_objects, table)
        
        query = objects.insert().values(section_value=section_value,value=value,order_value=order,name=name,hidden=hidden)
        
        rs = self.db.execute(query)
        
        if not rs:
            raise Exception('add_object')
        
        insert_id = rs.inserted_primary_key[0]
        
        self.debug_text("add_object(): Added object as ID: insert_id")
        return insert_id
    
    """
     * edit_object()
     *
     * Edits a given Object
     *
     * @return bool Returns True if successful, False otherwise
     *
     * @param int Object ID #
     * @param string Object Section Value
     * @param string Object Name
     * @param string Object Value
     * @param int Display Order
     * @param int Hidden Flag, either 1 to hide, or 0 to show
     * @param string Object Type, either 'ACO', 'ARO', or 'AXO'
    """
    def edit_object(self, object_id, section_value, name, value, order=0, hidden=0, object_type=None):
        object_type = ['aco','aro','axo']
        if object_type == 'aco':
            table = self._db_table_prefix + 'aco'
            object_map_table = self._db_table_prefix + 'aco_map'
        if object_type == 'aro':
            table = self._db_table_prefix + 'aro'
            object_map_table = self._db_table_prefix + 'aro_map'
        if object_type == 'axo':
            table = self._db_table_prefix + 'axo'
            object_map_table = self._db_table_prefix + 'axo_map'
        
        self.debug_text("edit_object(): ID: object_id Section Value: section_value Value: value Order: order Name: name Object Type: object_type")
        
        section_value = section_value.strip()
        name = name.strip()
        value = value.strip()
        order = int(order)
        hidden = int(hidden)
        
        if not object_id or not section_value:
            raise Exception("edit_object(): Object ID (object_id) OR Section Value (section_value) is empty, this is required")
        
        if not name:
            raise Exception("edit_object(): name (name) is empty, this is required")
        
        if not object_type:
            raise Exception("edit_object(): Object Type (object_type) is empty, this is required")
        
        self.db.BeginTrans()
        
        # Get old value incase it changed, before we do the update.
        query = 'SELECT value, section_value FROM '+ table + ' WHERE id=' + object_id
        old = self.db.GetRow(query)
        
        query  = '' + \
            ' UPDATE    '+ table + \
            ' SET        section_value=' + self.db.quote(section_value) +', ' + \
            ' value='+ self.db.quote(value) +',' + \
            ' order_value='+ self.db.quote(order) +', ' + \
            ' name='+ self.db.quote(name) +', ' + \
            ' hidden=' + hidden + \
            ' WHERE    id=' + object_id
        rs = self.db.Execute(query)
        if not rs:
            self.debug_db('edit_object')
            self.db.RollbackTrans()
            return False
        
        self.debug_text('edit_object(): Modified ' + object_type.upper() + ' ID: ' + object_id)
        
        if (old[0] != value or old[1] != section_value) :
            self.debug_text("edit_object(): Value OR Section Value Changed, update other tables.")

            query  = '' + \
                ' UPDATE    ' + object_map_table + \
                ' SET        value=' + self.db.quote(value) + ', ' + \
                ' section_value=' + self.db.quote(section_value) + \
                ' WHERE    section_value=' + self.db.quote(old[1]) + \
                ' AND    value=' + self.db.quote(old[0])
            rs = self.db.Execute(query)
            
            if not rs:
                self.debug_db('edit_object')
                self.db.RollbackTrans()
                return False
            
            self.debug_text ('edit_object(): Modified Map Value: ' + value + ' Section Value: ' + section_value)
        
        self.db.CommitTrans()
        return True
    
    """
     * del_object()
     *
     * Deletes a given Object and, if instructed to do so, erase all referencing objects
     *
     * ERASE feature by: Martino Piccinato
     *
     * @return bool Returns True if successful, False otherwise.
     *
     * @param int Object ID #
     * @param string Object Type, either 'ACO', 'ARO', or 'AXO'
     * @param bool Erases all referencing objects if True, leaves them alone otherwise.
    """
    def del_object(self, object_id, object_type=None, erase=False):
        assert object_type in ['aco','aro','axo']
        if object_type == 'aco':
            table = self._db_table_prefix + 'aco'
            object_map_table = self._db_table_prefix + 'aco_map'
        elif object_type == 'aro':
            table = self._db_table_prefix + 'aro'
            object_map_table = self._db_table_prefix + 'aro_map'
            groups_map_table = self._db_table_prefix + 'aro_groups_map'
            object_group_table = self._db_table_prefix + 'groups_aro_map'
        elif object_type == 'axo':
            table = self._db_table_prefix + 'axo'
            object_map_table = self._db_table_prefix + 'axo_map'
            groups_map_table = self._db_table_prefix + 'axo_groups_map'
            object_group_table = self._db_table_prefix + 'groups_axo_map'
        else:
            raise Exception('del_object(): Invalid Object Type: ' +  object_type)
        
        self.debug_text("del_object(): ID: object_id Object Type: object_type, Erase all referencing objects: erase")
        
        if not object_id:
            self.debug_text("del_object(): Object ID (object_id) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("del_object(): Object Type (object_type) is empty, this is required")
            return False
        
        self.db.BeginTrans()
        
        #sections = getattr(gacl_sections, object_sections_table)
        #self.db.execute(sections.delete().where(sections.c.id==object_section_id))

        #  Get Object section_value/value (needed to look for referencing objects)
        query = 'SELECT section_value,value FROM ' + table + ' WHERE id=' + object_id
        object = self.db.GetRow(query)
        
        if not object:
            self.debug_text('del_object(): The specified object (' +  object_type.upper() + ' ID: ' +  object_id + ') could not be found.')
            self.db.RollbackTrans()
            return False
        
        section_value = object[0]
        value = object[1]

        #  Get ids of acl referencing the Object (if any)
        query = "SELECT acl_id FROM object_map_table WHERE value='value' AND section_value='section_value'"
        acl_ids = self.db.GetCol(query)
        
        if (erase) :
            #  We were asked to erase all acl referencing it
            
            self.debug_text("del_object(): Erase was set to True, delete all referencing objects")
            
            if (object_type == "aro" or object_type == "axo"):
                #  The object can be referenced in groups_X_map tables
                #  in the future this branching may become useless because
                #  ACO might me "groupable" too
                #  Get rid of groups_map referencing the Object
                query = 'DELETE FROM ' + object_group_table + ' WHERE ' + object_type + '_id=' + object_id
                rs = self.db.Execute(query)
                
                if not rs:
                    self.debug_db('edit_object')
                    self.db.RollBackTrans()
                    return False
            
            if acl_ids:
                # There are acls actually referencing the object
                if (object_type == 'aco') :
                    #  I know it's extremely dangerous but
                    #  if asked to really erase an ACO
                    #  we should delete all acl referencing it
                    #  (and relative maps)
                    #  Do this below this branching
                    #  where it uses orphan_acl_ids as
                    #  the array of the "orphaned" acl
                    #  in this case all referenced acl are
                    #  orhpaned acl
                    orphan_acl_ids = acl_ids
                else:
                    #  The object is not an ACO and might be referenced
                    #  in still valid acls regarding also other object.
                    #  In these cases the acl MUST NOT be deleted
                    #  Get rid of object_id map referencing erased objects
                    query = "DELETE FROM object_map_table WHERE section_value='section_value' AND value='value'"
                    rs = self.db.Execute(query)

                    if not rs:
                        self.debug_db('edit_object')
                        self.db.RollBackTrans()
                        return False
                    
                    #  Find the "orphaned" acl. I mean acl referencing the erased Object (map)
                    #  not referenced anymore by other objects
                    sql_acl_ids = ','.join(acl_ids)
                    query = '' + \
                        ' SELECT        a.id ' + \
                        ' FROM        ' +  self._db_table_prefix + 'acl a ' + \
                        ' LEFT JOIN    ' +  object_map_table + ' b ON a.id=b.acl_id ' + \
                        ' LEFT JOIN    ' +  groups_map_table + ' c ON a.id=c.acl_id ' + \
                        ' WHERE        b.value IS None ' + \
                        ' AND        b.section_value IS None ' + \
                        ' AND        c.group_id IS None ' + \
                        ' AND        a.id in (' +  sql_acl_ids + ')'
                    orphan_acl_ids = self.db.GetCol(query)
                
                #  End of else section of "if (object_type == "aco")"
                 
                if (orphan_acl_ids) :
                    #  If there are orphaned acls get rid of them
                    for acl in orphan_acl_ids:
                        self.del_acl(acl)
            #  End of if (acl_ids)
            
            #  Finally delete the Object itself
            query = "DELETE FROM table WHERE id='object_id'"
            rs = self.db.Execute(query)
            if not rs:
                self.debug_db('edit_object')
                self.db.RollBackTrans()
                return False
            
            self.db.CommitTrans()
            return True
            
        #  End of "if (erase)"
         
        groups_ids = False

        if (object_type == 'axo' or object_type == 'aro') :
            #  If the object is "groupable" (may become unnecessary,
            #  see above

            #  Get id of groups where the object is assigned:
            #  you must explicitly remove the object from its groups before
            #  deleting it (don't know if this is really needed, anyway it's safer ;-)

            query = 'SELECT group_id FROM ' +  object_group_table + ' WHERE ' +  object_type + '_id=' +  object_id
            groups_ids = self.db.GetCol(query)
        

        if acl_ids or groups_ids:
            #  The Object is referenced somewhere (group or acl), can't delete it
            # self.debug_text("del_object(): Can't delete the object as it is being referenced by GROUPs (" + implode(groups_ids) + ") or ACLs (" + implode(acl_ids,",") + ")")
            self.db.RollBackTrans()
            return False
        else:
            #  The Object is NOT referenced anywhere, delete it
            query = "DELETE FROM table WHERE id='object_id'"
            rs = self.db.Execute(query)
            if not rs:
                self.debug_db('edit_object')
                self.db.RollBackTrans()
                return False
            
            self.db.CommitTrans()
            return True
        
        self.db.RollbackTrans()
        return False
    
    """
     *
     * Object Sections
     *
    """

    """
     * get_object_section_section_id()
     *
     * Gets the object_section_id given the name AND/OR value of the section.
     *
     * Will only return one section id, so if there are duplicate names it will return False.
     *
     * @return int Object Section ID if the object section is found AND is unique, or False otherwise.
     *
     * @param string Object Name
     * @param string Object Value
     * @param string Object Type, either 'ACO', 'ARO', 'AXO', or 'ACL'
     *
    """
    def get_object_section_section_id(self, name = None, value = None, object_type = None) :
        self.debug_text("get_object_section_section_id(): Value: value Name: name Object Type: object_type")
        ot = object_type.strip().lower()
        if ot in ['aco','aro','axo','acl']:
            table = self._db_table_prefix . ot
            object_sections_table = self._db_table_prefix + ot + '_sections'
        else:
            self.debug_text('get_object_section_section_id(): Invalid Object Type (' + ot + ')')
            return False
        
        name = name.strip()
        value = value.strip()
        if not name and not value:
            self.debug_text('get_object_section_section_id(): Both Name (' + name + ') and Value (' + value + ') are empty, you must specify at least one.')
            return False
        
        query = 'SELECT id FROM ' + object_sections_table
        where = ' WHERE '

        #  limit by value if specified
        if value:
            query += where + 'value=' + self.db.quote(value)
            where = ' AND '

        #  only use name if asked, this is SLOW
        if name:
            query += where +'name='+ self.db.quote(name)
        
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('get_object_section_section_id')
            return False
        
        row_count = rs.RecordCount()

        #  If only one row is returned
        if (row_count == 1) :
            #  Return only the ID in the first row.
            row = rs.FetchRow()
            return row[0]
        
        #  If more than one row is returned
        #  should only ever occur when using name as values are unique.
        if (row_count > 1) :
            self.debug_text('get_object_section_section_id(): Returned ' +  row_count + ' rows, can only return one. Please search by value not name, or make your names unique.')
            return False
        
        #  No rows returned, no matching section found
        self.debug_text('get_object_section_section_id(): Returned ' +  row_count + ' rows, no matching section found.')
        return False
    
    """
     * add_object_section()
     *
     * Inserts an object Section
     *
     * @return int Object Section ID of new section
     *
     * @param string Object Name
     * @param string Object Value
     * @param int Display Order
     * @param int Hidden flag, hides section if 1, shows section if 0
     * @param string Object Type, either 'ACO', 'ARO', 'AXO', or 'ACL'
    """
    def add_object_section(self, name, value=0, order=0, hidden=0, object_type=None):
        assert object_type in ['aco','aro','axo','acl']
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            object_sections_table = self._db_table_prefix + 'aco_sections'
        elif ot == 'aro':
            object_type = 'aro'
            object_sections_table = self._db_table_prefix + 'aro_sections'
        elif ot == 'axo':
            object_type = 'axo'
            object_sections_table = self._db_table_prefix + 'axo_sections'
        elif ot == 'acl':
            object_type = 'acl'
            object_sections_table = self._db_table_prefix + 'acl_sections'
        
        self.debug_text("add_object_section(): Value: value Order: order Name: name Object Type: object_type")

        name = name.strip()
        value = value.strip()
        order = str(order).strip()
        hidden = int(hidden)

        if (order == None or order == ''):
            order = 0
        
        if not name:
            self.debug_text("add_object_section(): name (name) is empty, this is required")
            raise ValueError("add_object_section(): name (name) is empty, this is required")
        
        if not object_type:
            self.debug_text("add_object_section(): Object Type (object_type) is empty, this is required")
            raise ValueError("add_object_section(): Object Type (object_type) is empty, this is required")
        
        # insert_id = self.db.GenID(self._db_table_prefix + object_type + '_sections_seq',10)
        
        sections = getattr(gacl_sections, object_sections_table)
         
        # query = 'insert into ' + object_sections_table + ' (id,value,order_value,name,hidden) VALUES( ' + insert_id + ', ' + \
        #    self.db.quote(value) + ', ' + order + ', ' + self.db.quote(name) + ', '+ hidden +')'
        
        query = sections.insert().values(value=value,order_value=order,name=name,hidden=hidden)
        rs = self.db.execute(query)
        insert_id = rs.inserted_primary_key[0]
        if not rs:
            self.debug_db('add_object_section')
            raise Exception('add_object_section')
        else:
            self.debug_text("add_object_section(): Added object_section as ID: insert_id")
            return insert_id
        
    
    """
     * edit_object_section()
     *
     * Edits a given Object Section
     *
     * @return bool Returns True if successful, False otherwise
     *
     * @param int Object Section ID #
     * @param string Object Section Name
     * @param string Object Section Value
     * @param int Display Order
     * @param int Hidden Flag, hide object section if 1, show if 0
     * @param string Object Type, either 'ACO', 'ARO', 'AXO', or 'ACL'
    """
    def edit_object_section(self, object_section_id, name, value=0, order=0, hidden=0, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix + 'aco'
            object_sections_table = self._db_table_prefix  + 'aco_sections'
            object_map_table = self._db_table_prefix  + 'aco_map'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix  + 'aro'
            object_sections_table = self._db_table_prefix  + 'aro_sections'
            object_map_table = self._db_table_prefix  + 'aro_map'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix  + 'axo'
            object_sections_table = self._db_table_prefix  + 'axo_sections'
            object_map_table = self._db_table_prefix  + 'axo_map'    
        elif ot == 'acl':
            object_type = 'acl'
            table = self._db_table_prefix  + 'acl'
            object_sections_table = self._db_table_prefix  + 'acl_sections'
        else:
            self.debug_text('edit_object_section(): Invalid Object Type: ' +  object_type)
            return False
        
        self.debug_text("edit_object_section(): ID: object_section_id Value: value Order: order Name: name Object Type: object_type")
        
        name = name.strip()
        value = value.strip()
        order = order.strip()
        hidden = int(hidden)
        
        if not object_section_id:
            self.debug_text("edit_object_section(): Section ID (object_section_id) is empty, this is required")
            return False
        
        if not name:
            self.debug_text("edit_object_section(): name (name) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("edit_object_section(): Object Type (object_type) is empty, this is required")
            return False
        
        self.db.BeginTrans()

        # Get old value incase it changed, before we do the update.
        query = "select value from object_sections_table where id=object_section_id"
        old_value = self.db.GetOne(query)
        
        query = "update object_sections_table set " + \
                       " value='value', " + \
                       " order_value='order', " + \
                       " name='name', " + \
                       " hidden=hidden " + \
            " where   id=object_section_id"
        rs = self.db.Execute(query)
        
        if not rs:
            self.debug_db('edit_object_section')
            self.db.RollbackTrans()
            return False
        else:
            self.debug_text("edit_object_section(): Modified aco_section ID: object_section_id")
            if (old_value != value):
                self.debug_text("edit_object_section(): Value Changed, update other tables.")
                query = "update table set " + \
                    " section_value='value' " + \
                    " where section_value = 'old_value'"
                rs = self.db.Execute(query)
                
                if not rs:
                    self.debug_db('edit_object_section')
                    self.db.RollbackTrans()
                    return False
                else:
                    if object_map_table:
                        query = "update object_map_table set " + \
                            " section_value='value' " + \
                            " where section_value = 'old_value'"
                        rs = self.db.Execute(query)
                        if not rs:
                            self.debug_db('edit_object_section')
                            self.db.RollbackTrans()
                            return False
                        else:
                            self.debug_text("edit_object_section(): Modified ojbect_map value: value")
                            self.db.CommitTrans()
                            return True
                    else:
                        # ACL sections, have no mapping table. Return True.
                        self.db.CommitTrans()
                        return True                    
        self.db.CommitTrans()
        return True
    
    """
     * del_object_section()
     *
     * Deletes a given Object Section and, if explicitly asked, all the section objects
     *
     * ERASE feature by: Martino Piccinato
     *
     * @return bool Returns True if successful, False otherwise
     *
     * @param int Object Section ID # to delete
     * @param string Object Type, either 'ACO', 'ARO', 'AXO', or 'ACL'
     * @param bool Erases all section objects assigned to the section
    """
    def del_object_section(self, object_section_id, object_type=None, erase=False) :
        assert object_type in ['aco','aro','axo','acl']
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            object_sections_table = self._db_table_prefix  + 'aco_sections'
        elif ot == 'aro':
            object_type = 'aro'
            object_sections_table = self._db_table_prefix  + 'aro_sections'
        elif ot == 'axo':
            object_type = 'axo'
            object_sections_table = self._db_table_prefix  + 'axo_sections'
        elif ot == 'acl':
            object_type = 'acl'
            object_sections_table = self._db_table_prefix  + 'acl_sections'
        
        self.debug_text("del_object_section(): ID: object_section_id Object Type: object_type, Erase all: erase")

        if not object_section_id:
            self.debug_text("del_object_section(): Section ID (object_section_id) is empty, this is required")
            raise Exception("del_object_section(): Section ID (object_section_id) is empty, this is required")
        
        if not object_type:
            self.debug_text("del_object_section(): Object Type (object_type) is empty, this is required")
            raise Exception("del_object_section(): Object Type (object_type) is empty, this is required")
        
        sections = getattr(gacl_sections, object_sections_table)
        self.db.execute(sections.delete().where(sections.c.id==object_section_id))
        
        #  Get the value of the section
        # query="SELECT value FROM object_sections_table WHERE id='object_section_id'"
        # section_value = self.db.GetOne(query)
        
        # FIXME optionally delete all objects in the section
        if False:
            #  Get all objects ids in the section
            # object_ids = self.get_object(section_value, 1, object_type)
            if(erase) :
                #  Delete all objects in the section and for
                #  each object delete the referencing object
                #  (see del_object method)
                if is_list(object_ids) :
                        for id in object_ids:
                            if ( object_type == 'acl' ) :
                                self.del_acl(id)
                            else:
                                self.del_object(id, object_type, True)
            
            if(object_ids and not erase) :
                #  There are objects in the section and we
                #  were not asked to erase them: don't delete it
                self.debug_text("del_object_section(): Could not delete the section (section_value) as it is not empty.")
                return False
            else:
                #  The section is empty (or emptied by this method)
                query = "DELETE FROM object_sections_table where id='object_section_id'"
                rs = self.db.Execute(query)
                if (not is_object(rs)) :
                    self.debug_db('del_object_section')
                    return False
                else:
                    self.debug_text("del_object_section(): deleted section ID: object_section_id Value: section_value")
                    return True
        return False
    
    """
     * get_section_data()
     *
     * Gets the section data given the Section Value
     *
     * @return array Returns numerically indexed array with the following columns:
     *    - array[0] = (int) Section ID #
     *    - array[1] = (string) Section Value
     *    - array[2] = (int) Section Order
     *    - array[3] = (string) Section Name
     *    - array[4] = (int) Section Hidden?
     * @param string Section Value
     * @param string Object Type, either 'ACO', 'ARO', or 'AXO'
    """
    def get_section_data(self, section_value, object_type=None) :
        ot = object_type.strip().lower()
        if ot == 'aco':
            object_type = 'aco'
            table = self._db_table_prefix  + 'aco_sections'
        elif ot == 'aro':
            object_type = 'aro'
            table = self._db_table_prefix  + 'aro_sections'
        elif ot == 'axo':
            object_type = 'axo'
            table = self._db_table_prefix  + 'axo_sections'
        else:
            self.debug_text('get_section_data(): Invalid Object Type: ' +  object_type)
            return False

        self.debug_text("get_section_data(): Section Value: section_value Object Type: object_type")

        if not section_value:
            self.debug_text("get_section_data(): Section Value (section_value) is empty, this is required")
            return False
        
        if not object_type:
            self.debug_text("get_section_data(): Object Type (object_type) is empty, this is required")
            return False
        
        query = 'SELECT id, value, order_value, name, hidden FROM ' +  table  + ' WHERE value = \'' +  section_value  + '\''
        row = self.db.GetRow(query)

        if (row) :
            return row
        
        self.debug_text("get_section_data(): Section does not exist.")
        return False
    
    """
     * clear_database()
     *
     * Deletes all data from the phpGACL tables. USE WITH CAUTION.
     *
     * @return bool Returns True if successful, False otherwise
     *
    """
    def clear_database(self):
        tablesToClear = (
                self._db_table_prefix + 'acl',
                self._db_table_prefix + 'aco',
                self._db_table_prefix + 'aco_map',
                self._db_table_prefix + 'aco_sections',
                self._db_table_prefix + 'aro',
                self._db_table_prefix + 'aro_groups',
                self._db_table_prefix + 'aro_groups_map',
                self._db_table_prefix + 'aro_map',
                self._db_table_prefix + 'aro_sections',
                self._db_table_prefix + 'axo',
                self._db_table_prefix + 'axo_groups',
                self._db_table_prefix + 'axo_groups_map',
                self._db_table_prefix + 'axo_map',
                self._db_table_prefix + 'axo_sections',
                self._db_table_prefix + 'groups_aro_map',
                self._db_table_prefix + 'groups_axo_map'
                )

        #  Get all the table names and loop
        tableNames = self.db.MetaTables('TABLES')
        query = list()
        for key, value in tableNames:
                if value in tablesToClear:
                        query.append('TRUNCATE TABLE ' + value + ';')
        
        #  Loop the queries and return.
        for key, value in query:
            result = self.db.Execute(value)
        
        return True

