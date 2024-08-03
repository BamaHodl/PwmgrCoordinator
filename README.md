# Use the SeedSigner as an air-gapped password manager and secure messenger

Your seed serves as the encryption/decryption key using ECIES and the data is transmitted to and from this coordinator in encrypted format only.

The ECIES functionality was copied from Electrum wallet's "Encrypt/Decrypt Message" functionality and works exactly the same way.

It is safe to store the encrypted data anywhere--even in cloud storage or a webmail service.  The encrypted contents can only be decrypted with the seed that was used to encrypt it.

This is not an officially supported feature of the SeedSigner and thus the SeedSigner build (or emulator) must use the forked branch [here](https://github.com/BamaHodl/seedsigner/tree/PasswordManager)

## SeedSigner build notes
* This functionality requires pyaes, which is not included in the latest seedsigner-os.  If you are building a SD card image based on seedsigner-os, you'll need to add a line to `seedsigner-os/opt/[BOARD_TYPE]/configs/[BOARD_TYPE]_defconfig`
   - For most users this is pi0, so the file to edit is `seedsigner-os/opt/pi0/configs/pi0_defconfig`
   - Add this line to the end of that file: `BR2_PACKAGE_PYTHON_PYAES=y`
* To build the image for pi0 with seedsigner-os and pull from the forked repo branch with this funcionality included, the following should do it:
   - `SS_ARGS="--pi0 --app-repo='https://github.com/BamaHodl/seedsigner.git' --app-branch='PasswordManager'" docker compose up --force-recreate --build`

## Coordinator
* This coordinator requires opencv-python and qrcode to be installed.  Simply run `pip3 install -r requirements.txt` in the PwmgrCoordinator dir to install them
 
## Password Manager
* Brief demonstration of the Password Manager [(demo video here)](https://youtu.be/2L99mucvZrg)
* An example encrypted PWMgr data file is included in this repository as encrypted_pwmgr.txt
   - The seed used to encrypt/decrypt it is included in example_seed.txt and example_seedqr.png for convenience
* To create a new PWMgr data - simply go to Tool->Password Manager and select New PWMgr
* To load an existing encrypted PWMgr file run `pwmgr_sender.py -f <filename>`
  - e.g. `python3 ./pwmgr_sender.py -f example_pwmgr.txt` to load the provided example data
  - Scan it as you would any other QR input from the main Scan screen
  - Select the seed to be used to decrypt it--for the example included it can be decrypted with the provided example seed.
* To save the encrypted PWMgr file from the SeedSigner, run `pwmgr_receiver.py -f <filename>`
  - In the main PWMgr screen, select Export Encrypted and select/load the seed that will be used to encrypt it
  - Scan and save the encrypted PWMgr data by running `python3 ./pwmgr_receiver.py -f new_encrypted.txt`

## Secure Messenger
* A pubkey is used to encrypt a message, and only the seed associated with that pubkey can be used to decrypt it
* The general idea is you export the pubkey from your own seed and share it with your communication partner, and the communication partner exports the pubkey from their seed and shares it with you.  Then you can send messages to them encrypted with their pubkey, and they can send messages to you encrypted with your pubkey.  The encrypted messages can then be sent back and forth across an insecure communication channel without any chance of interception of the decrypted contents since only the seed that exported the pubkey can be used to decrypt the contents.
* To export the pubkey for a seed, go to Tools->Secure Messenger->Export Pubkey.  Then you can load or select the seed whose pubkey you want to export and it will be displayed on the screen.
* It can be saved by receiving with the same pwmgr_receiver.py by for example `python3 ./pwmgr_receiver.py -f mypubkey.txt`
* An example encrypted message data file is included in this repository as encrypted_message.txt
   - The seed used to encrypt/decrypt it is included in example_seed.txt and example_seedqr.png for convenience
* To load an existing encrypted message, run `pwmgr_sender.py -f <filename>`
  - e.g. `python3 ./pwmgr_sender.py -f example_message.txt` to load the provided example message
  - Scan it as you would any other QR input from the main Scan screen
  - Select the seed to be used to decrypt it--for the example included it can be decrypted with the provided example seed.
* To create an encrypted message, first scan the pubkey of the counterparty
  - This can be displayed to the SeedSigner with `python3 ./pwmgr_sender.py -f <pubkey_file>`
    - It uses a single frame QR so that you can print it out for re-use and to avoid the risk that the PC you're running the coordinator from is somehow compromised and the counterparty's pubkey is replaced with a pubkey of an attacker wishing to see what messages you're sending.  This risk can be further offset by verifying the pubkey used to encrypt each message by clicking View after compiling a message.  It displays the message contents that will be encrypted as well as the pubkey that is being used to encrypt it.
  - Once you scan the pubkey QR, you'll be taken to the input dialog for the message.  Input the text of the message, click the check to complete, and then review the message and the pubkey by clicking View.
  - If you're ok with the message you entered, click Export to export the encrypted data, similar to how you would for the Password Manager
  - Receive the encrypted message from the SeedSigner with `python3 ./pwmgr_receiver.py -f <send_message_filename>`
  - You can now share that encrypted message contents with the counterparty who gave you the pubkey you used to encrypt it
