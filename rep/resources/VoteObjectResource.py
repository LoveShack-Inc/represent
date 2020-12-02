import cherrypy

from . import VoteObjectHelper
from dataclasses import asdict

class VoteObjectResource(object):
    """
        CRUD for vote objects
    """
    def __init__(self, vote_objects_dao):
        self.vote_objects_dao = vote_objects_dao

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['vote_id'] = vpath.pop()
            return self

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, vote_id):
        vote_object =  VoteObjectHelper.get_vote_object_or_throw(self.vote_objects_dao, vote_id)
        return asdict(VoteObjectHelper.strip_blob(vote_object))
