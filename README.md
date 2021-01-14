# Overview

Repository d'une application permettant de récupérer les dons d'une chaîne YouTube sous la forme d'une liste de JSONs. Cette application s'appuie essentiellement sur les applications suivantes :
 * [chat-replay-downloader](https://github.com/xenova/chat-replay-downloader) de Xenova
 * [youtube-dl](https://github.com/ytdl-org/youtube-dl)
 * [Currency Converter](https://pypi.org/project/CurrencyConverter/)


<img src="img/chatmoney.PNG" width="579">


# Environnement Python

L'application tourne sur un environnement python. Les commandes suivantes vous permette de créer l'environnement `music`:

```
git clone https://github.com/hansglick/chat.git

conda env create -f environment.yml
conda activate music
```


# **L'application Grab Donations**


### **Utilisation**

Il s'agit de l'application principale du repository. Les commandes suivante permettent de récupérer dans le fichier `donations.json` l'ensemble des dons engrangés par la chaîne YouTube [Joey Ingram](https://www.youtube.com/user/joeingram1)

```
conda activate music
(music) bash grab_channel_donations.sh https://www.youtube.com/user/joeingram1 data/donations.json
```

***

### **Structure des données récupérées**

Le fichier de sortie est un json qui contient autant d'éléménts qu'il existe de vidéos.

```python

# Importation du JSON
with open(filename) as json_file: 
    donations = json.load("data/donations.json")

# Affiche les urls des videos de la channel
keys_list = list(donations.keys())
print(keys_list)

# Affiche un résumé des donnations de la video
donations[keys_list[0]]["resume"]

# Affiche les super chat events de la premiere video
donations[keys_list[0]]["messages"]

# Affiche les erreurs de conversions des donations pour la premiere video
donations[keys_list[0]]["errors"]

``` 
 * Structure d'une entrée [resume](https://github.com/hansglick/chat_replay_downloader/blob/master/img/dons_resume.PNG)
 * Structure d'un item de l'entrée [message](https://github.com/hansglick/chat_replay_downloader/blob/master/img/dons_message.PNG)



***

### **Les monnaies**


#### Préalable

Les dons récoltés sont convertis en euros par l'application [Currency Converter](https://pypi.org/project/CurrencyConverter/). Cependant, deux problèmes peuvent survenir : 

 1. Il existe une table des correspondances [currency table](...) qui fait le lien entre le symbole de la monnaie récupérée sur YouTube et le symbole de la monnaie selon la norme [ISO 4217](https://fr.wikipedia.org/wiki/ISO_4217). Afin d'être sûr que les monnaies soient convertis en euros il faut s'assurer que symbole YouTube et son symbole ISO soient présentes dans la table [currency table](...)

 2. Certaines monnaies ne sont pas prises en compte par le package [Currency Converter](https://pypi.org/project/CurrencyConverter/)


#### Remarques

 * Les dons exprimés dans une monnaie non présente dans la table [currency table](...) **ou bien** non prise en compte par l'application [Currency Converter](https://pypi.org/project/CurrencyConverter/) sont convertis en **0€**.

 * Afin de relever les erreurs de conversions éventuelles lors d'un run de l'application. Il suffit de retrouver les messages dont l'entrée `amount_euros` est égal à zéro.

 * Afin de relever les monnaies dont le symbole ISO 4217 est inconnu, on peut regarder les entrées `unknown_youtube_currencies` et `number_of_unknown_donations` dans l'objet `resume` du fichier de sortie. Ils représentent les monnaies dont l'ISO 4217 **doivent** être renseignées dans [currency table](...) et le nombre de dons qui n'ont pas pu être convertis (respectivement) :

 * Les dons sont convertis automatiquement en euros (lorsque les conditions sont remplies). Ils se trouvent dans l'entrée `amount_euros` dans les items contenus dans l'entrée `messages`:



```python

# Importation du JSON
with open(filename) as json_file: 
    donations = json.load("data/donations.json")

# Retrouver les dons n'ayant pas pu être convertis
for k,v in donations.items():
	for msg in v["messages"]:
		if msg["amount_euros"] == 0:
			print(item)

# Les monnaies dont le format ISO 4217 n'est pas renseignée dans la currency table et qui provoqueront des conversions à 0 €
donations[keys_list[4]]["resume"]["unknown_youtube_currencies"]

# Sort le premier don (en euros) de la video n°21 
donations[keys_list[21]["messages"][0]["amount_euros"]]

``` 

# **Applications intermédiaires**

### **Application Grab Channel**

Sous-application de **Grab Donations**. Les commandes suivantes permettent de récupérer des informations sur l'ensemble des vidéos de la chaîne [Joey Ingram](https://www.youtube.com/user/joeingram1). Les résultats sont stockées dans le fichier `joey_ingram_channel.txt`

```
conda activate music
(music) bash app_grab_channel.sh https://www.youtube.com/user/joeingram1 data/joey_ingram_channel.txt
```

***

### **Application Grab Money**

Sous-application de **Grab Donations**. Les commandes suivantes permettent de récupérer les dons récoltés lors des lives des vidéos YouTube dont les URLs sont stockées dans le fichier `urls.txt`. Les résultats sont contenus dans le fichier `donations.json`

```
conda activate music
(music) python app_money.py -u urls.txt -s donations.json
```