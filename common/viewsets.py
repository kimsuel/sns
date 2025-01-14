class MappingViewSetMixin(object):
    serializer_action_classes = {}

    def get_serializer_class(self):
        if self.serializer_action_classes.get(self.action, None):
            return self.serializer_action_classes[self.action]
        return self.serializer_class
