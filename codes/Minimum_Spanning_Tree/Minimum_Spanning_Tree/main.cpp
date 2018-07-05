#include <iostream>
#include <fstream>
#include <set>
#include <list>
#include <utility>
#include <omp.h>
#include <assert.h>

using namespace std;

int main()
{
	ifstream fin("map.csv");
	int v, e;
	fin >> v >> e;

	int *p = new int[v + 1];
	int *q = new int[e];
	double *r = new double[e];
	for (int i = 0; i < v + 1; i++)
		fin >> p[i];
	for (int i = 0; i < e; i++)
		fin >> q[i];
	for (int i = 0; i < e; i++)
	{
		fin >> r[i];
		assert(r[i] <= 1.001);
	}

	std::set<int> used;
	used.insert(0);
	std::pair<int, int> *T = new pair<int, int>[v - 1];
	list<int> edges;
	long double max = 0;

	for (int a = 0; a < v - 1; a++)
	{
		double maxd = 0;
		int maxe;
		for (int i = 0; i < v + 1; i++)
		{
			if (used.count(i) == 0)
				continue;
			for (int j = p[i]; j < p[i + 1]; j++)
			{
				if (used.count(q[j]) == 1)
					continue;
				if (r[j] > maxd)
				{
					T[a].first = i;
					T[a].second = q[j];
					maxd = r[j];
					maxe = j;
					edges.push_back(maxe);
				}
			}
		}
		used.insert(q[maxe]);
		max = max + r[maxe];
	}
	// 关联矩阵形式
	ofstream fout("tree.csv");
	int** M = new int*[v];
	for (int i = 0; i < v; i++)
	{
		M[i] = new int[v];
		memset(M[i], 0, sizeof(int)*v);
	}
	for (int i = 0; i < v - 1; i++)
	{
		M[T[i].first][T[i].second] = 1;
		M[T[i].second][T[i].first] = 1;
	}
	for (int i = 0; i < v; i++)
	{
		for (int j = 0; j < v; j++)
		{
			if (j == v - 1)
			{
				fout << M[i][j] << endl;
			}
			else
			{
				fout << M[i][j] << ",";
			}
		}
	}
}