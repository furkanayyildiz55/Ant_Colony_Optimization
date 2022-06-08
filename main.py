import math
import string

from aco import ACO, Graph  #Aco algoritmasını çalıştıracak yapı ##The structure to run the Aco algorithm
from plot import plot       #Algoritma çıktısını görselleştirmek için eklenen yapı ##Added structure to visualize the algorithm output


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    cities = []
    points = []
    #Gidilecek noktaların çekildiği veri dosyasından veriler çekiliyor ##Data is extracted from the data file from which the destinations are drawn
    with open('./data/data0.txt' ,encoding="utf8") as f:
        for line in f.readlines():
            city = line.split('-')
            cities.append(dict(index=float(city[0]), x=float(city[1]), y=float(city[2])))
            points.append((float(city[0]) ,float(city[1]), float(city[2]),  (city[3]) ))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    
    ant_count=10  #Modeldeki karınca sayısı
    iteration=500 #Modelin generasyon  sayısı
    alpha=1.0     #feromon seviyesinin formüle etkisi
    beta=10.0     #maliyetin formüle etkisi
    rho=0.5       #feromon buharlaşma oranı
    q=10          #feromon yoğunluğu

    aco = ACO(ant_count, iteration, alpha, beta, rho, q, 2) #ACO sınıfından aco nesnesini ilk değerlerini vererek üretiyoruz ##We generate the aco object from the ACO class by giving its initial values
    graph = Graph(cost_matrix, rank) #aco nesnsinin çözmesi için graph oluşturuyoruz ##We create a graph for the aco object to solve
    path, cost = aco.solve(graph) #aco.solve ile problemimizi çözüyoruz ##We solve our problem with aco.solve
    

    pathPrint=[]
    for i in path:
        pathPrint.append(i+1)
    print('Path: {}'.format(pathPrint))
    print('Cost: {}'.format(cost)) #Maliyet ve En kısa yolu yazdırıyoruz ##We print Cost and Shortest path


    plot(points, path ,iteration , cost  )  #En kısa yol rotasını çizdiriyoruz ##We draw the shortest route





if __name__ == '__main__':
    main()
