import importlib.util
import pathlib
import sys
import types
import unittest

class Map(dict):
    @classmethod
    def __class_getitem__(cls, item): return cls

class Decorator:
    def __call__(self, fn): return fn
    def payable(self, fn): return fn

class Address(str): pass
class FakeGL:
    Contract = object
    public = types.SimpleNamespace(write=Decorator(), view=Decorator())
    evm = types.SimpleNamespace(contract_interface=lambda cls: cls)
    message = types.SimpleNamespace(sender_address=Address('sponsor'), value=100)
    vm = types.SimpleNamespace(run_nondet_unsafe=lambda leader, validator: {'severity':'HIGH', 'confidence':90, 'rationale':'example', 'acquired_code':'source'})

module = types.ModuleType('genlayer')
module.gl = FakeGL
module.TreeMap = Map
module.Address = Address
module.u64 = module.u256 = module.u8 = int
sys.modules['genlayer'] = module
spec = importlib.util.spec_from_file_location('bounty_contract', pathlib.Path(__file__).with_name('contract.py'))
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)

class ReplayTests(unittest.TestCase):
    def setUp(self):
        FakeGL.message.sender_address = Address('sponsor')
        self.app = contract.AutonomousBugBountyArbiter()
        for name, annotation in type(self.app).__annotations__.items():
            if getattr(annotation, '__name__', None) == 'Map': setattr(self.app, name, Map())
        self.app.create_bounty_pool('project', 'https://example.org/code', 'scope', 100)

    def test_authorization_and_permanent_per_pool_reservation(self):
        FakeGL.message.sender_address = Address('attacker')
        with self.assertRaises(AssertionError): self.app.authorize_reporter(1, Address('attacker'))
        with self.assertRaises(AssertionError): self.app.submit_vulnerability_report(1, 'title', 'proof')
        FakeGL.message.sender_address = Address('sponsor')
        self.app.authorize_reporter(1, Address('researcher'))
        FakeGL.message.sender_address = Address('researcher')
        self.assertEqual(self.app.submit_vulnerability_report(1, 'title', 'proof'), 1)
        with self.assertRaises(AssertionError): self.app.submit_vulnerability_report(1, 'rewritten title', 'different proof')
        self.app.adjudicate_report(1)
        self.assertEqual(self.app.claimable_balances['researcher'], 50)
        with self.assertRaises(AssertionError): self.app.adjudicate_report(1)
        with self.assertRaises(AssertionError): self.app.submit_vulnerability_report(1, 'another title', 'another proof')
        self.assertEqual(self.app.claimable_balances['researcher'], 50)
        self.assertEqual(self.app.locked_bounty_pools['1'], 50)

    def test_pending_or_rejected_report_still_blocks_replay(self):
        self.app.authorize_reporter(1, Address('researcher'))
        FakeGL.message.sender_address = Address('researcher')
        self.app.submit_vulnerability_report(1, 'title', 'proof')
        self.app.report_statuses['1'] = 2
        with self.assertRaises(AssertionError): self.app.submit_vulnerability_report(1, 'new title', 'new proof')
        FakeGL.message.sender_address = Address('sponsor')
        with self.assertRaises(AssertionError): self.app.authorize_reporter(1, Address('someone else'))

    def test_other_pool_can_accept_an_independent_report(self):
        self.app.authorize_reporter(1, Address('researcher'))
        self.app.create_bounty_pool('project', 'https://example.org/code', 'scope', 100)
        self.app.authorize_reporter(2, Address('researcher'))
        FakeGL.message.sender_address = Address('researcher')
        self.assertEqual(self.app.submit_vulnerability_report(1, 'a', 'proof'), 1)
        self.assertEqual(self.app.submit_vulnerability_report(2, 'b', 'proof'), 2)

    def test_sponsor_refund_is_blocked_while_pending_and_excludes_claimable(self):
        transfers = []
        contract._Beneficiary = lambda address: types.SimpleNamespace(emit_transfer=lambda value: transfers.append((address, value)))
        self.app.authorize_reporter(1, Address('researcher'))
        FakeGL.message.sender_address = Address('researcher')
        self.app.submit_vulnerability_report(1, 'title', 'proof')
        with self.assertRaises(AssertionError): self.app.close_bounty_pool(1)
        FakeGL.message.sender_address = Address('sponsor')
        with self.assertRaises(AssertionError): self.app.close_bounty_pool(1)
        self.app.adjudicate_report(1)
        self.assertEqual(self.app.close_bounty_pool(1), 50)
        self.assertEqual(transfers, [(Address('sponsor'), 50)])
        self.assertEqual(self.app.claimable_balances['researcher'], 50)
        with self.assertRaises(AssertionError): self.app.close_bounty_pool(1)

if __name__ == '__main__': unittest.main()

