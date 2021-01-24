### ESTE SCRIPT NOS PERMITIRÁ SABER QUE TWEETS CON EL NOMBRE DE LA APLICACIÓN
### "MOZILLA THUNDERBIRD" HAN SIDO MÁS FAVEADOS.

# Primero activamos las librerías necesarias
library(rtweet)
library(tidyverse)

# Guardamos nuestras claves en variables
api_key <- "n0zihT8RhgzbnoQoT02iLGFPp"
api_secret_key <- "Jv72TVss1NBHsDoTezNdybuW1ors0M28u0IHCqCgLzIO8hNKDJ"
access_token <- "1344609429543653377-9RC4xllEhCYOvYpKoF1dG4RO2sTVLT"
access_token_secret <- "QwVL3WjYmV6yECUTBUBZkRbhsvMoDd0jJ6lrCjaQzhKWQ"

# Creamos el token de acceso con nuestras claves
token_acceso <- create_token(
  app = "BigDataUHU",
  consumer_key = api_key,
  consumer_secret = api_secret_key,
  access_token = access_token,
  access_secret = access_token_secret)

# Búscamos los tweets que contengan la palabra "Mozilla thunderbird"
# Thunderbird solo daba demasiados nombres de usuario
thunderbird <- search_tweets("mozilla thunderbird", n=1000, token = token_acceso)
saveRDS(thunderbird, "thunder_database.rds") # Guardamos el resultado como .rds

# Ajustamos los resultados para quitar los retweets y nos quedamos con las columnas
# que nos interesen
thunder_orig <- thunderbird %>%
  filter(is_retweet == "FALSE") %>% 
  select(screen_name, favorite_count,retweet_count, text, hashtags) %>% 
  arrange(desc(favorite_count))

# Agrupamos por nombre de usuario y sacamos la suma de favs y rts
thunder_favs <- thunder_orig %>% 
  group_by(screen_name) %>%
  summarize(tweets = n(),
            favs = sum(favorite_count),
            rts =  sum(retweet_count)) %>%
  arrange(desc(favs))

# Cogemos solos los 5 más faveados
thunder_top <- thunder_favs %>% top_n(5, favs)

# Sacamos la gráfica del resultado
ggplot(thunder_top) + 
  geom_bar(aes(x = reorder(screen_name, favs), y = favs),
           stat = "identity", fill = "yellow") +
  geom_text(aes(label = favs, y = favs, x = screen_name),  
            hjust=.5, size = 3, color = "black") +
  labs(x = "User", y =  "Número de favoritos", title = "Ranking de Favs") +
  coord_flip() 
