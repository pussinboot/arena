from arena.resource import Resource, resource_for_data


class Feed(Resource):
    base_endpoint = '/feed'

    def __call__(self, offset=0):
        page = self._get('', params={'offset': offset}, auth=True)
        return items, page
