#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstring>
#include <algorithm>
#include <windows.h>
using namespace std;

//start C:\Users\aleks\source\repos\shell\x64\Debug\shell.exe aleks ELBRUS C:\Users\aleks\Desktop\Virtual_File_System.tar C:\Users\aleks\Desktop\script.txt

void setConsoleColor(int color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}

vector<string> FileSystem(const string& file_system_path) {
    vector<string> List;
    ifstream tar_file(file_system_path, ios::binary);
    int n = 0;
    string root;
    while (true) {
        char header[512];
        tar_file.read(header, sizeof(header));

        if (tar_file.gcount() == 0 and all_of(begin(header), end(header), [](char c) { return c == 0; })) {
            break;
        }

        char file_name[100];
        memcpy(file_name, header, sizeof(file_name));
        file_name[99] = '\0';

        char size_str[12];
        memcpy(size_str, header + 124, sizeof(size_str));
        size_str[11] = '\0';
        size_t file_size = strtol(size_str, nullptr, 8);

        string FN = file_name;
        if (n == 0) {
            root = file_name;
        }
        else if (!FN.empty()){
            string temp1 = FN.substr(root.size() - 1);
            List.push_back("~" + temp1);
        }

        vector<char> fileData(file_size);
        tar_file.read(fileData.data(), file_size);

        string temp2;
        for (size_t i = 0; i < file_size; ++i) {
            temp2 += fileData[i];
        }

        if (!temp2.empty()) {
            if (temp2[0] == '/') {
                List.push_back("~" + temp2);
            }
            else {
                List.push_back(temp2);
            }
        }

        size_t padding = (file_size + 511) / 512 * 512 - file_size;
        tar_file.seekg(padding, ios::cur);
        n++;
    }
    return List;
}

vector<size_t> FileSizes(const string& file_system_path) {
    vector<size_t> List;
    ifstream tar_file(file_system_path, ios::binary);
    int n = 0;
    string root;
    while (true) {
        char header[512];
        tar_file.read(header, sizeof(header));

        if (tar_file.gcount() == 0 and all_of(begin(header), end(header), [](char c) { return c == 0; })) {
            break;
        }

        char file_name[100];
        memcpy(file_name, header, sizeof(file_name));
        file_name[99] = '\0';

        char size_str[12];
        memcpy(size_str, header + 124, sizeof(size_str));
        size_str[11] = '\0';
        size_t file_size = strtol(size_str, nullptr, 8);

        string FN = file_name;
        if (n == 0) {
            root = file_name;
        }
        else if (!FN.empty()) {
            string temp1 = FN.substr(root.size() - 1);
            List.push_back(file_size);
        }

        vector<char> fileData(file_size);
        tar_file.read(fileData.data(), file_size);

        string temp2;
        for (size_t i = 0; i < file_size; ++i) {
            temp2 += fileData[i];
        }

        if (!temp2.empty()) {
            if (temp2[0] == '/') {
                List.push_back(0);
            }
            else {
                List.push_back(file_size);
            }
        }

        size_t padding = (file_size + 511) / 512 * 512 - file_size;
        tar_file.seekg(padding, ios::cur);
        n++;
    }

    return List;
}

int cd(string path, const string& file_system_path, string& current_path) {
    if (path == "~") {
        current_path = path;
        return 0;
    }
    vector<string> FILES = FileSystem(file_system_path);
    for (int i = 0; i < FILES.size(); i++) {
        if ("~" + path + "/" == FILES[i]) {
            current_path = path;
            return 0;
        }
    }
    setConsoleColor(4);
    cout << "Console:~# Can't cd to " + path + ": No such file or directory.\n";
    setConsoleColor(7);
    return -1;
}


int ls(const string& file_system_path, string current_path) {
    int t = 0;
    if (current_path != "~") {
        current_path = "~" + current_path;
    }
    else {
        t++;
    }
    vector<string> FILES = FileSystem(file_system_path);
    for (int i = 0; i < FILES.size(); i++) {
        if (current_path + "/" == FILES[i]) {
            t++;
        }
    }
    if (t == 0) {
        setConsoleColor(4);
        cout << "Console:~# Can't ls " + current_path + ": No such file or directory.\n";
        setConsoleColor(7);
        return -1;
    }
    vector<int> TEMP;
    int k = 0;
    for (int a = 0; a < current_path.size(); a++) {
        if (current_path[a] == '/') {
            k++;
        }
    }
    for (int i = 0; i < FILES.size(); i++) {
        int n = 0;
        for (int j = 0; j < FILES[i].size(); j++) {
            if (FILES[i][j] == '/') {
                n++;
            }
            
        }
        if (FILES[i].back() == '/') {
            n--;
        }
        if (k == n - 1 and FILES[i].substr(0, current_path.size()) == current_path) {
            TEMP.push_back(i);
        }
    }
    for (int l = 0; l < TEMP.size(); l++) {
        setConsoleColor(2);
        cout << FILES[TEMP[l]].substr(current_path.size() + 1) << endl;
        setConsoleColor(7);
    }
    return 0;
}

void du(const string& file_system_path) {
    vector<string> FILES = FileSystem(file_system_path);
    vector<size_t> FILES2 = FileSizes(file_system_path);

    for (int j = FILES.size() - 1; j > 0; j--) {
        for (int k = 1; j - k >= 0; k++) {
            if (FILES[j].substr(0, FILES[j - k].size()) == FILES[j - k]) {
                FILES2[j - k] += FILES2[j];
                break;
            }
        }
            
    }

    for (int i = 0; i < FILES.size(); i++) {
        if (FILES[i][0] == '~') {
            setConsoleColor(2);
            cout << FILES[i].substr(2);
            setConsoleColor(6);
            cout << " | " << FILES2[i] << " bytes" << endl;
            setConsoleColor(7);
        }
    }
}

int wc(string path, const string& file_system_path) {
    path = "~" + path;
    vector<string> FILES = FileSystem(file_system_path);
    vector<size_t> FILES2 = FileSizes(file_system_path);
    for (int i = 0; i < FILES.size(); i++) {
        if (FILES[i] == path) {
            int lines = 1 + count(FILES[i + 1].begin(), FILES[i + 1].end(), '\n');
            int words = lines + count(FILES[i + 1].begin(), FILES[i + 1].end(), ' ');
            size_t bytes = FILES2[i];
            setConsoleColor(2);
            cout << lines << " lines | " << words << " words | "; 
            setConsoleColor(6);
            cout << bytes << " bytes" << endl;
            setConsoleColor(7);
            return 0;
        }
    }
    setConsoleColor(4);
    cout << "Console:~# Can't wc to " + path + ": Invalid path.\n";
    setConsoleColor(7);
    return -1;
}

void arg_warn(int arg_num) {
    if (arg_num != 5) {
        setConsoleColor(4);
        cout << "Console:~# Wrong number of arguments.\n";
        setConsoleColor(7);
        system("pause");
    }
}

void hello_words(string host_name) {
    setConsoleColor(2);
    cout << "Welcome to " + host_name + "/Windows" << endl << "----------------------------------------------------------" << endl << "In this OS shell emulator, you can use commands\nsuch as 'ls', 'cd', 'exit', 'wc', 'history' and 'du'.\n" << "----------------------------------------------------------" << endl;
    setConsoleColor(7);
}

int main(int argc, char* argv[]) {
    arg_warn(argc);
    vector<string> HISTORY;
    const string user_name = argv[1];
    const string host_name = argv[2];
    const string file_system_path = argv[3];
    const string start_script_path = argv[4];
    string current_path = "~";
    hello_words(host_name);
    ifstream inputFile(start_script_path);
    if (!inputFile.is_open()) {
        setConsoleColor(4);
        cout << "Console:~# The file could not be opened." << endl;
        setConsoleColor(7);
        return -1;
    }
    string line;
    while (getline(inputFile, line)) {
        if (line == "exit") {
            system("exit");
            return 0;
            HISTORY.clear();
        }
        else if (line.substr(0, 2) == "cd") {
            HISTORY.push_back(line);
            string path;
            if (line.size() < 4) {
                setConsoleColor(4);
                cout << "Console:~# Can't cd to " + path + ": No such file or directory.\n";
                setConsoleColor(7);
                continue;
            }
            else {
                cout << user_name + ":" + current_path + "# " << line << endl;
                path = line.substr(3);
                cd(path, file_system_path, current_path);
                continue;
            }
        }
        else if (line.substr(0, 2) == "ls") {
            HISTORY.push_back(line);
            string path;
            if (line.size() < 3) {
                cout << user_name + ":" + current_path + "# " << line << endl;
                ls(file_system_path, current_path);
                continue;
            }
            else {
                path = line.substr(3);
                cout << user_name + ":" + current_path + "# " << line << endl;
                ls(file_system_path, path);
                continue;
            }
        }
        else if (line.substr(0, 2) == "wc") {
            HISTORY.push_back(line);
            string path;
            if (line.size() < 4) {
                setConsoleColor(4);
                cout << "Console:~# Can't wc to " + path + ": No such file.\n";
                setConsoleColor(7);
                continue;
            }
            else {
                path = line.substr(3);
                cout << user_name + ":" + current_path + "# " << line << endl;
                wc(path, file_system_path);
                continue;
            }
        }
        else if (line.substr(0, 7) == "history") {
            if (line.length() == 7) {
                cout << user_name + ":" + current_path + "# " << line << endl;
                setConsoleColor(4);
                for (int i = 0; i < HISTORY.size(); i++) {
                    cout << i + 1 << " | " << HISTORY[i] << endl;
                }
                setConsoleColor(7);
            }
            else {
                string requests = line.substr(8);
                int count_of_requests = atoi(requests.c_str());
                if (count_of_requests > HISTORY.size()) {
                    setConsoleColor(4);
                    cout << "Console:~# The size of the saved history has been exceeded.\n";
                    setConsoleColor(7);
                }
                else {
                    cout << user_name + ":" + current_path + "# " << line << endl;
                    setConsoleColor(4);
                    for (int i = HISTORY.size() - 1; i >= HISTORY.size() - count_of_requests; i--) {
                        cout << i + 1 << " | " << HISTORY[i] << endl;
                    }
                    setConsoleColor(7);
                }
            }
        }
        else if (line.substr(0, 2) == "du") {
            HISTORY.push_back(line);
            cout << user_name + ":" + current_path + "# " << line << endl;
            du(file_system_path);
            continue;
        }
    }
    inputFile.close();
    while (true) {
        string input;
        cout << user_name + ":" + current_path + "# ";
        getline(cin, input);
        if (input == "exit") {
            system("exit");
            return 0;
            HISTORY.clear();
        }
        else if (input.substr(0, 2) == "cd") {
            HISTORY.push_back(input);
            string path;
            if (input.size() < 4) {
                setConsoleColor(4);
                cout << "Console:~# Can't cd to " + path + ": No such file or directory.\n";
                setConsoleColor(7);
                continue;
            }
            else {
                path = input.substr(3);
                cd(path, file_system_path, current_path);
                continue;
            }
        } 
        else if (input.substr(0, 2) == "ls") {
            HISTORY.push_back(input);
            string path;
            if (input.size() < 3) {
                ls(file_system_path, current_path);
                continue;
            }
            else {
                path = input.substr(3);
                ls(file_system_path, path);
                continue;
            }
        }
        else if (input.substr(0, 2) == "wc") {
            HISTORY.push_back(input);
            string path;
            if (input.size() < 4) {
                setConsoleColor(4);
                cout << "Console:~# Can't wc to " + path + ": No such file.\n";
                setConsoleColor(7);
                continue;
            }
            else {
                path = input.substr(3);
                wc(path, file_system_path);
                continue;
            }
        }
        else if (input.substr(0, 7) == "history") {
            if (input.length() == 7) {
                setConsoleColor(4);
                for (int i = 0; i < HISTORY.size(); i++) {
                    cout << i + 1 << " | " << HISTORY[i] << endl;
                }
                setConsoleColor(7);
            }
            else {
                string requests = input.substr(8);
                int count_of_requests = atoi(requests.c_str());
                if (count_of_requests > HISTORY.size()) {
                    setConsoleColor(4);
                    cout << "Console:~# The size of the saved history has been exceeded.\n";
                    setConsoleColor(7);
                }
                else {
                    setConsoleColor(4);
                    for (int i = HISTORY.size() - 1; i >= HISTORY.size() - count_of_requests; i--) {
                        cout << i + 1 << " | " << HISTORY[i] << endl;
                    }
                    setConsoleColor(7);
                }
            }
        }
        else if (input.substr(0, 2) == "du") {
            HISTORY.push_back(input);
            du(file_system_path);
            continue;
        }
        else if (input.empty()) {
            continue;
        }
        else {
            setConsoleColor(4);
            cout << "Console:~# Invalid command.\n";
            setConsoleColor(7);
            continue;
        }
    }
}