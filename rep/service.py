import cherrypy
import logging
import json
from dataclasses import asdict

from rep.dao.VoteObjectDao import VoteObjectDao
from rep.dataclasses.VoteObject import VoteObject
from rep.dataclasses.PagedResponse import PagedResponse

vote_objects_dao = VoteObjectDao()

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
        vote_object = _get_vote_object_or_throw(vote_id) 
        cherrypy.response.headers["Content-Type"] = "application/pdf"
        return vote_object.blob
    

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
        vote_object = _get_vote_object_or_throw(vote_id) 
        return asdict(_strip_blob(vote_object))


class VoteObjectCollectionResource(object):
    """
        Collection view for vote objects
    """
    def __init__(self, vote_objects_dao):
        self.vote_objects_dao = vote_objects_dao


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, page=0, size=100):
        page = int(page)
        size = int(size)
        vote_objects =  self.vote_objects_dao.getAll(size, page * size)
        count = self.vote_objects_dao.getCount()
        results = [
            asdict(_strip_blob(i))
            for i in vote_objects
        ]
        return _to_paginated_response(count, page, size, results)


#######
#
#    helpers
#
#######

def _get_vote_object_or_throw(vote_id):
    maybe_vote_object = vote_objects_dao.getById(vote_id)
    if maybe_vote_object:
        return maybe_vote_object
    else: 
        raise cherrypy.HTTPError(404)


def _to_paginated_response(total_count, page, size, results=[]):
    return asdict(PagedResponse(
        results,
        page,
        size,
        total_count,
    ))


def _strip_blob(vote_object):
    return VoteObject(
        vote_object.vote_id,
        # strip out the blob because it's a lot of data to send to the client
        # and it's unlikely that they even want it
        None,
        vote_object.sourceUrl,
        vote_object.sourceType,
        vote_object.sourceFormat,
        vote_object.isProcessed,
    )


def main():
    # defining as a dict just to make it easier to read this bit
    routes = {
        '/api/v1/vote': VoteObjectResource(vote_objects_dao),
        '/api/v1/votes': VoteObjectCollectionResource(vote_objects_dao),
        '/view/vote': VoteObjectViewResource(vote_objects_dao),
    }

    for route, handler in routes.items():
        cherrypy.tree.mount(handler, route)

    cherrypy.engine.start()
    cherrypy.engine.block()
