"""
   port of phpGACL - every effort will be made to release the enclosing flask extension under a permissive license
   and ultimately this code will be moved to an independent package (likely called pygacl) anyway
  
   Original License:
   
   Copyright (C) 2002,2003 Mike Benoit
  
   self library is free software you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation either
   version 2.1 of the License, or (at your option) any later version.
  
   self library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.
  
   You should have received a copy of the GNU Lesser General Public
   License along with self library if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
  
   For questions, help, comments, discussion, etc., please join the
   phpGACL mailing list. http:#sourceforge.net/mail/?group_id=57103
  
   You may contact the author of phpGACL by e-mail at:
   ipso@snappymail.ca
  
   The latest version of phpGACL can be obtained from:
   http:#phpgacl.sourceforge.net/
  
   @package phpGACL

  phpGACL main class
 
  Class gacl should be used in applications where only querying the phpGACL
  database is required.
 
  @package phpGACL
  @author Mike Benoit <ipso@snappymail.ca>
"""
from adodb import *
from utils import *
import sqlalchemy
from sqlalchemy import create_engine

class Gacl(object):
    
    # --- phpGACL Configuration path/file ---
    config_file = ' + /gacl.ini.php'
    
    # --- Private properties ---
    # @var boolean Enables Debug output if True
    _debug = False
    
    # --- Database configuration. ---
    
    # @var string Prefix for all the phpgacl tables in the database
    _db_table_prefix = ''
    # @var string The database type, based on available ADODB connectors - mysql, postgres7, sybase, oci8po See here for more: http:#php.weblogs.com/adodb_manual#driverguide 
    _db_type = 'mysql'
    # @var string The database server 
    _db_host = 'localhost'
    # @var string The database user name 
    _db_user = 'root'
    # @var string The database user password 
    _db_password = ''
    # @var string The database name 
    _db_name = 'gacl'
    # @var object An ADODB database connector object 
    _db = ''
    """
        NOTE:    This cache must be manually cleaned each time ACL's are modified.
        Alternatively you could wait for the cache to expire.
    """ 
    # @var boolean Caches queries if True 
    _caching = False
    # @var boolean Force cache to expire 
    _force_cache_expire = True
    # @var string The directory for cache file to eb written (ensure write permission are set) 
    _cache_dir = '/tmp/phpgacl_cache' # NO trailing slash
    # @var int The time for the cache to expire in seconds - 600 == Ten Minutes 
    _cache_expire_time=600
    # @var string A switch to put acl_check into '_group_' mode 
    _group_switch = '_group_'
    """
        Constructor
        @param array An arry of options to oeverride the class defaults
    """
    def __init__(self, options=None):
        available_options = ('db','debug','items_per_page','max_select_box_items','max_search_return_items','db_table_prefix','db_uri','db_type','db_host','db_user','db_password','db_name','caching','force_cache_expire','cache_dir','cache_expire_time')
        #Values supplied in options array overwrite those in the config file.
        #if ( file_exists(self.config_file) ) :
        #        config = parse_ini_file(self.config_file)
        #        if ( is_list(config) ) :
        #                gacl_options = array_merge(config, options)
        #        
        #        unset(config)
        
        #FIXME refactor completely
        
        if options is not None:
            for key in available_options:
                property = '_' + key
                setattr(self, property, options.get(key, None))
                
        if isinstance(self._db, type(sqlalchemy.engine.base.Connection)):
            self.db = self._db
        else:
            self.db_engine = create_engine(self._db_uri, echo=self._debug)
            self.db = self.db_engine.connect()
        
        if ( self._caching == True ) :
            raise NotImplementedError('caching')
            
            # Cache options. We default to the highest performance. If you run in to cache corruption problems,
            # Change all the 'False' to 'True', self will slow things down slightly however.
             
            cache_options = {
                'caching': self._caching,
                'cacheDir': self._cache_dir + '/',
                'lifeTime': self._cache_expire_time,
                'fileLocking': True,
                'writeControl': False,
                'readControl': False,
                'memoryCaching': True,
                'automaticSerialization': False               
            }
            self.Cache_Lite = Hashed_Cache_Lite(cache_options)
        return
    
    
    """
    * Prints debug text if debug is enabled.
    * @param string THe text to output
    * @return boolean Always returns True
    """
    def debug_text(self, text) :
        if (self._debug) :
            print "text<br>\n"
        return True
    
    """
    * Prints database debug text if debug is enabled.
    * @param string The name of the function calling self method
    * @return string Returns an error message
    """
    def debug_db(self, function_name = '') :
        if (function_name != '') :
            function_name += ' (): '
        return self.debug_text (function_name  + 'database error: ' +  self.db.ErrorMsg()  + ' (' +  self.db.ErrorNo()  + ')')
    
    """
    * Wraps the actual acl_query() function.
    *
    * It is simply here to return True/False accordingly.
    * @param string The ACO section value
    * @param string The ACO value
    * @param string The ARO section value
    * @param string The ARO section
    * @param string The AXO section value (optional)
    * @param string The AXO section value (optional)
    * @param integer The group id of the ARO ??Mike?? (optional)
    * @param integer The group id of the AXO ??Mike?? (optional)
    * @return boolean True if the check succeeds, False if not.
    """
    def acl_check(self, aco_section_value, aco_value, aro_section_value, aro_value, axo_section_value=None, axo_value=None, root_aro_group=None, root_axo_group=None) :
        acl_result = self.acl_query(aco_section_value, aco_value, aro_section_value, aro_value, axo_section_value, axo_value, root_aro_group, root_axo_group)
        return acl_result['allow']
    
    """
    * Wraps the actual acl_query() function.
    *
    * Quick access to the return value of an ACL.
    * @param string The ACO section value
    * @param string The ACO value
    * @param string The ARO section value
    * @param string The ARO section
    * @param string The AXO section value (optional)
    * @param string The AXO section value (optional)
    * @param integer The group id of the ARO (optional)
    * @param integer The group id of the AXO (optional)
    * @return string The return value of the ACL
    """
    def acl_return_value(self, aco_section_value, aco_value, aro_section_value, aro_value, axo_section_value=None, axo_value=None, root_aro_group=None, root_axo_group=None) :
        acl_result = self.acl_query(aco_section_value, aco_value, aro_section_value, aro_value, axo_section_value, axo_value, root_aro_group, root_axo_group)
        return acl_result['return_value']
    
    """
    * Handles ACL lookups over arrays of AROs
    * @param string The ACO section value
    * @param string The ACO value
    * @param array An named array of arrays, each element in the format aro_section_value=>list(aro_value1,aro_value1,...)
    * @return mixed The same data format as inputted.
    """
    def acl_check_list(self, aco_section_value, aco_value, aro_array) :
        """
            Input Array:
                Section => list(Value, Value, Value),
                Section => list(Value, Value, Value)
        """
        if (not is_list(aro_array)) :
            self.debug_text("acl_query_list(): ARO Array must be passed")
            return False
        
        for aro_section_value, aro_value_array in aro_array:
            for aro_value in aro_value_array:
                self.debug_text("acl_query_list(): ARO Section Value: aro_section_value ARO VALUE: aro_value")
                if( self.acl_check(aco_section_value, aco_value, aro_section_value, aro_value) ) :
                    self.debug_text("acl_query_list(): ACL_CHECK True")
                    retarr[aro_section_value].append(aro_value)
                else:
                    self.debug_text("acl_query_list(): ACL_CHECK False")
                
            
        
        return retarr
    
    """
    * The Main function that does the actual ACL lookup.
    * @param string The ACO section value
    * @param string The ACO value
    * @param string The ARO section value
    * @param string The ARO section
    * @param string The AXO section value (optional)
    * @param string The AXO section value (optional)
    * @param string The value of the ARO group (optional)
    * @param string The value of the AXO group (optional)
    * @param boolean Debug the operation if True (optional)
    * @return array Returns as much information as possible about the ACL so other functions can trim it down and omit unwanted data.
    """
    def acl_query(self, aco_section_value, aco_value, aro_section_value, aro_value, axo_section_value=None, axo_value=None, root_aro_group=None, root_axo_group=None, debug=None) :
                
        cache_id = 'acl_query_' + aco_section_value + '-' + aco_value + '-' + aro_section_value + '-' + aro_value + '-' + axo_section_value + '-' + axo_value + '-' + root_aro_group + '-' + root_axo_group + '-' + debug
        retarr = self.get_cache(cache_id)
        if (not retarr) :
            
            # Grab all groups mapped to self ARO/AXO
            
            aro_group_ids = self.acl_get_groups(aro_section_value, aro_value, root_aro_group, 'ARO')
            if (is_list(aro_group_ids) and not empty(aro_group_ids)) :
                sql_aro_group_ids = ','.join(aro_group_ids)
            
            if (axo_section_value != '' and axo_value != '') :
                axo_group_ids = self.acl_get_groups(axo_section_value, axo_value, root_axo_group, 'AXO')
                if (is_list(axo_group_ids) and not empty(axo_group_ids)) :
                    sql_axo_group_ids = ','.join(axo_group_ids)
                
            
            """
             * self query is where all the magic happens.
             * The ordering is very important here, as well very tricky to get correct.
             * Currently there can be  duplicate ACLs, or ones that step on each other toes. In self case, the ACL that was last updated/created
             * is used.
             *
             * this is probably where the most optimizations can be made.
            """
            order_by = list()
            query = 'SELECT      a.id,a.allow,a.return_value' + \
                    'FROM        ' +  self._db_table_prefix  + 'acl a' + \
                    'LEFT JOIN   ' +  self._db_table_prefix  + 'aco_map ac ON ac.acl_id=a.id'
            if (aro_section_value != self._group_switch) :
                query += 'LEFT JOIN   ' +  self._db_table_prefix  + 'aro_map ar ON ar.acl_id=a.id'
            
            if (axo_section_value != self._group_switch) :
                query += 'LEFT JOIN   ' +  self._db_table_prefix  + 'axo_map ax ON ax.acl_id=a.id'
            
            
            # if there are no aro groups, don't bother doing the join.
            
            try:
                isset(sql_aro_group_ids)
                query += 'LEFT JOIN   ' +  self._db_table_prefix  + 'aro_groups_map arg ON arg.acl_id=a.id' + \
                         'LEFT JOIN   ' +  self._db_table_prefix  + 'aro_groups rg ON rg.id=arg.group_id'
            except NameError:
                pass
            
            # self join is necessary to weed out rules associated with axo groups
            query += 'LEFT JOIN   ' +  self._db_table_prefix  + 'axo_groups_map axg ON axg.acl_id=a.id'
            """
             * if there are no axo groups, don't bother doing the join.
             * it is only used to rank by the level of the group.
            """
            if (isset(sql_axo_group_ids)) :
                query += 'LEFT JOIN   ' +  self._db_table_prefix  + 'axo_groups xg ON xg.id=axg.group_id'
            
            # Move the below line to the LEFT JOIN above for PostgreSQL's sake.
            # AND   ac.acl_id=a.id
            query += 'WHERE       a.enabled=1' + \
                     'AND     (ac.section_value=' +  self.db.quote(aco_section_value)  + ' AND ac.value=' +  self.db.quote(aco_value)  + ')'
            # if we are querying an aro group
            if (aro_section_value == self._group_switch) :
                # if acl_get_groups did not return an array
                try:
                    isset(sql_aro_group_ids)
                except NameError:
                    self.debug_text ('acl_query(): Invalid ARO Group: ' +  aro_value)
                    return False
                
                query += 'AND     rg.id IN (' +  sql_aro_group_ids  + ')'
                order_by.append('(rg.rgt-rg.lft) ASC')
            else:
                query += 'AND     ((ar.section_value=' +  self.db.quote(aro_section_value)  + ' AND ar.value=' +  self.db.quote(aro_value)  + ')'
                try:
                    isset(sql_aro_group_ids)
                    query += ' OR rg.id IN (' +  sql_aro_group_ids  + ')'
                    order_by.append('(CASE WHEN ar.value IS None THEN 0 ELSE 1 END) DESC')
                    order_by.append('(rg.rgt-rg.lft) ASC')
                except NameError:
                    pass
                
                query += ')'
            
            # if we are querying an axo group
            if (axo_section_value == self._group_switch) :
                # if acl_get_groups did not return an array
                if ( not isset (sql_axo_group_ids) ) :
                    self.debug_text ('acl_query(): Invalid AXO Group: ' +  axo_value)
                    return False
                
                query += 'AND     xg.id IN (' +  sql_axo_group_ids  + ')'
                order_by.append('(xg.rgt-xg.lft) ASC')
            else:
                query += 'AND     ('
                if (axo_section_value == '' and axo_value == '') :
                    query += '(ax.section_value IS None AND ax.value IS None)'
                else:
                    query += '(ax.section_value=' +  self.db.quote(axo_section_value)  + ' AND ax.value=' +  self.db.quote(axo_value)  + ')'
                
                try:
                    isset(sql_axo_group_ids)
                    query += ' OR xg.id IN (' +  sql_axo_group_ids  + ')'
                    order_by.append('(CASE WHEN ax.value IS None THEN 0 ELSE 1 END) DESC')
                    order_by.append('(xg.rgt-xg.lft) ASC')
                except NameError:
                    query += ' AND axg.group_id IS None'
                
                query += ')'
            
            """
             * The ordering is always very tricky and makes all the difference in the world.
             * Order (ar.value IS NOT None) DESC should put ACLs given to specific AROs
             * ahead of any ACLs given to groups. self works well for exceptions to groups.
            """
            order_by.append('a.updated_date DESC')
            query += 'ORDER BY    ' +  ','.join(order_by) 
            
            # we are only interested in the first row
            rs = self.db.SelectLimit(query, 1)
            if not rs:
                self.debug_db('acl_query')
                return False
            
            row = rs.FetchRow()
            #
            # Return ACL ID. This is the key to "hooking" extras like pricing assigned to ACLs etc... Very useful.
            #
            if (is_list(row)):
                # Permission granted?
                allow = False
                try:
                    if row[1] == 1:
                        allow = True
                except NameError:
                    pass
                
                retarr = {'acl_id': row[0], 'return_value': row[2], 'allow': allow}
            else:
                # Permission denied.
                retarr = {'acl_id': None, 'return_value': None, 'allow': False}
            
            #
            # Return the query that we ran if in debug mode.
            #
            if (debug == True) :
                retarr['query'] = query
            
            #Cache data.
            self.put_cache(retarr, cache_id)
        
        self.debug_text("<b>acl_query():</b> ACO Section: aco_section_value ACO Value: aco_value ARO Section: aro_section_value ARO Value aro_value ACL ID: " +  retarr['acl_id']  + ' Result: ' +  retarr['allow'])
        return retarr
    
    """
    * Grabs all groups mapped to an ARO. You can also specify a root_group for subtree'ing.
    * @param string The section value or the ARO or ACO
    * @param string The value of the ARO or ACO
    * @param integer The group id of the group to start at (optional)
    * @param string The type of group, either ARO or AXO (optional)
    """
    def acl_get_groups(self, section_value, value, root_group=None, group_type='ARO') :
        if group_type.lower() == 'axo':
            group_type = 'axo'
            object_table = self._db_table_prefix  + 'axo'
            group_table = self._db_table_prefix  + 'axo_groups'
            group_map_table = self._db_table_prefix  + 'groups_axo_map'
        else:
            group_type = 'aro'
            object_table = self._db_table_prefix  + 'aro'
            group_table = self._db_table_prefix  + 'aro_groups'
            group_map_table = self._db_table_prefix  + 'groups_aro_map'
        
        #profiler.startTimer( "acl_get_groups()")
        #Generate unique cache id.
        cache_id = 'acl_get_groups_' + section_value + '-' + value + '-' + root_group + '-' + group_type
        retarr = self.get_cache(cache_id)
        if (not retarr) :
            # Make sure we get the groups
            query = 'SELECT      DISTINCT g2.id'
            if (section_value == self._group_switch) :
                query += 'FROM        ' + group_table + ' g1,' + group_table + ' g2'
                where = 'WHERE       g1.value=' + self.db.quote( value )
            else:
                query += 'FROM        ' +  object_table  + ' o,' +  group_map_table  + ' gm,' +  group_table  + ' g1,' +  group_table  + ' g2'
                where = 'WHERE       (o.section_value=' +  self.db.quote(section_value)  + ' AND o.value=' +  self.db.quote(value)  + ')' + \
                        'AND     gm.' +  group_type  + '_id=o.id' + \
                        'AND     g1.id=gm.group_id'
            
            """
             * If root_group_id is specified, we have to narrow self query down
             * to just groups deeper in the tree then what is specified.
             * self essentially creates a virtual "subtree" and ignores all outside groups.
             * Useful for sites like sourceforge where you may seperate groups by "project".
            """
            if ( root_group != '') :
                #It is important to note the below line modifies the tables being selected.
                #self is the reason for the WHERE variable.
                query += ',' +  group_table  + ' g3'
                where += 'AND     g3.value=' +  self.db.quote( root_group )  + \
                         'AND     ((g2.lft BETWEEN g3.lft AND g1.lft) AND (g2.rgt BETWEEN g1.rgt AND g3.rgt))'
            else:
                where += 'AND     (g2.lft <= g1.lft AND g2.rgt >= g1.rgt)'
            
            query += where
            # self.debug_text(query)
            rs = self.db.Execute(query)
            if not rs:
                self.debug_db('acl_get_groups')
                return False
            
            retarr = list()
            #Unbuffered query?
            while (not rs.EOF) :
                retarr.append(reset(rs.fields))
                rs.MoveNext()
            
            #Cache data.
            self.put_cache(retarr, cache_id)
        
        return retarr
    
    """
    * Uses PEAR's Cache_Lite package to grab cached arrays, objects, variables etc...
    * using unserialize() so it can handle more then just text string.
    * @param string The id of the cached object
    * @return mixed The cached object, otherwise False if the object identifier was not found
    """
    def get_cache(self, cache_id) :
        if ( self._caching == True ) :
            self.debug_text("get_cache(): on ID: cache_id")
            if ( self.is_string(self.Cache_Lite.get(cache_id) ) ) :
                return unserialize(self.Cache_Lite.get(cache_id) )
            
        
        return False
    
    """
    * Uses PEAR's Cache_Lite package to write cached arrays, objects, variables etc...
    * using serialize() so it can handle more then just text string.
    * @param mixed A variable to cache
    * @param string The id of the cached variable
    """
    def put_cache(self, data, cache_id) :
        if ( self._caching == True ) :
            self.debug_text("put_cache(): Cache MISS on ID: cache_id")
            return self.Cache_Lite.save(serialize(data), cache_id)
        
        return False
    