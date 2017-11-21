#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

bool is_connected(bool* graph[], int size);

int main(int argc, char* argv[])
{
    int size = 7;
    bool** graph;
    float density = 0.27;
    float probability;

    srand(time(0)); // seed random number generator
    graph = new bool*[size]; // allocate first dimension
    for (int i = 0; i < size; ++ i) {
        graph[i] = new bool[size]; // allocate the second dimension
    }

    // Initialize the graph (diagonally symmetric)
    for (int i = 0; i < size; ++ i) {
        for (int j = i; j < size; ++ j) { // upper triangle
            if (i == j) {
                graph[i][j] = false; // avoid loops
            } else {
                // Fill both upper and lower triangles of the matrix
                probability = static_cast<float>(rand()) / RAND_MAX;
                graph[i][j] = graph[j][i] = (probability < density);
            }
        }
    }

    // Display the graph
    cout << "Graph's adjacency matrix:" << endl;
    for (int i = 0; i < size; ++ i) {
        for (int j = 0; j < size; ++ j) {
            cout << "  " << graph[i][j]; // add to the current row
        }
        cout << endl; // move to the next row
    }

    // Apply connectivity algorithm to the graph
    if (is_connected(graph, size)) {
        cout << "The graph is connected" << endl;
    } else {
        cout << "The graph is not connected" << endl;
    }

    // Delete the graph
    for (int i = 0; i < size; ++ i) {
        delete[] graph[i];
    }
    delete[] graph;
}

bool is_connected(bool* graph[], int size) {
    int c_size = 0;
    bool answer = false;
    bool* closed = new bool[size];
    bool* open = new bool[size];

    // Initialize empty sets
    for (int i = 0; i < size; ++ i) {
        open[i] = closed[i] = false;
    }
    open[0] = true; // add a vertex into the open set (initialize)

    for (int n = 0; (n < size) && (answer == false); ++ n) {
        // Cycle through vertices (rows) and add to the closed set
        // worst case (n variable): each cycle only one vertex is added
        // into the closet set (even if the graph is connected)
        for (int i = 0; i < size; ++ i) {
            if ((open[i] == true) && (closed[i] == false)) {
                // A vertex is in the open set, but not in the closed one
                closed[i] = true;
                c_size ++;
                if (c_size == size) {
                    // Stop if the closed set has all the vertices
                    answer = true;
                    break;
                }
                // Cycle through the vertex images, add them to the open set
                for (int j = 0; j < size; ++ j) {
                    open[j] = open[j] || graph[i][j];
                }
            }
        }
    }
    delete[] closed;
    delete[] open;
    return answer;
}

// vim: et ts=8 sts=4 sw=4
