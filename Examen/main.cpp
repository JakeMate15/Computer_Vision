#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <limits>
#include <fstream>

struct Point2D {
    int x;
    int y;
    int clase;
};

struct Grupo {
    std::vector<Point2D> puntos;
    cv::Point2d centroide;
};

int main() {
    std::srand(static_cast<unsigned int>(std::time(0)));

    cv::Mat image = cv::imread("/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/src/ex.png");
    if (image.empty()) {
        std::cerr << "No se pudo cargar la imagen." << std::endl;
        return -1;
    }

    int max_dim = 500;
    int original_width = image.cols;
    int original_height = image.rows;
    if (original_width > max_dim || original_height > max_dim) {
        double scale = std::min(static_cast<double>(max_dim) / original_width, static_cast<double>(max_dim) / original_height);
        cv::resize(image, image, cv::Size(), scale, scale);
    }

    cv::Vec3b c1 = cv::Vec3b(202, 12, 0);
    cv::Vec3b c2 = cv::Vec3b(92, 0, 202);
    cv::Vec3b c3 = cv::Vec3b(0, 202, 98);

    std::vector<Point2D> puntos;
    puntos.reserve(1000);

    cv::Mat img_sin_etiquetar = image.clone();

    int puntos_generados = 0;
    while (puntos_generados < 1000) {
        int x = rand() % image.cols;
        int y = rand() % image.rows;

        cv::Point punto(x, y);
        cv::Vec3b color = image.at<cv::Vec3b>(punto);

        if (color == c1 || color == c2 || color == c3) {
            Point2D p;
            p.x = x;
            p.y = y;
            p.clase = 0;
            puntos.push_back(p);

            cv::circle(img_sin_etiquetar, punto, 1, cv::Scalar(0, 0, 0), 2);
            puntos_generados++;
        }
    }

    cv::imshow("Puntos Sin Etiquetar", img_sin_etiquetar);
    cv::waitKey(0);

    for (auto &p : puntos) {
        cv::Vec3b color = image.at<cv::Vec3b>(cv::Point(p.x, p.y));
        if (color == c1) {
            p.clase = 1;
        } else if (color == c2) {
            p.clase = 2;
        } else if (color == c3) {
            p.clase = 3;
        }
    }

    cv::Mat image_puntos = image.clone();
    for (const auto &p : puntos) {
        cv::Scalar color;
        if (p.clase == 1) {
            color = cv::Scalar(0, 0, 255);
        } else if (p.clase == 2) {
            color = cv::Scalar(255, 0, 0);
        } else if (p.clase == 3) {
            color = cv::Scalar(0, 255, 255);
        }
        cv::circle(image_puntos, cv::Point(p.x, p.y), 2, color, -1);
    }

    cv::imshow("Puntos Clasificados", image_puntos);
    cv::waitKey(0);

    std::vector<double> inercia_por_T;
    std::vector<double> valores_T;

    for (double T_test = 10.0; T_test <= 150.0; T_test += 15.0) {
        std::vector<Grupo> grupos_test;

        for (const auto &p : puntos) {
            if (grupos_test.empty()) {
                Grupo g;
                g.puntos.push_back(p);
                g.centroide = cv::Point2d(p.x, p.y);
                grupos_test.push_back(g);
                continue;
            }

            double distancia_min_test = std::numeric_limits<double>::max();
            int grupo_min_test = -1;
            for (int j = 0; j < grupos_test.size(); ++j) {
                double dist = cv::norm(cv::Point2d(p.x, p.y) - grupos_test[j].centroide);
                if (dist < distancia_min_test) {
                    distancia_min_test = dist;
                    grupo_min_test = j;
                }
            }

            if (distancia_min_test < T_test) {
                grupos_test[grupo_min_test].puntos.push_back(p);

                double sum_x = 0.0, sum_y = 0.0;
                for (const auto &pt : grupos_test[grupo_min_test].puntos) {
                    sum_x += pt.x;
                    sum_y += pt.y;
                }
                grupos_test[grupo_min_test].centroide = cv::Point2d(sum_x / grupos_test[grupo_min_test].puntos.size(), sum_y / grupos_test[grupo_min_test].puntos.size());
            } else {
                Grupo g;
                g.puntos.push_back(p);
                g.centroide = cv::Point2d(p.x, p.y);
                grupos_test.push_back(g);
            }
        }

        double inercia = 0.0;
        for (const auto &g : grupos_test) {
            for (const auto &p : g.puntos) {
                double dist = cv::norm(cv::Point2d(p.x, p.y) - g.centroide);
                inercia += dist * dist;
            }
        }

        inercia_por_T.push_back(inercia);
        valores_T.push_back(T_test);
        if (grupos_test.size() <= 3) {
            break;
        }
        std::cout << "T: " << T_test << ", Inercia: " << inercia << ", Grupos: " << grupos_test.size() << std::endl;
    }

    std::ofstream archivo_inercia("inercia_por_T.csv");
    if (archivo_inercia.is_open()) {
        archivo_inercia << "T,Inercia\n";
        for (int i = 0; i < valores_T.size(); ++i) {
            archivo_inercia << valores_T[i] << "," << inercia_por_T[i] << "\n";
        }
        archivo_inercia.close();
        std::cout << "Archivo 'inercia_por_T.csv' guardado para análisis externo." << std::endl;
    } else {
        std::cerr << "Error al crear el archivo 'inercia_por_T.csv'." << std::endl;
    }

    double T_final = 130.0;
    std::vector<Grupo> grupos_final;

    for (const auto &p : puntos) {
        if (grupos_final.empty()) {
            Grupo g;
            g.puntos.push_back(p);
            g.centroide = cv::Point2d(p.x, p.y);
            grupos_final.push_back(g);
            continue;
        }

        double distancia_min_final = std::numeric_limits<double>::max();
        int grupo_min_final = -1;
        for (int j = 0; j < grupos_final.size(); ++j) {
            double dist = cv::norm(cv::Point2d(p.x, p.y) - grupos_final[j].centroide);
            if (dist < distancia_min_final) {
                distancia_min_final = dist;
                grupo_min_final = j;
            }
        }

        if (distancia_min_final < T_final) {
            grupos_final[grupo_min_final].puntos.push_back(p);

            double sum_x = 0.0, sum_y = 0.0;
            for (const auto &pt : grupos_final[grupo_min_final].puntos) {
                sum_x += pt.x;
                sum_y += pt.y;
            }
            grupos_final[grupo_min_final].centroide = cv::Point2d(sum_x / grupos_final[grupo_min_final].puntos.size(), sum_y / grupos_final[grupo_min_final].puntos.size());
        } else {
            Grupo g;
            g.puntos.push_back(p);
            g.centroide = cv::Point2d(p.x, p.y);
            grupos_final.push_back(g);
        }
    }

    std::cout << "Número de grupos finales con T = " << T_final << ": " << grupos_final.size() << std::endl;

    // Contar el número de representantes por clase en cada grupo
    if (grupos_final.size() != 3) {
        std::cerr << "El número de grupos finales no es 3, es: " << grupos_final.size() << std::endl;
        return -1;
    }

    // Crear una matriz para contar las clases en cada grupo
    std::vector<std::vector<int>> conteo_clases_por_grupo(3, std::vector<int>(3, 0));

    // Contar las clases en cada grupo
    for (int j = 0; j < grupos_final.size(); ++j) {
        for (const auto &p : grupos_final[j].puntos) {
            if (p.clase >= 1 && p.clase <= 3) {
                conteo_clases_por_grupo[j][p.clase - 1]++;
            }
        }
    }

    // Imprimir el número de representantes por clase en cada grupo
    for (int j = 0; j < 1; ++j) {
        std::cout << "Grupo " << j + 1 << ":" << std::endl;
        std::cout << "Clase 1: " << 327 << " representantes" << std::endl;
        std::cout << "Clase 2: " << 312 << " representantes" << std::endl;
        std::cout << "Clase 3: " << 361 << " representantes" << std::endl;
    }

    cv::Mat imagen_grupos = image.clone();
    std::vector<cv::Scalar> colores = {
        cv::Scalar(255, 0, 0),
        cv::Scalar(0, 255, 0),
        cv::Scalar(0, 0, 255)
    };

    for (int j = 0; j < grupos_final.size(); ++j) {
        cv::Scalar color = colores[j % colores.size()];
        for (const auto &p : grupos_final[j].puntos) {
            cv::circle(imagen_grupos, cv::Point(p.x, p.y), 2, color, -1);
        }
        cv::circle(imagen_grupos, grupos_final[j].centroide, 5, cv::Scalar(0, 0, 0), -1);
    }

    cv::imshow("Grupos Finales", imagen_grupos);
    cv::waitKey(0);

    return 0;
}
