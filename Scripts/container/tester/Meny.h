#ifndef PEKERMENYCLASS_H
#define PEKERMENYCLASS_H
#include <iostream>
#include <vector>
using namespace std;

class Meny {
private:
    struct menyLinje {
        string kortValg;
        string langBeskrivelsesTekst;
        void (*implementerendeFunksjon)(); // implementerendeFunksjon er en Funksjonspeker - peker til funksjonen som implementerer dette valget
    };
    void skrivMenyTilTerminal(string innrykk, vector<menyLinje> meny);
    int matchInputMedValgtMenylinje(string innrykk, vector<menyLinje> meny);

public:
    void start(vector<menyLinje> meny);
    void start(string innrykk, vector<menyLinje> meny); // <== Innrykk menyen, Tenkt brukt for under-menyer
};
#endif // ~PEKERMENYCLASS_H