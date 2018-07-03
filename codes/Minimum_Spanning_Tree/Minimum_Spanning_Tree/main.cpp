#include <iostream>
#include <set>
#include <utility>

int main()
{
	//ÇëÔÚ´ËÌî³ä´úÂë
	int v, e;
	std::cin >> v >> e;
	int *p = new int[v + 1];
	int *q = new int[e];
	int *r = new int[e];
	for (int i = 0; i < v + 1; i++)
		std::cin >> p[i];
	for (int i = 0; i < e; i++)
		std::cin >> q[i];
	for (int i = 0; i < e; i++)
		std::cin >> r[i];

	std::set<int> used;
	used.insert(0);
	std::pair<int, int> *T = new std::pair<int, int>[v - 1];
	int min = 0;

	for (int a = 0; a < v - 1; a++)
	{
		int mind = INT_MAX;
		int mine;
		for (int i = 0; i < v + 1; i++)
		{
			if (used.count(i) == 0)
				continue;
			for (int j = p[i]; j < p[i + 1]; j++)
			{
				if (used.count(q[j]) == 1)
					continue;
				if (r[j] < mind)
				{
					T[a].first = i;
					T[a].second = q[j];
					mind = r[j];
					mine = j;
				}
			}
		}
		used.insert(q[mine]);
		min = min + r[mine];
	}

	for (int i = 0; i < v - 1; i++)
	{
		std::cout << "[" << T[i].first << " -> " << T[i].second << "]";
	}
	std::cout << " " << min << std::endl;
}