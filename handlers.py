from piston.handler import BaseHandler
from drip.models import NodeData

class NodeDataHandler(BaseHandler):
   allowed_methods = ('GET','PUT','POST',)
   model = NodeData

  