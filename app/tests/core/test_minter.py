from core.minter import mint_new_noid

def test_get_noid():
    n = 0
    assert mint_new_noid(n=n) == '00000000'
    n = n+1
    assert mint_new_noid(n=n) == '00000017'

def test_get_noid_with_naa():
    n = 0
    assert mint_new_noid(n=n, naa='id') == 'id/00000000'
    n = n+1
    assert mint_new_noid(n=n, naa='id') == 'id/00000017'