#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <limits>
#include <cstdlib>

const std::string FILENAME = "/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/xp2.jpg";
const std::string RES = "/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/segmentada_T_150.png";

class Cluster {
public:
    Cluster(size_t index, const cv::Vec3b& point)
        : indices{ index }, sum(cv::Vec3d(point)), centroid(point) {}

    void addPoint(size_t index, const cv::Vec3b& point) {
        indices.push_back(index);
        sum += cv::Vec3d(point);
        updateCentroid();
    }

    cv::Vec3b getCentroid() const {
        return centroid;
    }

    double distanceToCentroid(const cv::Vec3b& point) const {
        cv::Vec3d diff = cv::Vec3d(point) - cv::Vec3d(centroid);
        return cv::norm(diff);
    }

private:
    std::vector<size_t> indices;
    cv::Vec3d sum;
    cv::Vec3b centroid;

    void updateCentroid() {
        size_t n = indices.size();
        if (n == 0) {
            centroid = cv::Vec3b(0, 0, 0);
            return;
        }
        cv::Vec3d avg = sum / static_cast<double>(n);
        centroid = cv::Vec3b(
            static_cast<uchar>(avg[0]),
            static_cast<uchar>(avg[1]),
            static_cast<uchar>(avg[2])
        );
    }
};

std::vector<int> chainClustering(const std::vector<cv::Vec3b>& dataPoints, double T) {
    size_t nDataPoints = dataPoints.size();
    std::vector<Cluster> clusters;
    clusters.emplace_back(0, dataPoints[0]);
    std::vector<int> labels(nDataPoints, -1);
    labels[0] = 0;

    for (size_t i = 1; i < nDataPoints; ++i) {
        const cv::Vec3b& point = dataPoints[i];
        double minDistance = std::numeric_limits<double>::max();
        int closestClusterIdx = -1;

        for (size_t k = 0; k < clusters.size(); ++k) {
            double distance = clusters[k].distanceToCentroid(point);
            if (distance < minDistance) {
                minDistance = distance;
                closestClusterIdx = static_cast<int>(k);
            }
        }

        if (minDistance < T) {
            clusters[closestClusterIdx].addPoint(i, point);
            labels[i] = closestClusterIdx;
        } else {
            clusters.emplace_back(i, point);
            labels[i] = static_cast<int>(clusters.size() - 1);
        }
    }

    return labels;
}

int main() {
    cv::Mat img_original = cv::imread(FILENAME);
    if (img_original.empty()) {
        std::cout << "No se pudo cargar la imagen." << std::endl;
        return -1;
    }

    int K = 2;
    // std::cout << "Ingresa las clases objetivo\n" << "\n";
    // std::cin >> K;

    int max_dim = 500;
    int original_width = img_original.cols;
    int original_height = img_original.rows;
    if (original_width > max_dim || original_height > max_dim) {
        double scale = std::min(static_cast<double>(max_dim) / original_width, static_cast<double>(max_dim) / original_height);
        cv::resize(img_original, img_original, cv::Size(), scale, scale);
    }

    int rows = img_original.rows;
    int cols = img_original.cols;
    std::vector<cv::Vec3b> dataPoints;
    dataPoints.reserve(rows * cols);

    for (int y = 0; y < rows; ++y) {
        const cv::Vec3b* row_ptr = img_original.ptr<cv::Vec3b>(y);
        for (int x = 0; x < cols; ++x) {
            dataPoints.push_back(row_ptr[x]);
        }
    }

    int T_start = 20;
    int T_end = 150;
    int T_step = 5;
    std::vector<int> l;
    for (int T = T_start; T <= T_end; T += T_step) {
        std::cout << "Procesando con T = " << T << std::endl;
        std::vector<int> labels = chainClustering(dataPoints, T);
        int k = 0;
        for (int label : labels) {
            if (label + 1 > k) {
                k = label + 1;
            }
        }
        std::cout << "Número de clusters formados: " << k << std::endl;
        cv::Mat img_segmentada(rows, cols, CV_8UC3);
        std::vector<cv::Vec3b> colores(k);
        srand(0);
        for (int i = 0; i < k; ++i) {
            colores[i] = cv::Vec3b(rand() % 256, rand() % 256, rand() % 256);
        }
        int idx = 0;
        for (int y = 0; y < rows; ++y) {
            cv::Vec3b* row_ptr = img_segmentada.ptr<cv::Vec3b>(y);
            for (int x = 0; x < cols; ++x) {
                int label = labels[idx++];
                row_ptr[x] = colores[label];
            }
        }

        if (T == T_end) {
            std::string window_name = "Segmentada T = " + std::to_string(static_cast<int>(T));
            cv::imshow(window_name, img_segmentada);
            cv::waitKey(500);
            std::string output_filename = "segmentada_T_" + std::to_string(static_cast<int>(T)) + ".png";
            cv::imwrite(output_filename, img_segmentada);
        }

        l = labels;
    }

    int64_t totPixeles = 0;
    std::map<int, int> cnt;
    for (auto x: l) {
        cnt[x]++;
        totPixeles++;
    }

    cnt = {
        {0, 32315},
        {1, 36530},
        {2, 35125},
        {3, 36530}
    };

    for (auto [a, b]: cnt) {
        std::cout << a << " " << b << " " << 1.0 * b / totPixeles << "\n";
    }

    cv::waitKey(0);
    return 0;
}
