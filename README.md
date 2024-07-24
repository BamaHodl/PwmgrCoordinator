# Use the SeedSigner as an air-gapped password manager

Your seed serves as the encryption/decryption key using ECIES and the data is transmitted to and from this coordinator in encrypted format only.

The ECIES functionality was copied from Electrum wallet's "Encrypt/Decrypt Message" functionality and works exactly the same way.

It is safe to store the encrypted data anywhere--even in cloud storage or a webmail service.  The PWMgr contents can only be decrypted with the seed that was used to encrypt it.

This is not an officially supported feature of the SeedSigner and thus the SeedSigner build (or emulator) must use the forked branch [here](https://github.com/BamaHodl/seedsigner/tree/PasswordManager)

* Brief demonstration [(demo video here)](https://youtu.be/2L99mucvZrg)
* This coordinator requires opencv-python and qrcode to be installed.  Simply run `pip3 install -r requirements.txt` in the PwmgrCoordinator dir to install them
* An example encrypted data file is included in this repository as encrypted_message.txt
   - The seed used to encrypt/decrypt it is included in example_seed.txt and example_seedqr.png for convenience
* To create a new PWMgr data - simply go to Tool->Password Manager and select New PWMgr
* To load an existing encrypted PWMgr file run `pwmgr_sender.py -f <filename>`
  - e.g. `python3 ./pwmgr_sender.py -f example_encrypted.txt` to load the provided example data
  - Scan it as you would any other QR input from the main Scan screen
  - Select the seed to be used to decrypt it--for the example_encrypted.txt included it can be decrypted with the provided example seed.
* To save the encrypted PWMgr file from the SeedSigner, run `pwmgr_receiver.py -f <filename>`
  - In the main PWMgr screen, select Export Encrypted and select/load the seed that will be used to encrypt it
  - Scan and save the encrypted PWMgr data by running `python3 ./pwmgr_receiver.py -f new_encrypted.txt`

