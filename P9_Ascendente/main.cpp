#include <bits/stdc++.h>
#include <opencv2/opencv.hpp>
using namespace std;

const int ITERACIONES = 50;
const string FILENAME = "/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/jp2.jpg";

cv::Scalar HSVtoBGR(float H, float S, float V) {
    float C = V * S;
    float X = C * (1 - abs(fmod(H / 60.0, 2) - 1));
    float m = V - C;
    float r, g, b;

    if(H >= 0 && H < 60){
        r = C; g = X; b = 0;
    }
    else if(H >= 60 && H < 120){
        r = X; g = C; b = 0;
    }
    else if(H >= 120 && H < 180){
        r = 0; g = C; b = X;
    }
    else if(H >= 180 && H < 240){
        r = 0; g = X; b = C;
    }
    else if(H >= 240 && H < 300){
        r = X; g = 0; b = C;
    }
    else{
        r = C; g = 0; b = X;
    }

    int B = static_cast<int>((b + m) * 255);
    int G = static_cast<int>((g + m) * 255);
    int R = static_cast<int>((r + m) * 255);

    return cv::Scalar(B, G, R);
}

class Cluster {
public:
    Cluster(size_t index, const cv::Vec3b& individual) : indices{ index }, sumIndividuals(cv::Vec3d(individual)) {
        centroid = individual;
    }

    cv::Vec3b getCentroid() const {
        return centroid;
    }

    double distanceTo(const Cluster& other) const {
        cv::Vec3d diff = cv::Vec3d(centroid) - cv::Vec3d(other.centroid);
        return cv::norm(diff);
    }

    void mergeWith(const Cluster& other) {
        indices.insert(indices.end(), other.indices.begin(), other.indices.end());
        sumIndividuals += other.sumIndividuals;
        updateCentroid();
    }

    const std::vector<size_t>& getIndices() const {
        return indices;
    }

private:
    std::vector<size_t> indices;
    cv::Vec3b centroid;
    cv::Vec3d sumIndividuals;

    void updateCentroid() {
        size_t n = indices.size();
        if (n == 0) {
            centroid = cv::Vec3b(0, 0, 0);
            return;
        }
        cv::Vec3d avg = sumIndividuals / static_cast<double>(n);
        centroid = cv::Vec3b(
            static_cast<uchar>(avg[0]),
            static_cast<uchar>(avg[1]),
            static_cast<uchar>(avg[2])
        );
    }
};

std::vector<int> hierarchicalClustering(const std::vector<cv::Vec3b>& dataPoints, int k, const std::string& outputFilename) {
    std::vector<Cluster> clusters;
    size_t nDataPoints = dataPoints.size();
    for (size_t i = 0; i < nDataPoints; ++i) {
        clusters.emplace_back(i, dataPoints[i]);
    }

    std::ofstream outFile(outputFilename);
    if (!outFile.is_open()) {
        std::cerr << "No se pudo abrir el archivo para escribir: " << outputFilename << std::endl;
        return {};
    }

    std::vector<std::vector<double>> nc;
    int iteration = 0;
    while (clusters.size() > static_cast<size_t>(k)) {
        size_t n = clusters.size();
        std::vector<std::vector<double>> distanceMatrix(n, std::vector<double>(n, 0.0));

        double minDistance = std::numeric_limits<double>::max();
        size_t clusterA = 0, clusterB = 0;

        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < n; ++j) {
                if (i == j) continue;
                double distance = clusters[i].distanceTo(clusters[j]);
                distanceMatrix[i][j] = distance;
                if (distance < minDistance) {
                    minDistance = distance;
                    clusterA = i;
                    clusterB = j;
                }
            }
        }

        nc = distanceMatrix;

        outFile << "Iteración " << iteration << ":\n";
        outFile << "Matriz de distancias:\n";
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < n; ++j) {
                outFile << distanceMatrix[i][j] << "\t";
            }
            outFile << "\n";
        }
        outFile << "Clusters a fusionar: " << clusterA << " y " << clusterB << " con distancia " << minDistance << "\n\n";

        clusters[clusterA].mergeWith(clusters[clusterB]);
        clusters.erase(clusters.begin() + clusterB);

        ++iteration;
    }

    outFile << "Final " << ":\n";
    outFile << "Matriz de distancias:\n";
    for (size_t i = 0; i < nc.size() - 1; ++i) {
        for (size_t j = 0; j < nc.size() - 1; ++j) {
            outFile << nc[i][j] << "\t";
        }
        outFile << "\n";
    }

    outFile.close();
    std::cout << "Clustering completado. Información guardada en: " << outputFilename << std::endl;

    std::vector<int> labels(nDataPoints, -1);
    for (size_t clusterIdx = 0; clusterIdx < clusters.size(); ++clusterIdx) {
        const std::vector<size_t>& indices = clusters[clusterIdx].getIndices();
        for (size_t idx : indices) {
            labels[idx] = static_cast<int>(clusterIdx);
        }
    }

    return labels;
}

int main() {
    cv::Mat img_original = cv::imread(FILENAME);
    if (img_original.empty()) {
        cout << "No se pudo cargar la imagen." << endl;
        return -1;
    }

    cv::Mat img_sin_etiquetar = img_original.clone();
    cv::Mat img_marked_points = img_original.clone();

    int n, k = 2;
    cout << "Ingresa el número de puntos: ";
    cin >> n;

    vector<pair<cv::Point, cv::Vec3b>> puntos;
    srand(time(0));

    for (int i = 0; i < n; i++) {
        int x = rand() % img_original.cols;
        int y = rand() % img_original.rows;

        cv::Point punto(x, y);
        cv::Vec3b color = img_original.at<cv::Vec3b>(y, x);
        puntos.push_back({ punto, color });

        cv::circle(img_sin_etiquetar, punto, 1, cv::Scalar(0, 0, 0), 10);
    }

    std::vector<cv::Vec3b> dataPoints;
    for (const auto& p : puntos) {
        dataPoints.push_back(p.second);
    }

    auto clasificacion = hierarchicalClustering(dataPoints, k, "clustering_output.txt");

    vector<cv::Scalar> colores(k);
    const float golden_angle = 137.5;
    for (int i = 0; i < k; i++) {
        float H = fmod(i * golden_angle, 360.0);
        float S = 0.9;
        float V = 0.9;
        colores[i] = HSVtoBGR(H, S, V);
    }

    for (size_t i = 0; i < puntos.size(); ++i) {
        int clase = clasificacion[i];
        cv::Point punto = puntos[i].first;
        cv::Scalar color = colores[clase];
        cv::circle(img_marked_points, punto, 1, color, 10);
    }

    cv::namedWindow("Imagen Original", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen sin etiquetar", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen con Puntos Marcados", cv::WINDOW_NORMAL);

    cv::resizeWindow("Imagen Original", 800, 600);
    cv::resizeWindow("Imagen sin etiquetar", 800, 600);
    cv::resizeWindow("Imagen con Puntos Marcados", 800, 600);

    cv::imshow("Imagen Original", img_original);
    cv::imshow("Imagen sin etiquetar", img_sin_etiquetar);
    cv::imshow("Imagen con Puntos Marcados", img_marked_points);

    cv::waitKey(0);
    return 0;
}
