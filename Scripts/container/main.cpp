// #include <std_lib_facilities.h>
#include <iostream>
#include <memory>
#include "Meny.h"
#include "Tester.h"
#include "Farger.h"
#include "container.h"
using namespace std;




int main() {

    cout
    <<
    BOLD_RED_BACKGROUND
    " TDT4102 Oving 10, oppgave 1, 2, 3 og 4: "
    RESET
    << endl
    << endl;


    // Menysystem for øving 10

        Meny().start({

        {  "X", YELLOW "Tester menyen" RESET, testMeny},
        {  "0", YELLOW "Avslutt" RESET, nullptr},
        {  "1", YELLOW "Tester MinesweeperWindow" RESET, runContainer},

        });

        return 0;

    return 0;

    }
