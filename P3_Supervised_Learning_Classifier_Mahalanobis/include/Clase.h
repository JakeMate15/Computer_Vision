//
// Created by erik on 24/09/24.
//

#ifndef CLASE_H
#define CLASE_H

#include<bits/stdc++.h>

typedef long double ld;

#define RAND(a, b) uniform_int_distribution<int>(a, b)(rng)
#define RANDR(a, b) uniform_real_distribution<double>(a, b)(rng)
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

struct Clase {
    int n;
    vector<double> x, y;
    double cX = 0.0, cY = 0.0, dX = 0.0, dY = 0.0;
    string color;
    vector<double> Punto;
    matrix<double> Xv, Xt, S, sInv;

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

            cx += xi;
            cy += yi;
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

    void preCalc() {
        Xv = matrix<double>(2, 1);
        Xv[0][0] = Punto[0] - cX;
        Xv[1][0] = Punto[1] - cY;

        Xt = Xv.transpose();

        matrix<double> SS = matrix<double>(2, n);
        for (int i = 0; i < n; i++) {
            SS[0][i] = x[i] - cX;
            SS[1][i] = y[i] - cY;
        }

        S = (SS * SS.transpose()) * (1.0 / (n));

        if (S.determinant() == 0) {
            cerr << "La matriz de covarianza no es invertible. \n";
            exit(0);
        }

        sInv = S.inverse();
    }

    double mahalanobis () {
        auto sq = Xt * sInv * Xv;
        assert(sq.n == sq.m && sq.n == 1);
        return sqrt(sq.determinant());
    }

    ld proB() {
        double detS = S.determinant();
        if (detS <= 0) {
            cerr << "La matriz de covarianza no es invertible. \n";
            exit(0);
        }
        ld den = sqrt(pow(2 * M_PI, 2) * detS);
        ld exponent = -0.5 * (Xt * sInv * Xv)[0][0];
        ld ex = exp(exponent);
        return ex / den;
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

    vector<double> getPunto() {
        return Punto;
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

    void setPunto (vector<double> Punto) {
        this->Punto = Punto;
        preCalc();
    }

    pair<double, double> obtenCentroide() {
        return make_pair(cX, cY);
    }
};

void getNB(vector<ld> &probs) {
    ld sum = accumulate(probs.begin(), probs.end(), 0.0);
    for (auto &x : probs) {
        x = (x / sum) * 100.0;
    }
}

vector<string> tab20Colors = {
    "#1f77b4", "#aec7e8",
    "#ff7f0e", "#ffbb78",
    "#2ca02c", "#98df8a",
    "#d62728", "#ff9896",
    "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94",
    "#e377c2", "#f7b6d2",
    "#7f7f7f", "#c7c7c7",
    "#bcbd22", "#dbdb8d",
    "#17becf", "#9edae5"
};



#endif //CLASE_H
