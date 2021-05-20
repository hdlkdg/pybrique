from flask import request, abort
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource
from marshmallow import Schema, fields

from requetes import Artiste

class QuerySchema(Schema):
    ark = fields.Str(description="L'identifiant ARK de l'artiste", required=True)
    info = fields.Str(description="L'information voulue", required=True)

schema = QuerySchema()

class InfoArtist(Resource):
    def get(self):
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        ark = schema.load(request.args)['ark']
        info = schema.load(request.args)['info']
        artist = Artiste(ark)
        functions = {
                'name':artist.name,
                'bio':artist.bio,
                'img':artist.img,
                'caption':artist.caption,
                'imslp':artist.imslp,
                'partitions':artist.partitions,
                'works':artist.works,
                'worksincat':artist.worksincat,
                'gallica':artist.gallica,
                'about':artist.about,
                'aboutincat':artist.aboutincat,
                'bibliozik':artist.bibliozik,
                'wikipedia':artist.wikipedia,
                'musicbrainz':artist.musicbrainz,
                'site':artist.site
                }
        return functions[info](), 200
