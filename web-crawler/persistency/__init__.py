from pyorient import OrientDB
from utils import configuration
    
def add_connections(newConnections):
    
    client_ = OrientDB(configuration.get_prop('srv_addr'), configuration.get_prop('srv_port'))
    client_.connect(configuration.get_prop('user'), configuration.get_prop('pass'))
    client_.db_open(configuration.get_prop('db_name'), configuration.get_prop('user'), configuration.get_prop('pass'))
    
    for links in newConnections:
        
        v1 = client_.query('SELECT FROM Site WHERE url = "%s"' % (links[0]), 1)
        if (len(v1) == 0):
            client_.command('CREATE VERTEX Site SET url = "%s"' % (links[0]))      
                        
        v2 = client_.query('SELECT FROM Site WHERE url = "%s"' % (links[1]), 1)
        if (len(v2) == 0):
            client_.command('CREATE VERTEX Site SET url = "%s"' % (links[1]))

        count = newConnections[links]
        
        edge_query = client_.query('SELECT FROM links_to WHERE out in (SELECT @rid FROM Site WHERE url = "%s") '
                             'and in in (SELECT @rid FROM Site WHERE url = "%s")' % (links[0], links[1]))
        
        if (len(edge_query) == 0):
            client_.command('CREATE EDGE links_to FROM (SELECT FROM Site WHERE url = "%s") '
                              'TO (SELECT FROM Site WHERE url = "%s") SET count = %d' % (links[0], links[1], count))
        else:
            edge = edge_query[0].oRecordData
            new_count = edge['count'] + count
            client_.command('UPDATE %s SET count = %d' % (edge_query[0]._rid, new_count))
            