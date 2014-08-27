import sys
import json
start = int(sys.argv[1])
end = int(sys.argv[2])+1
data = []
for i in range(start,end):
    f = open('%s.json'%i,'r')
    j = json.loads(f.read())
    data += j
    print len(data)
    print len(j)
    f.close()
open('%s-%s_fav.json'%(start,end-1),'w').write(json.dumps(data))
