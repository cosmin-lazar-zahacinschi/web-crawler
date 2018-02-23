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
            v1 = client_.query('SELECT FROM Site WHERE url = "%s"' % (links[0]))          
            
            
        v2 = client_.query('SELECT FROM Site WHERE url = "%s"' % (links[1]), 1)
        if (len(v2) == 0):
            client_.command('CREATE VERTEX Site SET url = "%s"' % (links[1]))
            v2 = client_.query('SELECT FROM Site WHERE url = "%s"' % (links[1]))

        count = newConnections[links]
        batch_cmds = ['begin']
        
        for i in range(count):
            batch_cmds.append('CREATE EDGE links_to FROM (SELECT FROM Site WHERE url = "%s") '
                              'TO (SELECT FROM Site WHERE url = "%s")' % (links[0], links[1]))
        
        batch_cmds.append("commit retry 100;")
        cmd = ';'.join(batch_cmds)
        client_.batch(cmd)