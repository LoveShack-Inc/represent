import cherrypy
import logging
import json

from rep.dao.VoteObjectDao import VoteObjectDao
from rep.dao.ProcessedVoteResultDao import ProcessedVoteResultDao
from rep.resources.ProcessedVoteResultResource import ProcessedVoteResultResource
from rep.resources.VoteObjectCollectionResource import VoteObjectCollectionResource
from rep.resources.VoteObjectResource import VoteObjectResource
from rep.resources.VoteObjectViewResource import  VoteObjectViewResource

vote_objects_dao = VoteObjectDao()
processed_vote_result_dao = ProcessedVoteResultDao()


def main():
    # defining as a dict just to make it easier to read this bit
    routes = {
        '/api/v1/vote': VoteObjectResource(vote_objects_dao),
        '/api/v1/votes': VoteObjectCollectionResource(vote_objects_dao),
        '/api/v1/result': ProcessedVoteResultResource(processed_vote_result_dao),
        '/api/v1/view/vote': VoteObjectViewResource(vote_objects_dao),
    }

    for route, handler in routes.items():
        cherrypy.tree.mount(handler, route)
    
    # defaults to localhost only
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
