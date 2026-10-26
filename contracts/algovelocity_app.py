# PyTeal / Algorand AVM Application
# QMOOSA AlgoVelocity x402 Settlement Gateway
from pyteal import *

def approval_program():
    on_creation = Seq([
        App.globalPut(Bytes("admin"), Txn.sender()),
        App.globalPut(Bytes("total_settled"), Int(0)),
        Approve()
    ])

    settle_payment = Seq([
        Assert(Gtxn[0].type_enum() == TxnType.Payment),
        Assert(Gtxn[0].receiver() == App.globalGet(Bytes("admin"))),
        Assert(Gtxn[0].amount() >= Int(1000)), # Min 0.001 ALGO
        App.globalPut(
            Bytes("total_settled"),
            App.globalGet(Bytes("total_settled")) + Gtxn[0].amount()
        ),
        Approve()
    ])

    return Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.NoOp, settle_payment],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Txn.sender() == App.globalGet(Bytes("admin")))]
    )

def clear_state_program():
    return Approve()

if __name__ == "__main__":
    print(compileTeal(approval_program(), Mode.Application, version=8))
