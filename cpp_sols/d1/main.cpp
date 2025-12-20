#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int sol_p1(ifstream& file){
    int zero_count {};
    int pos = 50;

    string line;
    while (getline(file, line)){
        int rot = stoi(line.substr(1)); // from 1 to end of substr
        if (auto dir = line[0]; dir == 'L'){
            rot = -rot;
        }
        pos = (pos + rot) % 100;

        if (pos == 0){
            zero_count++;
        }
    }

    return zero_count;
}


int sol_p2(ifstream& file){
    int zero_count {};
    int pos = 50;

    string line;
    while (getline(file, line)){

        int x = 1;

        int rot = stoi(line.substr(1)); // from 1 to end of substr
        if (auto dir = line[0]; dir == 'L'){
            x = -1;
        }
        for (int i=0; i < rot; i++){
            pos = (pos + x) % 100;

            if (pos == 0){
                zero_count++;
            }
        }
    }
    return zero_count;
}


int main(){

    ifstream data("data.txt");

    if (!data.is_open()){
        cerr << "Error opening file" << endl;
        return 1;
    }

    cout << "Part 1 solution " << sol_p1(data) << std::endl;

    // Reset file read to beginning
    data.clear();
    data.seekg(0, std::ios::beg);

    cout << "Part 2 solution " << sol_p2(data) << std::endl;
    
    data.close();

    return 0;
}
