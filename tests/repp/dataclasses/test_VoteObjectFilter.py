from rep.dataclasses.VoteObjectFilter import VoteObjectFilter

def test_itFailsToBuildIfNoFieldsAreSpecified():
    try:
        VoteObjectFilter()
        assert False
    except ValueError as _:
        pass
