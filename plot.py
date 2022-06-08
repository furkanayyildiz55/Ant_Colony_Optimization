import operator
from xml.etree.ElementTree import tostring
import matplotlib.pyplot as plt 


def plot(points, path: list , iteration ,min_cost ):
    """
    :param points: Yolu oluşturan noktalar
    :param path: Aco ile bulunan en kısa yol
    :param points: Yolu oluşturan noktalar
    :param path: Aco ile bulunan en kısa yol

    :param points: The points that make up the path
    :param path: Shortest path found with aco
    :param points: The points that make up the path
    :param path: Shortest path found with aco

    """

    x = []
    y = []
    for point in points:
        print( "Nokta: {} X Ekseni {} Y Ekseni {}" .format(point[0] , point[1] , point[2] )  )
        x.append(point[1])
        y.append(point[2])

    plt.plot(x, y, 'co')

    #Noktalar oluşturuluyor
    for point in points:
        plt.annotate( point[3] ,(point[1],point[2]))

    #Noktalar arası çizgiler
    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]

        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)


    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)


    plt.text(0, 0, f'İterasyon:{iteration}  Min Maliyet = {round(min_cost,2)}', family='fantasy', fontsize=12,style='italic',color='mediumvioletred')
    plt.title("Karınca Kolonisi Optimizasyonu")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("Rota.png")
    plt.show()
