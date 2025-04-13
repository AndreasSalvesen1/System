#include "Meny.h"
using namespace std;


void Meny::skrivMenyTilTerminal(string innrykk, vector<menyLinje> meny) {
    cout << innrykk << "Vennligst velg:" << endl;
    for (int i = 0; i < static_cast<int> (meny.size()); i++)
        cout
            << innrykk 
            << meny[i].kortValg
            << ":\t"
            << meny[i].langBeskrivelsesTekst
            << endl;
    cout
        << innrykk
        << endl
        << "Valgt alternativ - ("
        << meny[0].kortValg
        << ".."
        << meny[meny.size() - 1].kortValg
        << "): ";
}

// Returnerer index for valgt menylinje
int Meny::matchInputMedValgtMenylinje(string innrykk, vector<menyLinje> meny) {
    skrivMenyTilTerminal(innrykk, meny);
    string inp;
    while (true) {
        cin >> inp;
        for (int i = 0; i < static_cast<int> (meny.size()); i++) {
            if (meny[i].kortValg == inp) {
                // cout << "Yes, "<< inp << " is an excelent choice";
                return i;
            }
        }
        cout << innrykk << "Beklager, men " << inp << " er ikke et gyldig valg." << endl << innrykk << "Velg noe annet..." << endl;
        skrivMenyTilTerminal(innrykk, meny);
    }
    return 0;
}

void Meny::start(vector<menyLinje> meny) {
    start("",meny);
}

void Meny::start(string innrykk, vector<menyLinje> meny) {

    // Dersom "0" ikke allerede ligger inne som et kortvalg, setter vi 
    // inn en rad "0 - Avslutter" eller "0 - Returner" (dersom innrykk != "")
  
    bool menyInneholderValg0 = false;
    for (int i = 0; i < static_cast<int> (meny.size()); i++) {
        if (meny[i].kortValg == "0") {
            menyInneholderValg0 = true;
        }
    }

    if (!menyInneholderValg0)
        meny.push_back({"0", innrykk == "" ? "Avslutter" : "Returner" , nullptr}); 


    while (true) {
        int valgtIndex = matchInputMedValgtMenylinje(innrykk, meny);
        string valg = meny[valgtIndex].langBeskrivelsesTekst;

        if (meny[valgtIndex].kortValg == "0") {
            cout << "\n\n";
            cout <<innrykk<<"Menyen avsluttes ... "<< meny[valgtIndex].langBeskrivelsesTekst << endl; // "Avslutter" eller "Returnerer"
            cout << "\n\n";
            return;
        } 
        
        meny[valgtIndex].implementerendeFunksjon(); // Utfør valgt funksjon
 
        cout 
            << "\n\n\n";
    }
}