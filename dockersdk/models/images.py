from .resource import Collection, Model


class Image(Model):
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    @property
    def short_id(self):
        """
        Returns the "sha256:" prefix plus 10 characters of the ID
        """
        return self.id[:17]

    @property
    def name(self):
        return self.tags[0] if self.tags else self.short_id

    @property
    def tags(self):
        return [
            tag for tag in self.attrs['RepoTags']
            if tag != '<none>:<none>'
        ]

    def tag(self, *args, **kwargs):
        self.api_client.tag(self.id, *args, **kwargs)


class ImageCollection(Collection):
    model = Image

    def pull(self, repository, **kwargs):
        self.api_client.pull(repository, **kwargs)
        data = self.api_client.inspect_image(repository)
        return self.prepare_model(data)

    def list(self, *args, **kwargs):
        return [
            self.prepare_model(r)
            for r in self.api_client.images(*args, **kwargs)
        ]

    def remove(self, *args, **kwargs):
        self.api_client.remove_image(*args, **kwargs)
