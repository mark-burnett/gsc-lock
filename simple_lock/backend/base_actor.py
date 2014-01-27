import abc


class ActorBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def cleanup(self):
        pass

    @abc.abstractmethod
    def list_claims(self, limit, offset, resource, status,
            minimum_ttl, maximum_ttl,
            minimum_active_duration, maximum_active_duration,
            minimum_waiting_duration, maximum_waiting_duration):
        pass

    @abc.abstractmethod
    def create_claim(self, resource, timeout, user_data):
        pass

    @abc.abstractmethod
    def get_claim(self, claim_id):
        pass
