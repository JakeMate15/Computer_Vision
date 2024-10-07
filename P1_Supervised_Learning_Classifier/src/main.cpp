#include<bits/stdc++.h>
#include "matplotlibcpp.h"

using namespace std;
namespace plt = matplotlibcpp;

struct Clase {
    int n;
    vector<double> x, y;
    double cX = 0.0, cY = 0.0;
    string color;

    Clase(int n) {
        this->n = n;
    }

    Clase(int n, vector<double> x, vector<double> y) {
        this->n = n;
        this->x = x;
        this->y = y;

        for (const auto& xi: this->x) {
            cX += xi;
        }
        for (const auto& yi: this->y) {
            cY += yi;
        }
        cX /= this->n;
        cY /= this->n;
    }

    vector<double> getX() {
        return x;
    }

    vector<double> getY() {
        return y;
    }

    string getColor() {
        return color;
    }

    void setX(vector<double> x1) {
        x = x1;
    }

    void setY(vector<double> y1) {
        y = y1;
    }

    void setColor(string color) {
        this->color = color;
    }

    pair<double, double> obtenCentroide() {
        return make_pair(cX, cY);
    }
};

string randColor() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 255);

    int r = dis(gen);
    int g = dis(gen);
    int b = dis(gen);

    ostringstream oss;
    oss << "#"
        << std::setw(2) << std::setfill('0') << std::hex << r
        << std::setw(2) << std::setfill('0') << std::hex << g
        << std::setw(2) << std::setfill('0') << std::hex << b;

    return oss.str();
}

const double maxDist = 10.0;

void run (vector<double> vU) {
    int individuos = 4;
    vector<Clase> clases;
    vector<double> dist;

    clases.emplace_back(individuos, vector<double>{0, 1, 0, 3}, vector<double>{0, 2, 3, 0});
    clases.emplace_back(individuos, vector<double>{4, 4, 4, 5}, vector<double>{0, 3, 2, 6});
    clases.emplace_back(individuos, vector<double>{6, 7, 7, 8}, vector<double>{0, 1, 3, 2});
    clases.emplace_back(individuos, vector<double>{0, -1, 0, -3}, vector<double>{0, -2, -3, 0});
    clases.emplace_back(individuos, vector<double>{-4, -4, -4, -5}, vector<double>{0, -3, -2, -6});
    clases.emplace_back(individuos, vector<double>{-6, -7, -7, -8}, vector<double>{0, -1, -3, -2});

    double size = 50.0;
    set<string> colores;
    string c;

    auto genColor = [&] () -> string {
        string color = randColor();
        while (colores.contains(color)) {
            color = randColor();
        }
        return color;
    };

    plt::clf();

    int idx = 1;
    for (auto &[n, x, y, cX, cY, color] : clases) {
        c = genColor();

        colores.insert(c);
        color = c;

        plt::scatter(x, y, size, {{"color", c}, {"edgecolor", "black"}, {"label", "Clase " + to_string(idx)}});
        plt::scatter(std::vector<double>{cX}, std::vector<double>{cY}, size * 5, {{"color", c}, {"edgecolor", "black"}});

        dist.emplace_back(hypot(cX - vU[0], cY - vU[1]));

        idx++;
    }

    for (auto x: dist) {
        cout << x << " ";
    }
    cout << "\n";

    int mnIdx = min_element(dist.begin(), dist.end()) - dist.begin();
    if (dist[mnIdx] > maxDist) {
        cout << "El individuo ingresado no pertence a alguna clase\n";
        c = genColor();
    } else {
        cout << "El individuo pertence a la clase " << mnIdx + 1 << "\n";
        c = clases[mnIdx].getColor();
    }

    plt::scatter(vector<double>{vU[0]}, vector<double>{vU[1]}, size, {{"marker", "x"}, {"color", c}, {"label", "Vu"}});

    plt::legend();
    plt::grid(true);
    plt::xlabel("Eje X");
    plt::ylabel("Eje Y");
    plt::title("Scatter Plot con Colores Diferentes por Grupo");
    plt::show();
}

int main() {
    string op = "c";
    int n = 2;
    vector<double> v(n);

    while (op == "c") {
        cout << "Ingrese su vector de " << n << " caracteristicas, solo se consideraran los primeros " << n << " elementos ingresados\n";
        for (auto &x: v) {
            cin >> x;
        }

        run(v);

        cout << "\nIngrese\n";
        cout << "c para ingresar otro vector\n";
        cout << "Cual otra letra para salir\n";
        cin >> op;
    }

    return 0;
}
