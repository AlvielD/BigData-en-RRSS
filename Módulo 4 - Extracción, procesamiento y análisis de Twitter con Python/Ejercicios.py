import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
import collections
import seaborn as sns

# Añadir las claves (Yo las quito para evitar problemas con mi cuenta de desarrolador)
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#Para OAuth 1.0 (Objeto con mis credenciales)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Conexión a la API
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

"""

    Tarea 1

    Diseñar un script para descargar, mediante la función api.search(), los 500 últimos tweets
    (excluyendo los RT) y guardar el resultado en un dataframe, que tendrá 4 columnas con la siguiente
    información:

        Fecha del tweet
        Nombre del usuario que lo ha escrito
        Texto completo del tweet
        Número de retweets que ha tenido el tweet

    Los criterios de búsqueda serán:

        Que contengan las palabras "ONG" o "inmigrante"
        Que sean del día 28 de enero de 2021
        Que estén escritos en castellano

    A partir del dataframe, generar una gráfica de barras que muestre los 5 usuarios que más tweets
    han escrito en el conjunto descargado.

"""

datos = []        # Tabla a convertir en dataframe
num_tweets = 500  # Número de tweets a buscar

# Parámetros de la búsqueda que vamos ha realizar
tweetsBuscados = tweepy.Cursor(api.search,
                               q="ONG" or "inmigrante",
                               tweet_mode="extended",
                               lang="es",
                               since="2021-01-28",
                               until="2021-01-29",
                               excluded_replies = True,
                               include_rts = False).items(num_tweets)

for tweet in tweetsBuscados:
    datos.append([tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.retweet_count])

# Transformamos la tabla en un dataframe y lo mostramos por pantalla
datos = pd.DataFrame(datos, columns = ["Fecha", "Nombre_Usuario", "Tweet", "RTs"])
datos

# Creamos una lista que almacenará los usuarios
usuarios = []

# Recorremos el dataframe almacenando cada usuario en la lista
for i in datos.index:
    usuarios.append(datos["Nombre_Usuario"][i])
    
# Creamos una colección que cuente las veces que aperece el usuario en el dataframe, es decir, el número de
# veces que ha tuiteado sobre el tema
n_tweets = collections.Counter(usuarios).most_common(5)

# Guardamos cada dato de la colección en una lista separada para posteriormente graficar los resultados
listaUsers = []
listaTweets = []
for usuario, tweets in n_tweets:
    listaUsers.append(usuario)
    listaTweets.append(tweets)
print(listaUsers)
print(listaTweets)

fig, ax = plt.subplots()
# Ponemos una etiqueta al eje Y
ax.set_ylabel("Número de Tweets")
# Ponemos una etiqueta al eje X
ax.set_xlabel("Usuario")
# Ponemos los nombres de usuario en vertical para que quepan
plt.xticks(rotation="vertical")
# Sacamos la gráfica por pantalla
sns.barplot(x=listaUsers, y=listaTweets,  edgecolor="black", linewidth=1)

"""

    Tarea 2 (opcional)

    El script "Tarea2.ipynb" (está en la sección "Otros recursos") realiza, mediante streaming,
    una descarga de tweets y almacena, en un fichero csv, 4 campos (la fecha del tweet, el screen_name
    del autor, el texto del tweet y los hashtags).

    Modificarlo para que, además, recupere y almacene el nombre completo del usuario y su localización.
    
"""
class MiListener(tweepy.StreamListener):
    
    def __init__(self, api=None):
        #super().__init__()
        self.counter = 0
        self.limit = 10
    
    def on_connect(self):
        print("Conexión correcta!!!!")
             
    def on_data(self, data):
        
        status = json.loads(data)
        
        ###### Este bloque es para recuperar, correctamente, el texto del tweet #################################
        if 'text' in status:
            text = status['text']
        if 'extended_tweet' in status:
            text = status['extended_tweet']['full_text']
        if 'retweeted_status' in status:
            status_RT = status['retweeted_status']
            if 'text' in status_RT:
                text = 'RT @' + status['retweeted_status']['user']['screen_name'] + status_RT['text']    
                if 'extended_tweet' in status_RT:
                    extended_RT = status_RT['extended_tweet']
                    text = 'RT @' + status['retweeted_status']['user']['screen_name'] + extended_RT['full_text']
        ###### Este bloque es para recuperar, correctamente, el texto del tweet #################################
        
        
        ###### Para recuperar los hashtags que están dentro de una estructura de tipo diccionario #############
        hashtags = []
        for hashtag in status['entities']['hashtags']:
            hashtags.append(hashtag['text'])
        ###### Para recuperar los hashtags que están dentro de una estructura de tipo diccionario #############
        
        
        #### Este bloque sirve para almacenar alguna información del tweet en un fichero csv
        #### En este caso la fecha "status['created_at']",el screen_name del autor "status['user']['screen_name']",
        #### el texto del tweet "text.replace("\n", "")" y los hashtags "hashtags"
        #### Modificarlo para que también añada el nombre completo del autor y su localización
        # status["user"]["name"] --> Nombre completo del usuario
        # status["user"]["location"] --> Localización
        # añadimos %s por cada variable añadida al fichero y \t por cada separación de elementos
        with open("Tarea2.csv", "a", encoding='utf-8') as f:
            f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (status['created_at'],status['user']['screen_name'],status["user"]["name"],
                                              status["user"]["location"],text.replace("\n", ""), hashtags))
        
        self.counter += 1
        if self.counter < self.limit:
            return True
        else:
            return False

    def on_error(self, status_code):
        print("Error", status_code)
        

listener = MiListener(api=tweepy.API(wait_on_rate_limit=True, wait_on_rate_limit_notify=True)) 
MiStreamer = tweepy.Stream(auth=auth, listener=listener)

MiStreamer.filter(track = ['immigrant'])

dfStream = pd.read_csv('Tarea2.csv', sep='\t', encoding = 'UTF-8', header = None)
dfStream.columns = ['Fecha','Autor','Nombre_Completo','Location','Tweet','Hashtags']
dfStream.shape
dfStream