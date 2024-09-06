#include<bits/stdc++.h>
#include "matplotlibcpp.h"
using namespace std;
namespace plt = matplotlibcpp;

#define RAND(a, b) uniform_int_distribution<int>(a, b)(rng)
#define RANDR(a, b) uniform_real_distribution<double>(a, b)(rng)
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

struct Clase {
    int n;
    vector<double> x, y;
    double cX = 0.0, cY = 0.0, dX = 0.0, dY = 0.0;
    string color;

    Clase(int n, double cX, double cY, double dX, double dY) {
        this->n = n;
        this->cX = cX;
        this->cY = cY;
        this->dX = dX;
        this->dY = dY;

        double cx = 0.0, cy = 0.0;
        for (int i = 0; i < n; i++) {
            double xi = RANDR(cX - dX / 2, cX + dX / 2);
            double yi = RANDR(cY - dY / 2, cY + dY / 2);
            this->x.push_back(xi);
            this->y.push_back(yi);

            cx += xi; cy += yi;
        }

        cX = cx / n;
        cY = cy / n;
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

    void setColor(string Color) {
        this->color = Color;
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

const double maxDist = 20.0;

void run (vector<Clase> &clases, double X, double Y) {
    double size = 50.0;
    vector<double> dist;

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
    for (auto &[n, x, y, cX, cY, dX, dY, color] : clases) {
        c = genColor();

        colores.insert(c);
        color = c;

        plt::scatter(x, y, size, {{"color", c}, {"edgecolor", "black"}, {"label", "Clase " + to_string(idx)}});
        plt::scatter(std::vector<double>{cX}, std::vector<double>{cY}, size * 5, {{"color", c}, {"edgecolor", "black"}});

        dist.emplace_back(hypot(cX - X, cY - Y));

        idx++;
    }

    int mnIdx = min_element(dist.begin(), dist.end()) - dist.begin();
    if (dist[mnIdx] > maxDist) {
        cout << "El individuo ingresado no pertence a alguna clase\n";
        c = genColor();
    } else {
        cout << "El individuo pertence a la clase " << mnIdx + 1 << "\n";
        c = clases[mnIdx].getColor();
    }

    plt::scatter(vector<double>{X}, vector<double>{Y}, size, {{"marker", "x"}, {"color", c}, {"label", "Vu"}});

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
