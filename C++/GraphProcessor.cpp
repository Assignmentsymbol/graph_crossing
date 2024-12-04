#include <ogdf/basic/Graph_d.h>
#include <ogdf/basic/GraphAttributes.h>
#include <ogdf/planarity/PlanarizationLayout.h>
#include <ogdf/fileformats/GraphIO.h>
#include <ogdf/energybased/FMMMLayout.h>
#include "json.hpp"
#include <fstream>
#include <iostream>
#include <cmath>
#include <vector>
#include <unordered_map>
#include <algorithm>

using namespace ogdf;
using namespace std;
using json = nlohmann::json;

struct CrossingTable {
    std::unordered_map<node, vector<pair<node, node>>> crossing;
};

struct pair_hash {
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2>& pair) const {
        auto hash1 = std::hash<T1>{}(pair.first);
        auto hash2 = std::hash<T2>{}(pair.second);
        return hash1 ^ (hash2 << 1); // Combine the two hashes
    }
};

void readJSON(const string &filename, Graph &G, GraphAttributes &GA) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return;
    }

    json data;
    try {
        file >> data;
    } catch (const json::parse_error& e) {
        cerr << "JSON parsing error: " << e.what() << endl;
        return;
    }

    unordered_map<int, node> idToNode;
    for (const auto &n : data["nodes"]) {
        node v = G.newNode();
        idToNode[n["id"]] = v;
        GA.x(v) = n["x"];
        GA.y(v) = n["y"];
    }

    for (const auto &e : data["edges"]) {
        G.newEdge(idToNode[e["source"]], idToNode[e["target"]]);
    }
}

CrossingTable calculateCrossing(const Graph &G, const GraphAttributes &GA) {
    CrossingTable table;

    for (auto e1 : G.edges) {
        for (auto e2 : G.edges) {
            if (e1 == e2) continue;
            node s1 = e1->source();
            node t1 = e1->target();
            node s2 = e2->source();
            node t2 = e2->target();

            double x1 = GA.x(s1), y1 = GA.y(s1);
            double x2 = GA.x(t1), y2 = GA.y(t1);
            double x3 = GA.x(s2), y3 = GA.y(s2);
            double x4 = GA.x(t2), y4 = GA.y(t2);

            auto cross = [](double a, double b, double c, double d) {
                return (a - c) * (b - d) > 0;
            };

            if (cross(x1, y1, x3, y3) != cross(x2, y2, x4, y4)) {
                table.crossing[s1].push_back({s2, t2});
            }
        }
    }

    return table;
}

int getMaxCrossing(const CrossingTable &table, const Graph &G, const GraphAttributes &GA) {
    int maxCrossing = 0;

    for (auto e1 : G.edges) {
        for (auto e2 : G.edges) {
            if (e1 == e2) continue;

            node s1 = e1->source();
            node t1 = e1->target();
            node s2 = e2->source();
            node t2 = e2->target();

            auto it1 = table.crossing.find(s1);
            auto it2 = table.crossing.find(s2);

            if (it1 != table.crossing.end() && it2 != table.crossing.end()) {
                int crossingCount = 0;

                for (auto &pair1 : it1->second) {
                    for (auto &pair2 : it2->second) {
                        if (pair1 == pair2) {
                            crossingCount++;
                        }
                    }
                }

                maxCrossing = max(maxCrossing, crossingCount);
            }
        }
    }

    return maxCrossing;
}

void preprocessNodes(Graph &G, GraphAttributes &GA, CrossingTable &table) {
    vector<pair<node, int>> nodes;

    for (node v : G.nodes) {
        int degree = v->degree();
        degree += table.crossing[v].size();
        nodes.emplace_back(v, degree);
    }

    sort(nodes.begin(), nodes.end(), [](const auto &a, const auto &b) {
        return a.second > b.second;
    });

    int layer = 0;
    int offset = 0;

    for (size_t i = 0; i < nodes.size(); i++) {
        int x = layer * ((i % 2 == 0) ? 1 : -1) + offset;
        int y = layer * ((i % 2 == 0) ? -1 : 1) - offset;

        GA.x(nodes[i].first) = x;
        GA.y(nodes[i].first) = y;

        if (i % 8 == 0) {
            layer++;
            offset = -layer;
        } else {
            offset++;
        }
    }

    cout << "Maximum crossing after preprocessing: " << getMaxCrossing(table, G, GA) << endl;
}

void moveNodes(Graph &G, GraphAttributes &GA, CrossingTable &table) {
    for (node v : G.nodes) {
        if (table.crossing[v].empty()) continue;

        unordered_map<pair<node, node>, int, pair_hash> edgeCount;
        for (const auto &edge : table.crossing[v]) {
            edgeCount[edge]++;
        }

        auto maxEdge = max_element(edgeCount.begin(), edgeCount.end(), [](const auto &a, const auto &b) {
            return a.second < b.second;
        });

        if (maxEdge != edgeCount.end()) {
            auto [s, t] = maxEdge->first;

            double midX = (GA.x(s) + GA.x(t)) / 2;
            double midY = (GA.y(s) + GA.y(t)) / 2;

            GA.x(v) = round(midX + (midX - GA.x(v)));
            GA.y(v) = round(midY + (midY - GA.y(v)));
        }
    }
}

void interactiveIteration(Graph &G, GraphAttributes &GA, CrossingTable &table) {
    char choice;
    
    while (true) {
        cout << "Do you want to preprocess nodes? (y/n): ";
        cin >> choice;
        if (choice == 'n') break;

        moveNodes(G, GA, table);

        cout << "Maximum crossing after iteration: " << getMaxCrossing(table, G, GA) << endl;
    }
}

int main() {
    Graph G;
    GraphAttributes GA(G, GraphAttributes::nodeGraphics | GraphAttributes::edgeGraphics);

    readJSON("/Users/jeffk/Desktop/DE/TUM/W_24-25/Practical_course/C++/benchmark_2024/graph8.json", G, GA);

    CrossingTable table = calculateCrossing(G, GA);
    preprocessNodes(G, GA, table);

    interactiveIteration(G, GA, table);

    return 0;
}
