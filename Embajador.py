import http.client
from datetime import datetime
import hashlib
ts = datetime.now()
cpb = 'c1d13a3edb994f0731e0a3d38b032a4d'
cpv = 'abe489414a3c3b1f0282f294d6452b6530422a51'
hash = hashlib.md5(ts*cpb*cpv)


