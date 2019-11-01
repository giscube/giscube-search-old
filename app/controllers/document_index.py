import math

from asyncpg.exceptions import UndefinedTableError

from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy import and_, func, or_, cast
from sqlalchemy.sql import select
from geoalchemy2 import Geography

from app.models.document_index import get_table


class DocumentIndexController(HTTPMethodView):
    async def get(self, request, index):
        document_index = get_table(index)
        qs = select([document_index])

        q = request.args.get('q', None)
        if q:
            qs = qs.where(document_index.c.body == q)

        c = request.args.get('c', None)
        if c:
            qs = qs.where(document_index.c.content_type.in_(c.split(',')))

        p = request.args.get('p', None)
        if p:
            latlon = p.split(',')
            latlon = list(map(float, latlon))
            distance = int(request.args.get('r', 25))
            geom = func.ST_GeomFromEWKT('SRID=4326;POINT(%s %s)' % (latlon[1], latlon[0]))
            qs = qs.where(
                or_(
                    and_(
                        document_index.c.geom_point.isnot(None),
                        func.ST_DistanceSphere(document_index.c.geom_point, geom) < distance
                    ),
                    and_(
                        document_index.c.geom_linestring.isnot(None),
                        func.ST_DistanceSphere(document_index.c.geom_linestring, geom) < distance
                    ),
                    and_(
                        document_index.c.geom_polygon.isnot(None),
                        func.ST_Contains(document_index.c.geom_polygon, geom)
                    )
                )
            )

        try:
            rows = await request.app.db.fetch_all(qs)
        except UndefinedTableError:
            return json({'error': 'ERROR: The index does\'t exist'})
        results = []
        i = 0
        for x in rows:
            results.append({
                'content_type': x['content_type'],
                'object_id': x['object_id'],
                'data': x['data']
            })
            i += 1
        return json({'results': results, 'count': i})
