#include <iostream>
#include <vector>
bool *flag;
int *A;
int *B;
int v, e;

void dfs(int des, int now, std::vector<int> path, std::ostream &outputStream)
{
	if (now == des && path.size() >= 2)
	{
		outputStream << "[";
		for (int i = 0; i < path.size(); i++)
		{
			if (i != path.size() - 1)
				outputStream << path[i] << " -> ";
			else
				outputStream << path[i] << "]";
		}
		return;
	}
	for (int i = A[now]; i < A[now + 1]; i++)
	{
		if (!flag[B[i]])
		{
			flag[B[i]] = 1;
			std::vector<int> temp = path;
			temp.push_back(B[i]);
			dfs(des, B[i], temp, outputStream);
			flag[B[i]] = 0;
		}
	}
}

void USSolver::Solve(std::istream &inputStream, std::ostream &outputStream)
{
	//ÇëÔÚ´ËÌî³ä´úÂë
	inputStream >> v >> e;
	A = new int[v + 1];
	B = new int[e];
	for (int i = 0; i <= v; i++)
		inputStream >> A[i];
	for (int i = 0; i < e; i++)
		inputStream >> B[i];
	int **M = new int *[v];
	for (int i = 0; i < v; i++)
	{
		M[i] = (int *)malloc(v * sizeof(int));
		memset(M[i], 0, v * sizeof(int));
	}
	for (int i = 0; i < v; i++)
		for (int j = A[i]; j <= A[i + 1] - 1; j++)
		{
			M[i][B[j]] = 1;
		}
	for (int k = 0; k < v; k++)
		for (int i = 0; i < v; i++)
			for (int j = 0; j < v; j++)
				M[i][j] = M[i][j] || (M[i][k] && M[k][j]);
	int n;
	inputStream >> n;
	for (int i = 1; i <= n; i++)
	{
		int vs, ve;
		inputStream >> vs >> ve;
		if (M[vs][ve] == 0)
		{
			outputStream << "NO PATH" << std::endl;
		}
		else
		{
			flag = new bool[v];
			memset(flag, 0, v * sizeof(bool));
			std::vector<int> path;
			path.push_back(vs);
			flag[vs] = 1;
			flag[ve] = 0;
			dfs(ve, vs, path, outputStream);
			outputStream << std::endl;
		}
	}
}