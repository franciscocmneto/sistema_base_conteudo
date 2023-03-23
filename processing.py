import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm


books = pd.read_csv("new_books_genres.csv") #faz a leitura do arquivo csv

books = books.dropna() #retira as linhas que possuem celulas nulas

def find_book_index(book_name):
    try:    
        book_index = books[books['title'] == book_name].index[0]
    
    except ValueError:
        print("invalid input to function")

    return book_index

def processing(book_liked):
    genre_list = []
    vector_list = []
    knn6 = []
    knn_recomendations = []

    #faz a limpeza das strings contidas na coluna "genres" para a retirada de  "{,}, espacos" e separar a string em listas de strings
    books['genres'].str.replace(' ','')
    books['genres'] = books['genres'].apply(lambda x: x.replace('{', '') if isinstance(x, str) else x)
    books['genres'] = books['genres'].apply(lambda x: x.replace('}', '') if isinstance(x, str) else x)
    books['genres'] = books['genres'].apply(lambda x: x.replace("'", "") if isinstance(x, str) else x)
    books['genres'] = books['genres'].apply(lambda x: x.split(',') if isinstance(x, str) else x)

    #atribui a coluna para uma variavel para melhor manipulacao
    genre_column = books['genres']

    #adiciona a uma lista todos as categorias de genero presentes nesse dataset, sem repetir categorias. 
    for cells in genre_column:
        for item in cells:
            item = item.strip()
            if item not in genre_list:
                genre_list.append(item)

    #cria um vetor com o mesmo tamanho da lista das categorias e compara o genero de cara livro com a lista de categorias de genero
    #quando o genero for igual ao presente na lista, é atribuido 1 ao index, assim, é gerado um vetor de comparacao para cada um dos livros
    for cell in genre_column:
        vector = [0]*100
        for genre in genre_list:
            for item in cell:
                item = item.strip()
                if genre == item:
                    vector[genre_list.index(genre)] = 1
        vector_list.append(np.array(vector))

    #cria uma nova coluna no dataframe contendo esse vetor de comparacao 
    books['vector_genre'] = vector_list

    #aqui acaba o periodo de pre-processamento dos dados e se inicia o processamento para determinar o KNN

    genre_score_vector = books['vector_genre']

    #encontra o index o livro que o usuario gostou
    position_book_liked = find_book_index(book_liked)

    vector_book_liked = genre_score_vector[position_book_liked]
    
    knn6.append(position_book_liked)

    vector_distance = []
    i = 0
    #calcula a distancia euclidiana para cara livro em relacao ao livro que o usuario gostou
    
    for item in genre_score_vector:
        #distance = np.linalg.norm(item - vector_book_liked)
        
        
        dot_product = np.dot(vector_book_liked, item)
        norm_a = np.linalg.norm(vector_book_liked)
        norm_b = np.linalg.norm(item)

        cos_sim = dot_product / (norm_a * norm_b)
        
        vector_distance.append([cos_sim,i])
        i+=1

    sorted_vector_distance = sorted(vector_distance)

    
    #atribui a um vetor, as posicoes dos livros que estao no knn = 6
    for item in sorted_vector_distance:
        if item[1] not in knn6:
            knn6.append(item[1])
        if len(knn6) == 6:
            break
    
    #retira o primeiro item do knn pois é mesmo index do livro dado como entrada
    knn6.pop(0)

    for item in knn6:
        item2 = int(item)
        row = books.loc[item2]
        knn_recomendations.append(row[0])

    print(knn_recomendations)
    return knn_recomendations

if __name__ == '__main__':

    #book_liked = input("informe um livro que vc gostou \n")
    
    processing('the warriors')
   