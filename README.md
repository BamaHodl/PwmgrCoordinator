# Use the SeedSigner as a password manager.

Your seed serves as the encryption/decryption key using ECIES (largely copied from Electrum's encrypt/decrypt message functionality) and the data is transmitted to and from this coordinator in encrypted format only.

It is safe to store the encrypted data anywhere--even in a cloud storage or webmail service.  The PWMgr contents can only be decrypted with the seed that was used to encrypt it.

This is not an officially supported feature of the SeedSigner and thus the SeedSigner build (or emulator) must use the forked branch [here](www.github.com)

* Guided demonstration [(demo video here)](https://youtu.be/)

