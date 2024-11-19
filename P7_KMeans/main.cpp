#include <bits/stdc++.h>
#include <opencv2/opencv.hpp>
using namespace std;

const int ITERACIONES = 50;
const string FILENAME = "/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/jp.jpg";

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

    // Convertir a BGR y escalar a [0,255]
    int B = static_cast<int>((b + m) * 255);
    int G = static_cast<int>((g + m) * 255);
    int R = static_cast<int>((r + m) * 255);

    return cv::Scalar(B, G, R);
}

vector<pair<int, cv::Point>> KMeans (int k, int n, vector<pair<cv::Point, cv::Vec3b>> puntos) {
    vector<cv::Vec3b> centroides;
    vector<pair<int, cv::Point>> clases(n);

    for (int i = 0; i < n; i++) {
        clases[i].second = puntos[i].first;
    }

    srand(time(0));
    for (int i = 0; i < k; i++) {
        centroides.push_back(puntos[rand() % puntos.size()].second);
    }

    auto distancia = [] (cv::Vec3b a, cv::Vec3b b) {
        return sqrt(
            pow(a[0] - b[0], 2) +
            pow(a[1] - b[1], 2) +
            pow(a[2] - b[2], 2)
        );
    };

    for (int iter = 0; iter < ITERACIONES; iter++) {
        // Asignar cada punto al centroide más cercano
        for (int i = 0; i < n; i++) {
            double min_dist = std::numeric_limits<double>::max();
            int min_class = -1;
            for (int j = 0; j < k; j++) {
                double dist = distancia(puntos[i].second, centroides[j]);
                if (dist < min_dist) {
                    min_dist = dist;
                    min_class = j;
                }
            }
            clases[i].first = min_class;
        }

        // Recalcular los centroides
        vector<cv::Vec3d> sum_centroides(k, cv::Vec3d(0, 0, 0));
        vector<int> count_centroides(k, 0);

        for (int i = 0; i < n; i++) {
            int cls = clases[i].first;
            sum_centroides[cls][0] += puntos[i].second[0];
            sum_centroides[cls][1] += puntos[i].second[1];
            sum_centroides[cls][2] += puntos[i].second[2];
            count_centroides[cls]++;
        }

        for (int j = 0; j < k; j++) {
            if (count_centroides[j] > 0) {
                centroides[j][0] = sum_centroides[j][0] / count_centroides[j];
                centroides[j][1] = sum_centroides[j][1] / count_centroides[j];
                centroides[j][2] = sum_centroides[j][2] / count_centroides[j];
            }
        }
    }

    return clases;
}


int main() {
    cv::Mat img_original = cv::imread(FILENAME);
    if (img_original.empty()) {
        cout << "No se pudo cargar la imagen." << endl;
        return -1;
    }

    cv::Mat img_sin_etiquetar = img_original.clone();
    cv::Mat img_marked_points = img_original.clone();

    int n, k;
    cout << "Ingresa el número de puntos y k: ";
    cin >> n >> k;

    vector<pair<cv::Point, cv::Vec3b>> puntos;
    srand(time(0));

    for (int i = 0; i < n; i++) {
        int x = rand() % img_original.cols;
        int y = rand() % img_original.rows;

        cv::Point punto(x, y);
        cv::Vec3b color = img_original.at<cv::Vec3b>(y, x);
        puntos.push_back({punto, color});

        cv::circle(img_sin_etiquetar, punto, 1, cv::Scalar(0, 0, 0), 2);
    }

    auto clasificacion = KMeans(k, n, puntos);

    vector<cv::Scalar> colores(k); // Inicializa con k elementos
    const float golden_angle = 137.5;
    for (int i = 0; i < k; i++) {
        float H = fmod(i * golden_angle, 360.0);
        float S = 0.9;
        float V = 0.9;
        colores[i] = HSVtoBGR(H, S, V); // Asigna directamente al índice i
    }

    for (const auto &[clase, punto]: clasificacion) {
        cv::circle(img_marked_points, punto, 1, colores[clase], 2);
    }

    // cv::Size tamaño_deseado(400, 400);

    // cv::imshow("Imagen Original", img_original);
    // cv::imshow("Imagen sin etiquetar", img_sin_etiquetar);
    // cv::imshow("Imagen con Puntos Marcados", img_marked_points);

    cv::namedWindow("Imagen Original", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen sin etiquetar", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen con Puntos Marcados", cv::WINDOW_NORMAL);

    // Opcional: Ajustar el tamaño de las ventanas
    cv::resizeWindow("Imagen Original", 800, 600);
    cv::resizeWindow("Imagen sin etiquetar", 800, 600);
    cv::resizeWindow("Imagen con Puntos Marcados", 800, 600);

    // Mostrar las imágenes
    cv::imshow("Imagen Original", img_original);
    cv::imshow("Imagen sin etiquetar", img_sin_etiquetar);
    cv::imshow("Imagen con Puntos Marcados", img_marked_points);

    // cv::Mat concatenada_horizontal;
    // cv::hconcat(std::vector<cv::Mat>{img_original, img_sin_etiquetar, img_marked_points}, concatenada_horizontal);
    // cv::imshow("Todas las Imágenes", concatenada_horizontal);

    // cout << "Puntos seleccionados y sus valores RGB:" << endl;
    // for (const auto& p : puntos) {
    //     cout << "Posición: (" << p.first.x << ", " << p.first.y
    //          << "), RGB: (" << (int)p.second[2] << ", " << (int)p.second[1] << ", " << (int)p.second[0] << ")" << endl;
    // }

    cv::waitKey(0);
    return 0;
}
