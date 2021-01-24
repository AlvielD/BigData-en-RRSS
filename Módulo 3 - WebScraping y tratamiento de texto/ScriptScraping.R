require(tidyverse)
require(rvest)
require(stringr)
require(tidytext)


# Creamos la función para raspar El Diario cuyo nombre será 'scraping_EM()' ------------------------

scrapingWeb <- function (x){
  read_html(x) %>%
  rvest::html_nodes(".ni-title ") %>%     # Llamo a la función html_nodes() y especifico las etiquetas de los títulos 
  rvest::html_text() %>%                  # Llamo a la función html_text() para especificar el formato 'chr' del título.
  tibble::as_tibble() %>%                 # Llamo a la función as_tibble() para transforma el vector en tabla 
  dplyr::rename(titulo = value)           # Llamo a la función rename() para renombrar la variable 'value'
}


# Usamos la función para scrapear El Diario ----------------------------------------------

(El_Diario <- scrapingWeb("https://www.eldiario.es/"))


# Tokenizamos los títulos ---------------------------

El_Diario %>%                                           # Pasamos los datos a formato tabular
  tidytext::unnest_tokens(palabra, titulo) %>%          # Función para tokenizar
  dplyr::count(palabra) %>%                             # Columna de datos a contar
  dplyr::arrange(dplyr::desc(n)) %>%                    # Columna de frecuencia a ordenar en forma decreciente
  dplyr::filter(n > 2) %>% 
  dplyr::filter(!palabra %in% tm::stopwords("es")) %>%  # Filtramos las palabras más comunes del español
  dplyr::filter(palabra != "si") %>%
  dplyr::filter(palabra != "dos") %>%
  dplyr::filter(palabra != "eldiario.es") %>%
  dplyr::filter(palabra != "puede") %>%
  dplyr::filter(palabra != "19") %>%
  dplyr::filter(palabra != "3") %>%
  
  ggplot2::ggplot(ggplot2::aes(y = n, x = stats::reorder(palabra, + n))) + 
    ggplot2::geom_bar(ggplot2::aes(fill = as_factor(n)), stat = 'identity', show.legend = F) + 
    ggplot2::geom_label(aes(label = n), size = 5) + ggplot2::labs(title = "Raspado de \"El Diarío\"", x = NULL, y = "Frecuencia") + 
    ggplot2::coord_flip() + 
    ggplot2::theme_bw() + 
    ggplot2::theme(axis.text.x = ggplot2::element_blank(), axis.text.y = ggplot2::element_text(size = 16), plot.title = ggplot2::element_text(size = 18, hjust = .5, face = "bold", color = "black"))

# Fin del script ----------------------------------------------------------------------------------