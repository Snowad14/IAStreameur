<h1 align="center">AIStreameur</h1>

AIStreameur est un projet GitHub qui vous permet de faire diffuser en direct vos personnes préférées ! En utilisant la puissance de l'intelligence artificielle, ce projet combine GPT pour le texte, ElevenLabs pour la voix et Wav2Libs pour créer une personnalité réaliste !

## Screenshot 🤩

![AIStreameur web screenshot](https://i.imgur.com/EnR7lRJ.jpg)

## Installation 🖥️

Vous devez avoir une carte graphique **NVIDIA**  
Installer **conda ou Miniconda** : [direct link](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) ou un [tuto youtube](https://www.youtube.com/watch?v=P17GY1gSnFk&t=120s)   
Installer **cuda**, de préférence une version assez nouvelle genre 11.8, [tuto youtube](https://www.youtube.com/watch?v=ctQi9mU7t9o) 
Installer **python >= 3.6**, [tuto youtube](https://www.youtube.com/watch?v=3nrCgMTDTdY)   
Crée un **environnement anaconda** : ```conda create -n IASpeaker```, puis on l'active ```conda activate -n IASpeaker```  
Installer **pytorch avec cuda** : ```pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```   
**Télécharger le .zip du repo** et extrayer le, ouvrez le pour enfin éxécuter la commande ```pip install -r requirements.txt```  
Maintenant il faut **télécharger les modèles d'IA :** [wav2lip.pth](https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels%2Fwav2lip%2Epth&parent=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels&ga=1) dans ```IA_Speaker\simpleWav2Lip\checkpoints``` et [s3fd-619a316812.pth](https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth) renommé en ```s3fd.pth``` dans ```IA_Speaker\simpleWav2Lip\face_detection\detection\sfd```  
**Crée le fichier** : ```IA_Speaker/.env``` avec vos clée api, le pseudo du streamer, le **nom de la voix** que vous avez crée sur le panel d'ElevenLabs, comme ceci :   
```bash
ELEVENLABS_KEY = "VOTRE_CLE_ELEVENLABS"
OPENAI_KEY = "VOTRE_CLE_OPENAI"
TWITCH_TOKEN = "VOTRE_OAUTH_TWITCH"
ELEVENLABS_VOICE="Macron"
STREAMER_PSEUDO="squeezie"
```  
**Ensuite**, vous allez ajouté vos vidéo en format **mp4** de la personne voulu dans ```IA_Speaker\simpleWav2Lip\sample_data\videos```.  
**N'oubliez pas**, d'ajouter vos vidéos en format **mp4** de quelque chose pour combler le stream pendant la génération de la vidéo, mettez la dans ```IA_Speaker\flaskServer\static\waiting```.  
Enfin, vous allez **modifier votre raccourcie chrome** pour y ajouter ```--autoplay-policy=no-user-gesture-required```  
**Avant de lancez**, pour rendre la génération **10x plus rapide**, vous devez mettre en cache l'output du detector, pour se faire, vous devez ouvrir un terminal dans le dossier ```simpleWav2Lip``` pour ensuite faire un ```python cacheVideo.py```, vous devrez **refaire cette opération** a chaque fois que vous modifier ou ajouter une vidéo !     
Il ne vous reste plus que lancez les **programmes python dans 2 terminal différent :** ```python server.py``` dans ```IA_Speaker\flaskServer``` et ```python main.py```   
Libre a vous de modifier le fichier ```base.css``` pour **modifier ou ajouter des choses a l'overlay**, j'ai fait très simple avec juste la question


## TODO 📝

- [ ]  Ajouter LLama ou au moins une alternative gratuite a gpt
- [ ]  Ajouter une alternative a 11Labs genre VITS+RVC
- [x]  Speed Up Wav2Lips

## Remerciements

- twitch.tv/ask_jesus pour l'idée du projet
- twitch.tv/defendintelligence pour l'idée d'utiliser un server web

