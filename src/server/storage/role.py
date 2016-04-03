class Role:
    def __init__(self, path, users=set()):
        self.path = path
        self.users = users

    def __eq__(self, other):
        return self.path == other.path and \
               self.users == other.users

    def __str__(self):
        return 'Role {{ path={0} users={1} }}'.format(self.path, self.users)

    def __hash__(self):
        return hash(self.path)
