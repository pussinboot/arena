import arena
from arena.search import search
from arena.resource import Resource, paginated


class Channel(Resource):
    base_endpoint = '/channels'

    def __init__(self, slug, **data):
        self.slug = slug
        if not data:
            data = self.thumb()

        # temp solution, to not override the `contents` method
        data.pop('contents')

        self._set_data(data)
        self.user = arena.User(**self.user)

    @paginated
    def all(self, **kwargs):
        """gets full representation of this channel (paginated)"""
        return self._get('/{}'.format(self.slug), params=kwargs['params'])

    def thumb(self, **kwargs):
        """gets a small representation of this channel"""
        return self._get('/{}/thumb'.format(self.slug))

    @paginated
    def connections(self, **kwargs):
        """get connections for this channel (paginated)"""
        page = self._get('/{}/connections'.format(self.slug), params=kwargs['params'])
        chans = [Channel(**d) for d in page.pop('channels')]
        return chans, page

    @paginated
    def channels(self, **kwargs):
        """get connected channels for this channel (paginated)"""
        page = self._get('/{}/channels'.format(self.slug), params=kwargs['params'])
        chans = [Channel(**d) for d in page.pop('channels')]
        return chans, page

    @paginated
    def contents(self, **kwargs):
        """get only contents for this channel (paginated)"""
        # for some reason this one is missing pagination data?
        page = self._get('/{}/contents'.format(self.slug), params=kwargs['params'])
        contents = []
        for d in page.pop('contents'):
            cls = d['base_class']
            if cls == 'Block':
                obj = arena.Block(**d)
            elif cls == 'Channel':
                obj = arena.Channel(**d)
            else:
                raise TypeError('Unknown base_class: "{}"'.format(cls))
            contents.append(obj)
        return contents, page

    def collaborators(self):
        """get only collaborators for this channel"""
        page = self._get('/{}/collaborators'.format(self.slug))
        users = [arena.User(**d) for d in page.pop('users')]
        return users, page

    # TODO
    # <http://dev.are.na/documentation/channels#block_45048>
    # def add_collaborator(self):
        # return self._post('{}/collaborators'.format(self.slug)

    def update(self, **kwargs):
        """update a channel's attributes
        can specify:
        - title: str
        - status: one of ['public', 'closed', 'private']
        """
        return self._put('/{}'.format(self.slug), data=kwargs)

    def delete(self):
        """deletes a channel"""
        return self._delete('/{}'.format(self.slug))

    def add_block(self, source=None, content=None):
        """add a new block to the channel.
        one of `source` or `content` must be specified:
        - source: a url
        - content: github-flavored markdown
        """
        if source is not None:
            data = {'source': source}
        elif content is not None:
            data = {'content': content}
        else:
            raise ValueError('One of `source` or `content` must be specified')
        return self._post('/{}/blocks'.format(self.slug), data=data)


class Channels(Resource):
    base_endpoint = '/channels'

    @paginated
    def list(self, **kwargs):
        """list channels (paginated)"""
        page = self._get('', params=kwargs['params'])
        for k in ['users', 'blocks']:
            page.pop(k)
        chans = [Channel(**d) for d in page.pop('channels')]
        return chans, page

    def create(self, title, status='public'):
        """creates a new channel"""
        return self._post('', data={
            'title': title,
            'status': status
        })

    def channel(self, slug):
        """get an existing channel"""
        return Channel(slug)

    @paginated
    def search(self, query, **kwargs):
        """searches channels"""
        page = search.channels(query, **kwargs)
        for k in ['users', 'blocks']:
            page.pop(k)
        chans = [Channel(**d) for d in page.pop('channels')]
        return chans, page

