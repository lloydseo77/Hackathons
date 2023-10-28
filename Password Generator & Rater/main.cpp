#include <algorithm>
#include <cctype>
#include <iostream>
#include <math.h>
#include <string>
#include <time.h>
#include <vector>
using namespace std;

// checks input of user to make sure it's a valid input
bool inputCheck(string password);

// finds index of what is being looked for, if it doesn't exist, then returns -1
int stringSearch(string original, string search);

// return length score
double lenScore(string password);

// determines if a character is in set
// if not, append to character set
void inSet(vector<int> &set);

// finds out what ascii range it's in
int ascRange(char c);

// special case if ascii changes only by one
bool checkSpec(vector<int> &set, string password);

// variety counter
// returns variety score
double variScore(string password);

// return char set score
double setScore(string password);

// determines strength of password
int detStr(string password);

// generates a password of random strength
string passMaker();

// generates a random character (different strenth values = different variety of
// categories used)
string charMaker();

int main() {
  srand(time(NULL));

  int strength;
  string pass;
  bool check;
  int menu;

  cout << "\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ "
          "~\n\n";
  cout
      << "\nWelcome to the Safe Fish Password Security Generator! >゜)))><\n\n";
  cout << "The Safe Fish Password Security does two things: \n1. Randomly "
          "generate a strong password. \n2. Take in a user-inputted password "
          "and gives it a security rating from 1 to 5. \n\n";
  cout << "Enter 1 to generate a new and strong random password, or 2 to input "
          "a password to be evaluated: ";
  cin >> menu;
  while (menu != 1 && menu != 2 && isdigit(menu) == false) {
    cout << "\n><((((ﾟ< \nInvalid input. Please enter 1 or 2: ";
    cin >> menu;
  }

  // random password generator
  if (menu == 1) {
    pass = passMaker();
    cout << "\nA fresh newly generated level 5 password just for you! " << pass
         << endl;
  }
  // password evaluator
  else {
    cout << "\nPlease input a password to be tested (max of 24 "
            "characters): ";
    cin >> pass;
    check = inputCheck(pass);

    while (check == false) {
      cout << "\n><((((ﾟ< Please input a valid password: ";
      cin >> pass;
      check = inputCheck(pass);
    }

    cout << "\nThe strength of your password is: " << detStr(pass) << endl;
    double min = lenScore(pass) / 53;
    if (min > variScore(pass) / 32)
      min = variScore(pass);
    else if (min > setScore(pass) / 15)
      min = setScore(pass);

    if (lenScore(pass) + variScore(pass) + setScore(pass) == 100 ||
        detStr(pass) == 5)
      cout << "Perfect password, no changes needed!\n";
    else {
      cout << "\nTo improve your password, consider ";
      if (min == lenScore(pass))
        cout << " adding more characters.  <º))))><\n";
      if (min == variScore(pass))
        cout << " alternating between lowercase, uppercase, and special "
                "characters more often.  <º))))><\n";
      if (min == setScore(pass))
        cout << " using less duplicate characters  <º))))><\n";
    }
  }
  cout << "Thank you much for using the Safe Fish Password Security! We hope "
          "that you leave with a secure and safe fish password! ♪ ~ >`)))>< \n";

  cout << "\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ "
          "~\n\n";
  cout << "\nOur password strength is based on three aspects: password length, "
          "uniqueness of characters used, and variety in character types.";
  cout << "\n\nPassword length: Refers to the character length of the "
          "password. The maximum length of a password is 24 characters long. ";
  cout << "\nUniqueness of characters used: Refers to all the distinct "
          "characters used in the password (how many repeated characters that "
          "exist or do not exist). ";
  cout << "\nVariety in character types: Refers to how many times throughout "
          "the password the character type (uppercase, lowercase, digits, "
          "symbols) changes.";
}

// 1 - uppercase , 2 - lowercase, 3 - numbers, 4 - special char
int ascRange(char c) {
  if (c >= 65 && c <= 90)
    return 1;
  else if (c >= 97 && c <= 122)
    return 2;
  else if (c >= 48 && c <= 57)
    return 3;
  else
    return 4;
}

bool inputCheck(string password) {
  if (password.length() > 24)
    return false;
  else if (stringSearch(password, " ") != -1)
    return false;
  else
    return true;
}

double lenScore(string password) {
  return -50.4142 /
             (1 + 9.2602 * exp(0.689261 * (password.length() - 12.538))) +
         52.4064;
}

void inSet(vector<int> &set, string password) {
  for (int i = 0; i < password.length(); i++) {
    // if password character is not already in character set
    if (find(set.begin(), set.end(), password[i]) == set.end())
      set.push_back(password[i]);
  }
}

bool checkSpec(char a, char b) {
  // if character types changes, special case doesn't matter
  if (ascRange(a) == ascRange(b)) {
    // special case: ascii value changes by 1
    if (a == b || a == b - 1 || a == b)
      return true;
    else
      return false;
  } else
    return false;
}

double variScore(string password) {
  int var = 0;
  int length = password.length();

  for (int i = 0; i < password.length() - 1; i++) {
    // if character type changes, increase variety counter
    if (ascRange(password[i]) != ascRange(password[i + 1])) {
      var++;
    }
    // check for special case
    checkSpec(password[i], password[i + 1]);
  }

  if (length >= 12 && length <= 24)
    return (var * (15.0 / length));
  else if (length >= 8 && length <= 12)
    return (var * (14.0 / length));
  else if (length >= 4 && length < 8)
    return (var * (10.0 / length));
  else
    return (var * (1.3 / length));
}

double setScore(string password) {
  string check;
  int length = password.length();

  for (int count = 0; count < password.length() - 1; count++) {
    if (stringSearch(check, password.substr(count, 1)) == -1)
      check += password.substr(count, 1);
  }

  if (length >= 12 && length <= 24)
    return ((check.length()) * (32.0 / length));
  else if (length >= 8 && length <= 12)
    return ((check.length()) * (28.0 / length));
  else if (length >= 4 && length < 8)
    return ((check.length() * (22.0 / length)));
  else
    return ((check.length() * (18.0 / length)));
}

int detStr(string password) {
  int score =
      round(lenScore(password) + variScore(password) + setScore(password));
  if (score <= 20)
    return 1;
  else if (score <= 40)
    return 2;
  else if (score <= 60)
    return 3;
  else if (score <= 80)
    return 4;
  else if (score <= 100)
    return 5;
  else
    return -1;
}

int stringSearch(string original, string search) {
  for (int x = 0; x < original.length(); x++)
    if (original.substr(x, 1) == search)
      return x;

  return -1;
}

string passMaker() {
  string output;
  int part, length, specChar;

  length = rand() % 10 + 15;

  for (int count = 0; count < length; count++)
    output += charMaker();

  return output;
}

string charMaker() {
  int length, category = 0, specChar, cate0 = 0;
  string part;

  category = rand() % 4 + 1;

  cate0 = category;

  switch (category) {
  case 1:
    part = rand() % 26 + 97;
    break;
  case 2:
    part = rand() % 26 + 65;
    break;
  case 3:
    part = rand() % 10 + 48;
    break;
  case 4: {
    specChar = rand() % 5 + 1;
    switch (specChar) {
    case 1:
      part = rand() % 15 + 33;
      break;
    case 2:
      part = rand() % 7 + 58;
      break;
    case 3:
      part = rand() % 6 + 91;
      break;
    case 4:
      part = rand() % 4 + 123;
      break;
      break;
    }
  }
  }
  return part;
}