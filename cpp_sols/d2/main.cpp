#include <functional>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

bool is_invalid_id_p1(const long long iid){
    string sid = to_string(iid);
    size_t id_len = sid.length();
    size_t base = id_len >> 1; // div by 2

    string left = sid.substr(0, base);
    string right = sid.substr(base);

    if (left.compare(right) == 0){
        return true;
    }
    return false;

}

bool is_invalid_id_p2(const long long iid){
    string sid = to_string(iid);
    size_t id_len = sid.length();
    
    for (size_t i=1; i<= id_len / 2; i++){
        if ( id_len % i != 0) continue;

        string pattern = sid.substr(0, i);
        bool match = true;
        for (size_t j = i; j < id_len; j+=i){ // check i long substrs
            if (sid.substr(j,i).compare(pattern)!=0){
                match = false;
                break;
            }

        }
        if (match == true) return true;
    }
    return false;
}

long long sol(ifstream& data, function<bool(const long long)> is_invalid){

    long long invalid = 0;
    string line;
    
    getline(data, line); // all data in single line
    
    stringstream ss(line);
  
    long long left , right;
    
    char comma;

    while (ss >> left >> comma >> right){   

        cout << "[DEBUG] Parsed range: " << left << " to " << right << " (separator: '" << comma << "')" << endl;

        for (long long i = left; i<=right ; i++){
            if (is_invalid(i) == true){
                invalid+=i;
            }
        }
        if (ss.peek() == ',') ss.ignore();
    }
    return invalid;
}

int main(){

    ifstream data("data.txt");
    if (!data.is_open()){
        cerr << "Error oppening file" << endl;
        return 1;
    }

    cout << "Part 1 sol " << sol(data, is_invalid_id_p2) << endl;
    return 0;
}
