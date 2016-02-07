import six
import apigen
import storjlib
from . version import __version__  # NOQA


class Storjlib(apigen.Definition):

    def __init__(self, quiet=False, debug=False, verbose=False, noisy=False,
                 config=storjlib.common.CONFIG_PATH):
        if isinstance(config, dict):
            storjlib.config.validate(config)
            self._cfg = config
        else:
            self._cfg = storjlib.config.get(path=config)

    @apigen.command()
    def contract_validate(self, contract):
        # TODO validate input
        return storjlib.contract.validate(contract)

    @apigen.command()
    def contract_sign(self, contract, key):
        raise NotImplementedError()

    @apigen.command()
    def contract_is_complete(self, contract):
        raise NotImplementedError()

    @apigen.command()
    def audit_validate(self, proof, root, challengenum, leaves):

        # validate input
        assert(isinstance(proof, list))
        assert(storjlib.util.is_hex_hash(root))
        assert(isinstance(leaves, list))
        for leaf in leaves:
            assert(storjlib.util.is_hex_hash(leaf))
        assert(isinstance(challengenum, six.integer_types))
        assert(0 <= challengenum < len(leaves))

        return storjlib.audit.validate(proof, root, challengenum, leaves)

    @apigen.command()
    def audit_perform(self, shardid, leaves, challenge):
        raise NotImplementedError()

    @apigen.command()
    def audit_prepare(self, shardid, challenges):
        raise NotImplementedError()

    @apigen.command()
    def store_add(self, shard_path):
        shard = open(storjlib.util.full_path(shard_path), "rb")
        storjlib.store.manager.add(self._cfg["storage"], shard)
        return storjlib.store.shard.get_id(shard)


if __name__ == "__main__":
    apigen.run(Storjlib)
