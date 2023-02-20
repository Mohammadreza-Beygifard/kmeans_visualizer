import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

class Point:
    def __init__(self, x, y, color = "blue"):
        self.x = x
        self.y = y
        self.color = color

    def EucDist(self, point):
        x = self.x - point.x
        y = self.y - point.y
        return np.sqrt(x**2 + y**2)

    def Show(self, ax):
        ax.scatter(self.x, self.y, color=self.color)

class DataPoint(Point):
    def __init__(self, x, y, color = "blue"):
        super().__init__(x, y, color)
        self.centroid = Point(0, 0, "blue")

    def Show(self, ax):
        ax.scatter(self.x, self.y, color=self.color)

class Centroid(Point):
    def __init__(self, x, y, color = "red"):
        super().__init__(x, y, color)
        self.data_points = []

    def AssignDataPoint(self, data_point):
        self.data_points.append(data_point)

    def Show(self, ax, iteration):
        ax.scatter(self.x, self.y, s=200, color=self.color, marker="+")
        ax.text(self.x+.03, self.y+.03, str(iteration), fontsize=9)


class Kmeans:
    def __init__(self, x_min, x_max, y_min, y_max, num_clusters):
        self.colors = ["red", "black", "pink", "purple","olive"]
        self.iteration = 0
        self.max_iterations = 1000
        self.x_min = x_min
        self.x_max = x_max        
        self.y_min = y_min
        self.y_max = y_max
        self.plt_border = 1
        self.data_points = []
        self.centroids = []
        self.epsilon = 0.01
        self.centroid_finished_counter = 0
        self.num_clusters = num_clusters
        self.finished = False
        self.fig, self.ax = plt.subplots(figsize=(12,8))

    def InitializePoints(self, num_points):
        x_list = (self.x_max - self.x_min) * np.random.random_sample(num_points) + self.x_min
        y_list = (self.y_max - self.y_min) * np.random.random_sample(num_points) + self.y_min

        for index in range(x_list.size):
            self.data_points.append(DataPoint(x_list[index], y_list[index]))
    
    def InitializeCentroids(self, num_centroids):
        x_list = (self.x_max - self.x_min) * np.random.random_sample(num_centroids) + self.x_min
        y_list = (self.y_max - self.y_min) * np.random.random_sample(num_centroids) + self.y_min

        for index in range(x_list.size):
            self.centroids.append(Centroid(x_list[index], y_list[index], self.colors[index%len(self.colors)]))

    def DefinePoints(self, data_points):
        self.data_points = data_points

    def DefineMeanPoints(self, centroids):
        self.centroids = centroids

    def AssignDataPointsToNearestCluster(self):
        for data_point in self.data_points:
            dist = data_point.EucDist(self.centroids[0])
            self.centroids[0].AssignDataPoint(data_point)
            data_point.color = self.centroids[0].color
            for centroid in self.centroids:
                dist_tmp = data_point.EucDist(centroid)
                if(dist_tmp < dist and centroid is not self.centroids[0]):
                    dist = dist_tmp
                    if(self.centroids[0].data_points.count(data_point) > 0):
                        self.centroids[0].data_points.remove(data_point)
                    centroid.AssignDataPoint(data_point)
                    data_point.color = centroid.color
    
    def ReInitializeCentroids(self):
        new_centroids = []
        self.centroid_finished_counter = 0
        for centroid in self.centroids:
            data_points = centroid.data_points
            x = 0
            y = 0
            for data_point in data_points:
                x += data_point.x
                y += data_point.y
            if(len(data_points) == 0):
                return
            x /= len(data_points)
            y /= len(data_points)
            new_centroid = Centroid(x,y, centroid.color)
            dist = centroid.EucDist(new_centroid)
            if(dist < self.epsilon):
                self.centroid_finished_counter += 1
            new_centroids.append(new_centroid)
        self.centroids = new_centroids
        if (self.centroid_finished_counter >= len(self.centroids)):
            self.finished = True

    def MakeClusters(self):
        self.InitializeCentroids(self.num_clusters)
        self.Show()

    def Show(self):
        # self.fig = plt.figure(figsize=(12,8))
        # self.ax.clear()
        self.ax.set_xlim([self.x_min - self.plt_border, self.x_max + self.plt_border])
        self.ax.set_ylim([self.y_min - self.plt_border, self.y_max + self.plt_border])
        for point in self.data_points:
            point.Show(self.ax)
        for point in self.centroids:
            point.Show(self.ax, self.iteration)

    def Animate(self, i):
        while(not self.finished and self.iteration <= self.max_iterations):
            self.iteration += 1
            print(self.iteration)
            self.AssignDataPointsToNearestCluster()
            self.ReInitializeCentroids()
            self.Show()
        self.anim.event_source.stop()
        if(self.iteration > self.max_iterations):
            print("K-means did not converge")
    
    def Run(self):
        self.MakeClusters()
        self.anim = animation.FuncAnimation(self.fig, self.Animate, interval=1000)
        plt.show()






p1 = DataPoint(0, 0)
p2 = DataPoint(0, 1)
p3 = DataPoint(1, 0)
p4 = DataPoint(1, 1)

p10 = DataPoint(10, 10)
p20 = DataPoint(10, 11)
p30 = DataPoint(11, 10)
p40 = DataPoint(11, 11)

m1 = Centroid(5,5, "red")
m2 = Centroid(7,7, "black")

p_list = [p1, p2, p3, p4, p10, p20, p30, p40]


k = Kmeans(0, 20, 0, 20, 3)
k.InitializePoints(20)
# k.DefinePoints(p_list)
# k.DefineMeanPoints([m1, m2])
k.Show()

# k.AssignDataPointsToNearestCluster()
# k.Show()

# k.ReInitializeCentroids()
# k.Show()

# k.MakeClusters()
k.Run()
k.Show()
plt.show()