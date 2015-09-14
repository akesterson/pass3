import nose
import pass3.encryption
import pass3.config
import pass3.exceptions
from nose.tools import assert_raises

def test_encrypt_decrypt_goodpass():
    (public, private) = pass3.encryption.generate_keypair(passphrase='testing')
    cfg = pass3.config.get_config()
    cfg['encryption']['public_key'] = public
    cfg['encryption']['private_key'] = private
    (goodcipher, goodmessage) = pass3.encryption.encrypt_message('test phrase', 'testing')
    assert(goodmessage != 'test phrase')
    
    assert_raises(ValueError, pass3.encryption.decrypt_message, goodmessage, goodcipher, 'wrongpassphrase')
    assert(pass3.encryption.decrypt_message(goodmessage, goodcipher, 'testing') == 'test phrase')
    pass3.config._cfg = None

def test_encrypt_decrypt_badpass():
    (public, private) = pass3.encryption.generate_keypair(passphrase='testing')
    cfg = pass3.config.get_config()
    cfg['encryption']['public_key'] = public
    cfg['encryption']['private_key'] = private
    (badcipher, badmessage) = pass3.encryption.encrypt_message('test', 'wrongpassphrase')
    (goodcipher, goodmessage) = pass3.encryption.encrypt_message('test', 'testing')
    assert(badmessage != 'test phrase')

    assert_raises(ValueError, pass3.encryption.decrypt_message, goodmessage, goodcipher, 'wrongpassphrase')
    assert(pass3.encryption.decrypt_message(badmessage, badcipher, 'testing') != 'test phrase')
    pass3.config._cfg = None
