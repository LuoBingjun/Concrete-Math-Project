#include <iostream>
#include <fstream>
#include <set>
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
				}
			}
		}
		used.insert(q[maxe]);
		max = max + r[maxe];
	}
	for (int i = 0; i < v - 1; i++)
	{
		cout << "[" << T[i].first << " -> " << T[i].second << "]";
	}
	cout << " " << max << endl;
}