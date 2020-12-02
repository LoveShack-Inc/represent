import cherrypy

from dataclasses import asdict
from rep.dataclasses.PagedResponse import PagedResponse
from rep.dataclasses.VoteObject import VoteObject

#######
#
#    helpers
#
#######

class VoteObjectHelper:
    @staticmethod
    def get_vote_object_or_throw(vote_objects_dao, vote_id):
        maybe_vote_object = vote_objects_dao.getById(vote_id)
        if maybe_vote_object:
            return maybe_vote_object
        else: 
            raise cherrypy.HTTPError(404)


    @staticmethod
    def to_paginated_response(total_count, page, size, results=[]):
        return asdict(PagedResponse(
            results,
            page,
            size,
            total_count,
        ))


    @staticmethod
    def strip_blob(vote_object):
        return VoteObject(
            vote_id=vote_object.vote_id,
            # strip out the blob because it's a lot of data to send to the client
            # and it's unlikely that they even want it
            blob=None,
            sourceUrl=vote_object.sourceUrl,
            sourceType=vote_object.sourceType,
            sourceFormat= vote_object.sourceFormat,
            isProcessed=vote_object.isProcessed,
        )
