#include<bits/stdc++.h>
#include "matplotlibcpp.h"
#include "matrix.h"
#include "Clase.h"
#include <cmath>

using namespace std;
namespace plt = matplotlibcpp;

typedef long double ld;

const double maxDist = 20.0;

void run(vector<Clase> &clases, double X, double Y) {
    double size = 50.0;
    vector<ld> dist, mahalanobis, naiveBayes;

    int idxColor = 0;
    string c;
    auto genColor = [&]() -> string {
        return tab20Colors[(idxColor++) % 20];
    };

    plt::clf();

    int idx = 1;
    for (auto &C : clases) {
        // Asignamos el punto a clasificar
        C.setPunto({X, Y});

        // Generamos y asignamos un color único
        c = genColor();
        C.setColor(c);

        // Obtenemos los datos de la clase
        vector<double> x = C.getX();
        vector<double> y = C.getY();
        double cX = C.cX;
        double cY = C.cY;

        // Graficamos los puntos y el centroide
        plt::scatter(x, y, size, {{"color", c}, {"edgecolor", "black"}, {"label", "Clase " + to_string(idx)}});
        plt::scatter(vector<double>{cX}, vector<double>{cY}, size * 5, {{"color", c}, {"edgecolor", "black"}});

        // Calculamos las distancias y probabilidades
        dist.emplace_back(hypot(cX - X, cY - Y));
        mahalanobis.push_back(C.mahalanobis());
        naiveBayes.push_back(C.proB());

        idx++;
    }

    getNB(naiveBayes);

    cout << "Con qué distancia quiere clasificar: \n";
    cout << "1 - Distancia Euclidiana\n";
    cout << "2 - Distancia Mahalanobis\n";
    cout << "3 - Probabilidades\n";
    int op;
    cin >> op;

    vector<ld> ops;
    bool isProbability = false;
    switch (op) {
        case 1:
            ops = dist;
        break;
        case 2:
            ops = mahalanobis;
        break;
        case 3:
            ops = naiveBayes;
        isProbability = true;
        break;
        default:
            cout << "Opción no válida." << endl;
        return;
    }

    for (int i = 0; i < ops.size(); i++) {
        cout << fixed << setprecision(20) << "Clase " << i + 1 << " " << ops[i] << "\n";
    }

    int selectedIdx;
    if (isProbability) {
        selectedIdx = max_element(ops.begin(), ops.end()) - ops.begin();
    } else {
        selectedIdx = min_element(ops.begin(), ops.end()) - ops.begin();
    }

    // cerr << ops[selectedIdx] << "\n";

    if (std::isnan(ops[selectedIdx])) {
        std::cout << "El individuo no pertenece a la clase" << std::endl;
    } else if (!isProbability && ops[selectedIdx] > maxDist) {
        std::cout << "El individuo ingresado no pertenece a alguna clase" << std::endl;
    } else {
        std::cout << "El individuo pertenece a la clase " << selectedIdx + 1 << std::endl;
    }

    plt::scatter(vector<double>{X}, vector<double>{Y}, size, {{"marker", "x"} });

    plt::legend();
    plt::grid(true);
    plt::xlabel("Eje X");
    plt::ylabel("Eje Y");
    plt::title("Visualizacion de las clases");
    plt::show();
}

int main() {
    int n, m;
    string op = "c";
    vector<Clase> clases;
    double cX, cY, dX, dY, x, y;

    do {
        if (op == "c") {
            clases.clear();

            cout << "Dame el numero de clases: ";
            cin >> n;
            cout << "Dame el numero de repsentantes por clase: ";
            cin >> m;

            for (int i = 0; i < n; i++) {
                cout << "Dame el controide de la clase " << i + 1 << "\n";
                cout << "Cx: ";
                cin >> cX;
                cout << "Cy: ";
                cin >> cY;

                cout << "Dame la dispersion de la clase\n";
                cout << "Dx: ";
                cin >> dX;
                cout << "Dy: ";
                cin >> dY;

                clases.emplace_back(m, cX, cY, dX, dY);
            }

            cout << "Ingresa el individuo que quieres clasificar x y\n";
            cin >> x >> y;

            run(clases, x, y);
        } else {
            cout << "Ingresa el individuo que quieres clasificar x y\n";
            cin >> x >> y;

            for (auto C: clases) {
                C.setPunto({x, y});
            }
            run(clases, x, y);
        }

        cout << "\nIngrese\n";
        cout << "c para crear una clase nueva\n";
        cout << "v para ingresar un vector diferente\n";
        cout << "Cual otra letra para salir\n";
        cin >> op;
    } while (op == "c" || op == "v");

    return 0;
}
