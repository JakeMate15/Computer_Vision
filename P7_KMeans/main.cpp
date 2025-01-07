#include <bits/stdc++.h>
#include <opencv2/opencv.hpp>
using namespace std;

const int MAX_ITERACIONES = 50;
const string FILENAME = "/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/ex.png";

// Función para convertir HSV a BGR
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

// Función KMeans con visualización y detección de convergencia
vector<pair<int, cv::Point>> KMeans(int k, int n, const vector<pair<cv::Point, cv::Vec3b>>& puntos,
                                   const cv::Mat& img_original) {
    vector<cv::Vec3b> centroides;
    vector<pair<int, cv::Point>> clases(n, { -1, cv::Point() });

    // Inicializar las clases con los puntos proporcionados
    for (int i = 0; i < n; i++) {
        clases[i].second = puntos[i].first;
    }

    // Inicializar centroides aleatoriamente
    srand(time(0));
    for (int i = 0; i < k; i++) {
        centroides.push_back(puntos[rand() % puntos.size()].second);
    }

    // Definir la función de distancia
    auto distancia = [] (const cv::Vec3b& a, const cv::Vec3b& b) -> double {
        return sqrt(
            pow(a[0] - b[0], 2) +
            pow(a[1] - b[1], 2) +
            pow(a[2] - b[2], 2)
        );
    };

    bool cambio = true;
    int iter = 0;
    vector<cv::Scalar> colores;
    const float golden_angle = 137.5;

    // Generar colores únicos para cada clúster
    for (int i = 0; i < k; i++) {
        float H = fmod(i * golden_angle, 360.0);
        float S = 0.9;
        float V = 0.9;
        colores.push_back(HSVtoBGR(H, S, V));
    }

    // Crear una copia de la imagen para marcar los puntos
    cv::Mat img_marked = img_original.clone();

    while (iter < MAX_ITERACIONES && cambio) {
        cambio = false;

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
            if (clases[i].first != min_class) {
                cambio = true;
                clases[i].first = min_class;
            }
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
                centroides[j][0] = static_cast<uchar>(sum_centroides[j][0] / count_centroides[j]);
                centroides[j][1] = static_cast<uchar>(sum_centroides[j][1] / count_centroides[j]);
                centroides[j][2] = static_cast<uchar>(sum_centroides[j][2] / count_centroides[j]);
            }
        }

        // Visualizar el estado actual de la clasificación
        img_marked = img_original.clone();
        for (int i = 0; i < n; i++) {
            cv::circle(img_marked, clases[i].second, 2, colores[clases[i].first], -1);
        }

        // Dibujar los centroides
        for (int j = 0; j < k; j++) {
            cv::circle(img_marked, clases[j].second, 5, cv::Scalar(255, 255, 255), -1);
            // Opcional: Dibujar centroides en colores distintos o marcadores especiales
        }

        // Mostrar la imagen actualizada
        cv::imshow("KMeans Iteracion", img_marked);
        cv::waitKey(100); // Espera 100 ms entre iteraciones

        iter++;
    }

    cout << "KMeans convergió en " << iter << " iteraciones." << endl;

    return clases;
}

int main() {
    cv::Mat img_original = cv::imread(FILENAME);
    if (img_original.empty()) {
        cout << "No se pudo cargar la imagen." << endl;
        return -1;
    }

    // Redimensionar la imagen si es necesario
    int max_dim = 500;
    int original_width = img_original.cols;
    int original_height = img_original.rows;
    if (original_width > max_dim || original_height > max_dim) {
        double scale = std::min(static_cast<double>(max_dim) / original_width, static_cast<double>(max_dim) / original_height);
        cv::resize(img_original, img_original, cv::Size(), scale, scale);
    }

    // Clonar la imagen para visualizaciones
    cv::Mat img_sin_etiquetar = img_original.clone();
    cv::Mat img_marked_points = img_original.clone();

    int n, k;
    cout << "Ingresa el número de puntos y k: ";
    cin >> n >> k;

    vector<pair<cv::Point, cv::Vec3b>> puntos;
    srand(time(0));

    // Definir colores específicos (opcional)
    cv::Vec3b c1 = cv::Vec3b(202, 12, 0), c2 = cv::Vec3b(92, 0, 202), c3 = cv::Vec3b(0, 202, 98);

    for (int i = 0; i < n; i++) {
        cv::Point punto;
        cv::Vec3b color;
        while (true) {
            int x = rand() % img_original.cols;
            int y = rand() % img_original.rows;

            punto = cv::Point(x, y);
            color = img_original.at<cv::Vec3b>(punto);

            int avg = (color[0] + color[1] + color[2]) / 3;

            if (color == c1 || color == c2 || color == c3) {
                break;
            }
        }

        puntos.emplace_back(punto, color);
        cv::circle(img_sin_etiquetar, punto, 1, cv::Scalar(0, 0, 0), 2);
    }

    // Ejecutar KMeans con visualización
    auto clasificacion = KMeans(k, n, puntos, img_original);

    // Asignar colores a cada clúster para la visualización final
    vector<cv::Scalar> colores_final(k);
    const float golden_angle = 137.5;
    for (int i = 0; i < k; i++) {
        float H = fmod(i * golden_angle, 360.0);
        float S = 0.9;
        float V = 0.9;
        colores_final[i] = HSVtoBGR(H, S, V);
    }

    // Dibujar los puntos clasificados en la imagen final
    for (const auto &[clase, punto] : clasificacion) {
        cv::circle(img_marked_points, punto, 2, colores_final[clase], -1);
    }

    // Crear ventanas para mostrar las imágenes
    cv::namedWindow("Imagen Original", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen sin etiquetar", cv::WINDOW_NORMAL);
    cv::namedWindow("Imagen con Puntos Marcados", cv::WINDOW_NORMAL);

    // Ajustar el tamaño de las ventanas
    cv::resizeWindow("Imagen Original", 800, 600);
    cv::resizeWindow("Imagen sin etiquetar", 800, 600);
    cv::resizeWindow("Imagen con Puntos Marcados", 800, 600);

    // Mostrar las imágenes finales
    cv::imshow("Imagen Original", img_original);
    cv::imshow("Imagen sin etiquetar", img_sin_etiquetar);
    cv::imshow("Imagen con Puntos Marcados", img_marked_points);

    cv::waitKey(0);
    return 0;
}
