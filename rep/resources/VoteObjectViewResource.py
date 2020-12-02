import cherrypy

from . import VoteObjectHelper

class VoteObjectViewResource(object):
    """
        For viewing PDFs in browser, or downloading the blob
    """
    def __init__(self, vote_objects_dao):
        self.vote_objects_dao = vote_objects_dao

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['vote_id'] = vpath.pop()
            return self


    @cherrypy.expose
    def index(self, vote_id):
        vote_object = VoteObjectHelper.get_vote_object_or_throw(self.vote_objects_dao, vote_id) 
        cherrypy.response.headers["Content-Type"] = "application/pdf"
        return vote_object.blob
    